# Data sources

Check what this session can actually reach before gathering: search the tool list (ToolSearch or similar) for each source below. Never assume a connector exists, and never fill a gap with invented numbers. Use every source read-only.

## Status

| Status | When |
|---|---|
| `ok` | Connected and used, or the owner's own answer, screenshot or recording. |
| `demo` | A sample, a partial export, a screenshot with a cut-off date range, a free tier with partial data, or a third-party page you could only read through search results. |
| `no` | Not connected; connected but returning an error, "no plan" or "no access". Try a failing call once more; if it fails again, mark `no` and move on. |

Confidence in the report is the average of ok = 1, demo = 0.6, no = 0, so list only sources that matter for this review.

## Browser (the main source)

- **Tools:** Claude in Chrome, the built-in browser, a cloud browser, Playwright in the shell; WebFetch reads page text only.
- **Do:**
  - walk every key task as the persona, step by step, at desktop width; record the page, what you clicked and what you saw;
  - repeat the key steps at phone width (390px). If the window cannot be resized, open the page in a 390px same-origin iframe from a page of the same site, or use the shell's headless browser;
  - Tab through the header and the key task with the keyboard and log the focus order (a `focusin` listener that records each element's name is enough);
  - read forms with a script: visible fields, required, `type`, `autocomplete`, labels;
  - read hidden content (collapsed FAQ, menus) from the DOM rather than guessing.
- **Stay on the product's domain.** Review the domain the person named (and its `www`). Subdomains such as `get.`, `go.`, `lp.`, `staging.` or `old.` are often A/B-test variants, ad landing pages or staging copies: never walk them as the product. If search results send the persona there, note it once (it is what a searcher meets) and ask the owner what the subdomain is, instead of making it a finding.
- **Prove that a page is missing on the main domain.** Check the navigation and footer, the sitemap (`/sitemap_index.xml`, `/wp-sitemap.xml`, `/sitemap.xml`) and likely addresses with a same-origin `fetch()` from a page of that domain, which returns the real status. A cross-origin or `no-cors` request returns an opaque response with status 0: it proves nothing, so never report a page as present or missing from it.
- **Don't:** submit real forms, payments, messages, sign-ups, chats or newsletter boxes; accept cookies beyond what is needed (reject non-essential); log in to someone's account.
- **Fallback:** the owner's screenshots or a screen recording; mark the walkthrough `demo`.
- **Feeds:** every lens, the walkthrough and the friction strip.

## Analytics and behaviour

- **Tools:** GA4, Amplitude, Mixpanel, PostHog, Matomo; session tools such as Microsoft Clarity, Hotjar, FullStory.
- **Queries, last 90 days:**
  - step-to-step conversion of the key tasks (landing -> pricing -> demo form -> submitted);
  - form abandonment by field, if tracked;
  - rage clicks, dead clicks and quick backs on the key pages;
  - device split (how many people meet the phone layout);
  - internal site search terms and zero-result searches.
- **Fallback:** screenshots of the reports with the date range visible.
- **Feeds:** severity and impact (how many people meet an issue), walkthrough, mobile.

## Accessibility scanners

- **Tools:** axe or Lighthouse in the shell (`npx @axe-core/cli`, `npx lighthouse --only-categories=accessibility`), the browser's accessibility tree (read_page or similar).
- **Use for:** missing names and labels, contrast, focus order, landmarks. A scanner result is `ok` evidence; a clean scan does not prove the site is accessible, so keep the keyboard walk.
- **Feeds:** accessibility basics, forms.

## Search results and third-party pages

- **Tools:** web search, review sites (G2, Capterra), competitors' public pages.
- **Use for:** what the persona finds when they search the task outside the site ("X vs Y", "X pricing"), old URLs that now 404, how competitors answer the same question. Opening each result you cite is required; a snippet alone is `demo`.
- **Feeds:** decision support, error states, trust.

## Support and sales

- **Tools:** Intercom, Zendesk, Front, Help Scout, HubSpot, Salesforce; the owner's summary.
- **Queries:** top "how do I" questions, questions asked on demo calls that the site should answer, form-related complaints.
- **Fallback:** ask in step 0.5 what people ask most before buying.
- **Feeds:** microcopy, decision support, help (H10).

## Usability tests already run

- **Tools:** Maze, Lyssna, UserTesting recordings, the team's notes.
- **Use for:** observed task success, time on task and quotes. These outrank your own walkthrough when they disagree; say so.

## Recording numbers

For every number you use, keep the definition, the period, the source and known gaps. A number in a KPI must name its source (`src` in `audit.json`), and that source must not be marked `no`. Counts you made yourself on the live site (fields, clicks, results, pixels) are `ok` with source "Walkthrough"; give the date.
