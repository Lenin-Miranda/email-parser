import re

def extract_emails(text: str) -> list:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(email_pattern, text)))

def extract_phones(text: str) -> list:
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?[\d\s.-]{7,10}'
    return list(set(re.findall(phone_pattern, text)))

def extract_status(text: str) -> str:
    status_pattern = r'\b(accepted|rejected|pending|approved|denied)\b'
    match = re.search(status_pattern, text, re.IGNORECASE)
    return match.group(0) if match else 'Unknown'

def extract_links(text: str) -> list:
    patter = r'https?://[^\s]+'
    links = re.findall(patter, text)

    cleaned = [link.strip('.,;:()[]{}<>') for link in links]
    return list(set(cleaned))

def parse_email(text: str) -> dict:
    return {
        'emails': extract_emails(text),
        'phones': extract_phones(text),
        'status': extract_status(text),
        'links': extract_links(text)
    }