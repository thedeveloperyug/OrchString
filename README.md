# NEYTRA Intelligence Platform — Website

Official website: https://neytraintelligence.com/

**Primary project:** NEYTRA Intelligence Platform (NIP)  
**Status:** Active development  
**Tagline:** Think. Adapt. Act.

## Purpose

This repository contains the public-facing website for **NIP — NEYTRA Intelligence Platform**.

NIP is an OS-agnostic intelligent execution platform designed for reasoning, planning, model orchestration, memory, environment awareness, capability discovery, tool intelligence, multi-task execution, verification, developer intelligence and controlled autonomy.

**NIP is the current engineering focus. NEYTRA OS remains a separate future operating-system project and is intentionally preserved as part of the NEYTRA vision.**

## What NIP is

NIP is designed as a control plane and execution platform rather than a chatbot or simple LLM wrapper.

Its target lifecycle is:

**Understand → Decompose → Plan → Discover → Select → Authorize → Execute → Observe → Critique → Reason → Verify → Recover / Replan → Learn**

The architecture supports:

- Job and multi-task orchestration
- Dependency-based task graphs and parallelism
- Deterministic Core execution
- Goal-driven agents
- Planner / Executor / Observer / Critic / Reasoner / Verifier pipeline
- Scheduler and bounded dispatch
- Agent placement
- Execution attempts, leases and fencing
- Agent runtime and worker lifecycle
- Model invocation and model execution attempts
- Model/provider abstraction and future intelligent routing
- Capability and tool discovery
- Capability-first tool selection
- Evidence-backed tool behavior knowledge
- Security, policy and authorization boundaries
- Checkpoints and recovery
- Verification and evidence traceability
- Developer intelligence
- Linux and future multi-OS adapters
- Future deep NEYTRA OS integration

## NIP ↔ NEYTRA OS

The projects have a deliberate boundary:

| Project | Responsibility |
|---|---|
| **NIP** | Intelligence, jobs, tasks, agents, models, capabilities, tools, reasoning, verification |
| **NEYTRA OS** | Operating system, services, desktop, hardware, isolation and system-level authority |
| **Integration Bridge** | Requests, events, capabilities, permissions, execution results and artifacts |

**NEYTRA OS provides the system. NIP provides the intelligence.**

The website therefore presents NIP as the active platform while retaining NEYTRA OS as the future operating-system direction.

## Website design

The site keeps the existing NEYTRA visual language and animations, including:

- Animated particle field
- Interactive cursor glow
- Animated intelligence core
- Rotating rings and orbital effects
- Scroll-reactive core motion
- Device-orientation interaction where supported
- Reveal-on-scroll sections
- Animated grid background
- Hover / tilt-style cards
- Responsive mobile navigation
- Reduced-motion accessibility support

The new NIP-first experience adds visual representations for:

- NIP execution lifecycle
- Platform architecture
- Core capabilities
- Controlled execution
- Model runtime
- NIP ↔ NEYTRA OS boundary
- Development roadmap

## Repository naming

The current GitHub repository is named `neytra-os-website`. The intended identity of this website is now **NEYTRA Intelligence Platform**.

GitHub repository renaming is an account-level repository setting; after renaming it, update the GitHub Pages URL and any external references if GitHub does not automatically preserve the expected redirect.

## Deployment

GitHub Actions deploys `main` to GitHub Pages via:

`.github/workflows/deploy.yml`

## Founder

**Yogesh Pandey** — Founder & creator of the NEYTRA platform vision.

LinkedIn: https://www.linkedin.com/in/thedeveloperyug  
Email: thedeveloperyug@gmail.com

---

**NIP — The intelligence layer for NEYTRA.**

**Think. Adapt. Act.**

## SEO and domain routing

**Canonical website:** `https://neytraintelligence.com/` (the one-page public site).

**Secondary domain:** `neytraintelligence.in` is a redirect-only domain. Neither
the .in domain nor a `www` alias should serve a separately indexable copy.

The following should be configured at the DNS/CDN/registrar/hosting redirect layer,
**not** as a JavaScript redirect in `index.html`:

| Incoming URL | Expected response | Destination |
| --- | --- | --- |
| `http://neytraintelligence.in/` | 301 or 308 | `https://neytraintelligence.com/` |
| `https://neytraintelligence.in/` | 301 or 308 | `https://neytraintelligence.com/` |
| `http://www.neytraintelligence.in/` | 301 or 308 | `https://neytraintelligence.com/` |
| `https://www.neytraintelligence.in/` | 301 or 308 | `https://neytraintelligence.com/` |
| `https://www.neytraintelligence.com/` | 301 or 308 | `https://neytraintelligence.com/` |
| `http://neytraintelligence.com/` | 301 or 308 | `https://neytraintelligence.com/` |

Keep redirects **permanent, direct, and server-side**; preserve paths and query
strings when an equivalent destination exists. Ensure all four hostnames have
correct DNS and valid HTTPS certificates before requiring HTTPS redirects.
Do not add `noindex` or disallow these URLs in `robots.txt` merely to remove
Search Console's expected "Page with redirect" or "Alternate page with proper
canonical tag" classifications.

### Indexability signals

- `index.html` sets a self-referencing canonical and matching Open Graph URL.
- `robots.txt` allows crawlers and references `https://neytraintelligence.com/sitemap.xml`.
- `sitemap.xml` lists **only** the canonical homepage. The current navigation
  uses same-page hash fragments, which are not standalone pages to submit.
- The GitHub Pages workflow executes `.github/scripts/check_seo.py` before deploy
  to prevent accidental SEO regressions. Run it locally with
  `python3 .github/scripts/check_seo.py`.

### Google Search Console verification

1. Verify ownership of **both domains** (Domain properties if possible).
2. Submit `https://neytraintelligence.com/sitemap.xml` in the .com property's
   Sitemaps section.
3. In URL Inspection for `https://neytraintelligence.com/`, run **Test Live URL**
   and **Request Indexing** if it is eligible but not indexed.
4. Under Pages > Not indexed, inspect the **exact URLs** associated with
   "Page with redirect" and "Alternate page with proper canonical tag".
   These are normal when they point to the intended indexed .com canonical.
   Escalate only if the preferred .com URL is itself excluded or Google selects
   a different canonical.
5. Test HTTP status codes and final destinations for the table above.
   GitHub source code alone cannot configure the external .in forwarding service.

Google indexing and rankings are determined by Google's crawl/indexing systems;
deployment does not guarantee immediate inclusion in search results.
