from django import template

register = template.Library()

CZECH_MONTHS = [
    "leden",
    "únor",
    "březen",
    "duben",
    "květen",
    "červen",
    "červenec",
    "srpen",
    "září",
    "říjen",
    "listopad",
    "prosinec",
]


@register.filter
def czech_date(value):
    if not value:
        return ""
    try:
        day = value.day
        month = CZECH_MONTHS[value.month - 1]
        year = value.year
        return f"{day}. {month} {year}"
    except Exception:
        return value
