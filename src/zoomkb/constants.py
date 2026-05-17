PRODUCT_ALIASES = {
    "zoom-phone": {
        "name": "Zoom Phone",
        "aliases": [
            "Zoom Phone",
            "Phone System Management",
            "phone user",
            "phone users",
            "call queue",
            "call queues",
            "auto receptionist",
            "IVR",
            "shared line group",
            "direct phone number",
            "emergency address",
            "desk phone",
            "phone policy",
            "Zoom Phone policy",
            "common area phone",
            "call delegation",
            "phone site",
            "phone number management",
        ],
        "strong_signals": [
            "zoom phone",
            "phone system management",
            "phone user",
            "call queue",
            "auto receptionist",
            "shared line group",
            "common area phone",
            "call delegation",
            "phone site",
            "phone number",
        ],
        "medium_signals": [
            "phone users",
            "call queues",
            "direct numbers",
            "ivr",
            "emergency address",
            "desk phone",
            "phone policy",
            "phone site",
        ],
        "weak_signals": [
            "calling",
            "phone",
            "device",
            "extension",
            "desk phone",
            "dial",
            "voicemail",
            "phone number",
        ],
        "negative_signals": [
            "zoom meetings",
            "zoom rooms",
            "zoom contact center",
            "zoom webinar",
            "team chat",
            "whiteboard",
            "zoom clips",
            "zoom scheduler",
        ],
    },
}

DEFAULT_HEADERS = {
    "User-Agent": "ZoomKB-Builder/1.0 (research project; contact: internal)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

MIN_BODY_LENGTH = 200
MIN_WORD_COUNT = 50
REQUEST_TIMEOUT = 30
