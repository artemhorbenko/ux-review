# Hands-off: UX review: demo report (Parcelly)

Implementation brief generated from the UX review. Work top to bottom: tasks are ordered by ICE, and a task always comes after the ones it depends on. Every task ends with a short usability check; a fix is done when real users pass it, not when the code ships. Treat "rethink" and "hypothesis" tasks as experiments: prototype and test before building.

## Context

- **Main finding:** Shop owners give up at the label price: it appears only after sign-up
- Three of five tasks finished, but the one that decides a purchase — what a label costs — fails on the public site, and connecting a store hides its error behind a spinner. Fix the price answer first, then the connection error and the phone checkout.
- **Persona:** Owner of a small online shop shipping 50–300 parcels a month; first visit, often on a phone between orders.
- **Confidence:** 60%

### Key tasks walked

- T1 Understand what Parcelly does — done; 3 steps, worst friction 1/3
- T2 Find what a label costs — failed; 4 steps, worst friction 3/3
- T3 Start a free trial — stopped at submit; 4 steps, worst friction 2/3
- T4 Connect my shop — done with trouble; 4 steps, worst friction 3/3
- T5 Buy and print the first label — done with trouble; 4 steps, worst friction 2/3

### Owner answers and assumptions

- Who is the user?: Small shop owners, 50–300 parcels a month, often on a phone
- Which tasks matter?: Understand, price, trial, connect store, first label
- What data can you share?: Analytics and 120 pre-sale support tickets (sample)
- What was tested before? (skipped): Skipped. Assumption: no usability tests yet

### Data sources

- [ok] Walkthrough in a browser (desktop and 390px) — used
- [ok] Keyboard walk and accessibility scanner — used
- [ok] Test store connection — used
- [demo] Analytics (sample) — sample
- [demo] Support tickets (sample) — sample
- [no] Session recordings — not connected
- [no] Tests with real users — none yet

Missing, so lower confidence: Session recordings, Tests with real users.

## Rules for the implementer

- Do not buy real labels or connect real customer stores while testing; use the test store and test payment mode.
- Rates shown publicly must come from the live rate service, never typed by hand.
- Record before/after screenshots at 1280px and 390px and a keyboard pass for every changed control.
- Stay within UX: visual polish goes to a UI review, pricing strategy to a product review.
- For a hypothesis or rethink task, prototype and test first; stop if the threshold is not met.

## Suggested order

| # | ID | Task | Where | Severity | ICE | Type | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | UX03 | Move the chat bubble off the “Buy label” button on phones (top 3) | T5 · step 3 | 3 major | 567 | fix | observed |
| 2 | UX02 | Replace the endless import spinner with a clear empty state (top 3) | T4 · step 3 | 4 blocker | 512 | fix | observed |
| 3 | UX01 | Show label prices and a monthly cost calculator on the pricing page (top 3) | T2 · step 2 | 4 blocker | 432 | fix | observed |
| 4 | UX06 | Say “No card needed” next to the sign-up button | T3 · step 3 | 2 minor | 350 | fix | observed |
| 5 | UX04 | Cut sign-up to 3 fields and show password rules up front | T3 · step 2 | 3 major | 343 | fix | observed |
| 6 | UX05 | Write a plain error and a visible “Reconnect” button for failed syncs | T4 · step 4 | 3 major | 343 | fix | observed |
| 7 | UX08 | Use number keypads and units in the parcel fields on phones | T5 · step 2 | 2 minor | 324 | fix | observed |
| 8 | UX07 | Sort carriers by price and add parcel presets | T5 · step 2 | 2 minor | 252 | fix | observed |
| 9 | UX09 | Make help search understand shop owners' words | T2 · step 4 | 2 minor | 240 | fix | observed |
| 10 | UX11 | Add captions and a sound hint to the demo video | T1 · step 2 | 1 cosmetic | 192 | fix | observed |
| 11 | UX10 | Explain each store permission in one line | T4 · step 2 | 2 minor | 140 | fix | hypothesis |
| 12 | UX12 | A rates preview without an account: paste a postcode, see real label prices | T2 · step 3 | 3 major | 96 | rethink | hypothesis |

