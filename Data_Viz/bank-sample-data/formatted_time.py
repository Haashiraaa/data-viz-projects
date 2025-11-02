from datetime import datetime


def normalize_again(date_fmt):
    """
    Attempt to normalize dates with fallback formats.

    Tries multiple year-first formats, such as:
    - '2025-10-21 13:45:23'
    - '2025-Oct-21'
    - '2025-10-21'

    Args:
        date_fmt (str): The date string to parse.

    Returns:
        datetime.date | None: A date object if parsing succeeds, otherwise None.
    """
    date_obj = None
    date_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y %b %d %H:%M:%S",
        "%Y-%b-%d",
        "%Y-%m-%d"
    ]

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_fmt, fmt).date()
            break
        except ValueError:
            continue

    return date_obj


def normalize_date(date_fmt):
    """
    Normalize date strings from various formats to datetime.date.

    Handles formats with or without time, and falls back to `normalize_again()`
    if the standard formats do not match.

    Tries:
    - '21 Oct 2025 13:45:23'
    - '21 Oct 2025'
    - '21/10/2025'
    - and year-first formats via normalize_again()

    Args:
        date_fmt (str): The date string to parse.

    Returns:
        datetime.date | None: A date object if successful, otherwise None.
    """
    date_obj = None
    date_formats = [
        "%d %b %Y %H:%M:%S",
        "%d %b %Y",
        "%d/%m/%Y"
    ]

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_fmt, fmt).date()
            break
        except ValueError:
            continue

    if not date_obj:
        date_obj = normalize_again(date_fmt=date_fmt)

    return date_obj
