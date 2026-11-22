# Paper Stack Intro Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the opening headline on `story.html` with a dependency-free animated stack of six labeled paper checks that leads into the existing production-line timeline.

**Architecture:** Add a self-contained intro scene inside `#intro`, using existing page CSS variables and native CSS keyframes. Keep the existing line animation, observers, and downstream sections unchanged.

**Tech Stack:** HTML, CSS, vanilla JavaScript, static `story.html`

**Spec:** `docs/superpowers/specs/2026-11-22-paper-stack-intro-design.md`

## Global Constraints

- Use native HTML/CSS and no external Lottie, image, or JavaScript dependency.
- Preserve the existing opening's full-height layout and “Illustrative story with made-up data” caption.
- Show all six stage labels in the animation: Incoming, Fill, Seal, Best By, Packaging, Finished Case.
- Respect `prefers-reduced-motion`.
- Keep the intro copy and call to action accessible by text and keyboard.

## Review Focus

- Reduced motion must show the settled stack and copy immediately; test that `.paper-stack` sheets have no moving transform and the content is visible.
- Narrow viewports must not clip the stack or call-to-action; test a 320 px-wide viewport screenshot.
- Replaying or revisiting the intro must not leave invisible text or orphaned animation classes; test page reload.
- Existing timeline behavior must remain unchanged; test a 1440 px viewport and confirm station activation still works while the line story scrolls.
- Meaning must remain available without motion; test that the intro text names all six checks and explains the paperwork accumulation.

---

### Task 1: Add the Paper Stack Intro

**Files:**
- Modify: `story.html:802-821`
- Modify: `story.html:15-790` (add intro-specific CSS before the existing media query)
- Test: no automated test suite exists; use local HTTP plus browser verification

**Interfaces:**
- Consumes: existing `--bg`, `--surface`, `--text`, `--muted`, `--accent`, `--line`, `--warm` CSS variables and the `#intro` section.
- Produces: an `.paper-stack-intro` container with `.paper-stack`, six `.paper-sheet[data-stage]` elements, `.paper-stack-copy`, and a link to `#the-line`.
- The HTML uses exact sheet order: `Incoming`, `Fill`, `Seal`, `Best By`, `Packaging`, `Finished Case`.

- [ ] **Step 1: Add the intro HTML markup inside `#intro`, replacing only the opening copy block.**

Use this copy:

```html
<div class="paper-stack-intro">
  <div class="paper-stack" aria-label="Six paper checks from a production line">
    <!-- Add one .paper-sheet for each stage in the exact order above. -->
  </div>
  <div class="paper-stack-copy">
    <p class="eyebrow">One line. Six places to check.</p>
    <h1>Every check leaves a paper trail.</h1>
    <p class="lead">Before these checks become digital, they fill clipboards across the whole production line.</p>
    <a class="button" href="#the-line">Follow the line</a>
  </div>
</div>
<p class="caption">Illustrative story with made-up data.</p>
```

Each `.paper-sheet` contains a compact form title and placeholder rule lines, with the stage title in a visible heading or label. Mark decorative sheet internals `aria-hidden="true"` and keep the parent label on `.paper-stack`.

- [ ] **Step 2: Add scoped CSS for the intro layout and staggered falling sheets.**

Use fixed, viewport-responsive dimensions:

1. Center the scene in the existing section.
2. Place the stack on the left on wide screens and the copy on the right.
3. Stack sheets from `Incoming` on the lowest layer to `Finished Case` on the highest layer.
4. Give each sheet a slight rotation such that the stack reads as a physical pile without covering the stage labels.
5. Animate each sheet with a 700 ms `paper-fall` keyframe and stagger delays from 80 ms to 480 ms.
6. Keep the copy hidden only while motion runs and reveal it after the final sheet settles.
7. Add `@media (prefers-reduced-motion: reduce)` rules that set no sheet animation, no translated transform, and immediate copy visibility.
8. Below 700 px, switch to a stacked mobile layout and reduce the visual stack dimensions.

- [ ] **Step 3: Add a keyframe name and classes that do not conflict with existing `.scene` reveal behavior.**

Use only names prefixed by `paper-stack-`, `paper-sheet`, or `paper-fall`. Do not replace or rename `.scene`, `.is-visible`, or `.line-*` classes.

- [ ] **Step 4: Keep the existing `revealSections` JavaScript compatible.**

Do not add JavaScript for the intro unless it is required to restart CSS animation on reload. `#intro` already receives `is-visible` statically and must continue to render immediately.

- [ ] **Step 5: Verify markup and CSS structure locally.**

Run:

```bash
python3 -m http.server 4173 --directory /Users/max/Documents/GitHub/first_website
```

Open `http://127.0.0.1:4173/story.html`. Expected: the intro shows a paper stack and the approved copy instead of the QMS Manager headline, and `Follow the line` scrolls to `#the-line`.

- [ ] **Step 6: Verify the state matrix.**

In a browser at 1440 px:

1. Confirm six sheet labels are visible in the settled stack.
2. Confirm the sheet animation completes in under 1.5 seconds.
3. Enable reduced-motion emulation and reload.
4. Confirm all sheets and copy are immediately visible with no entrance animation.

In a browser at 320 px:

1. Confirm no horizontal overflow.
2. Confirm the stack, heading, lead, link, and caption remain visible.

- [ ] **Step 7: Verify existing behavior remains intact.**

Scroll through the line timeline and confirm:

1. `#the-line` opens below the intro.
2. Sticky station callouts still update.
3. The cup still moves to incoming, fill, seal, best-by, packaging, and finished stations.
4. No CSS selector or keyframe has altered `.line-story`, `.line-stage`, or `.line-step`.

- [ ] **Step 8: Review the diff and stop before committing unless the user separately requests a commit.**

Run:

```bash
git --no-pager diff --stat
git --no-pager diff -- story.html docs/superpowers/specs/2026-11-22-paper-stack-intro-design.md docs/superpowers/plans/2026-11-22-paper-stack-intro.md
```

Confirm only `story.html` and the approved design/plan files are changed.
