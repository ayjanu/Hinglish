# HinglishVinglish: Analysis & Implementation Plan

Exported October 26, 2026 from the living doc:
https://claude.ai/artifact/Nabpg79wfDYC2ymeBsYpRQ

The online doc is the source of truth; this package is a snapshot.

## Contents

| Path | What it is |
| --- | --- |
| `HinglishVinglish-plan.pdf` | All six sections in one PDF, with both diagrams |
| `markdown/` | Each section as Markdown (best for a repo's `docs/spec/`) |
| `word/` | Each section as an editable Word document |
| `diagrams/roadmap.png` | Phased roadmap: five phases and their gates |
| `diagrams/architecture.png` | System architecture: app, API, engine, stores, offline build |
| `code/phonetic_key.py` | The phonetic-key algorithm from the spec; run it to check the spec's examples |

## Sections

1. **Plan overview**: summary, decisions, MVP analysis, research, system and app design, data model, roadmap, risks, sources
2. **Linguistics & HV-Roman spec**: the normative romanization spec, phonology, normalization, phonetic key, grammar, ambiguity rules
3. **Learning science**: evidence behind each learning feature, learner model, curriculum, metrics
4. **Technical architecture**: stack, diagram, interfaces, API, budgets, multi-script design
5. **Development plan**: repo conventions, ticket backlog with acceptance criteria, launch checklist, testing strategy
6. **Data & licensing**: provenance and license of every source, and the build-time license gate
