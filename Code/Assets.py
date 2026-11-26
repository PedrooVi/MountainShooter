import os

import pygame

from Code.Const import (
    AIR_ZOMBIE_HEIGHT,
    BODY_HEIGHT,
    BODY_LEFT,
    BODY_TOP,
    BODY_WIDTH,
    DUCK_HEIGHT_RATIO,
    GROUND_ZOMBIE_HEIGHT,
    PLAYER_SCALE,
    WIN_HEIGHT,
    WIN_WIDTH,
)
from Code.Paths import asset_path

_CHARACTERS = None
_ZOMBIES = None
_CITIES = None
_SCALED_ZOMBIES = {}

FRAME_SIZE = 128


def load():
    """Carrega personagens, zumbis e cidades uma unica vez."""
    characters()
    zombie_names()
    cities()


def characters():
    global _CHARACTERS
    if _CHARACTERS is None:
        _CHARACTERS = {}
        for name in ("Shinobi", "Samurai"):
            folder = asset_path("Personagens", name)
            run_frames = _scale_frames(_slice_sheet(os.path.join(folder, "Run.png")), PLAYER_SCALE)
            jump_frames = _scale_frames(_slice_sheet(os.path.join(folder, "Jump.png")), PLAYER_SCALE)
            _CHARACTERS[name] = {
                "run": run_frames,
                "jump": jump_frames,
                "duck": [_duck_frame(frame) for frame in run_frames],
            }
    return _CHARACTERS


def character(name):
    return characters()[name]


def zombie_names():
    global _ZOMBIES
    if _ZOMBIES is None:
        root = asset_path("Zombies", "PNG")
        _ZOMBIES = {}
        for name in sorted(os.listdir(root)):
            animation = os.path.join(root, name, "animation")
            if not os.path.isdir(animation):
                continue
            _ZOMBIES[name] = {
                "run": _frames(animation, "Run"),
                "jump": _frames(animation, "Jump"),
            }
        if not _ZOMBIES:
            raise FileNotFoundError("Nenhum zumbi encontrado em asset/Zombies/PNG")
    return list(_ZOMBIES)


def zombie_frames(variant, action, height):
    key = (variant, action, height)
    if key not in _SCALED_ZOMBIES:
        frames = []
        for image in _ZOMBIES[variant][action]:
            frames.append(_scale_to_height(image, height, smooth=True))
        _SCALED_ZOMBIES[key] = frames
    return _SCALED_ZOMBIES[key]


def zombie_height(kind):
    if kind == "ground":
        return GROUND_ZOMBIE_HEIGHT
    return AIR_ZOMBIE_HEIGHT


def cities():
    global _CITIES
    if _CITIES is None:
        root = asset_path("Backgrounds")
        _CITIES = []
        names = [
            name for name in os.listdir(root)
            if os.path.isdir(os.path.join(root, name)) and name.lower().startswith("city")
        ]
        for name in sorted(names, key=lambda item: int(item.split()[-1])):
            folder = os.path.join(root, name)
            layers = []
            for file_name in os.listdir(folder):
                if not file_name.lower().endswith(".png"):
                    continue
                image = pygame.image.load(os.path.join(folder, file_name)).convert_alpha()
                if image.get_size() != (WIN_WIDTH, WIN_HEIGHT):
                    continue
                layers.append((int(os.path.splitext(file_name)[0]), image))
            layers.sort(key=lambda item: item[0])
            if layers:
                _CITIES.append([image for _, image in layers])
        if not _CITIES:
            raise FileNotFoundError("Nenhum cenario compativel em asset/Backgrounds")
    return _CITIES


def _slice_sheet(path):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for x in range(0, sheet.get_width(), FRAME_SIZE):
        if x + FRAME_SIZE > sheet.get_width():
            break
        frame = pygame.Surface((FRAME_SIZE, FRAME_SIZE), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (x, 0, FRAME_SIZE, FRAME_SIZE))
        frames.append(frame)
    if not frames:
        raise FileNotFoundError(f"Spritesheet vazio: {path}")
    return frames


def _frames(folder, prefix):
    files = []
    for file_name in os.listdir(folder):
        stem, ext = os.path.splitext(file_name)
        if ext.lower() != ".png" or not stem.startswith(prefix):
            continue
        number = stem[len(prefix):]
        if not number.isdigit():
            continue
        files.append((int(number), os.path.join(folder, file_name)))
    files.sort(key=lambda item: item[0])
    if not files:
        raise FileNotFoundError(f"Animacao {prefix} ausente em {folder}")
    return [pygame.image.load(path).convert_alpha() for _, path in files]


def _scale_frames(frames, scale):
    scaled = []
    for frame in frames:
        width = int(frame.get_width() * scale)
        height = int(frame.get_height() * scale)
        scaled.append(pygame.transform.scale(frame, (width, height)))
    return scaled


def _scale_to_height(image, height, smooth=False):
    width = max(1, int(image.get_width() * (height / image.get_height())))
    scaler = pygame.transform.smoothscale if smooth else pygame.transform.scale
    return scaler(image, (width, height))


def _duck_frame(frame):
    crop = pygame.Rect(
        int(frame.get_width() * BODY_LEFT),
        int(frame.get_height() * BODY_TOP),
        max(1, int(frame.get_width() * BODY_WIDTH)),
        max(1, int(frame.get_height() * BODY_HEIGHT)),
    )
    body = pygame.Surface(crop.size, pygame.SRCALPHA)
    body.blit(frame, (0, 0), crop)
    duck_height = max(1, int(body.get_height() * DUCK_HEIGHT_RATIO))
    return pygame.transform.scale(body, (body.get_width(), duck_height))
