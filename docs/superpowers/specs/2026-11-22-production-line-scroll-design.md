# Production Line Scroll Design

## Intent and why

Make the opening paper stack and the production-line timeline read as one continuous story: papers accumulate in the opener, then move to the six places on the line where operators perform checks.

## Goals

- Remove every visible “Illustrative story with made-up data.” caption.
- Transition the six opening paper sheets into the six visible paper icons on the production-line diagram.
- Keep the sticky production-line graphic as the only visual during the line-scroll section.
- Preserve the existing scroll behavior that highlights one station at a time and moves the product cup along the belt.
- Fix the bottom “The paper problem” bullets so text reads horizontally in normal reading order.
- Preserve reduced-motion behavior and mobile readability.

## Non-goals

- Removing or rewriting the station names and checks.
- Changing the production-line cup or station callout content.
- Changing the bottom narrative cards beyond removing the captions and correcting bullet layout.

## Anti-goals

- Do not keep full step articles, illustrations, or paper forms consuming scroll space in the line section.
- Do not remove the scroll markers needed to activate station highlights.
- Do not make the six papers disappear after entering the timeline.
- Do not add external animation or asset dependencies.

## Constraints

- Implement in the existing `story.html`.
- Use native HTML, CSS, and the existing IntersectionObserver logic.
- Preserve keyboard navigation and accessible text.
- Respect `prefers-reduced-motion`.

## Approaches

- Diagram-only scroll with paper-transition animation: use existing scroll markers to hide detailed step articles and animate the six opening sheets into their station icons. Recommended because it creates a direct visual handoff and keeps the sticky diagram as the focus.
- Keep detailed step sections: preserve the current illustrations and forms while still animating papers. Rejected because the requested result calls for only the production-line graphic during continued scrolling.
- Static remove-and-highlight: remove captions and detailed sections without moving papers. Rejected because it does not create the requested continuity from the opening stack into the line.

The diagram-only scroll approach is selected.

## Selected design

### Opening to line transition

After the opening stack is complete, the six sheets remain available as a handoff:

1. The `Follow the line` link scrolls to `#the-line`.
2. As the opening leaves and `#the-line` enters, the six labels animate to the six existing `.form-icon` positions: Incoming, Fill, Seal, Best By, Packaging, and Finished Case.
3. The existing station paper icons remain visible in the sticky SVG.
4. Reduced-motion users receive a settled, immediate transition with no motion.

### Line scroll

The existing `.line-steps` remains in the document for behavior and accessibility hooks, but detailed `.line-step` articles are visually compacted or hidden from normal layout:

1. The sticky `.line-stage` remains visible.
2. Each existing step marker continues to activate a station and callout.
3. The cup continues moving to the active station.
4. No step copy, illustration, or paper form is shown in the scrolling area.
5. The first station highlight is active as the user enters the line.

### Captions and bullets

1. Remove all four exact “Illustrative story with made-up data.” caption paragraphs.
2. Keep the `.problem-list` on the bottom paper-problem card in a three-column row on wide screens.
3. Use normal horizontal text wrapping; do not allow bullet text to split into vertical character flow.
4. On narrow screens, stack the bullets vertically while each bullet remains a full-width row with readable left-to-right text.

## Implementation boundaries

- Update only `story.html` and directly related tests/documentation.
- Reuse existing `.station`, `.form-icon`, `step-marker`, `activateStep`, and `positionCallout` structures.
- Do not alter the bottom card content or the existing station check definitions.
