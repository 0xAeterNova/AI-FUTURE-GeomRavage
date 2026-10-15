# BURHAN | Offline Evidence-Grounded Government Service Assistant

BURHAN answers questions about the twelve supplied government services using the organizer-provided `command-r7b-arabic:7b` model through a local Ollama instance.

## Evaluator command

From this folder, place the organizer's `questions.json` next to `main.py` and run:

```powershell
python main.py questions.json
```

The program writes UTF-8 `answers.json` in the same folder and preserves the input chat and message order, IDs, and original questions. Each message receives a model-generated `answer` and a list of source excerpts in `contexts`. Each chat maintains its own conversation history.

## Local checks

```powershell
python main.py --inspect
python main.py examples/questions_sample.json
python scripts/check_output.py examples/questions_sample.json answers.json
python scripts/audit_contexts.py examples/questions_sample.json answers.json
```

To run with a local custom Ollama endpoint or optional settings:

```powershell
$env:OLLAMA_MODEL = "command-r7b-arabic:7b"
$env:BURHAN_NUM_CTX = "6144"
$env:BURHAN_MAX_TOKENS = "500"
python main.py questions.json
```

## How it works

The engine parses the nine labeled sections of each source file, identifies the service and operation, and retrieves focused evidence for the question. Conditional fee questions include applicable notes and conditions. It calls the organizer's model at runtime, validates cited excerpt identifiers, and saves progress after each message. Follow-up questions inherit the appropriate service context, but separate chats remain independent. Missing or unclear information is handled by the model without inventing source facts.

## Contents

- `main.py`: standalone, standard-library batch entry point
- `data/`: twelve unmodified organizer service documents
- `scripts/`: optional preflight and output quality checks
- `examples/`: organizer sample input and expected answers, for rehearsal only

No prewritten answers, external AI services, vector databases, frontend, or training step are required.

## Live demonstration

See [`JUDGE_DEMO.md`](JUDGE_DEMO.md) for the short demonstration, offline evaluator instructions, and GitHub handoff. The sample questions are stored under `examples/`. The organizers supply their own `questions.json` for scoring.
