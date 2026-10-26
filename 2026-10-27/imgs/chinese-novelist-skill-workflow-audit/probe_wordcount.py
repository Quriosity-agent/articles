"""Bounded behavior probes for the pinned upstream word-count script.

Usage: python3 probe_wordcount.py /path/to/upstream/scripts/check_chapter_wordcount.py
Only synthetic fixtures in a temporary directory are written.
"""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    sys.dont_write_bytecode = True
    script = Path(sys.argv[1]).resolve()
    spec = importlib.util.spec_from_file_location("upstream_wordcount", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    observations = []

    def check(name, actual, expected):
        assert actual == expected, (name, actual, expected)
        observations.append({"probe": name, "observed": actual})

    def cli(*args):
        result = subprocess.run(
            [sys.executable, str(script), *map(str, args), "--json"],
            capture_output=True, text=True, check=False,
        )
        return result.returncode, json.loads(result.stdout)

    check("Only basic CJK characters count; Latin and digits excluded",
          module.count_chinese_words("中文ABC123，测试"), 4)

    with tempfile.TemporaryDirectory(prefix="novelist-probes-") as temp:
        root = Path(temp)
        chapter = root / "第01章-测试.md"
        chapter.write_text("# 第01章 标题\n\n正文", encoding="utf-8")
        code, data = cli(chapter, 2)
        check("Chapter title skipped; threshold met", [code, data["results"][0]["word_count"]], [0, 2])
        code, data = cli(chapter, 3)
        check("Below threshold returns exit 1", [code, data["results"][0]["status"]], [1, "fail"])

        chapter.write_text("# 第01章 标题\n\n## 摘要\n背景\n\n## 正文\n你好", encoding="utf-8")
        code, data = cli(chapter, 8)
        check("Metadata and section labels count alongside two-character prose",
              [code, data["results"][0]["word_count"]], [0, 8])

        chapter.write_text("# 第01章 标题\n" + "文" * 5001, encoding="utf-8")
        code, data = cli(chapter)
        check("Default check has no 5000-character upper bound",
              [code, data["results"][0]["word_count"]], [0, 5001])

        chapter.write_text("# 第01章 标题\n", encoding="utf-8")
        code, data = cli(chapter, -1)
        check("Negative minimum is accepted, even for empty prose",
              [code, data["results"][0]["status"]], [0, "pass"])

        code, data = cli(root / "missing.md")
        check("Missing single file returns exit 2",
              [code, data["summary"]["errors"]], [2, 1])
        code, data = cli(chapter, "invalid")
        check("Non-integer threshold returns structured error",
              [code, "error" in data], [2, True])

        plan_dir = root / "incomplete-project"
        plan_dir.mkdir()
        (plan_dir / "第01章-已有.md").write_text("# 第01章\n正文", encoding="utf-8")
        (plan_dir / "02-写作计划.json").write_text(json.dumps({
            "chapters": [{"filePath": "第01章-已有.md"}, {"filePath": "第02章-缺失.md"}]
        }, ensure_ascii=False), encoding="utf-8")
        code, data = cli("--all", plan_dir, 2)
        check("Directory scan does not reconcile missing chapters against a plan",
              [code, data["summary"]["total"], data["summary"]["errors"]], [0, 1, 0])

        for number in [10, 2]:
            (plan_dir / f"第{number}章-排序.md").write_text(f"# 第{number}章\n正文", encoding="utf-8")
        code, data = cli("--all", plan_dir, 2)
        check("Arabic chapter numbers sort numerically",
              [Path(item["file"]).name for item in data["results"]],
              ["第01章-已有.md", "第2章-排序.md", "第10章-排序.md"])

    print(json.dumps({"passed": len(observations), "observations": observations},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
