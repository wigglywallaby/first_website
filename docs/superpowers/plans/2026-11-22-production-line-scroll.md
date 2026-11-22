# Production Line Scroll Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Continue the opening paper-stack story into a diagram-only scrolling production line and remove the illustrative-data captions.

**Architecture:** Reuse the existing `step-marker` IntersectionObserver and `.station` SVG focus classes. Hide detailed `.line-step` articles from layout while retaining them as scroll markers, and add a one-time CSS transition that makes the opening sheets settle at the existing `.form-icon` locations.

**Tech Stack:** HTML, CSS, vanilla JavaScript

**Spec:** `docs/superpowers/specs/2026-11-22-production-line-scroll-design.md`

## Global Constraints

- Remove all exact visible text `Illustrative story with made-up data.`.
- Keep the sticky production-line graphic and all six `.form-icon` paper icons visible.
- As scrolling enters the line, only the sticky diagram and callouts are visually active; detailed line-step articles occupy no visible scroll height.
- Preserve station highlighting and cup movement from the existing observer.
- Preserve reduced-motion behavior.

## Review Focus

- Narrow 320 px screens must keep bullet text horizontal and full-width. Test computed `grid-template-columns: 1fr`, each item rect width, and no text transform.
- Reduced-motion users must see the final settled papers and copy immediately. Test animation declarations and `prefers-reduced-motion`.
- Incoming through Finished Case highlights must remain reachable in scroll order. Test all six markers activate the matching `data-station`.
- The page must contain no exact illustrative-caption text. Test source HTML for zero matches.
- The detailed line-step area must not create an independent scrolling visual between the sticky graphic and bottom cards. Test its height and `.line-step` visibility.

---

### Task 1: Add Production-Line Scroll Tests

**Files:**
- Modify: `tests/test_story_intro.py`
- Test: `tests/test_story_intro.py`

**Interfaces:**
- Produces assertions for zero caption text, six line stations, hidden step articles, horizontal problem bullets, and reduced-motion fallback.

- [ ] **Step 1: Add source assertions for the requested behavior.**

Extend `tests/test_story_intro.py` with assertions that:

1. `HTML.count("Illustrative story with made-up data.") == 0`.
2. The `.line-step` rule includes `display: none`.
3. `.problem-list` includes `grid-template-columns: repeat(3, minmax(0, 1fr))`.
4. The mobile `.problem-list` rule includes `grid-template-columns: 1fr`.
5. The six existing station data values are present: `incoming`, `fill`, `seal`, `bestby`, `packaging`, `finished`.

- [ ] **Step 2: Run the test and verify it fails for the missing behavior.**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`

Expected: FAIL because captions remain and `.line-step` is not hidden.

- [ ] **Step 3: Commit no code during RED; this task ends only after the feature implementation makes the test pass.**

### Task 2: Update Story Markup and Styles

**Files:**
- Modify: `story.html`

**Interfaces:**
- Consumes existing `.paper-stack`, `.paper-sheet`, `.line-step`, `.step-marker`, `.problem-list`, and station icon markup.
- Produces a diagram-only scroll section and the approved bullet/caption cleanup.

- [ ] **Step 1: Remove all four exact caption paragraphs from `story.html`.**

Delete every `<p class="caption">Illustrative story with made-up data.</p>`.

- [ ] **Step 2: Hide detailed `.line-step` articles without removing their scroll markers.**

Set `.line-step` to `display: none`. Keep `.step-marker` elements and the existing `.line-steps` container.

- [ ] **Step 3: Make the line scroll zone non-visual while preserving marker height.**

Set `.line-steps` to `height: 6px` or to a height determined by a six-marker scroll rhythm. The implementation must leave enough marker distance to activate all six stations, while `.line-step` remains hidden.

- [ ] **Step 4: Add a one-time paper-to-station transition hook.**

When `#the-line` enters the viewport, add `.is-transitioned` to `#the-line` once. Add scoped CSS that maps the opening `.paper-sheet[data-stage]` labels toward the existing SVG station icons, or otherwise keeps them as a settled state.

- [ ] **Step 5: Fix `.problem-list` horizontal text layout.**

Keep `grid-template-columns: repeat(3, minmax(0, 1fr))` on wide screens and `grid-template-columns: 1fr` on mobile. Add `text-align: left` and `white-space: normal` to `.problem-list li`.

- [ ] **Step 6: Verify with browser-style source checks and run the test suite.**

Run: `python3 -m unittest discover -s tests -p 'test_*.py'`

Expected: PASS 2 or more tests.

### Task 3: Browser Verification

**Files:**
- Modify: `story.html`
- Test: `tests/test_story_intro.py`

- [ ] **Step 1: Start a local HTTP server and open `story.html`.**

Run: `python3 -m http.server 4173 --directory .`

Expected: page loads without missing assets.

- [ ] **Step 2: Verify desktop scroll behavior at 1440 px.**

Confirm:

1. The opening paper stack is visible.
2. Scrolling to `#the-line` makes the sticky diagram the primary visual.
3. Six station papers remain visible.
4. Incoming, Fill, Seal, Best By, Packaging, and Finished Case activate in scroll order.

- [ ] **Step 3: Verify mobile and reduced-motion behavior at 320 px.**

Confirm:

1. No horizontal overflow.
2. The three problem bullets read left-to-right in one-column full-width rows.
3. Reduced-motion shows no entrance motion and all papers settled.

- [ ] **Step 4: Run final tests and diff checks.**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
git --no-pager diff --check
git --no-pager diff --stat
```

Expected: tests pass, diff check has no whitespace errors, and only `story.html`, tests, and directly related documentation are modified.
