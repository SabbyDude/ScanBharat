# scam_patterns.py
# This file contains the predefined common Indian scam patterns and their
# characteristic keywords and phrases. These patterns are used by the
# 'main.py' script for detection and categorization.

# The SCAM_PATTERNS dictionary maps a scam type (key) to a list of
# associated keywords and phrases (value).
# All keywords/phrases should be in lowercase to match preprocessed text.

SCAM_PATTERNS = {
    "WhatsApp Scam": [
        "your account will be deactivated",
        "click here to verify your number now",
        "hey it's me",
        "i lost my wallet",
        "can you send me",
        "earn daily",
        "contact us to start now",
        "congrats you've won",
        "whatsapp lottery",
        "share your bank details"
    ],
    "Instant Loan Scam": [
        "easy loans with minimal requirements",
        "fast disbursements",
        "advance fees",
        "unsolicited offers",
        "too good to be true",
        "excessive interest rates",
        "loan app",
        "get instant loan"
    ],
    "Fake Delivery Scam": [
        "your package couldn't be delivered",
        "extra charges needed to complete the delivery",
        "delivery agent",
        "click here to reschedule",
        "delivery fee",
        "pending delivery"
    ],
    "Digital Arrest Scam": [
        "impersonating state/ut police",
        "ncb",
        "cbi",
        "rbi",
        "digital arrest",
        "legal action",
        "blackmail",
        "urgent payment",
        "warrant",
        "summons"
    ],
    "Credit Card Scam": [
        "verify your credit card details",
        "otp",
        "pin",
        "account blocked",
        "unauthorized transaction",
        "credit card limit",
        "reward points",
        "card verification value"
    ]
}

