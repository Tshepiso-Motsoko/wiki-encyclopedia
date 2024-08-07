# encyclopedia/util.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES_DIR = os.path.join(BASE_DIR, 'entries')


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    try:
        return [f.replace(".md", "") for f in os.listdir(ENTRIES_DIR) if os.path.isfile(os.path.join(ENTRIES_DIR, f))]
    except OSError:
        return []


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content. If an existing entry with the same name exists,
    it will be overwritten.
    """
    filename = os.path.join(ENTRIES_DIR, f"{title}.md")
    with open(filename, "w") as f:
        f.write(content)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no entry exists with the given title, returns None.
    """
    try:
        filename = os.path.join(ENTRIES_DIR, f"{title}.md")
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None
