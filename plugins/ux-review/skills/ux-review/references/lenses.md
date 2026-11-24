# The 10 UX lenses

Each lens is one question about how people get things done in the product. For each, write 1-3 findings tied to something you saw on a named page and step. Skip a lens only if it truly has nothing to look at (say so in one line).

Scores 0-100 say how well the product already does on that lens: below 40 = people struggle, 40-60 = works with friction, above 60 = solid. Base each score on the findings and the walkthrough, and keep the scale consistent. In `audit.json` each lens has an icon id `i` and a group `g`:

| Lens | `i` | `g` |
|---|---|---|
| Nielsen's 10 heuristics | heur | base |
| Key task walkthroughs | walk | base |
| Information architecture and navigation | ia | find |
| Content clarity and microcopy | copy | find |
| Forms and friction | form | act |
| Error and empty states | state | act |
| Trust and reassurance | trust | decide |
| Decision support (pricing, comparison) | dec | decide |
| Accessibility basics | a11y | reach |
| Mobile ergonomics | mob | reach |

Groups: **base** foundations, **find** find and understand, **act** act and recover, **decide** decide with confidence, **reach** reach everyone.

## Scope

This skill is about whether people can **find, understand, decide and act**. Leave out:
- visual polish (spacing, colour harmony, typography taste, brand look) — that belongs to a UI review (`ui-review`);
- strategy (pricing model, market, growth loops, business model) — that belongs to `product-lens-audit`.

A visual problem is in scope only when it stops a task: low contrast that hides a button, a carousel that hides the only CTA, a sticky banner that covers a form field. A pricing problem is in scope only as decision support: can the person find a price or what it depends on, not whether the price is right.

## Foundations

- **Nielsen's 10 heuristics** — tag every issue with the heuristics it breaks (`H1`-`H10`):
  - H1 Visibility of system status — does the person always know what is happening (loading, saved, sent)?
  - H2 Match with the real world — the person's words, not internal jargon or release numbers.
  - H3 User control and freedom — undo, back, close, cancel; no traps.
  - H4 Consistency and standards — same thing, same name and place; follows platform conventions.
  - H5 Error prevention — constraints, defaults and confirmations stop mistakes before they happen.
  - H6 Recognition rather than recall — options visible; nothing to remember from one page to the next.
  - H7 Flexibility and efficiency — shortcuts for experts (autofill, keyboard, saved filters) without hurting novices.
  - H8 Aesthetic and minimalist design — nothing that competes with the task (only as far as it blocks the task).
  - H9 Help users recognize, diagnose and recover from errors — plain-language errors that say how to fix.
  - H10 Help and documentation — findable help, in context, task-focused.
  The lens score summarizes how many heuristics are broken and how badly.
- **Key task walkthroughs (cognitive walkthrough)** — for each key task, walk the steps as the persona and ask three questions at every step:
  1. **Know**: will the person know what to do here (is the right action visible and named in their words)?
  2. **See**: after acting, will they see that it worked (feedback, state change, next step)?
  3. **Recover**: if they go wrong, can they notice and get back?
  Mark each `y` (yes), `p` (partly), `n` (no) or `null` (not testable, e.g. a form you must not submit). Rate step friction 0 none, 1 minor, 2 major, 3 blocker. Record the task outcome: `ok` done without trouble, `hard` done with trouble, `fail` could not do it, `stop` stopped on purpose (a submit you must not press).

## Find and understand

- **Information architecture and navigation** — Can the person predict where things live? Check: top navigation labels in the persona's words, the page they need is at most 2 clicks from the home page, menu items hidden behind hover-only dropdowns, a label that leads somewhere else than it says, search when the site is large, breadcrumbs and a way back, filters that mix different kinds of category.
- **Content clarity and microcopy** — Does the first screen say what this is, for whom and what to do next? Check: headline states the job, not a slogan; button labels say what happens ("Book a demo", not "Submit"); numbers have context; no internal jargon; helper text next to inputs; empty claims ("premium", "next-generation") without proof nearby.

## Act and recover

- **Forms and friction** — Count visible fields and required ones; ask for each, "is it needed for this step?" Check: labels outside the field (not placeholder-only), correct input types and `autocomplete` attributes, required marked, optional fields that are required, field order, phone required without a reason, what happens after submit stated before submit, inline validation. **Never submit a real form**: inspect it, then stop; record what you could not test.
- **Error and empty states** — 404 pages, empty search results, "no results" after a filter, expired links, validation messages. Does each say what happened and offer a next step? Old URLs still listed in search results that now 404 count here.

## Decide with confidence

- **Trust and reassurance** — At the moment of commitment (form, price, sign-up) is there a reason to believe? Named customers with logos and roles, results with numbers and context, security and privacy notes near the form, what happens next, response time. Testimonials without a company, or proof far from the decision, are weak.
- **Decision support** — Can the person find a price or what it depends on, compare plans side by side, compare with the alternative they are weighing, and see which option fits them? Check: pricing reachable from the main navigation, ranges that cover the person's case, the recommended option visible first on phones, a comparison page with the main competitor, case studies filterable by the person's segment.

## Reach everyone

- **Accessibility basics** — Not a full WCAG audit; the basics that block tasks. Keyboard: Tab through the header and the key task — can every menu and control be reached and used, is focus visible, is there a skip link? Labels: every input has a label, every icon link and logo has a name (alt or aria-label), toggles expose state (`aria-expanded`). Contrast of text that carries the task. Say which checks you ran; use an accessibility scanner if one is connected.
- **Mobile ergonomics** — At phone width (360-390px): no sideways scroll, tap targets at least 24px (44px better), inputs 16px or larger so iOS does not zoom, the primary action reachable, the recommended option or key answer in the first screens, sticky or floating elements not covering content.

## Severity and priority

Give each issue a **severity** (how bad for the person, after Nielsen):
- 1 cosmetic — noticed, does not slow the task;
- 2 minor — slows the task or causes doubt;
- 3 major — many people will struggle or give up on this path;
- 4 blocker — the task cannot be done this way.

Then **ICE** (Impact, Confidence, Ease, each 1-10) decides the order of work. Severity and impact should agree: a severity-4 issue has impact 7 or more; a severity-1 issue rarely has impact above 5. Ease reflects the change, not the problem.

## Weighting by persona and task

Weight lenses by the persona's main tasks: for a B2B buyer comparing vendors, decision support, trust and IA matter most; for a returning user in an app, forms, states and efficiency (H7). Say in `lensesP` how you weighted them.
