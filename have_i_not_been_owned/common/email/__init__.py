from typing import Optional


def normalize_email(email: str) -> Optional[dict]:
    if not email or not email.strip():
        return None

    email = email.strip().upper()
    domain = _get_domain(email)

    # Reject emails that don't have the domain set.
    if not domain:
        return None

    return {
        'email': email,
        'domain': domain
    }


def _get_domain(email: str) -> Optional[str]:
    domain = email.split('@')[-1].strip()

    if domain == email:
        return None

    return domain