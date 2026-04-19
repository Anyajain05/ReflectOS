# Design Rationale

## Why These Questions

I designed the tree to feel like a short evening conversation rather than a diagnostic quiz. Each axis starts with a concrete recall prompt about "today" and then narrows into a discriminating question that surfaces the underlying psychological spectrum. The options are intentionally written in plain workplace language instead of academic vocabulary; a tired employee is more likely to recognize "I replayed what went wrong more than what I could do" than "I exhibited external locus of control."

For Axis 1, the questions distinguish between noticing leverage and noticing constraints. I tried to avoid blame-heavy wording. Internal locus is represented not as "I control everything," but as "I can still make the next move." That lines up with both Rotter's locus of control framing and Dweck's growth mindset emphasis on strategy, effort, and adjustment.

For Axis 2, I focused on the subtle difference between adding value and keeping score. Entitlement is hard to self-report directly, so the options surface it indirectly through recognition, owed support, and fairness-tracking. Contribution is represented through discretionary effort, helping, teaching, and taking responsibility beyond role boundaries, which maps well to Organizational Citizenship Behavior.

For Axis 3, the questions widen the unit of analysis from self to team to colleague to customer. That progression reflects perspective-taking and Maslow's later idea of self-transcendence. I wanted the axis to feel like expansion rather than moral pressure. The reflection for a narrow radius does not shame the user; it simply invites a larger frame.

## Branching Logic and Trade-Offs

The branching strategy is intentionally simple: each answer adds a tally to one pole of an axis, then a decision node routes to a reflection based on the dominant signal for that axis. This keeps the product deterministic, auditable, and easy for another developer to load. I used one major decision per axis rather than branching after every single question because too many micro-branches would make the tree harder to maintain and easier to accidentally moralize.

I also added "mixed" reflections for tied axes. This was an important design choice. Real employees are often ambivalent, and forcing every session into a binary winner would make the tree feel artificial. A mixed route preserves determinism while acknowledging that reflection is often about tension, not purity.

The biggest trade-off was depth versus readability. A much larger tree could tailor every downstream question to earlier answers, but the assignment emphasizes tree quality as data. I chose a compact structure that is still rich enough to produce distinct paths while remaining readable in one JSON file and one Mermaid diagram.

## Sources Used

- Julian Rotter, work on Locus of Control (especially the internal vs external distinction)
- Carol Dweck, *Mindset* and growth mindset framing around strategy, effort, and learning
- Campbell et al., work on Psychological Entitlement
- Dennis Organ, Organizational Citizenship Behavior
- Abraham Maslow's later writing on self-transcendence
- C. Daniel Batson, perspective-taking and empathy research

## What I Would Improve With More Time

I would expand the tree into more role-specific variants, especially around manager versus individual-contributor experiences. I would also test the option wording with real users to sharpen distinctions that may still feel too close together. On the product side, I would add a lightweight web UI, path analytics for reviewing common routes, and a small library of deterministic summary variants keyed to combinations of dominant axes.
