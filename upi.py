import os
import streamlit as st

# ---- SSL SAFETY FIX (Windows + Python 3.13) ----
os.environ["SSL_CERT_FILE"] = ""

from gmail_api import (
    get_gmail_service,
    read_inbox_emails,
    read_sent_emails,
    save_to_drafts
)
from rag import build_vector_store, retrieve_relevant_examples
#from privacy import scrub_data
from generator import extract_latest_message, generate_reply


# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="AI Gmail Assistant",
    layout="wide"
)

st.title("📧 AI Gmail Assistant (RAG Powered)")


# ---- SESSION INITIALIZATION ----
if "service" not in st.session_state:
    st.session_state.service = get_gmail_service()

service = st.session_state.service


# ---- CACHED GMAIL LOADERS (CRITICAL FIX) ----
@st.cache_data(show_spinner="📩 Loading sent emails...")
def load_sent_emails():
    return read_sent_emails(service)


@st.cache_data(show_spinner="📬 Loading inbox emails...")
def load_inbox_emails():
    return read_inbox_emails(service)


# ---- LOAD DATA BUTTONS ----
col1, col2 = st.columns(2)

with col1:
    if st.button("📬 Load Inbox Emails"):
        st.session_state.inbox_emails = load_inbox_emails()

with col2:
    if st.button("📩 Load Sent Emails (RAG Base)"):
        st.session_state.sent_emails = load_sent_emails()


# ---- INBOX VIEW ----
if "inbox_emails" in st.session_state:
    st.subheader("📨 Inbox Emails")

    selected_index = st.selectbox(
        "Select an email",
        range(len(st.session_state.inbox_emails)),
        format_func=lambda i: st.session_state.inbox_emails[i][:80]
    )

    raw_email = st.session_state.inbox_emails[selected_index]
    latest_email = extract_latest_message(raw_email)
    cleaned_email = latest_email  # No scrubbing (local-only RAG)

    st.text_area(
        "Email Content",
        cleaned_email,
        height=220
    )

    # ---- GENERATE REPLY ----
    if st.button("✨ Generate Reply"):

        if "sent_emails" not in st.session_state:
            st.warning("Please load sent emails first (RAG base).")
        else:
            with st.spinner("🧠 Generating reply using RAG..."):
                embedding_model, vector_index = build_vector_store(
                    st.session_state.sent_emails
                )

                style_examples = retrieve_relevant_examples(
                    cleaned_email,
                    embedding_model,
                    vector_index,
                    st.session_state.sent_emails
                )

                reply = generate_reply(style_examples, cleaned_email)
                st.session_state.generated_reply = reply


# ---- REPLY EDITOR ----
if "generated_reply" in st.session_state:
    st.subheader("✍️ AI Generated Reply")

    edited_reply = st.text_area(
        "Edit reply if needed",
        st.session_state.generated_reply,
        height=220
    )

    if st.button("💾 Save Draft to Gmail"):
        save_to_drafts(
            service,
            to_email="example@gmail.com",
            subject="Re: Email",
            body=edited_reply
        )
        st.success("✅ Draft saved to Gmail!")
