# OrchString — Website

Official website: https://orchstring.com/

**Primary project:** OrchString

**Status:** Active development  
**Tagline:** One intelligence platform<br>Infinite business possibilities

## Purpose

orchstring is an AI-powered, enterprise-oriented execution platform designed to transform business objectives into coordinated, controlled, and verifiable workflows.

This repository contains the public-facing website for **orchstring**.

orchstring is being developed as a complete enterprise software platform for
end-to-end business automation across planning, approvals,
execution, verification and recovery. Workflow automation and agent orchestration
are capabilities within that broader platform.

orchstring is an OS-agnostic intelligent execution platform designed for reasoning, planning, model orchestration, memory, environment awareness, capability discovery, tool intelligence, multi-task execution, verification, developer intelligence and controlled autonomy.

orchstring is the current engineering focus. The future operating-system project remains separate, with native integration planned as part of the long-term vision.

## What OrchString does

orchstring is designed as a control plane and execution platform rather than a chatbot or simple LLM wrapper.

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
- Future native OS integration

## OrchString and future OS integration

The projects have a deliberate boundary:

| Project | Responsibility |
|---|---|
| **OrchString** | Intelligence, jobs, tasks, agents, models, capabilities, tools, reasoning, verification |
| **Future OS project** | Operating system, services, desktop, hardware, isolation and system-level authority |
| **Integration Bridge** | Requests, events, capabilities, permissions, execution results and artifacts |

**The future OS project provides the system. orchstring provides the intelligence.**

The website therefore presents orchstring as the active platform while retaining the future OS project as the future operating-system direction.

## Website design

The site uses a white, blue and black visual system, including:

- Text-only navigation wordmark: blue **orch**, black **string**
- An open blue connector network converging on **OrchString Console**
- Recognizable icons for Teams, Outlook, Gmail, Google Drive, Microsoft and Google
  accounts, billing, payments, invoices and AI models
- Soft wave and jelly motion with signals traveling inward to the console
- The hero illustration is hidden on phones, including common landscape layouts
- Blue, slightly bold **OrchString** emphasis in the visible introductions
- Reveal-on-scroll sections
- Responsive mobile navigation
- Reduced-motion accessibility support with a still connector diagram
- Animation that pauses when off-screen or the browser tab is hidden

The orchstring experience adds visual representations for:

- OrchString execution lifecycle
- Platform architecture
- Core capabilities
- Controlled execution
- Model runtime
- Intelligence and operating-system boundary
- Development roadmap

## Repository and deployment

Source: https://github.com/thedeveloperyug/OrchString

The repository keeps its existing GitHub URL. Its website, documentation and
workflow use the orchstring brand.

GitHub Actions deploys `main` to GitHub Pages through
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). The workflow
validates branding, SEO metadata and the sitemap before uploading the static
website and running the deployment job. It also supports manual runs with
`workflow_dispatch`.

Run the deployment checks locally:

```sh
python3 .github/scripts/check_seo.py
node --check app.js
```

The Pages custom domain is `orchstring.com`. `CNAME` records the same domain in
source control. No build step or package installation is required.

The hero and navigation no longer display the previous logo. The browser icon
is a blue capital O SVG; the Apple touch icon uses the same O artwork. The console destination remains unchanged; the contact addresses now use
orchstring.com email accounts. The console link is labeled
**Explore OrchString Console**.

## Founder

**Yogesh Pandey** — Founder & creator of the orchstring platform vision.

LinkedIn: https://www.linkedin.com/in/thedeveloperyug  
Email: yogesh.pandey@orchstring.com

Co-founder: **Rishabh Saluja** — Business and growth  
Email: rishabh.saluja@orchstring.com

---

**OrchString — Intelligent business execution.**

**One intelligence platform**<br>
**Infinite business possibilities**

## SEO and domain routing

**Canonical website:** `https://orchstring.com/`.

**Sitemap:** https://orchstring.com/sitemap.xml

The site includes dedicated guides for AI workflow automation, agent
orchestration and invoice processing, plus a product FAQ. See the
[keyword themes and follow-up actions](docs/seo-plan.md).

Any previous domains or `www` aliases should redirect permanently and directly
to the canonical website at the DNS/CDN/registrar/hosting layer. Preserve paths
and query strings when an equivalent destination exists, and configure valid
HTTPS certificates for each redirecting hostname. External domain redirects are
managed outside this repository.

### Indexability signals

- `index.html` sets a self-referencing canonical and matching Open Graph URL.
- `robots.txt` allows crawlers and references `https://orchstring.com/sitemap.xml`.
- `sitemap.xml` lists the homepage, three workflow guides and the FAQ. Same-page
  navigation fragments are not separate sitemap pages.
- The GitHub Pages workflow executes `.github/scripts/check_seo.py` before deploy
  to validate every canonical page, internal link, schema, FAQ answer, sitemap
  entry and social preview asset. Run it locally with
  `python3 .github/scripts/check_seo.py`.

### Google Search Console verification

1. Verify ownership of `orchstring.com` (a Domain property if possible).
2. Submit `https://orchstring.com/sitemap.xml` in the property's Sitemaps section.
3. In URL Inspection for the homepage and each guide, run **Test Live URL** and
   **Request Indexing** if the URL is eligible but not indexed.
4. Confirm that redirected and alternate URLs point to the canonical homepage.
   Configure any old-domain forwarding at the external hosting or DNS provider.
5. Check HTTP status codes and final destinations after routing changes.

Google indexing and rankings are determined by Google's crawl/indexing systems;
deployment does not guarantee immediate inclusion in search results.
