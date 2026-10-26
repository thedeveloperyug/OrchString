# OrchString search and answer discovery

Updated: 26 October 2026

The implementation targets relevant search intent through useful, crawlable
content. These keyword themes follow the platform's documented scope; they are
not search-volume, competition or ranking measurements.

The core product identity is a complete enterprise execution platform being
developed to coordinate business operations from start to finish. Workflow
automation, agent orchestration and invoice processing are capabilities and
examples within that broader platform; they do not define its entire scope.

| Canonical page | Main intent | Keyword themes |
| --- | --- | --- |
| `https://orchstring.com/` | Product discovery | OrchString, enterprise execution platform, enterprise AI software, business operations orchestration |
| `https://orchstring.com/ai-workflow-automation/` | Understand and scope a workflow | AI workflow automation for business, enterprise workflow automation, human-in-the-loop workflows, business app integration |
| `https://orchstring.com/ai-agent-orchestration/` | Understand execution architecture | AI agent orchestration, multi-agent task coordination, model routing, controlled AI execution, agent verification |
| `https://orchstring.com/invoice-processing-automation/` | Evaluate a finance workflow | invoice processing automation, accounts payable workflow automation, purchase order matching, invoice approval workflows, three-way matching |
| `https://orchstring.com/faq/` | Get direct product answers | what is OrchString, integrations, AI models, approvals, development status, pilot and pricing inquiries |

## Implemented in the repository

- Unique titles, descriptions, canonical URLs and social metadata on each page.
- A descriptive homepage h1, topical section headings and crawlable guide links.
- Three distinct guides with definitions, examples, controls and evaluation criteria.
- A dedicated FAQ with direct answers and matching `FAQPage` semantic data.
- Consistent organization, application and website identities on the homepage.
- `WebPage`, `Article` and `BreadcrumbList` data for the guides, with visible dates
  and organization attribution. FAQ markup is descriptive; it does not promise
  eligibility for a Google rich result.
- A 1200 × 630 social preview image with descriptive alternate text.
- A sitemap listing all five real canonical pages. Same-page fragments are not
  submitted as separate pages.
- `robots.txt` permits crawling and points to the sitemap.
- A factual `llms.txt` summary links to primary pages and distinguishes product
  direction from deployment availability. It is an optional discovery aid,
  not a Google ranking requirement or a guarantee of AI citations.
- Content remains readable without JavaScript; the connector animation remains
  hidden on phone screens.
- CI validates metadata, local links and assets, schema-to-content consistency,
  FAQ parity, sitemap coverage and the preview image.

## Hosting and Search Console follow-up

The certificate for `orchstring.com` and `www.orchstring.com` is approved.
The audit found that `http://orchstring.com/` still returned content instead of
redirecting to HTTPS. The current GitHub integration rejected the Pages setting
update with HTTP 403, so HTTPS enforcement was not changed.

1. In GitHub **Settings → Pages**, enable **Enforce HTTPS**. Check that HTTP URLs
   redirect permanently to the matching HTTPS path and that the `www` variant
   points to the apex domain.
2. Verify the `orchstring.com` Domain property in Google Search Console using
   the DNS record Google provides. No verification token has been invented or
   added by this change.
3. Submit `https://orchstring.com/sitemap.xml` in **Sitemaps**. Publication of the
   file does not itself confirm that Search Console has accepted a submission.
4. Inspect the homepage and each guide with **URL Inspection → Test live URL**.
   Request indexing for eligible pages after deployment.
5. Monitor impressions, clicks, queries, selected canonical URLs and indexing
   coverage. Group queries by the themes above, then improve content based on
   observed demand and the team's actual product support.
6. Publish verified product documentation, measured case studies and legitimate
   references as they become available. Do not add invented reviews, customer
   results, certifications, addresses or unsupported integrations.

No Search Console submission or ranking measurement was performed by this
repository change. Search crawling, indexing, ranking and generative-answer
citations are determined by the relevant services and are not guaranteed.

## Reference guidance

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview)
- [Schema.org FAQPage](https://schema.org/FAQPage)