## Tasks

### 1. UX03 — Move the chat bubble off the “Buy label” button on phones

- Lens: Mobile · Severity: 3 major · ICE 567 = 7×9×9 · fix · observed
- Where: T5 Buy and print the first label → step 3: Pay for the label (/app/checkout)
- Heuristics broken: H5 Error prevention; H8 Minimalist design
- Effort: ≈2 hours

**What we saw.** At 390px the sticky chat bubble covers the right half of the “Buy label” button on /app/checkout; tapping it opened the chat. Analytics sample: 41% of trial sign-ups start on a phone.

**Proposed change.** On checkout screens the chat bubble moves above the bottom action bar, or collapses into a “Help” link in the header.

**Hypothesis.** If the chat bubble moves above the bottom bar during checkout, phone users will reach “Buy label” on the first tap, because nothing covers it.

**Steps:**

1. Hide or move the bubble on /app/checkout at widths under 600px.
2. Make the “Buy label” button full width with 48px height.
3. Check with a 360px and a 390px screen.

**Acceptance criteria:**

- [ ] Nothing overlaps “Buy label” at 360px and 390px
- [ ] The button is at least 48px tall

**Verify with users:**

- Task script: On a phone: buy the label for order #1.
- Success when: Taps “Buy label” on the first try.
- Watch for: Mis-taps, zooming in.

**Cheapest check:** One-line CSS change; compare chat opens from checkout a week before and after

**Metric:** Chat opens from /app/checkout on phones; phone label purchases

**Risk / guardrail:** Less visible help during payment; keep “Help” in the header.

**Alternatives rejected:**

- Shrink the bubble — rejected: still covers part of the button.
- Remove chat in the app — rejected: users need help during their first label.

**Pre-mortem:** It failed because the chat vendor's script re-positioned the bubble after load. So set the position through the vendor's settings, not only in CSS.


### 2. UX02 — Replace the endless import spinner with a clear empty state

- Lens: Error states · Severity: 4 blocker · ICE 512 = 8×8×8 · fix · observed
- Where: T4 Connect my shop → step 3: Wait for orders to import (/app/orders)
- Heuristics broken: H1 Visibility of system status; H9 Recognize and recover from errors
- Effort: 2–3 days

**What we saw.** After connecting a store with no paid orders, /app/orders showed a spinner for over 2 minutes and never changed. Nothing said the connection worked or that the store simply had no orders.

**Proposed change.** Within 10 seconds of connecting: either the imported orders, or an empty state saying “Connected. No paid orders yet” with a button to create a test order and a link to help.

**Hypothesis.** If an empty store shows “No paid orders yet — create a test order” within 10 seconds, new users will not abandon the connection step, because they will know it worked.

**Steps:**

1. Return an explicit “zero orders” result from the import instead of waiting.
2. Show the empty state with a test-order button.
3. Time out after 30 seconds with a plain error and “Try again”.
4. Log empty, error and timeout cases separately.

**Acceptance criteria:**

- [ ] An empty store shows the empty state within 10 seconds
- [ ] A failed import shows a plain error and “Try again” within 30 seconds

**Verify with users:**

- Task script: Connect this test store (it has no paid orders) and tell me when you are ready to ship.
- Success when: Understands within 15 seconds that the store is connected and empty.
- Watch for: Refreshing the page; going back to connect again.

**Cheapest check:** Ship the empty state behind a flag for half of new accounts for 2 weeks

**Metric:** Share of new accounts that reach the first order screen in the first session

**Risk / guardrail:** Showing “No orders” while a slow import is still running; wait for the import's own result.

**Alternatives rejected:**

- A progress bar — rejected: there is nothing to show progress on for an empty store.
- An email when the import finishes — kept as a later addition for large stores.

**Pre-mortem:** It failed because large stores import slowly and now see a false timeout. So set the timeout by order count and show progress for big imports.


### 3. UX01 — Show label prices and a monthly cost calculator on the pricing page

