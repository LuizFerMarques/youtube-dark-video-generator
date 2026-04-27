from app.config import (
    NARRATION_WORDS_PER_SECOND,
    MIN_SCENE_DURATION,
    MAX_SCENE_DURATION,
)
from app.models import Scene
from app.services.roteiro_service import split_roteiro_blocks


def estimate_scene_duration(text: str) -> float:
    words = len(text.split())
    duration = words / NARRATION_WORDS_PER_SECOND
    duration = max(MIN_SCENE_DURATION, duration)
    duration = min(MAX_SCENE_DURATION, duration)
    return round(duration, 2)


def build_scenes(roteiro: str) -> list[Scene]:
    blocks = split_roteiro_blocks(roteiro)
    scenes: list[Scene] = []
    current_time = 0.0

    for idx, block in enumerate(blocks, start=1):
        duration = estimate_scene_duration(block)
        start_time = round(current_time, 2)
        end_time = round(current_time + duration, 2)

        scenes.append(
            Scene(
                index=idx,
                text=block,
                duration=duration,
                start_time=start_time,
                end_time=end_time,
            )
        )
        current_time = end_time

    return scenes