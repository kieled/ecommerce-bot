def extract_unique_code(text) -> int | None:
    try:
        return int(text.split()[1]) if len(text.split()) == 2 else None
    except ValueError:
        return None
