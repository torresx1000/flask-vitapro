import os

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    return ("." in filename) and (filename.rsplit(".", 1)[1].lower() in allowed_extensions)


def clean_old_files(folder: str, hours: int = 24) -> int:
    """Remove files older than `hours` from `folder`. Returns number of deleted files."""
    now = os.path.getmtime
    import time

    current = time.time()
    limit = hours * 3600

    deleted = 0

    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue

        if current - os.path.getmtime(path) > limit:
            os.remove(path)
            deleted += 1

    return deleted
