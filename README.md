# 📧 Gmail AI Assistant

An intelligent email reply generator that uses AI and your writing style to automatically draft professional responses to incoming emails.

## ✨ Features

- **AI-Powered Replies**: Generates contextual email responses using Ollama with Mistral LLM
- **Style Matching**: Uses RAG (Retrieval-Augmented Generation) to analyze your sent emails and match your writing tone
- **Privacy-First**: All processing happens locally - no data sent to external APIs
- **Smart Detection**: Automatically identifies when personal information is requested
- **Draft Management**: Saves generated replies to Gmail drafts for review before sending
- **Tone Customization**: Supports both professional and personal modes

## 🏗️ Architecture

The assistant follows a 6-step pipeline:

1. **Email Extraction** - Reads latest user message (removes quoted/forwarded text)
2. **Local Processing** - All data stays local (no cloud scrubbing)
3. **RAG Retrieval** - Finds similar sent emails to understand your writing style
4. **AI Generation** - Uses Ollama to generate a reply matching your tone
5. **Personal Info Detection** - Appends your identity only if explicitly requested
6. **Draft Creation** - Saves the reply to Gmail drafts

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed with Mistral model (`ollama pull mistral`)
- Google Gmail API credentials (OAuth 2.0)
- ~3GB RAM for embeddings model

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd gmail_ai_assistant
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials as `credentials.json` and place in project root

### 5. Configure settings

Edit `config.py`:

```python
MODE = "professional"  # or "personal"
OLLAMA_MODEL = "mistral"
MY_IDENTITY = """
Your Name
Title | Organization
Email | Phone
"""
```

### 6. Start Ollama

```bash
ollama serve
# In another terminal: ollama pull mistral
```

## 📖 Usage

### Run the assistant

```bash
python app.py
```

The script will:
1. Connect to Gmail
2. Read your sent emails for style reference
3. Build a local embeddings index
4. Process each inbox email
5. Generate AI replies matching your tone
6. Save drafts to Gmail

### Review and Send

- Check Gmail drafts for generated replies
- Edit if needed
- Send or discard

## 📁 Project Structure

```
gmail_ai_assistant/
├── app.py              # Main entry point
├── gmail_api.py        # Gmail API interactions
├── generator.py        # AI reply generation using Ollama
├── rag.py              # Vector embeddings & retrieval
├── intent.py           # Personal info detection
├── config.py           # Configuration settings
├── privacy.py          # Privacy utilities
├── requirements.txt    # Python dependencies
└── credentials.json    # Gmail API credentials (git-ignored)
```

## 🔧 Configuration Options

### `config.py`

| Setting | Options | Description |
|---------|---------|-------------|
| `MODE` | "professional", "personal" | Tone for generated replies |
| `OLLAMA_MODEL` | "mistral", "llama2", etc. | LLM model to use |
| `MY_IDENTITY` | String | Your signature/contact info |
| `SCOPES` | Gmail API scopes | API permissions (read inbox/compose) |

## 🔒 Privacy & Security

- ✅ All email processing happens locally
- ✅ Embeddings generated locally using Sentence Transformers
- ✅ No data sent to external APIs (except Gmail OAuth)
- ✅ OAuth 2.0 authentication for Gmail
- ✅ Credentials never committed to version control

## ⚠️ Limitations

- Requires Ollama running locally
- Processes one inbox at a time
- Limited to first 20 sent emails for style reference
- May need tuning for non-English emails

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## 📜 License

This project is provided as-is for personal use.

## 🆘 Troubleshooting

### Gmail connection fails
- Verify `credentials.json` exists and is valid
- Re-authenticate: Delete `token.pickle` and re-run

### No replies generated
- Check if emails need actual responses (informational emails return `NO_REPLY`)
- Ensure Ollama is running: `ollama serve`
- Verify Mistral model: `ollama list`

### Slow performance
- Embeddings computation is resource-intensive
- Reduce number of sent emails in `gmail_api.py` `max_results` parameter
- Ensure sufficient RAM available

## 📝 Notes

- Replies are saved as **drafts only** - review before sending
- Personal information appended only when explicitly requested
- Generated content follows strict rules to avoid copying original emails
- Writing style learned from your past sent emails

---

**Built with ❤️ using Ollama, FAISS, and Sentence Transformers**
