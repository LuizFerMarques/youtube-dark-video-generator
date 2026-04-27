from pathlib import Path
from gtts import gTTS

from app.utils import ensure_dir


def generate_narration(text: str, output_path: Path, voice_name: str | None = None) -> Path:
    """
    Versão estável usando Google TTS
    """
    ensure_dir(output_path.parent)

    tts = gTTS(
        text=text,
        lang="pt-br",
        slow=False
    )

    tts.save(str(output_path))

    return output_path