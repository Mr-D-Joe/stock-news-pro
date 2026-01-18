# DESIGN.md  
## UI Layout & Scaling Rules (JavaFX)

This document defines **non-negotiable layout and scaling rules** for this project.
Its purpose is to **prevent layout fighting, uncontrolled growth, and instability**
caused by text rendering, font scaling, or width bindings.

These rules override all aesthetic preferences.

---

## 1. Core Design Principle

> **Function beats appearance. Always.**

The UI must remain:
- stable
- deterministic
- readable
- scalable

at **any window size**.

If a visual style violates layout stability, it is forbidden.

---

## 2. Fundamental Constraint (Most Important Rule)

> **Text must NEVER control container width.**

Containers define width.
Text adapts to containers — never the other way around.

Any implementation that allows text to influence layout width is considered a bug.

---

## 3. Text Rules (Strict)

### Allowed
- `TextAlignment.LEFT`
- `setWrapText(true)`
- `setMaxWidth(Double.MAX_VALUE)`

### Forbidden (No Exceptions)
- `TextAlignment.JUSTIFY`
- CSS `-fx-text-alignment: justify`
- Dynamic width bindings on text or labels
- Any attempt to "fill" horizontal space via text alignment

**Reason:**  
Justified text introduces non-linear word spacing and causes feedback loops
when combined with responsive layouts and font scaling.

---

## 4. Scaling Rules

### 4.1 Font Scaling (Allowed)

- Font scaling is applied **ONLY** at the root node
- Implemented via CSS:
  ```css
  -fx-font-size: <scaled-value>px;

  	•	Scaling may be dampened (e.g. sqrt(width))

4.2 Padding & Spacing (Forbidden to Scale)
	•	Padding and spacing MUST be fixed values
	•	No bindings
	•	No heuristics
	•	No proportional scaling

Reason:
Scaled padding causes container growth and layout instability when text wraps.

⸻

5. Width Management Rules

Allowed
	•	setMaxWidth(<reasonable value>)
	•	Editorial / readable widths (e.g. 760–900 px)
	•	Centering via parent containers

Forbidden
	•	prefWidthProperty().bind(...)
	•	layoutBoundsProperty() feedback
	•	Width calculations based on text metrics
	•	Scale transforms (ScaleX, ScaleY, global scaling)

⸻

6. Centering Strategy (Mandatory Pattern)

Center content by constraining width, not by stretching text.

Canonical Pattern
	•	Outer container:
	•	Takes full available width
	•	Centers content horizontally
	•	Inner content container:
	•	Has a defined maxWidth
	•	Uses full width up to that limit

This pattern is implemented via CenteredContentPane.

Any deviation must be explicitly justified.

⸻

7. Approved Layout Utility

CenteredContentPane

This is the only approved solution for centered, scalable content areas.

Characteristics:
	•	Outer container expands freely
	•	Inner container has a max readable width
	•	No width bindings
	•	No scale transforms
	•	Stable across all screen sizes

If content grows infinitely, this class was not used correctly.

⸻

8. Known Anti-Patterns (Hard Fail)

The following patterns are known to break JavaFX layouts and are forbidden:
	•	Justified text in responsive layouts
	•	Binding padding or spacing to window size
	•	Binding prefWidth/maxWidth to font size
	•	Using Scale transforms for responsiveness
	•	Allowing labels or text nodes to define layout width
	•	Mixing linear layout logic with non-linear scaling math

If any of these appear in code reviews, they must be removed immediately.

⸻

9. Definition of “Done”

A UI change is considered correct only if:
	•	No container grows without an explicit max width
	•	Text wrapping does not increase container width
	•	Resizing the window does not cause layout jitter
	•	The UI remains readable from small laptops to large monitors

⸻

10. Final Rule

If something grows unexpectedly, it is a bug — not a styling issue.

Fix the layout, not the symptom.