- Lens: Decision support · Severity: 4 blocker · ICE 432 = 9×8×6 · fix · observed
- Where: T2 Find what a label costs → step 2: Find the cost per label (/pricing)
- Heuristics broken: H1 Visibility of system status; H6 Recognition rather than recall
- Effort: 3–5 days plus carrier approval

**What we saw.** /pricing lists three monthly plans; label prices say “See your rates after sign-up”. There is no calculator or example. Support sample: 23 of 120 pre-sale tickets ask what a label costs.

**Proposed change.** A rates block under the plans: typical label prices per carrier for common parcel sizes, and a calculator (labels per month, average weight, destination) that shows the monthly total including the plan fee.

**Hypothesis.** If shop owners can see label prices and a monthly total before signing up, more of them will start a trial, because the price is the question that decides whether to try.

**Steps:**

1. Agree with carriers which rates may be shown publicly; show ranges where exact rates differ by account.
2. Add a rates table for 3 parcel sizes and the 4 main carriers.
3. Add a calculator with 3 inputs that returns plan + labels = monthly total.
4. Link “What will 200 labels cost?” from the home page and the help article.

**Acceptance criteria:**

- [ ] /pricing shows label prices without an account
- [ ] The calculator total equals plan fee + labels × rate from the live rate service
- [ ] Works at 390px with number keypads

**Verify with users:**

- Task script: “You ship about 200 small parcels a month. How much would Parcelly cost you?” Start on the home page.
- Success when: States a monthly total within 2 minutes without creating an account.
- Watch for: Whether they trust the number; which inputs confuse them.

**Cheapest check:** Add a static rates table and a 3-input calculator; compare 2 weeks of trial starts from /pricing with the 2 weeks before

**Metric:** Trial starts per 100 pricing-page visits; pre-sale tickets about label price

**Risk / guardrail:** Shown rates must stay current: pull them from the same source as the app, never type them in.

**Alternatives rejected:**

- A “from $0.xx per label” line only — rejected: still no total for the owner's volume.
- A rates PDF — rejected: does not answer “what will I pay” and goes stale.

**Pre-mortem:** It failed because the shown rates differed from the rates after sign-up and users felt misled. So pull the table from the live rate service and label it “typical rates, yours may be lower”.

**Copy variants:**

- “What will 200 labels cost? Work it out in 10 seconds”: uses the persona's own question.
- “Plan + labels = your monthly total”: explains the two parts of the price in one line.


### 4. UX06 — Say “No card needed” next to the sign-up button

- Lens: Trust · Severity: 2 minor · ICE 350 = 5×7×10 · fix · observed
- Where: T3 Start a free trial → step 3: Check whether a card is needed (/signup)
- Heuristics broken: H6 Recognition rather than recall
- Effort: ≈30 minutes

**What we saw.** The sign-up page does not say whether a card is needed; the answer “No card needed” is in the pricing FAQ.

**Proposed change.** “No card needed — 14 days free” as a line under the “Create account” button.

**Steps:**

1. Add the line under the button on /signup and on the home-page CTA.
2. Remove the duplicate FAQ answer or link to it.

**Acceptance criteria:**

- [ ] Metric: Sign-up starts per visit

**Verify with users:**

- Task script: Before signing up: “Will this charge you anything today?”
- Success when: Answers correctly without leaving the page.
- Watch for: Scrolling to find the answer.

**Metric:** Sign-up starts per visit

**Risk / guardrail:** Only if it is true for every plan.


### 5. UX04 — Cut sign-up to 3 fields and show password rules up front

- Lens: Forms · Severity: 3 major · ICE 343 = 7×7×7 · fix · observed
- Where: T3 Start a free trial → step 2: Fill in the sign-up form (/signup)
- Heuristics broken: H5 Error prevention; H6 Recognition rather than recall
- Effort: 1–2 days

**What we saw.** /signup has 9 fields, 6 required, including a company VAT number and “How did you hear about us?”. Password rules (12 characters, one number) appear only after a failed attempt.

**Proposed change.** Email, password and shop platform only; the rest asked later inside the app when needed. Password rules shown under the field before typing.

