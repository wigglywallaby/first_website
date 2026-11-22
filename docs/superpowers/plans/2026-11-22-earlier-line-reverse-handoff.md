# Earlier Line and Reverse Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the production-line diagram enter earlier and let its six papers animate back to the opening stack when scrolling upward.

**Architecture:** Add a short viewport-height change to the opening and line heading, then extend the existing paper-handoff JavaScript with a reverse clone animation triggered by the line section crossing back into/above the viewport.

**Tech Stack:** HTML, CSS, vanilla JavaScript

**Spec:** `docs/superpowers/specs/2026-11-22-earlier-line-reverse-handoff-design.md`

## Task 1: Add failing source tests

**Files:**
- Modify: `tests/test_story_intro.py`

- [ ] **Step 1:** Add assertions that `.story-section` has a `90svh` minimum height, `.line-heading` has reduced top padding, `runPaperReverseHandoff()` exists, and the line observer can remove `is-transitioned`.

- [ ] **Step 2:** Run `python3 -m unittest discover -s tests -p 'test_*.py'`; expect RED.

## Task 2: Implement earlier entry and reverse handoff

**Files:**
- Modify: `story.html`

- [ ] **Step 1:** Change the opening `.story-section` minimum height to `90svh` without changing the other line section behavior.

- [ ] **Step 2:** Reduce `.line-heading` top padding and bottom padding so the diagram reaches the viewport sooner.

- [ ] **Step 3:** Add `runPaperReverseHandoff()` beside `runPaperHandoff()`.

The function:

1. Returns immediately for `reducedMotion`.
2. Maps the same six stage/station pairs.
3. Uses the `.form-icon` rect as the clone source and the `.paper-sheet[data-stage]` rect as the destination.
4. Creates a `.paper-handoff-clone` with the stage text.
5. Positions the clone at the destination icon center.
6. Animates from the destination icon scale to the opening sheet position and scale.
7. Removes the clone after animation.

- [ ] **Step 4:** Update the `#the-line` observer so it runs forward on entry and reverse when it leaves while scrolling upward.

- [ ] **Step 5:** Remove `is-transitioned` after the reverse animation starts so a later entry reruns the forward handoff.

- [ ] **Step 6:** Run tests and browser verification at 1440 px and 320 px.
