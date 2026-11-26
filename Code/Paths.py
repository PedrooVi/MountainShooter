import os
import sys


def project_root():
    """Pasta do jogo no Python e tambem no executavel compilado."""
    if getattr(sys, "frozen", False):
        candidates = [os.path.dirname(sys.executable)]
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            candidates.append(meipass)
    else:
        candidates = [os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))]

    for base in candidates:
        if any(os.path.isdir(os.path.join(base, folder)) for folder in ("assets", "asset")):
            return base
    return candidates[0]


def asset_path(*parts):
    root = project_root()
    folder = next(
        (name for name in ("assets", "asset") if os.path.isdir(os.path.join(root, name))),
        "assets",
    )
    return os.path.join(root, folder, *parts)
