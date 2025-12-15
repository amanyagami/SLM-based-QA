# PDF Question Answering with Supermemory and HF Inference

NANDI is a simple Flask-based web service that lets you upload a PDF, index its content into Supermemory, and then query it using multiple LLMs via the Hugging Face Inference API.

## Features

- Upload a PDF file (server-side size limit: 16 MB).
- Extract text from the PDF with `pypdf`.
- Store and index the extracted text in [Supermemory](https://supermemory.ai/).
- Query the stored content:
  - Retrieve relevant chunks from Supermemory.
  - Call multiple models hosted via Hugging Face Inference (Groq, Novita, etc.).
  - Compare responses:
    - With Supermemory context.
    - With raw PDF content only (no retrieval).

## Requirements

- Python 3.9+ (recommended)
- A valid Hugging Face API token (`HF_TOKEN`)
- A valid Supermemory API key

Install dependencies:

```
pip install flask pypdf transformers torch huggingface_hub supermemory
```

(Adjust package names/versions as needed.)

## Configuration

Environment variables:

- `HF_TOKEN`: Hugging Face API token used by `InferenceClient`.

- Uploaded PDFs are saved to a `store/` directory in the current working directory.
- The app expects an `index.html` file in the same directory as the script for the main UI.

## Usage

1. Run the script:

   ```
   python app.py
   ```

### Endpoints

#### `GET /`

- Serves `index.html` via `render_template_string`.
- This should contain a simple UI for uploading a PDF and sending queries.

#### `POST /upload`

- Accepts a PDF file (form field name: `file`).
- Steps:
  - Validates file presence and extension (`.pdf` only).
  - Saves the file to `store/`.
  - Extracts text with `PdfReader`.
  - Stores the text in an in-memory dictionary (`data_in_file`).
  - Adds the text as a memory in Supermemory (`client.memories.add`).
- Returns JSON with:
  - `success`: `true` or `false`
  - `message`: details about upload
  - `filename`: sanitized filename used as `container_tag`
  - `path`: local file path

#### `POST /query`

- Expects raw text in the request body (the user’s question).
- Steps:
  1. Uses Supermemory’s search to retrieve relevant chunks for the query.
  2. Builds a prompt that includes:
     - The retrieved facts from Supermemory.
     - The user question.
  3. For each model in the `Models` dictionary:
     - Calls it via `InferenceClient.chat.completions.create`.
     - Stores the response under the model name.
  4. Builds a second prompt using the full PDF content (no Supermemory retrieval).
  5. Queries each model again and stores responses under keys prefixed with `"Without Supermemory "`.
- Returns JSON with:
  - `success`: `true`
  - `responses`: a dictionary of model name → response text.

## Models

The `Models` dict maps model names to a provider and an approximate parameter size, for example:

```
Models = {
    "meta-llama/Meta-Llama-3-70B-Instruct": ["novita", 70],
    "meta-llama/Llama-3.1-8B-Instruct": ["novita", 8],
    "openai/gpt-oss-20b": ["groq", 20],
    "openai/gpt-oss-120b": ["groq", 120],
    "deepseek-ai/DeepSeek-V3": ["novita", 671],
    "meta-llama/Llama-3.2-1B-Instruct": ["novita", 1],
    "meta-llama/Llama-4-Scout-17B-16E-Instruct": ["groq", 17],
    "unsloth/Meta-Llama-3.1-8B-Instruct": ["featherless-ai", 8]
}
```
