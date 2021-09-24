from datetime import datetime


def try_parse_string_to_date(text: str) -> datetime:
    """ This function will attempt to parse a
    string to a date using multiple combination of date format
    """
    for fmt in ("%b %Y", "%B %Y"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError("no valid date format found")