**Steps:**

1. Remove VAT number, company size and source from sign-up; ask for VAT at first invoice.
2. Show the password rules under the field and tick them off as they are met.
3. Add autocomplete attributes (email, new-password).

**Acceptance criteria:**

- [ ] Metric: Sign-up form completion rate; errors per sign-up

**Verify with users:**

- Task script: Create an account for your shop; stop before the last button.
- Success when: Fills the form in under a minute without an error.
- Watch for: Pauses at optional fields; reaction to password rules.

**Metric:** Sign-up form completion rate; errors per sign-up

**Risk / guardrail:** Marketing loses the “how did you hear” answer; ask it after the first label instead.


### 6. UX05 — Write a plain error and a visible “Reconnect” button for failed syncs

- Lens: Error states · Severity: 3 major · ICE 343 = 7×7×7 · fix · observed
- Where: T4 Connect my shop → step 4: Retry the connection (/app/settings)
- Heuristics broken: H9 Recognize and recover from errors; H3 User control and freedom
- Effort: 2 days
- Depends on: UX02

**What we saw.** When sync fails, the only message is “Sync job 4 failed (code 0)” in Settings › Advanced, where “Reconnect” also lives. The orders screen shows nothing.

**Proposed change.** A banner on the orders screen: what failed in plain words, and a “Reconnect” button right there.

**Steps:**

1. Map sync error codes to 4 plain messages (permission removed, store offline, timeout, unknown).
2. Show a banner on /app/orders with the message and “Reconnect”.
3. Keep the technical code in a “Details” toggle for support.

**Acceptance criteria:**

- [ ] Metric: Time from a sync failure to the next successful sync

**Verify with users:**

- Task script: Your orders stopped appearing. Get them back.
- Success when: Reconnects from the banner within 1 minute.
- Watch for: Whether they go to Settings first.

**Metric:** Time from a sync failure to the next successful sync

**Risk / guardrail:** Too many banners for short outages; show after 2 failed attempts.


### 7. UX08 — Use number keypads and units in the parcel fields on phones

- Lens: Mobile · Severity: 2 minor · ICE 324 = 4×9×9 · fix · observed
- Where: T5 Buy and print the first label → step 2: Enter the parcel size (/app/orders/1)
- Heuristics broken: H7 Flexibility and efficiency
- Effort: ≈1 hour

**What we saw.** At 390px the weight and size fields open a full text keyboard and show no units next to the numbers.

**Proposed change.** Numeric keypads (inputmode="decimal") and units shown inside the fields.

**Steps:**

1. Set inputmode="decimal" on weight and size.
2. Show “g” and “cm” as suffixes.
3. Check on iOS and Android.

**Acceptance criteria:**

- [ ] Metric: Errors in parcel size per label

**Verify with users:**

- Task script: On a phone: enter a 1.2 kg, 30×20×10 cm parcel.
- Success when: Enters it in one go without switching keyboards.
- Watch for: Unit confusion.

**Metric:** Errors in parcel size per label

**Risk / guardrail:** Low.


### 8. UX07 — Sort carriers by price and add parcel presets

- Lens: Forms · Severity: 2 minor · ICE 252 = 6×7×6 · fix · observed
- Where: T5 Buy and print the first label → step 2: Enter the parcel size (/app/orders/1)
- Heuristics broken: H7 Flexibility and efficiency; H6 Recognition rather than recall
- Effort: 3 days

**What we saw.** Carriers are listed by name. Parcel size has to be typed every time; there are no presets.

**Proposed change.** Carriers sorted by price with delivery time shown; up to 5 saved parcel presets.

**Steps:**

1. Sort by price by default with a toggle for speed.
2. Add “Save as preset” to the parcel form.
3. Pre-fill the last used preset.

**Acceptance criteria:**

- [ ] Metric: Time to buy a label (median)

**Verify with users:**

- Task script: Ship order #2, same box as last time, cheapest option.
- Success when: Done in under 40 seconds.
- Watch for: Scanning the carrier list.

**Metric:** Time to buy a label (median)

