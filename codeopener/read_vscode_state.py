import os
import json
import sqlite3
from typing import List
from .exception import CodeOpenerException


def parse_vscode_state(value: str) -> List[str]:
    try:
        folder_uris = []
        value = json.loads(value)
        if 'entries' not in value:
            raise CodeOpenerException("VSCode state does not contain 'entries'")
        entries = value['entries']
        for entry in entries:
            if 'folderUri' in entry:
                folder_uris.append(entry['folderUri'])
        return folder_uris
    except json.JSONDecodeError:
        raise CodeOpenerException("VSCode state is not a valid JSON")


def read_vscode_state() -> List[str]:
    if 'APPDATA' not in os.environ:
        raise CodeOpenerException("APPDATA is not found in environment variables")
    p = os.path.join(os.environ['APPDATA'], "Code", "User", "globalStorage", "state.vscdb")
    if not os.path.exists(p):
        raise CodeOpenerException("VSCode state file is not found")
    conn = sqlite3.connect(p)
    c = conn.cursor()
    c.execute("SELECT * FROM ItemTable")
    state = c.fetchall()
    conn.close()
    for (key, value) in state:
        if key == "history.recentlyOpenedPathsList":
            return parse_vscode_state(value)
    raise CodeOpenerException("VSCode state file does not contain history.recentlyOpenedPathsList")
