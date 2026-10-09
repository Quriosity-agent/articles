---
title: "Anthropic's Cyber Verification Program: Not Removing Safeguards, but Turning Frontier Cyber Capability Into Tiered Access"
date: 2026-10-06
source: "https://x.com/AnthropicAI/status/2107546569654636883"
canonical: "https://www.anthropic.com/news/cyber-verification-program"
tags:
  - Anthropic
  - Cyber Verification Program
  - Claude Mythos 5.1
  - Claude Opus 5.5
  - Cybersecurity
  - Tiered Access
  - AI Safety
  - Project Glasswing
---

# Anthropic's Cyber Verification Program: Not Removing Safeguards, but Turning Frontier Cyber Capability Into Tiered Access

> **In one sentence:** Anthropic has not simply “unlocked Claude for hacking.” It has divided access to the same frontier models into Defense, Red Team, and Specialized tiers. The closer the work gets to live offensive operations, the stronger the requirements become for identity, credentials, devices, network egress, data retention, and continuing review. The product is not fewer refusals alone; it is a revocable and attributable access regime.

- **Original post:** [Anthropic expands the Cyber Verification Program](https://x.com/AnthropicAI/status/2107546569654636883)
- **Official announcement:** [Expanding the Cyber Verification Program](https://www.anthropic.com/news/cyber-verification-program)
- **Published:** October 6, 2026
- **Checked:** October 9, 2026

In April 2026, Project Glasswing gave a small group of critical-infrastructure and software organizations access to the unreleased Claude Mythos Preview. The strategy was straightforward: do not broadly distribute the capability yet; let defenders move first. I examined that phase in an [earlier Mythos and Glasswing analysis](../2026-04-08/claude-mythos-non-release-project-glasswing-analysis-en.md).

Six months later, Anthropic is turning that limited partnership into a program that can be applied for, provisioned, and operated. The expanded Cyber Verification Program, or CVP, covers Claude Opus 5.5, Sonnet 5.5, Mythos 5.1, and future models. It also folds the old CVP and Project Glasswing into three access tiers.

The important change is not that “the safety restrictions are gone.” It is that **one common model-level boundary is becoming a layered system of classifiers, customer verification, organizational controls, monitoring, and revocation.**

## 01 | Four Operating States, Not Three Different Models

Anthropic's comparison places generally available usage next to the three CVP tiers:

![Generally available usage and the three Anthropic Cyber Verification Program tiers](imgs/anthropic-cyber-verification-tiered-access/01-cvp-access-tiers.png)

| Operating state | Core work allowed | Who can qualify | Boundary that remains |
|---|---|---|---|
| Generally available | Secure code review, patching known issues, finding vulnerabilities in owned source, and alert triage | All users | Deeper malware analysis and exploit validation may be interrupted |
| Defense Access | SOC and incident response, malware reverse engineering, detection engineering, and vulnerability analysis and validation | Companies, universities, government bodies, open-source maintainers, bug bounty hunters, and individual researchers | Multi-stage offensive work is still expected to encounter substantial blocking |
| Red Team Access | Authorized penetration testing, red teaming, adversary emulation, offensive tooling, and exploit validation | Organizations only | Ransomware, physical harm, mass disruption, and high-risk safety systems remain blocked in real time |
| Specialized Access | Authorized offensive testing of systems such as power grids, aviation, telecoms, and interbank infrastructure | A limited set of deeply vetted organizations | The Usage Policy still applies; eligibility and controls are most stringent |

The four columns are not four separate models. The public tier uses generally available models with conservative cyber safeguards; all three CVP tiers cover Opus 5.5, Sonnet 5.5, and Mythos 5.1. As access rises, the changes include classifier configuration, permitted scope, entitlement to Mythos, and the controls the customer must operate.

CVP is therefore not a “good person switch.” Anthropic cannot infer the true authorization behind a prompt with certainty. It decomposes the judgment instead: verify the applicant, limit the approved work, attribute requests to named identities, preserve real-time blocks for prohibited outcomes, and retain the ability to narrow or revoke the grant.

## 02 | How the Same Model Produces Very Different Completion Rates

Anthropic tested Opus 5.5 on CyScenarioBench, which evaluates multi-stage, interactive cyber operations. Each tier ran five attempts on each of ten challenges, for 50 trials:

- Generally available: all 50 were blocked on the first prompt.
- Defense Access: 46 were blocked at some point; four succeeded.
- Red Team Access: no trial was blocked, and 34 succeeded.
- No-safeguards reference: a 67.6% success rate, effectively the same as Red Team's 34 out of 50.

![Opus 5.5 completion rates on CyScenarioBench under different CVP tiers](imgs/anthropic-cyber-verification-tiered-access/02-cyscenariobench-results.png)

The result supports two separate observations.

First, the access layer materially changes which tasks the model can execute. Defense is not merely a cheaper or weaker Red Team tier. It is intentionally configured to interrupt complex attack chains. Red Team restores performance to approximately the unsafeguarded capability ceiling.

Second, **not being blocked does not mean succeeding**. None of the 50 Red Team trials triggered a classifier block, but only 34 completed. The other failures came from model capability, planning, tool use, or the environment rather than the safety classifier. Refusal rate and task success rate must be kept separate.

This remains a calibration test run by Anthropic on only ten scenarios. It does not show that identity checks prevent insider abuse, measure a long-running agent's chance of escaping authorization in a real enterprise network, or report false-positive rates on ordinary defensive work. It demonstrates that **the three classifier configurations behave differently**, not that the complete governance system has been validated end to end.

## 03 | As Work Approaches Live Offense, Eligibility Becomes Enterprise Security Architecture

The X post makes CVP sound like a verification program for professionals. The Help Center requirements are much more concrete.

Every access level needs a named security contact and attribution to a specific user or workload identity. Organizations must report a relevant security incident within 24 hours and begin investigating identified misuse within 48 hours.

From December 15, 2026, Defense Access requires phishing-resistant MFA and disallows long-lived API keys. Individuals can qualify only for this tier, and their traffic must be retained and monitored; zero data retention is unavailable to them.

Red Team Access further requires:

- organization-domain accounts and, by default, no more than 25 approved users;
- short-lived credentials instead of static long-lived keys;
- an off-host network egress allow-list with logging wherever agentic offensive work occurs;
- organization-managed devices;
- identity checks and, where lawful, background checks for approved users;
- the ability to revoke compromised identities or credentials within 24 hours;
- removal of departed or reassigned users within three business days.

Specialized Access adds SSO, endpoint malware controls, and stricter device and organizational review. Applications involving power, aviation, telecommunications, and financial infrastructure are currently reviewed organization by organization in collaboration with the US government.

Anthropic's unit of safety is therefore no longer only a prompt classifier. It is a combination of **identity, least privilege, short-lived credentials, managed endpoints, network isolation, logs, incident response, and supplier review**. As model capability rises, the customer's own security maturity becomes an access requirement.

## 04 | Data Retention Is the Most Concrete Cost of the Program

CVP requires data retention by default so Anthropic can monitor cyber misuse and investigate anomalies. That is not a minor detail for a security team. Inputs may contain undisclosed vulnerabilities, malware samples, internal network topology, proprietary source code, and incident logs.

Anthropic's proposed bridge is Enterprise Frontier Safeguards, or EFS. Once available, eligible organizations should be able to store data in cloud infrastructure they control while preserving stronger safeguards. For now, organizations that already have a zero-data-retention exemption for Fable 5.1 or Mythos 5.1 can use CVP with ZDR. Individual Defense Access explicitly cannot.

This is not a fully resolved privacy problem. It is a trade: **less blocking requires stronger identity binding and observability**. For security firms handling regulated or customer-confidential material, joining CVP depends on data residency, contractual liability, and monitoring scope as much as it depends on model capability.

## 05 | Project Glasswing's Numbers Are Large, but Their Denominators Matter

Anthropic uses six months of Project Glasswing evidence to justify expanding access. Its chart combines 33 partner reports with Anthropic's open-source scanning:

![Vulnerabilities identified by Project Glasswing partners and Anthropic scanning](imgs/anthropic-cyber-verification-tiered-access/03-glasswing-vulnerability-impact.png)

| Stage | Count |
|---|---:|
| Candidate findings | 595,597 |
| Triaged findings | 208,175 |
| Confirmed true positives | 135,610 |
| High severity | 27,989 |
| Critical severity | 5,680 |
| Reported as patched | 9,333 |

The announcement summarizes this as at least 129,000 verified vulnerabilities found by partners between April and July 2026, plus about 5,500 found by Anthropic in open-source software between April and October. More than 33,000 were high or critical severity.

Those numbers are strong evidence that frontier models can expand vulnerability discovery at scale. They do not mean 135,610 distinct CVEs, nor do they mean every finding has been fixed. Anthropic says the data are based on partial self-reporting, partners used different triage methods, and fewer than half disclosed patch counts. The 9,333 patches are therefore a reported lower bound, not a defensible denominator for a true patch rate. Conversely, Anthropic's claim that real impact is at least five times higher remains an estimate rather than an independent audit.

The careful conclusion is that **the bottleneck is moving from candidate discovery to triage, deduplication, disclosure, and remediation**. Once models can generate hundreds of thousands of findings, the scarce resource may no longer be scanning but the human and engineering capacity required to validate and fix them.

## 06 | Approval Does Not Let a Company Repackage the Grant as a Product

A CVP grant covers work on an organization's own code, products, and infrastructure. Running the privileged model against customer systems, exposing it through a client-facing application, or productizing CVP capability requires separate approval.

That boundary is essential. Otherwise, one approved red-team firm could become a shared relay for every customer, bypassing the meaning of organization vetting and the 25-seat limit.

Third-party platforms currently support Defense and Red Team access only, not Specialized Access. CVP is available through Anthropic's first-party products, the Claude Platform, Google Cloud Vertex AI, and Microsoft Foundry. Amazon Bedrock support is currently limited to customers eligible for EFS. Approval is therefore not a portable badge attached to one account; it is a grant bound to workspaces, cloud accounts, platform capabilities, and administrator provisioning.

## 07 | What This Governance Model Changes

Model releases used to have two simple states: public or withheld. CVP creates an operational middle layer. The model can remain the same while users receive different capability boundaries. Higher access is not unlocked by accepting a disclaimer; it depends on eligibility, technical controls, and continuing review.

That makes frontier models look more like controlled infrastructure than ordinary software subscriptions:

- **Entitlement becomes part of the product.** What the system can do depends on a grant, not only on the selected model.
- **Safety extends into the customer's environment.** MFA, credential lifetime, device management, network egress, and incident response become conditions of access.
- **Responsibility is shared.** Anthropic tunes classifiers; the customer must establish authorization, user identity, and operating controls.
- **Revocability becomes a core feature.** Anthropic can narrow or withdraw a grant, and administrators must be able to revoke internal credentials quickly.

The pattern may extend beyond cybersecurity. Anthropic's Life Sciences Verification Program already follows a related approach. As models become more capable in high-risk domains, “same model, different entitlement, different audit requirements” may become a common delivery architecture.

## 08 | Seven Questions Security Teams Should Ask

For an organization considering CVP, the useful questions go well beyond whether Claude will refuse less often:

1. Is the work ordinary secure development, Defense, Red Team, or high-risk Specialized activity?
2. Can every test be tied to asset ownership or explicit authorization?
3. Can long-lived API keys be replaced with short-lived identity credentials before the cutoff?
4. Can agent network egress be enforced outside the host and logged completely?
5. Who owns 24-hour incident reporting, 48-hour investigation, and 24-hour credential revocation?
6. May vulnerability data be retained and monitored, or must the organization wait for EFS or a ZDR path?
7. If discovery accelerates, can triage, deduplication, disclosure, and patching keep up?

Without answers, fewer model blocks merely move the bottleneck from Claude into the organization.

## Conclusion: Capability Is Being Wrapped in an Institution

The expanded CVP signals that frontier cyber capability is leaving behind the assumption that one model should behave identically for every user.

General users retain code review, patching, and vulnerability analysis on owned code. Verified defenders can reduce false blocks. Professional red teams can recover capability close to the no-safeguards baseline inside authorized scope. Testing critical safety systems enters a deeper layer of organizational and government review.

CyScenarioBench shows that these tiers meaningfully change model behavior. Glasswing's results show why organizations want the capability. Neither proves that governance is finished. The effectiveness of applicant verification, the privacy cost of monitoring, insider misuse, and the capacity to remediate hundreds of thousands of findings still have to be tested in real operations.

Anthropic is not abandoning cyber safeguards. It is turning the question of **who may use which capability, in what environment, with what accountability** into the product itself. The model is the engine; the real release is a licensing system.

## Primary Sources

- [Anthropic's X announcement](https://x.com/AnthropicAI/status/2107546569654636883)
- [Expanding the Cyber Verification Program](https://www.anthropic.com/news/cyber-verification-program)
- [Cyber Verification Program Help Center](https://support.claude.com/en/articles/14604842-cyber-verification-program)
- [CVP Security Requirements](https://support.claude.com/en/articles/17202708-cyber-verification-program-security-requirements)
- [Project Glasswing](https://www.anthropic.com/glasswing)
- [Developing Enterprise Frontier Safeguards](https://www.anthropic.com/news/enterprise-frontier-safeguards)

*This article reflects official announcement and Help Center material available on October 9, 2026. Eligibility, supported platforms, models, and retention requirements may change.*
