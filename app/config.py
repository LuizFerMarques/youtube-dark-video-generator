from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
IMAGENS_DIR = ASSETS_DIR / "imagens"
MUSICAS_DIR = ASSETS_DIR / "musicas"
PROJETOS_DIR = ASSETS_DIR / "projetos"
SAIDA_DIR = ASSETS_DIR / "saida"

for folder in [AUDIO_DIR, IMAGENS_DIR, MUSICAS_DIR, PROJETOS_DIR, SAIDA_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

VOICE_NAME = os.getenv("VOICE_NAME", "pt-BR-FranciscaNeural")
FPS = int(os.getenv("FPS", "24"))
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1920"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1080"))
DEFAULT_IMAGE_EXTENSION = os.getenv("DEFAULT_IMAGE_EXTENSION", ".png")
BACKGROUND_MUSIC_VOLUME = float(os.getenv("BACKGROUND_MUSIC_VOLUME", "0.12"))
NARRATION_WORDS_PER_SECOND = float(os.getenv("NARRATION_WORDS_PER_SECOND", "2.2"))
MIN_SCENE_DURATION = float(os.getenv("MIN_SCENE_DURATION", "4.0"))
MAX_SCENE_DURATION = float(os.getenv("MAX_SCENE_DURATION", "8.0"))
DEFAULT_THEME_STYLE = os.getenv(
    "DEFAULT_THEME_STYLE",
    "cinematic, emotional, dramatic lighting, ultra realistic, 4k"
)

TRANSITION_DURATION = float(os.getenv("TRANSITION_DURATION", "0.6"))
TEXT_OVERLAY_FONT_SIZE = int(os.getenv("TEXT_OVERLAY_FONT_SIZE", "46"))
TEXT_OVERLAY_COLOR = os.getenv("TEXT_OVERLAY_COLOR", "white")
TEXT_OVERLAY_STROKE_COLOR = os.getenv("TEXT_OVERLAY_STROKE_COLOR", "black")
TEXT_OVERLAY_STROKE_WIDTH = float(os.getenv("TEXT_OVERLAY_STROKE_WIDTH", "1.5"))
TEXT_OVERLAY_MARGIN_BOTTOM = int(os.getenv("TEXT_OVERLAY_MARGIN_BOTTOM", "120"))
TEXT_OVERLAY_WIDTH_PERCENT = float(os.getenv("TEXT_OVERLAY_WIDTH_PERCENT", "0.82"))
TEXT_OVERLAY_ENABLED_DEFAULT = os.getenv("TEXT_OVERLAY_ENABLED_DEFAULT", "false").lower() == "true"