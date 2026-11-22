# Earlier Line and Reverse Paper Handoff Design

## Intent

Make the production-line diagram appear sooner after the opening paper-stack section and let the six papers animate back to their original opening-stack positions when the user scrolls upward away from the line.

## Goals

- Reduce the amount of blank scroll space between the opening stack and the production-line diagram.
- Keep the opening screen compact enough that the diagram can enter quickly.
- Preserve the existing sticky diagram, six station highlights, callouts, cup movement, and check forms.
- When scrolling back above the line, animate paper clones from the six line icons back to the matching opening paper sheets.
- Respect reduced-motion by skipping clone animation.

## Non-goals

- Redesign the opening copy or remove the opening paper-stack animation.
- Change station names or check-form content.
- Change the scroll activation height for the six step markers.

## Selected design

The existing opening `.story-section` stays full enough to frame the paper stack, but becomes `90svh` instead of `100svh`. The line heading uses less top and bottom padding so `#the-line` and `.line-stage` enter earlier.

The existing forward handoff remains:

- On entry to `#the-line`, six paper clones fly from the opening sheets to the six `.form-icon` locations.
- The clones fade at the destination and the existing station icons remain visible.

The reverse handoff is added as the symmetrical behavior:

- When the user scrolls upward and `#the-line` leaves the viewport, six paper clones start at the six line-icon locations.
- Each clone moves and scales to the matching `.paper-sheet[data-stage]` location.
- The clone becomes the original opening stack sheet at that position and fades away.
- The `is-transitioned` state is removed so a later forward entry can animate again.
- Reduced-motion users see the settled states immediately with no clones.

## Approaches considered

- Shorten the opening and add a bidirectional handoff: selected.
- Only shorten the opening: less work, but leaves no reverse paper motion.
- Only add the reverse handoff: leaves the excessive blank spacing unsolved.

## Constraints

- Native HTML, CSS, and JavaScript only.
- No external animation dependency.
- Preserve existing `IntersectionObserver`, marker, and callout behavior.
- No change to check-form content.
