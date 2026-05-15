
# 📧 MaskED - Masked Email Drafts (AI E-mail Assistant)

![Status](https://img.shields.io/badge/Status-1st_Place_Winner-gold) ![License](https://img.shields.io/badge/License-MIT-blue) ![Tech](https://img.shields.io/badge/Stack-GenAI_/_LLM-red)

**1st Place Winner** at the 12-hour GenAI & LLM Hackathon. **MASKED** is an intelligent email reply generator that uses local LLMs and RAG (Retrieval-Augmented Generation) to automatically draft professional responses matching your unique writing style.

---

## 🏆 Hackathon Achievement
* **Event:** 12-Hour GenAI & LLM Hackathon
* **Result:** **1st Prize** 🥇
* **Challenge:** Building a high-performance, privacy-first AI agent in under 12 hours.

---

## 👥 Meet the Team
This winning project was conceptualized and built during a continuous 12-hour sprint.

* **[Suma](https://github.com/Suma-1417) (Team Lead & AI Architect)**: Directed project vision and led the core development of the RAG (Retrieval-Augmented Generation) pipeline and Gmail API integration.
* **[Vineetha](https://github.com/Vineetha-17) (Lead AI Developer)**: Primary architect of the LLM orchestration using Ollama and developed the vector embedding logic for style matching.
* **[Devisri](https://github.com/Devisri1103) (Data & Security Engineer)**: Managed the secure OAuth 2.0 authentication flow and implemented the personal information detection logic.
* **Shammera (QA & Privacy Specialist)**: Conducted rigorous testing of tone-matching accuracy and optimized the local data cleaning pipeline.

---

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
git clone [https://github.com/Suma-1417/MASKED-Email-Assistant.git](https://github.com/Suma-1417/MASKED-Email-Assistant.git)
cd MASKED-Email-Assistant

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
2. Create a new project and enable Gmail API
3. Create OAuth 2.0 credentials and save as `credentials.json` in the project root

### 5. Configure settings

Edit `config.py`:

```python
MODE = "professional"  # or "personal"
OLLAMA_MODEL = "mistral"
MY_IDENTITY = """
Your Name
Title | Organization
"""

```

## 📖 Usage

### Run the assistant

```bash
python app.py

```

1. Connects to Gmail via OAuth.
2. Builds a local vector index of your sent emails.
3. Generates drafts in your Gmail account for review.

## 📁 Project Structure

```
gmail_ai_assistant/
├── app.py              # Main entry point
├── gmail_api.py        # Gmail API interactions
├── generator.py        # AI reply generation using Ollama
├── rag.py              # Vector embeddings & retrieval
├── intent.py           # Personal info detection
├── config.py           # Configuration settings
└── requirements.txt    # Python dependencies

```

## 🔒 Privacy & Security

* ✅ All email processing happens locally via Ollama.
* ✅ Embeddings generated locally using Sentence Transformers.
* ✅ OAuth 2.0 authentication ensures secure access to Gmail.

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

**Built with ❤️ by the 1st Place Winning Team using Ollama, FAISS, and Sentence Transformers**