**Risk / guardrail:** Cheapest is not always best; show delivery days next to price.


### 9. UX09 — Make help search understand shop owners' words

- Lens: Microcopy · Severity: 2 minor · ICE 240 = 5×6×8 · fix · observed
- Where: T2 Find what a label costs → step 4: Look for the answer in help (/help)
- Heuristics broken: H2 Match with the real world; H10 Help and documentation
- Effort: ≈1 day

**What we saw.** Help search for “label price” returns 0 results; the article that answers it is titled “Carrier rates explained”.

**Proposed change.** Help search that maps shop owners' words to the right articles, and article titles in their words.

**Steps:**

1. Add synonyms: label price → carrier rates, cost, fee.
2. Rename the article “What a label costs”.
3. Review zero-result searches monthly.

**Acceptance criteria:**

- [ ] Metric: Zero-result help searches

**Verify with users:**

- Task script: Find in help what a label to Germany costs.
- Success when: Opens the right article from the first search.
- Watch for: Words they type.

**Metric:** Zero-result help searches

**Risk / guardrail:** Low.


### 10. UX11 — Add captions and a sound hint to the demo video

- Lens: Accessibility · Severity: 1 cosmetic · ICE 192 = 3×8×8 · fix · observed
- Where: T1 Understand what Parcelly does → step 2: Watch the 30-second demo (/)
- Heuristics broken: H1 Visibility of system status
- Effort: ≈2 hours

**What we saw.** The home-page video autoplays without captions; on a phone it starts muted with no sign that it has sound. The scanner flagged the video as having no captions track.

**Proposed change.** Captions on by default and a visible “Sound on” control.

**Steps:**

1. Add a captions track.
2. Show a “Sound on” button on muted playback.

**Acceptance criteria:**

- [ ] Metric: Video completion rate

**Verify with users:**

- Task script: Watch the video on a phone in a quiet room. What did it say?
- Success when: Can repeat the main point.
- Watch for: Whether they look for sound.

**Metric:** Video completion rate

**Risk / guardrail:** Low.


### 11. UX10 — Explain each store permission in one line

- Lens: Trust · Severity: 2 minor · ICE 140 = 4×5×7 · fix · hypothesis
- Where: T4 Connect my shop → step 2: Approve access in the shop (platform pop-up)
- Heuristics broken: H10 Help and documentation
- Effort: ≈half a day

**What we saw.** The platform pop-up lists 11 permissions; Parcelly does not explain why it needs them. Whether this stops people is a hypothesis: no data on drop-off at this step.

**Proposed change.** Before the pop-up, a short list of what Parcelly reads and writes and why.

**Steps:**

1. Write one line per permission group.
2. Show it on /app/connect before redirecting.
3. Track how many cancel in the pop-up.

**Acceptance criteria:**

- [ ] Metric: Share who cancel at the platform pop-up

**Verify with users:**

- Task script: Connect your shop. Would you approve this? Why?
- Success when: Approves and can say why access is needed.
- Watch for: Hesitation at the pop-up.

**Metric:** Share who cancel at the platform pop-up

**Risk / guardrail:** A long list can scare more than it reassures; keep it to 4 lines.


### 12. UX12 — A rates preview without an account: paste a postcode, see real label prices

- Lens: Decision support · Severity: 3 major · ICE 96 = 8×4×3 · rethink · hypothesis
- Where: T2 Find what a label costs → step 3: Estimate the monthly total (/pricing)
- Heuristics broken: H1 Visibility of system status; H6 Recognition rather than recall
- Effort: 1–2 weeks
- Depends on: UX01

