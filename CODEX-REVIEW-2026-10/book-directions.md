# Noah Garage Doors: mobile booking directions

Review date: October 3, 2026. Audience: a homeowner arriving from the Google Business Profile Book button, often with a broken door and little patience for a complicated form.

**Recommendation: Direction 1, “A direct line to Noah.”** Make the owner, callback expectation, contact fields, and phone alternative immediately understandable. Direction 2 is a useful alternative if the existing problem choices help customers start. Direction 3 makes the strongest visual impression, at the cost of a longer route to the form.

This is a design review and proposal, not an implementation. Conversion improvements below are hypotheses, not measured results.

## Research scope and evidence

I read `book/index.html`, `quote-form.js`, and `cookie-consent.js`, fetched the live booking HTML and shared contact script over the network, and confirmed that both match their local counterparts after normalizing line endings. I visually inspected the existing hero and the real image files named below.

I also inspected five public booking/request pages through network page extraction, with direct HTML inspection where useful. No available browser supported a rendered mobile inspection in this session. Consequently, current-page fold positions are CSS-based estimates, competitor observations concern their accessible content and structure, and proposed 390 × 844 layouts are design budgets to validate during implementation. I did not submit any forms or verify competitors' appointment availability.

### Five pages worth learning from

| Company and inspected URL | What was observable | One or two patterns worth borrowing |
| --- | --- | --- |
| **Precision Garage Door San Diego**: [Schedule](https://www.garagedoorssandiego.net/schedule) | A dedicated appointment heading, phone access, service-area information, reasons to choose the company, and review proof. The scheduling widget itself was not exposed in the text extraction. | **1. Keep a phone route beside the online route.** **2. Put local credibility close to the request.** For Noah, compress this to San Diego County, the exact Google rating/review count, and the license; do not reproduce the long regional directory. |
| **A1 Garage Door Service**: [Book online](https://a1garage.com/book-online/) | An explicit scheduling heading and booking buttons, plus a phone alternative for people unsure where to start. Promotions and location navigation extend the page. The inner scheduler was not inspected. | **1. Make the task unmistakable in the heading and CTA.** **2. Offer human help for uncertainty.** Adapt the task to a callback request, since Noah's current form does not reserve a time. The promotional modules are unnecessary here. |
| **Radford Garage Doors & Gates, San Diego**: [Book repair or service](https://radfordgaragedoor.com/book-repair-or-service/) | The page explicitly offers a form, phone, or email; it includes local contact details and business hours. Its navigation distinguishes estimates from service. Embedded form fields were not exposed. | **1. Give repair requests a clear destination separate from new-door browsing.** **2. Make the direct contact alternative explicit.** Noah can preserve a new-door option within the form without turning this landing page into a product showroom. |
| **Mr. Handyman of Greater Sioux Falls**: [Request service](https://www.mrhandyman.com/greater-sioux-falls/request-service/) | Indexed page content and directly fetched HTML configuration show an explanation of the callback/scheduling sequence, a contact-information section, required-field labels, and optional texting consent. The contact configuration includes name, address, email, and phone fields. | **1. Explain the next human interaction before collecting information.** **2. Divide a longer flow into understandable sections.** Borrow the clarity; Noah does not need its address and email burden to return a call. No claim is made about uninspected later steps. |
| **Garage Door Pro LLC, Central Indiana**: [Book online](https://www.garagedoorpro.services/book-online/) | A service/quote request with four broad service categories, followed by a service-details section containing address, phone, full name, and additional information; customer reviews follow. | **1. Group the request around the problem and then contact details.** **2. Place proof alongside the request journey.** For Noah, use customer symptoms and a prominent uncertainty option; postpone the address until the conversation. |

The useful common ground is clear intent, a human alternative, organized inputs, and proof. These examples do not establish that a particular color, number of steps, or large hero increases conversion. National-brand scheduling infrastructure and claims should not be copied into a one-person callback flow.

## Honest critique of the current page

### Hierarchy and first screen

The page has good ingredients but gives too many of them equal visual weight. The photograph, condensed uppercase headline, rating capsule, numbered sections, seven icon tiles, glowing submit button, green phone button, and floating contact bar all compete. The result feels busier than the underlying task warrants.

The hero has a 380px minimum height, with a large top gap before the headline. The content overlaps it by 72px. At 390px wide, the rating strip will likely wrap its licensing claim, and the form starts roughly 390px down. The service choices alone consume approximately 370px before the contact section's spacing. On a 390 × 844 viewport, the initial experience is predominantly hero, rating, and problem selection. Name and phone begin around or below the bottom edge; Submit is farther down. These are estimates, not screenshot measurements.

The page's actual purpose, “Request a call back,” is a visually hidden heading. A visitor arriving through Book may expect a confirmed appointment. The visible headline does not resolve that expectation, and “acting up?” is slightly casual for someone whose car is trapped. Lead with Noah and the action; state that he calls to discuss the problem and arrange a visit.

### Friction

The short data requirement is a strength: name, phone, service, and an optional note. Telephone input, autocomplete, optional ZIP inside the note, and the uncertainty choice are worth keeping.

But seven large tiles ask the homeowner to classify a fault before seeing how little contact information is needed. Several symptoms overlap. A door that will not open could also have a broken spring, cable problem, or opener fault. The customer should not feel responsible for diagnosis.

The numbered headings suggest a two-step process, but everything is one scrolling form. They add visual machinery without reducing the amount on screen. Use either a genuinely compact single form or a genuine two-step interaction.

The visible name and phone labels are placeholders. Accessible hidden labels exist, but the visual labels disappear when typing. Persistent labels would make reviewing and correcting details easier.

### The floating contact bar is a concrete integration issue

`cookie-consent.js` injects a fixed Call/Text bar on `/book/`. Its overlap guard looks for `#quote`, but this page only has `#quoteForm`. Consequently, the guard never hides the bar around this form. Bottom padding lets users scroll past it, but does not prevent it from covering fields or competing with Submit along the way.

There are also duplicate in-page phone/text actions. The floating copy says “Text us,” which breaks the one-person voice. The page's explicit tracking listeners cover `#callBtn` and `#textBtn`; the injected links do not receive those listeners in the reviewed scripts. A redesign needs one deliberate contact treatment and consistent measurement.

### Trust and expectations

The accurate **5.0 rating and 129 Google reviews**, real customer photograph, and licensing information are meaningful strengths. However, the license number is relegated to the footer, and the explanation of the callback and visit sits after the form and review. Put a concise next-step explanation before the request and show **CSLB #1159513** with the trust details.

The existing `/book/hero-doors.jpg` visually matches the real black-door project in `gallery1.jpeg`; the current booking hero should not be described as an AI van or person. Its weakness is placement and treatment: a substantial darkened installation photograph takes priority over arranging help. The existing Ren image is a close-up of garage-door hardware, not a portrait of Noah.

“Right back” and “shortly” create unnecessary callback-speed expectations for a sole operator. Replace them with a clear sequence without a time promise. Also remove or clarify “Free, no obligation” unless the owner has established exactly which part is free; it can be read as a free visit. Retain the existing price-before-work reassurance as a statement from Noah.

### Consent and visual quality

The two SMS checkboxes appear **after** Submit. This creates an awkward reading order: the user reaches the action before encountering the communication choices. Move the complete, unchanged consent block above the final submit button in every direction. Keep both choices optional and unchecked.

Consent copy is currently 10.5px, using `#6B778C` on `#111723`. Those solid CSS colors produce approximately **3.97:1 contrast**, below a 4.5:1 normal-text target. Placeholder text uses the same faint color on another dark panel. This is a practical readability problem on a phone, particularly outdoors.

The dark palette itself is not the problem. The accumulation of low-contrast panels, borders, pill shapes, shadows, glows, icons, and a pulsing availability dot makes the page feel like a template interface. Reduce the decorative vocabulary. Let clear typography, a single action color, generous grouping, and authentic photography do the work.

## Shared requirements for all three directions

These requirements are part of each direction, including the two-step option.

### Form and behavior contract

| Element | Preserve |
| --- | --- |
| Form | One `form#quoteForm`; preserve the existing submission integration. |
| Final submit | `button#quoteSubmit[type="submit"]` containing `#quoteSubmitText`. |
| Feedback | `#formError` with `role="alert"` and `tabindex="-1"`; `#formSuccess` with `role="status"` and `aria-live="polite"`. Both initially use `.hidden`. |
| Attribution | Hidden `#leadSource` with `name="lead_source"`; hidden `#formStartedAt` with `name="form_started_at"`. Preserve initialization by `quote-form.js`. |
| Honeypot | Input `name="website"`, outside the visible flow, excluded from keyboard navigation and assistive presentation as currently implemented. |
| Customer data | `name="name"`, `name="phone"`, required `name="service"`, and optional `name="message"`. Retain existing `quoteName`, `quotePhone`, and `quoteMessage` IDs and name/phone validation attributes. |
| Texting choices | `name="sms_consent_service"` / `id="quoteSmsService"` and `name="sms_consent"` / `id="quoteSmsConsent"`. Both optional and initially unchecked. |

Use the existing seven service payload values: `Emergency Repair`, `Spring Replacement`, `Off Track Repair`, `Cable Repair`, `Opener Installation`, `Full Door Replacement`, and `Other / Not Sure`. Plain-language labels may describe symptoms. The existing opener value is a routing label, not authorization for an installation. Leave the initial selection empty and require a deliberate choice, including “Not sure.”

Name and phone remain required; do not add email, address, date, account creation, photo upload, or payment. Preserve the note as a real field even if its optional disclosure is closed.

`quote-form.js` calls `form.reportValidity()`, reads named fields, hides the form on success, and reveals its sibling success container. Keep `#formSuccess` outside the form and outside any ancestor hidden on success. The script resets the button to a quote-related label after an error; preserve an equivalent page-specific label correction for the chosen callback CTA. Do not accidentally introduce a second network submission handler.

### Exact consent text, visible beside the corresponding checkbox

**`sms_consent_service`:**

> By checking this box, you agree to receive transactional and informational text messages about your service request and appointments from Noah Garage Doors. Message frequency varies. Msg & data rates may apply, reply HELP for help or STOP to opt out.

**`sms_consent`:**

> By checking this box, you agree to receive promotional and marketing text messages from Noah Garage Doors. Message frequency varies. Msg & data rates may apply, reply HELP for help or STOP to opt out.

Keep the accompanying sentence and links visible:

> Both boxes are optional and not required to get service. [SMS Terms](https://www.noahgaragesd.com/sms-terms.html) · [Privacy Policy](https://www.noahgaragesd.com/privacy-policy.html)

Use 14px consent text with roughly 21px line height, adequate contrast, and a comfortably tappable label row. These paragraphs occupy real vertical space. Do not force a full form into one screen by shrinking them, hiding them behind a disclosure, truncating them, or replacing them with a link. “Visible” means expanded in the document next to the checkbox, not necessarily above the initial fold.

### Copy, media, and interaction rules

- All new business-authored copy speaks as Noah: “I,” “me,” and “my.” The required legal wording stays verbatim; genuine reviews retain the customer's voice and attribution.
- If rating proof appears, use **5.0 · 129 Google reviews**. Use **Licensed & insured · CSLB #1159513**, **Open 24/7**, **San Diego County**, and **(619) 572-4266** consistently.
- No arrival or callback-speed promises, warranty inventions, unsupported credentials, Google endorsement badges, or em dashes in proposed copy.
- Use only the supplied real-photo families: `gallery1.jpeg` through `gallery4.jpeg`, `before_*.jpeg`, `after_*.jpeg`, and `reviews/img/*.webp`. Do not use `hero-mobile.webp`, `hero_*.jpg`, generated people or vans, or an unidentified person as Noah.
- Use at least 16px input text, persistent labels, 48px minimum interactive row heights, visible focus, and selection indicators that do not depend on color alone. Do not autofocus and open the phone keyboard on arrival.
- Make `tel:+16195724266` available on the first screen. Keep texting secondary with `sms:+16195724266` and the label “Text me.” Do not imply it is a live chat.
- Resolve the shared contact bar explicitly during implementation. Directions 1 and 2 use a header phone link and no floating contact bar; Direction 3 uses in-flow contact actions. Merely adding another sticky CTA would compound the current issue.
- Success copy: **“I've received your request. I'll call you to discuss your door and arrange a visit.”** Follow with **“You can also call me at (619) 572-4266.”** This confirms a request, not a booked appointment. Preserve entered data after failure and offer a phone alternative.

## Direction 1: A direct line to Noah

**Core idea:** A calm, personal callback form puts Noah's identity and the few necessary inputs ahead of decoration.

### First screen at 390 × 844

Approximate content-viewport budget, at default text size with the keyboard closed; 20px horizontal gutters and 350px usable width:

| Vertical position | Visible content |
| --- | --- |
| 0–64px | Compact Noah Garage Doors wordmark; “Call me” phone link with a 48px tap area. |
| 64–225px | Sentence-case headline: **“I'm Noah. Let's get your door working.”** Supporting copy: **“Leave your number. I'll call to discuss the problem and arrange a visit.”** |
| 225–315px | Two quiet proof lines: **5.0 · 129 Google reviews** and **Licensed & insured · CSLB #1159513**; small San Diego County / Open 24/7 metadata. |
| 315–585px | Visible callback heading, name field, phone field, and compact required service select, each with a persistent label. |
| 585–665px | Optional note disclosure and **“I'll explain the price before I start work.”** |
| 665–844px | “Text message options” label and the start of the full consent block. Natural continuation below the fold is intentional. |

Below the fold: remaining consent text, legal links, the single final CTA **“Ask me to call”**, then a modest project image and optional genuine review. No attempt to squeeze Submit above unreadable legal copy.

### Form flow

**Single page.** Name → phone → required service select → optional message → both complete consent paragraphs → Submit. Use the existing seven service values, with a disabled empty prompt and a clearly worded uncertainty option. Label the service control **“What can I help with?”**

The optional message disclosure reads **“Anything else I should know? (optional)”**. A short helper may invite a ZIP without creating another required field. Keep all submission and success behavior under the shared contract.

### Visual style

- **Palette:** warm background `#F7F5EF`, white fields `#FFFFFF`, ink `#172923`, muted text `#52615A`, dark green action `#185B46`, light border `#D4DDD6`, restrained gold star accent `#A66F08`.
- **Google Fonts:** **Manrope**, weights 600/700 for 30–32px headings; **DM Sans**, weights 400/500/700 for body, labels, and controls. No uppercase display headline.
- **Surfaces:** mostly an open page rather than a card inside a card; 10px field corners, subtle rules, a flat green CTA, no glow or pulse.
- **Imagery:** no first-screen hero. Use the inspected `gallery2.jpeg` below the form, preserving the cream door and natural daylight. Caption in Noah's voice: **“A garage door I installed.”** The image is supporting evidence rather than a prerequisite to contact.

### Why it should convert better

It exposes the actual effort early, restores the owner's voice, and avoids making stressed visitors scan a diagnostic menu. The phone route is immediately available without covering the form. The warmer treatment should make the business feel approachable while clearer labels and contrast reduce correction effort.

**Tradeoff:** A select hides the choices until tapped and this direction has less photographic impact. It is the strongest default for visitors who have already evaluated Noah's Google profile and now want to act.

## Direction 2: Let me help you narrow it down

**Core idea:** A focused two-step flow separates an easy symptom choice from the contact-and-consent task.

### First screen at 390 × 844

Use 20px gutters, a light background, and one question panel:

| Vertical position | Visible content |
| --- | --- |
| 0–60px | Compact wordmark and “Call me.” |
| 60–145px | **“I'll help with your garage door.”** Small **5.0 · 129 Google reviews** proof line. |
| 145–225px | Honest progress: **“1 of 2 · The problem”**. Question: **“What can I help with?”** Helper: **“You don't need to diagnose it. I'll help.”** |
| 225–635px | Seven full-width, roughly 48px radio rows with small gaps. Familiar symptoms from the current page, with **“Not sure”** equally prominent. No large icon tiles. |
| 635–707px | In-flow full-width **“Continue”** button. Selecting an option does not automatically advance. |
| 707–810px | **“Next, I'll ask for your name and number.”** Compact license and Open 24/7 details. |
| 810–844px | Breathing room. No fixed bar covering the action. |

The contact fields and consent text are on step 2, not hidden below the first-step choices. A smaller effective viewport can scroll naturally; the page is not locked to a device height.

### Form flow

**Two steps, one `form#quoteForm`.** Step 1 contains required `service` radios with the existing seven values. Continue is `type="button"` and advances only after an explicit choice. Step 2 shows **“2 of 2 · Your callback”**, the chosen problem with an Edit action, name, phone, optional message, both expanded consent paragraphs, legal links, and **“Ask me to call”** as the only submit button.

Step 2 is allowed to scroll. Both full consent paragraphs appear next to their checkboxes before final submission; they are not deferred until after the request. Back preserves all values. Focus moves to the step heading when advancing or returning, and a selected radio has both a check indicator and a border change.

This requires a small page-level step controller. Do not assume preserving IDs alone makes a wizard compatible: `quote-form.js` validates the whole form. Prevent implicit submission on step 1, validate that step's radio group independently, and reveal/focus a step if it contains an invalid field. Do not leave required hidden inputs that the browser cannot focus or disabled fields that silently bypass validation. Keep the complete single-page form as the no-step-controller fallback.

### Visual style

- **Palette:** background `#F3F6FC`, white panel `#FFFFFF`, ink `#15233B`, muted text `#526078`, cobalt action `#254FBE`, selected-row fill `#EAF0FF`, border `#CBD5E3`.
- **Google Fonts:** **Plus Jakarta Sans**, weights 600/700 for 28–30px headings; **Inter**, weights 400/500/600 for body and controls.
- **Surfaces:** one restrained 16px-radius question panel, flat radio rows, a simple two-segment progress indicator. No chat bubbles, typing simulation, or bot avatar.
- **Imagery:** none in step 1. Below the step-2 form, use the real `reviews/img/ren.webp` hardware image with its existing attributed review, if included. Do not present it as Noah's portrait or imply an unrelated project belongs to that reviewer.

### Why it should convert better

It removes the first-screen wall of fields and legal text while making the total number of steps explicit. The uncertainty option reduces diagnostic anxiety, and the next-step preview avoids surprising users with a contact form. This is a meaningful change in interaction rather than a recolor of the current numbered sections.

**Tradeoff:** One extra transition and additional accessibility/validation complexity. Some ready-to-call-back visitors may prefer all fields immediately. Measure completed requests, not just symptom selections, before deciding it wins.

## Direction 3: My work, your peace of mind

**Core idea:** Lead with one credible piece of Noah's work and a personal introduction, then offer a deliberate choice between calling and requesting a callback.

### First screen at 390 × 844

Use a photo-led editorial composition with 20px text gutters:

| Vertical position | Visible content |
| --- | --- |
| 0–60px | Small wordmark and Open 24/7 metadata on a warm white header. |
| 60–230px | Edge-to-edge 170px crop of `gallery1.jpeg`, centered on the real black garage doors. No text overlay. |
| 230–345px | **“I'm Noah. I repair garage doors.”** A quiet caption identifies the image: **“A garage door installation I completed.”** |
| 345–415px | **5.0 · 129 Google reviews**, **Licensed & insured · CSLB #1159513**, and San Diego County metadata. |
| 415–505px | Primary in-page anchor **“Ask me to call”** and secondary **“Call me: (619) 572-4266”**. The primary scrolls to the form; it does not send a request. |
| 505–590px | Callback section heading and **“I'll call to discuss your door and arrange a visit.”** |
| 590–844px | Required service select, name, and phone fields begin directly in the document. No modal or additional route. |

Below the fold: optional note, full consent block, final Submit, then a real before/after pair. The first-screen anchor targets the callback heading, not a distant form below a gallery.

### Form flow

**Single page with an in-page callback anchor.** Required service select → name → phone → optional message → both full consent paragraphs and legal links → `#quoteSubmit`. The first-screen CTA and the actual submit are distinct elements; only the latter gets `#quoteSubmit` and `#quoteSubmitText`.

The anchor scrolls to and focuses the form heading without opening the keyboard. Avoid a modal or drawer: a long consent block and on-screen keyboard need ordinary page scrolling. There is no persistent floating CTA. A small “Text me” link can sit below the form as a tertiary alternative.

### Visual style

- **Palette:** background `#FBF8F2`, ink `#182B3B`, deep blue action `#163F59`, white fields `#FFFFFF`, muted text `#59646B`, pale stone borders `#DCD6CC`, restrained terracotta accent `#A34C32`.
- **Google Fonts:** **DM Serif Display**, regular, for a 30–32px personal headline; **DM Sans**, weights 400/500/700 for everything functional. The serif is limited to the headline so the form remains direct and legible.
- **Surfaces:** generous editorial spacing, thin dividers, 6–8px form corners, no nested dark cards or heavy shadows. Photography supplies the visual character.
- **Imagery:** use the inspected `gallery1.jpeg` as the single hero. Crop to the doors, not the street number or upper-story windows. Below the completed form, show the inspected matching `before_door1.jpeg` and `after_door1.jpeg` pair with explicit Before/After labels and a shared caption, **“A door I replaced.”** Do not use a draggable comparison slider, carousel, or autoplay video.

### Why it should convert better

It demonstrates actual work without fabricated faces, creates a more memorable visual identity, and ties that evidence to a specific local owner. The first-screen callback and phone actions remain visible before the proof grows into a portfolio. It may suit homeowners who want reassurance before sharing their number.

**Tradeoff:** The form starts lower than in Direction 1, and an installation photograph can attract new-door interest more than emergency repair interest. Keep the photo shallow, explicitly lead with repair in the headline, and keep further imagery below the form.

## How to choose and validate

| Direction | Main conversion hypothesis | Principal cost |
| --- | --- | --- |
| **1. A direct line to Noah** | Immediate contact fields and personal clarity help already-motivated GBP visitors finish. | Less visual drama; service options require opening a select. |
| **2. Let me help you narrow it down** | One manageable decision encourages uncertain visitors to begin and continue. | Added transition and step-controller complexity. |
| **3. My work, your peace of mind** | Real-work evidence builds enough confidence to request contact. | More content before contact fields. |

Start with Direction 1. It addresses the strongest source-backed weaknesses with the least interaction complexity while still delivering a clear visual change.

Before release, verify the chosen design at a 390 × 844 content viewport, at a smaller effective viewport with browser chrome, with enlarged text, and with the phone keyboard open. Check selected/unselected services, optional note expansion, unchecked consents, validation errors, request failure, success, and Back behavior if using steps. Verify that the shared contact script cannot cover the form and that no real leads are created during testing.

Measure successful callback requests per GBP landing session, alongside phone and text clicks. A tap is not a completed call or booked job. Where the owner's workflow supports it, compare qualified conversations and actual appointments as the business outcome. For the two-step option, track progression and abandonment as diagnostics, not as the winning metric. Use comparable traffic periods and retain uncertainty if volume is too low to distinguish the designs.
