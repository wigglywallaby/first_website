# Paper Stack Intro Design

## Intent and why

Replace the opening QMS Manager headline on `story.html` with a short visual introduction that makes the amount of physical paperwork on an applesauce production line immediately understandable.

## Goals

- Open the interactive demo with an animated stack of paper checks.
- Use the six existing production-line stages: Incoming Material, Fill, Seal, Best By, Packaging, and Finished Case.
- Preserve the existing production-line timeline and its later paper-form examples.
- Keep the static site dependency-free and usable on mobile.
- Respect `prefers-reduced-motion`.

## Non-goals

- Replacing the timeline, line-step sections, or existing paper-form illustrations.
- Recreating a photorealistic factory or adding external animation assets.
- Inventing production quantities or compliance claims beyond the existing illustrative copy.

## Anti-goals

- Do not make the first screen feel like a generic loading screen.
- Do not keep users on an opening animation without a clear way to continue.
- Do not require JavaScript or a remote library for the basic static page.

## Constraints

- Implement in the existing `story.html` so navigation and page behavior remain unchanged.
- Use native HTML, CSS, and existing JavaScript patterns.
- Preserve accessible text and provide no motion-only meaning.
- Follow the existing warm, understated visual system and color variables.

## Approaches

- Native CSS/HTML paper stack: six labeled sheets fall and settle into a visible stack. Recommended because it matches the existing form system, needs no external asset, and can degrade cleanly.
- External Lottie asset: can provide richer motion, but introduces a remote or bundled dependency and another asset format to maintain.
- Simple scroll reveal: less complex, but less clearly communicates a sudden accumulation of paperwork on arrival.

The native CSS/HTML approach is selected.

## Selected design

The intro remains a full-height opening section, but the initial role-copy is replaced by a paper-stack scene:

1. A neutral desk or surface establishes the stage.
2. Six compact paper sheets enter one at a time, briefly staggered and with small rotation differences.
3. Each sheet carries the same form-like styling and a stage label: Incoming, Fill, Seal, Best By, Packaging, or Finished Case.
4. Once settled, a short line reads: “6 production checks. 1 continuous line.” The exact wording may be adjusted only for clarity.
5. A concise follow-up line explains: “Before the line can become digital, each check leaves a paper trail.” This is proposed copy based on the objective and will be verified against existing narrative language.
6. The existing “Illustrative story with made-up data” caption remains.
7. A “Follow the line” text link or button may reveal/scroll to `#the-line`; the implementation will preserve normal keyboard focus and avoid hiding content behind the animation.
8. On reduced-motion settings, all sheets and copy are immediately visible with no entrance motion.

The headline “You're the new QMS Manager at an applesauce plant.” is removed or replaced. The final opening copy should orient the user around paperwork and then lead naturally into the existing production-line diagram.

## Implementation boundaries

- Add intro-specific styles to the existing `<style>` block.
- Add a small intro-specific HTML structure inside `#intro`.
- Add only the minimal JavaScript needed for replay-once behavior or cleanup, if CSS alone cannot cover it; otherwise CSS handles timing and animation classes.
- Do not alter the timeline, `lineSteps`, station details, or scroll observer behavior.