**What we saw.** Even with a rates table (#1) owners want their own numbers. A preview that takes a postcode and parcel size and shows live rates without an account might convince more; untested.

**Proposed change.** A public “Check your rates” page: from and to postcodes, parcel size, then live label prices and the monthly total.

**Steps:**

1. Prototype with live rates for one carrier.
2. Test with 5 owners against the rates table.
3. Build only if it beats #1 on confidence and trial starts.

**Acceptance criteria:**

- [ ] Metric: Trial starts after a rates check

**Verify with users:**

- Task script: Find out exactly what your usual parcel would cost to ship.
- Success when: Gets a price they trust and wants to start a trial.
- Watch for: Whether they mind entering a postcode.

**Metric:** Trial starts after a rates check

**Risk / guardrail:** API cost and abuse of a public rates endpoint; rate-limit it.

## Usability-test plan (5 tasks)

- **Participants:** Owners or managers of small online shops shipping 50–300 parcels a month, not Parcelly users; 3 on a phone, 2 on a laptop.
- **How many:** 5 sessions of 40 minutes; repeat with 5 new people after the top fixes
- **Format:** Moderated remote, think-aloud, screen sharing; a test store for task 4. Read each task aloud; do not help.
- **Before the session:** Consent to record; explain we test the app, not them; ask how they ship today.

1. **A friend recommended Parcelly. Take a minute and tell me what it does and whether it fits your shop.**
   - Start: Home page
   - Success: Describes label printing for small shops in their own words.
   - Watch for: Whether they play the video; what they skip.
   - Ask afterwards: Who do you think this is for?
2. **You ship about 200 small parcels a month. Find out what Parcelly would cost you.**
   - Start: Home page
   - Success: States a monthly total without creating an account.
   - Watch for: Where they look for label prices; reaction to “after sign-up”.
   - Ask afterwards: How sure are you of that number (1–7)? / What would stop you from trying it?
3. **You want to try it. Get to the point where you would create the account, then stop.**
   - Start: Pricing page
   - Success: Completes the form in under a minute and knows whether a card is needed.
   - Watch for: Optional fields; password errors.
   - Ask afterwards: What do you expect to happen next?
4. **Connect this test store and get ready to ship your first order.**
   - Start: Empty app after sign-up
   - Success: Understands the store is connected and has no paid orders.
   - Watch for: Waiting, refreshing, reconnecting.
   - Ask afterwards: At which moment did you know it worked?
5. **Ship order #1 with the cheapest option and print the label.**
   - Start: Orders screen with one test order
   - Success: Prints a label in under 2 minutes.
   - Watch for: Carrier choice; parcel fields; the chat bubble on phones.
   - Ask afterwards: What would make this faster next time?

**Measure:** Task success: done, done with help, not done; Time on task; Single Ease Question (SEQ, 1–7) after each task; Wrong turns and taps that open chat; Quotes that explain each failure.

**After the sessions:** Match each failure to a walkthrough step; raise or lower confidence on the matching issues; re-run tasks 2, 4 and 5 after the top three fixes.

## Glossary

- **ICE** (priority score): Impact × Confidence × Ease, each 1–10. The higher the product, the sooner to do it.
- **Nielsen's 10 heuristics** (usability rules of thumb): Ten general principles for interface design by Jakob Nielsen, such as visibility of system status and error prevention. Each issue here is tagged H1–H10.
- **heuristics** (usability rules of thumb): Here, Nielsen's 10 principles; H1–H10 in the tables.
- **Severity** (how bad for the user): 1 cosmetic, 2 minor (slows down), 3 major (many struggle or give up), 4 blocker (cannot be done this way).
- **empty state** (screen with nothing yet): What a screen shows when there is no data, such as a store with no orders. A good one says why and what to do next.
- **inputmode** (keyboard hint): An HTML attribute that tells a phone which keyboard to show, such as numbers only.
- **autocomplete** (autofill hint): An attribute that tells the browser what a field is so it can fill it in.
- **think-aloud** (say what you think): Participants speak their thoughts while doing a task, so you hear why they hesitate.
- **SEQ** (one-question ease score): Single Ease Question: “Overall, how easy was this task?” on a 1–7 scale.
- **pre-mortem** (imagine it failed): Assume the fix failed three months from now and explain why; the reasons become checks to do first.
- **FAQ** (questions and answers): Frequently asked questions; here, on the pricing page.
- **IA** (information architecture): How content is grouped, named and linked, so people can predict where things are.
- **VAT** (sales tax number): A company tax number; here asked at sign-up although it is only needed for invoices.
