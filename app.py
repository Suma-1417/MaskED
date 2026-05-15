from gmail_api import (
    get_gmail_service,
    read_sent_emails,
    read_inbox_emails,
    save_to_drafts
)

from rag import build_vector_store, retrieve_relevant_examples
from generator import extract_latest_message, generate_reply
from intent import is_personal_info_requested
from config import MY_IDENTITY

print("🔐 Connecting to Gmail...")
service = get_gmail_service()
print("✅ Gmail connected")

print("📩 Reading sent emails...")
sent_emails = read_sent_emails(service)

embedding_model, vector_index = build_vector_store(sent_emails)

print("📬 Reading inbox emails...")
inbox_emails = read_inbox_emails(service)

for email in inbox_emails:
    # 1️⃣ Extract only the latest user-written message
    latest = extract_latest_message(email)

    # 2️⃣ No scrubbing (local-only RAG)
    cleaned = latest

    # 3️⃣ Retrieve tone & style examples using RAG
    style_examples = retrieve_relevant_examples(
        cleaned,
        embedding_model,
        vector_index,
        sent_emails
    )

    # 4️⃣ Generate reply in YOUR tone
    reply = generate_reply(style_examples, cleaned)

    # 5️⃣ Append personal info ONLY if explicitly requested
    if is_personal_info_requested(cleaned):
        reply = reply.strip() + "\n\n" + MY_IDENTITY

    # 6️⃣ Save draft if reply is valid
    if reply.strip():
        save_to_drafts(
            service,
            to_email="example@gmail.com",
            subject="Re: Email",
            body=repl
        )
        print("✉️ Draft saved")
