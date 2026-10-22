---
title: "LayerFS 1.0 拆解：把多 Agent 的工作目录变成可分叉、可回溯的共享历史"
date: 2026-10-21
source: "https://x.com/yifanxu_ephai/status/2112876555907064008"
tags:
  - LayerFS
  - Ephemeral AI Lab
  - Agent Infrastructure
  - Multi-Agent
  - Filesystem
  - Copy-on-Write
  - SQLite
  - FUSE
  - DeepSeek Harness
  - Source Audit
---

# LayerFS 1.0 拆解：把多 Agent 的工作目录变成可分叉、可回溯的共享历史

当五个 Agent 同时修改一个项目时，工程上的麻烦往往先于模型能力出现：工作目录怎么隔离？依赖要不要安装五遍？一次失败实验能从哪一步重新开始？两个 Agent 的修改怎样汇合？

2026 年 10 月 21 日，Yifan Xu 发布了 MIT 开源的 LayerFS v1.0.0。它把项目文件、依赖和修改历史装进共享 Store，为每次尝试提供可以快速挂载的工作区。模型继续负责推理，LayerFS 负责保存和组织工作状态。

**它最值得研究的是“廉价分叉 + 完整依赖 + 细粒度历史”的组合。** 当前实现也有明确边界：Store 访问要求共用一个 Linux 内核，macOS 通过 Docker 运行；发布版本只启用 Disposable 模式，没有主机崩溃或断电后的持久性保证。

![LayerFS 官方历史树模拟演示](imgs/layerfs-v1-agent-workspace-history/official-history-demo.jpg)

*上图取自官方网页模拟演示的第 8 秒。分支、Commit 和终端活动用于解释交互设计，不能作为真实并行任务完成情况或性能证据。*

