from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Scene:
    index: int
    text: str
    duration: float
    prompt: str = ""
    image_path: str = ""
    start_time: float = 0.0
    end_time: float = 0.0


@dataclass
class VideoProject:
    slug: str
    theme: str
    title: str
    roteiro: str
    scenes: List[Scene] = field(default_factory=list)
    audio_path: Optional[Path] = None
    subtitle_path: Optional[Path] = None
    video_path: Optional[Path] = None
    metadata_path: Optional[Path] = None