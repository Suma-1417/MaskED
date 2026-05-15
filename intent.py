# intent.py

def is_personal_info_requested(email_text: str) -> bool:
    """
    Detects whether the incoming email explicitly asks
    for personal or contact information.
    """

    triggers = [
        "your name",
        "your contact",
        "your details",
        "your designation",
        "your role",
        "how can we reach you",
        "share your contact",
        "please provide your details",
        "contact details",
        "signature"
    ]

    email_lower = email_text.lower()
    return any(trigger in email_lower for trigger in triggers)
