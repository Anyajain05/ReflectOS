# DT Fellowship Assignment: The Daily Reflection Tree

This repository contains a deterministic reflection tool built for the DT Fellowship assignment. The runtime product uses no LLM calls. The reflection flow is fully encoded as data and executed by a generic agent.

## Structure

```text
tree/
  reflection-tree.json
  tree-diagram.md
agent/
  reflection_agent.py
transcripts/
  persona-1-transcript.md
  persona-2-transcript.md
write-up.md
README.md
```

## Part A

- `tree/reflection-tree.json`: the reflection tree data
- `tree/tree-diagram.md`: Mermaid diagram of the branching structure
- `write-up.md`: design rationale, trade-offs, psychological grounding

The tree includes:

- 25 nodes total
- 10 question nodes
- 4 decision nodes
- 9 non-interactive narrative nodes (`start`, `reflection`, `bridge`, `summary`, `end`)
- all 3 axes in sequence: locus -> orientation -> radius

## Part B

The bonus agent is a small Python CLI that:

- loads the tree from JSON
- renders question nodes with fixed options
- routes decision nodes deterministically
- tallies per-axis signals
- interpolates earlier answers into the summary
- supports scripted runs for transcript generation

## Run It

From the repository root:

```bash
python agent/reflection_agent.py
```

To run a scripted path:

```bash
python agent/reflection_agent.py --choices 4 4 4 4 4 4 1 1 1
python agent/reflection_agent.py --choices 1 1 1 1 1 1 4 3 3
```

To save a transcript:

```bash
python agent/reflection_agent.py --choices 1 1 1 1 1 1 4 3 3 --save-transcript transcripts/persona-2-transcript.md
```

## Notes

- No free text is collected at runtime.
- No randomness is used in branching.
- No external APIs or LLM calls are required.
- The code is intentionally generic so another tree file could be swapped in with minimal changes.
