import re
import nh3

ALLOWED_EMAIL_DOMAIN = 'upec.edu.ec'

ALLOWED_TAGS = {'p', 'b', 'i', 'em', 'strong', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'a', 'img', 'iframe', 'blockquote', 'pre', 'code',
                'table', 'thead', 'tbody', 'tr', 'th', 'td', 'br', 'hr', 'span', 'div', 'figure', 'figcaption'}

ALLOWED_ATTRIBUTES = {
    'a': {'href', 'target', 'rel'},
    'img': {'src', 'alt', 'width', 'height', 'title'},
    'iframe': {'src', 'width', 'height', 'frameborder', 'allowfullscreen', 'allow'},
    'td': {'colspan', 'rowspan'},
    'th': {'colspan', 'rowspan'},
    'span': {'class', 'style'},
    'div': {'class'},
}

def validate_upec_email(email: str) -> bool:
    if not email or '@' not in email:
        return False
    domain = email.rsplit('@', 1)[1].lower()
    return domain == ALLOWED_EMAIL_DOMAIN

def sanitize_html(raw_html: str) -> str:
    return nh3.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
