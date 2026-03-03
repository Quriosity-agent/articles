# Vercel CLI Complete Guide: 40+ Commands for Full-Stack Deployment

> **TL;DR**: Vercel CLI covers 40+ commands: deploy, domains, DNS, env vars, cache, certs, Blob storage, microfrontends, rolling releases, and more. Key highlights: `bisect` (binary search deployments for bugs), `rolling-release` (gradual traffic shifting), `mcp` (MCP integration for AI agents), and `curl/httpstat` (debug with deployment protection bypass).

---

## Key Commands

| Category | Commands | Purpose |
|----------|----------|---------|
| **Deploy** | deploy, build, redeploy | Build and ship |
| **Rollback** | rollback, promote, bisect | Undo and debug |
| **Release** | rolling-release | Gradual rollout |
| **Monitor** | list, inspect, logs | View deployments |
| **Domains** | domains, alias, dns, certs | Domain management |
| **Storage** | blob, cache | Object storage & CDN cache |
| **Config** | env, pull, target | Environment variables |
| **Debug** | curl, httpstat, dev | HTTP testing & local dev |
| **AI** | mcp | MCP protocol integration |

## Standout Features

1. **bisect** — Binary search through deployments to find the one that introduced a bug
2. **rolling-release** — Gradual traffic shifting for zero-downtime deploys
3. **mcp** — Built-in MCP client configuration for AI agent integration
4. **curl/httpstat** — Debug with automatic deployment protection bypass

## QCut Relevance
If QCut website migrates from GitHub Pages to Vercel: SSR, API routes, Edge Functions, faster CDN. CLI enables full automation for AI-driven deployment workflows.

## Resources
- Docs: <https://vercel.com/docs/cli>
- Install: `npm i vercel`

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-03*
*Tags: Vercel CLI / Deployment / DevOps / CDN / Rolling Release / MCP*
