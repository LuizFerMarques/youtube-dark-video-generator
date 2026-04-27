from pathlib import Path
from app.models import Scene
from app.utils import format_srt_timestamp, save_text


def generate_srt(scenes: list[Scene], output_path: Path) -> Path:
    blocks: list[str] = []

    for scene in scenes:
        blocks.append(str(scene.index))
        blocks.append(
            f"{format_srt_timestamp(scene.start_time)} --> {format_srt_timestamp(scene.end_time)}"
        )
        blocks.append(scene.text)
        blocks.append("")

    save_text(output_path, "\n".join(blocks))
    return output_path