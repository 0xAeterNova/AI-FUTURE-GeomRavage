# BURHAN
### Offline Evidence-Grounded Government Services Assistant

BURHAN is an offline AI-powered assistant designed to answer questions about government services using official documentation. It combines structured information retrieval with the **Command R7B Arabic (7B)** language model, running locally through Ollama, to deliver accurate, context-aware, and evidence-supported responses.

Developed for the **AI Future 26 Hackathon at 42 Irbid**, BURHAN prioritizes factual correctness, source reliability, and efficient local inference.

## Key Features

- **Evidence-Grounded Responses:** Generates answers using retrieved information from official service documents, with supporting source excerpts.
- **Intelligent Service Retrieval:** Identifies the relevant service and operation to prevent confusion between similar government procedures.
- **Contextual Reasoning:** Handles conditional fees, eligibility requirements, exceptions, and complex service procedures.
- **Arabic Language Understanding:** Supports formal Arabic, Jordanian dialect, and common linguistic variations.
- **Multi-Turn Conversations:** Maintains context across related questions while keeping individual conversations independent.
- **Hallucination Mitigation:** Uses document-grounded generation and citation validation to reduce unsupported answers.
- **Offline Processing:** Runs locally without external AI APIs or internet connectivity during inference.
- **Efficient Execution:** Uses focused context selection to reduce unnecessary model processing.

## Supported Services

BURHAN processes 12 official government service documents across three categories:

| Service Category | Supported Operations |
|---|---|
| Passport | First Issuance, Renewal, Lost, Damaged |
| Family Book | First Issuance, Renewal, Lost, Damaged |
| Smart ID Card | First Issuance, Renewal, Lost, Damaged |

## System Architecture

The system follows a lightweight Retrieval-Augmented Generation (RAG) approach:

**Question Input → Service Identification → Evidence Retrieval → Local LLM Inference → Response Validation → JSON Output**

The processing pipeline consists of:

1. **Document Parsing:** Extracts structured information from the local service documents.
2. **Intent Recognition:** Identifies the requested service, operation, and relevant question category.
3. **Evidence Selection:** Retrieves supporting passages, including applicable conditions and exceptions.
4. **Answer Generation:** Uses Command R7B Arabic through Ollama to produce a grounded response.
5. **Output Validation:** Processes source references and preserves the required conversation structure.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Language Model | Command R7B Arabic 7B |
| Model Runtime | Ollama |
| Retrieval | Structured, Service-Aware Retrieval |
| Knowledge Source | Local Text Documents |
| Interface | Command-Line Processing |
| Output Format | UTF-8 JSON |

## Project Structure

```text
BURHAN/
├── data/           # Official government service documents
├── scripts/        # Validation and utility scripts
├── main.py         # Application entry point
└── README.md       # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.11 or newer
- Ollama installed and running
- Command R7B Arabic model downloaded locally

### Model Installation

```powershell
ollama pull command-r7b-arabic:7b
```

### Configuration

Optional environment variables can be used to configure inference:

```powershell
$env:OLLAMA_MODEL = "command-r7b-arabic:7b"
$env:BURHAN_NUM_CTX = "6144"
$env:BURHAN_MAX_TOKENS = "500"
```

### Running BURHAN

Place the input `questions.json` in the project root and execute:

```powershell
python main.py questions.json
```

BURHAN processes the questions and generates `answers.json` in the same directory.

The output preserves the original chat structure and includes:

- **answer:** Model-generated response to the question.
- **contexts:** Retrieved document excerpts supporting the generated answer.

### Document Inspection

```powershell
python main.py --inspect
```

This command displays the recognized government services and parsed document sections.

## Design Principles

BURHAN is built around four fundamental principles:

1. **Accuracy:** Prioritize correct information and context-specific reasoning.
2. **Transparency:** Associate generated answers with relevant source evidence.
3. **Efficiency:** Minimize unnecessary processing through focused information retrieval.
4. **Privacy:** Execute inference locally without transmitting document contents to external AI services.

## Project Scope

BURHAN demonstrates how lightweight language models and evidence-based retrieval can improve access to complex government-service information.

The application uses only the provided government documents as its knowledge source and generates answers at runtime without fine-tuning or prewritten responses.

---

**BURHAN | Reliable Answers. Verifiable Evidence. Local Intelligence.**
