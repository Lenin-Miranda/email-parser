import re
import spacy

nlp = spacy.load("en_core_web_sm")

STATUS_PATTERNS = [
    ("offer", [
        r"\bextend an offer\b",
        r"\boffer letter\b",
        r"\bpleased to offer you\b",
        r"\bexcited to offer you\b",
        r"\bcongratulations\b",
    ]),
    ("rejected", [
        r"\bregret to inform you\b",
        r"\bunfortunately\b",
        r"\bnot moving forward\b",
        r"\bmove forward with other candidates\b",
        r"\bposition has been filled\b",
    ]),
    ("interview", [
        r"\binvite you to (an )?interview\b",
        r"\bschedule (a|an)? ?(call|interview)\b",
        r"\bselect a time\b",
        r"\bnext step in the process\b",
        r"\binterview has been scheduled\b",
    ]),
    ("applied", [
        r"\breceived your application\b",
        r"\bthank you for applying\b",
        r"\bapplication has been received\b",
        r"\bwe are reviewing your application\b",
    ]),
]


def extract_emails(text: str) -> list[str]:
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(email_pattern, text)))


def extract_phones(text: str) -> list[str]:
    phone_pattern = r"\+?\d[\d\s().-]{7,}\d"
    return list(set(re.findall(phone_pattern, text)))


def extract_status(text: str) -> str:
    normalized_text = text.lower()

    for status, patterns in STATUS_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                return status

    return "saved"


def extract_companies(doc) -> list[str]:
    companies = [ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"]
    return list(set(companies))


def extract_names(doc) -> list[str]:
    names = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    return list(set(names))


def extract_dates(doc) -> list[str]:
    dates = [ent.text.strip() for ent in doc.ents if ent.label_ == "DATE"]
    return list(set(dates))


def extract_links(text: str) -> list[str]:
    pattern = r"https?://[^\s]+"
    links = re.findall(pattern, text)
    cleaned = [link.strip(".,;:()[]{}<>") for link in links]
    return list(set(cleaned))


def parse_email(text: str) -> dict:
    doc = nlp(text)

    return {
        "emails": extract_emails(text),
        "phones": extract_phones(text),
        "status": extract_status(text),
        "links": extract_links(text),
        "companies": extract_companies(doc),
        "names": extract_names(doc),
        "dates": extract_dates(doc),
    }