- 原帖：[Yifan Xu：LayerFS v1.0.0](https://x.com/yifanxu_ephai/status/2112876555907064008)
- 发布：[v1.0.0 Release](https://github.com/Ephemeral-AI-Lab/layerfs/releases/tag/v1.0.0)，标签提交 `2aaf2552ce21154928b9f9c83582e41a637f5910`
- 官网：[layerfs.ai](https://layerfs.ai/)
- 核查日期：2026-10-22；阅读发布标签源码、SDK、发布说明及当日官网文档，未安装运行时或独立复测基准

## 一次 Bash 调用怎样留下历史

LayerFS 把工作分成两条路径。

读取、搜索和编辑文件可以通过 JavaScript SDK 直接访问 SQLite Store，无须为这些操作启动容器。产生文件变化的写操作可以形成一个 Commit；只读或没有改变状态的调用不会凭空制造检查点。

需要运行 Bash、测试或构建时，再挂载一个 Workspace。程序看到的是完整可写目录，实际修改先进入自己的 overlay；调用方显式提交后，变化进入共享历史，然后卸载工作区。

![文件操作与 Bash 的两条路径](imgs/layerfs-v1-agent-workspace-history/idea-01-ephemeral.png)

*官方概念图：文件写入直达 Store，命令执行经过 mount、exec、commit、unmount。*

用 v1.0.0 的接口名称表达，这个周期是：

```text
fs.write / fs.edit → 文件变更与 Commit

workspace.mount(branch)
  → workspace.exec(workspace, command)
  → workspace.commit(workspace)
  → workspace.unmount(workspace)
```

“每个工具调用都有检查点”需要 Harness 正确接入这条流程。`exec` 结束本身不会自动提交，文件历史也不会自动保存命令输出、进程内存或正在运行的服务。

原帖用“Agent 大约 80% 时间在思考”解释为什么不必一直占着执行环境。这个比例属于作者的设计动机，不是所有 Agent 工作负载的实测定律。发布 SDK 也会复用容器：同一镜像的 Sandbox 可容纳最多 16 个 Workspace，空闲约两分钟才关闭。工作区短暂存在，并不意味着每条命令结束后整套计算资源立即归零。[发布 SDK](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/sdk/js/README.md)

## 五个概念怎样配合

| 概念 | 承担的工作 | 一个例子 |
|---|---|---|
| Store | 保存共享文件内容、树和历史 | 项目的 SQLite Store |
| Branch | 一条可写的尝试路线 | `fix-login`、`try-cache` |
| Commit | 保存一次文件状态 | 改完测试后的检查点 |
| Workspace | 暴露给普通程序的可写视图 | 执行 `npm test` 的目录 |
| Layer | 发布到 `main` 的状态 | 通过验收后采纳的版本 |

分叉只需要记录起点，无须把整个项目再复制一次。已有文件的内容继续共享，分支产生新改动时才保存增量。因此，一个 Agent 可以尝试方案 A，再从 A 的某个 Commit 派生 A1、A2，测试后选择合适结果。

![递归分叉的官方示意](imgs/layerfs-v1-agent-workspace-history/idea-04-recursive.png)

这为搜索式编程、反复修复和多候选实验提供了便宜的状态管理。至于哪个分支更好，仍需要测试、评估器或人来决定；文件系统不会替团队定义验收标准。

## 依赖也进入快照，改变了新工作区的准备成本

LayerFS 初始化时会捕获整个项目树，包括 `.git`、`node_modules`、缓存和 `.gitignore` 忽略的文件。后续分支可以直接看到这些内容，不必每次从源码重新安装。

![依赖随挂载一起出现](imgs/layerfs-v1-agent-workspace-history/idea-06-bootstrap.png)

*官方说明图中的耗时用于表达工作流差异，不是本文的安装或挂载实测。*

这里解决的是 Git 跟踪边界与可执行环境之间的空隙。Git worktree 已经能共享 Git 对象，但不会自动让新的目录拥有全部未跟踪依赖；LayerFS 把这些文件一并纳入版本化工作状态。

收益取决于原工作流。已有容器镜像、共享依赖缓存或文件系统快照的团队，未必还会经历每个分支重复安装。挂载也只是延迟读取，第一次打开文件仍要付出实际 I/O。原生模块还必须与容器镜像的系统和架构匹配。

捕获范围扩大也有一个直接后果：忽略文件不等于排除文件。如果源目录有 `.env` 或本地凭据，它们可能随初始化进入历史。准备实验目录时，应先明确哪些文件允许进入共享 Store。

## 多 Agent 协调究竟解决到哪一层

多个 Workspace 可以并行工作，提交时再与当前 Branch head 合并。共享 Store 的发布步骤仍是短时间单写者，重型构建和准备工作可以并行执行。

![多 Agent 与分支汇合示意](imgs/layerfs-v1-agent-workspace-history/idea-03-coordination.png)

原帖将规则概括为“同文件冲突拒绝”。发布源码更细：会比较共同基线和两侧内容，相同字节不会制造冲突；文本有三方合并路径，无法兼容的变化才需要处理。发生冲突时应读取诊断、查看新 head，再解决问题，不能把并行编辑理解为自动正确协作。[合并实现](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/core/crates/layerfs-content/src/merge/decide.rs)

根目录的 `/.lww` 提供另一种选择：对匹配路径使用 last-writer-wins。实现按修改时间保留较新一侧，时间相同时保留 ours，并记录选择结果。这适用于可以重建的生成文件和缓存；对源码或锁文件使用之前，必须接受另一侧修改可能被丢弃的含义。一个较新的 lockfile，并不自动包含两个分支各自新增的依赖。[规则实现](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/core/crates/layerfs-content/src/merge/lww.rs)

这套机制维护文件与历史的一致性，业务正确性仍要靠合并后的测试。

## “去中心化”目前能跨到哪里

原帖提到不同电脑上的 Agent 共享一个 Store。当前平台文档同时明确要求：所有打开 Store 的进程和 daemon 必须共用一个 Linux 内核，Store 位于本地 ext4、xfs 或 btrfs；NFS、virtiofs 和来自 macOS 的目录绑定不受支持。

因此，当前可确认的部署形态，是同一 Linux 主机或同一 Docker Linux VM 内共享 Store。远端 Agent 若通过主机侧服务代理访问，那属于额外集成，不能直接把 SQLite 文件放在 NAS 上就获得跨主机一致性。

Mac 用户可以通过 LayerFS × DSH 使用 Docker Desktop。Host 在 Linux 容器中执行 Store 操作，让持久卷留在 Linux 文件系统内，而非直接在 APFS 项目目录中运行 FUSE。[平台说明](https://layerfs.ai/docs/platform/)

## 压缩数字应该怎样读

内容寻址负责让重复数据只存一次；大文件的分块和增量表示让小修改复用旧内容；zstd 再压缩已经保存的数据。

![去重与压缩的官方说明图](imgs/layerfs-v1-agent-workspace-history/idea-05-storage.png)

*“约 1.05 份”“约 0.31 份”为概念图示例。官方 Core Ideas 与素材说明均将此类演示数字标为说明用途。*

正式发布列出了另一组有方法记录的测试：

| 测试 | 官方结果 | 应如何理解 |
|---|---|---|
| `fs-bench` | 5.20 秒对 8.88 秒，约 1.71 倍 | 与 Cloudflare Computer 的同镜像文件操作套件比较，12 个场景中 10 个更快 |
| `dsh-dedup` | 157 个快照，Store 100.1 MB；Btrfs + zstd 为 1,994.6 MB | 这一项目历史的存储比较，约小 19.9 倍；156/156 后续快照读回 |
| `pjdfstest` | 无未预期失败，保留 overlayfs 约 76% 的通过项 | 剩余差异属于声明的格式限制，不能写成 POSIX 全兼容 |
| `fsx` / `fsstress` | 14/14 通过、零字节不一致；提交重挂载后 3,755/3,755 条目一致 | 数据正确性证据，不是断电恢复证据 |
| `fio` | 顺序写入约为 FUSE 对照的 0.31 倍 | 更省空间不等于所有 I/O 都更快 |

上述结果来自作者在 `e5c7aaae05` 上的发布测试。环境为 arm64 Mac、Docker Desktop `linux/arm64`、8 CPU、约 8.3 GB 内存，每个案例单次运行。本文未复测，不能把它们推广成整个 Agent 完成任务快 1.71 倍，或任何文件都能压缩 19.9 倍。[基准方法与记录](https://layerfs.ai/benchmarks/)

## “历史保留下来”与“断电后可靠”需要分开看

发布代码里的持久化配置确实存在 Durable 和 Disposable 两种枚举，但当前安装入口只接受 Disposable；其 SQLite 配置是 WAL 配合 `synchronous=OFF`。

这降低了提交等待成本，却不保证操作系统崩溃或断电后仍可恢复全部历史，甚至可能损坏 Store。文件对象不可变只能说明正常工作时不会覆盖旧对象，无法替代落盘与恢复保证。[配置源码](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/core/crates/layerfs-persistence/src/backend/sqlite/profile.rs)

另外，当前没有历史垃圾回收。删除文件只是让新快照不再引用它，旧 Commit 仍可保留内容。大量分支的共享很便宜，长期保存所有新改动的总量仍会增长。

因此，当前合理定位是可重建的 Agent 工作状态和实验历史；需要长期保存的成果仍应进入 Git 远端或其他独立存储。

## 1.0 的接入还需要哪些工程工作

v1.0.0 是源码发布，没有 npm 包、预编译二进制或公共运行时镜像。需要从同一标签构建 SDK native addon 与 Linux daemon，再准备 Docker 镜像。DSH 集成还需要 Node 22.19+、pnpm 和 DeepSeek Harness checkout。

截至核查日，官网部分文档仍列出旧 `sandbox.*` 生命周期和 1 MiB 输出上限，而 Release 与标签 SDK 已采用 `workspace.*`，大输出改为分页处理。接入时应以发布标签的 SDK 和 Release 为准，保持 addon、daemon 和 JS 版本一致。[v1.0.0 SDK](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/sdk/js/README.md)

它也不会自动接管任何现有 Coding Agent。Harness 必须把文件工具和 Bash 生命周期接到 LayerFS；目前公开的主要路径是 LayerFS × DSH，而官网把 Pi 集成列为 planned。

## 哪些团队最值得试

| 工作负载 | 可能获得的收益 | 要验证的实际成本 |
|---|---|---|
| 多分支修复、候选方案搜索 | 复用起点，保留每次尝试 | 合并正确性、评估和调度 |
| 依赖较重、反复创建环境 | 共享已安装文件 | 首次读取、镜像与架构匹配 |
| Agent 训练或排障 | 回到某个文件状态继续实验 | 日志、模型上下文需另外记录 |
| 单 Agent 的普通小项目 | 部分历史与隔离收益 | 新增构建和运行时管理是否值得 |

LayerFS 展示了一种值得关注的 Agent 基础设施方向：把尝试过程本身做成可分叉的文件状态，让执行环境能按需出现，让失败实验仍留下可分析的历史。真正的采用依据应是团队测到的环境准备成本、分叉数量和恢复体验，而不只是首页动画里的分支长得有多快。

## 来源与证据

- [原始发布帖](https://x.com/yifanxu_ephai/status/2112876555907064008)与 [v1.0.0 Release](https://github.com/Ephemeral-AI-Lab/layerfs/releases/tag/v1.0.0)
- [MIT 源码仓库](https://github.com/Ephemeral-AI-Lab/layerfs)与[发布标签 SDK](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/sdk/js/README.md)
- [Core Ideas](https://layerfs.ai/docs/core-ideas/)、[Platform and Limits](https://layerfs.ai/docs/platform/)、[LayerFS × DSH](https://layerfs.ai/docs/integrations/dsh/)
- [Benchmark Index](https://layerfs.ai/benchmarks/)与 [dsh-dedup](https://layerfs.ai/benchmarks/dsh-dedup/)
- [官方素材说明](https://github.com/Ephemeral-AI-Lab/layerfs/blob/v1.0.0/docs/assets/official_release/README.md)：说明网页历史演示为模拟，图示数值为说明用途

*本文为官方材料与源码核查。没有完成 LayerFS 的本地部署、性能复现或故障恢复实验；文中未将上游测试结果当成独立实测。*
