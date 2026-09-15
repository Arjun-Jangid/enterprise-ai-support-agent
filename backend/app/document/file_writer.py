
def save_text_file(text, save_path) -> bool:
    if not text:
        return False

    try:
        save_path.write_text(text, encoding="utf-8")
        return True

    except Exception:
        return False