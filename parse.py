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
        r"\bnot moving forward with your application\b",
    ]),
    ("interview", [
        r"\binvite you to (an )?interview\b",
        r"\bschedule (a|an)? ?(call|interview)\b",
        r"\bselect a time\b",
        r"\bnext step in the process\b",
        r"\byour interview .* has been scheduled\b",
        r"\binterview .* has been scheduled\b",
        r"\bjoin the meeting here\b",
        r"\bpick a time\b",
    ]),
    ("applied", [
        r"\breceived your application\b",
        r"\bthank you for applying\b",
        r"\bapplication has been received\b",
        r"\bwe are reviewing your application\b",
    ]),
]

COMPANY_BLACKLIST = {
    "software",
    "frontend developer",
    "backend engineer",
    "software engineer",
    "recruiting team",
    "recruitment team",
    "hiring team",
    "hr team",
}

def extract_emails(text: str) -> list[str]:
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(email_pattern, text)))


def extract_phones(text: str) -> list[str]:
    phone_pattern = r'(?:\+1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}'
    return list(set(re.findall(phone_pattern, text)))


def extract_status(text: str) -> str:
    normalized_text = text.lower()

    for status, patterns in STATUS_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                return status

    return "saved"


def extract_companies(doc) -> list[str]:
    companies = []

    for ent in doc.ents:
        if ent.label_ == 'ORG':
            company = ent.text.strip()

            lowered = company.lower()

            if lowered in COMPANY_BLACKLIST:
                continue
            if any(word in lowered for word in ['team', 'recruiting', 'recruitment', 'hiring', 'hr']):
                continue
            companies.append(company)

    return list(set(companies))


def extract_names(doc) -> list[str]:
    names = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            lowered = name.lower()

            if any(word in lowered for word in ["team", "recruiting", "recruitment", "hiring", "hr"]):
                continue

            names.append(name)

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