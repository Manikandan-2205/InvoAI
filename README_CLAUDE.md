# Claude OpenRouter Testing

This guide helps you set up and test Claude via the OpenRouter API **locally** within the `InvoAI` project.

## Prerequisites
- Python 3.10+ installed on your machine.
- An OpenRouter API key. You can obtain one from https://openrouter.ai/.
- The model name you wish to use (e.g., `anthropic/claude-3-opus-20240229`).

## 1. Create a virtual environment (local only)
```bat
:: create a virtual environment in the project folder
python -m venv .venv

:: activate the environment
.venv\Scripts\activate
```

## 2. Install project dependencies
```bat
pip install -r requirements.txt
```

## 3. Configure your OpenRouter credentials
Edit the `.env` file located at the project root and replace the placeholder values with your actual credentials:
```
OPENROUTER_API_KEY=your_actual_openrouter_api_key
CLAUDE_MODEL_NAME=anthropic/claude-3-opus-20240229
```
> **Do not** add these values to any global environment variables; they are read from the local `.env` file.

## 4. Run the Claude client
```bat
python backend\claude_client.py
```
You will see a prompt:
```
Claude OpenRouter Test. Type 'exit' to quit.
You:
```
Type any message and press **Enter**. Claude will respond. Type `exit` or `quit` to stop.

## 5. (Optional) Quick test script
If you prefer a one‑click batch file, run `run_claude_test.bat`:
```bat
call .venv\Scripts\activate
python backend\claude_client.py
```

---
**Note:** The client uses the `httpx` library for HTTP requests and `python-dotenv` to load the `.env` file. Ensure your internet connection is active when testing.

Enjoy experimenting with Claude!
