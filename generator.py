import subprocess
from config import MODE, OLLAMA_MODEL
def extract_latest_message(email_text):
    """
    Extract only the most recent message content
    (removes quoted / forwarded text).
    """
    stop_markers = [
        "-----Original Message-----",
        "From:",
        "Sent:",
        "On ",
        ">"
    ]

    for marker in stop_markers:
        if marker in email_text:
            return email_text.split(marker)[0].strip()

    return email_text.strip()

def is_personal_info_requested(email_text: str) -> bool:
    triggers = [
        "your name",
        "your contact",
        "your details",
        "your designation",
        "your role",
        "how can we reach you",
        "share your contact",
        "please provide your details"
    ]

    email_lower = email_text.lower()
    return any(trigger in email_lower for trigger in triggers)

def generate_reply(style_examples, cleaned_email):
    tone = (
        "Use a formal and professional tone."
        if MODE == "professional"
        else "Use a friendly and casual tone."
    )

    prompt = f"""
You are an AI assistant that writes EMAIL REPLIES on my behalf.

CRITICAL INSTRUCTION:
You must respond WITHOUT reusing, paraphrasing, or referencing
any sentences, phrases, facts, dates, links, or structure
from the original email.

If the email is informational, promotional, or does not ask for a response,
return EXACTLY:
NO_REPLY

If a reply is appropriate, follow ALL rules strictly.

STRICT RULES FOR REPLY:
- Write ONLY the reply (no subject, no HTML)
- Write in first person (as me)
- Do NOT restate or summarize the email
- Do NOT mention event details, links, dates, or content
- Keep it short (2–4 sentences maximum)
- The reply must sound like a human acknowledgment or response
- {tone}
- Match my writing style
- End with: Palavalasa Vineetha

WRITING STYLE EXAMPLES (do NOT copy content, only tone):
{style_examples}

EMAIL (for context only — do NOT reuse wording):
{cleaned_email}
"""

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    )

    reply = result.stdout.strip()

    if reply == "NO_REPLY":
        return ""

    return reply
