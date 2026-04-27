from pathlib import Path

from moviepy import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
)
from moviepy.audio.fx.AudioLoop import AudioLoop
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut

from app.config import (
    FPS,
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
    BACKGROUND_MUSIC_VOLUME,
    TRANSITION_DURATION,
    TEXT_OVERLAY_FONT_SIZE,
    TEXT_OVERLAY_COLOR,
    TEXT_OVERLAY_STROKE_COLOR,
    TEXT_OVERLAY_STROKE_WIDTH,
    TEXT_OVERLAY_MARGIN_BOTTOM,
    TEXT_OVERLAY_WIDTH_PERCENT,
)
from app.models import Scene
from app.utils import wrap_text_for_screen


def create_base_image_clip(image_path: str, duration: float) -> ImageClip:
    clip = ImageClip(image_path).with_duration(duration)
    clip = clip.resized((VIDEO_WIDTH, VIDEO_HEIGHT))
    clip = clip.resized(lambda t: 1 + (0.015 * t / max(duration, 0.1)))
    clip = clip.with_effects([
        FadeIn(TRANSITION_DURATION),
        FadeOut(TRANSITION_DURATION),
    ])
    return clip


def create_text_overlay_clip(text: str, duration: float) -> TextClip:
    wrapped = wrap_text_for_screen(text, width=28)

    clip = TextClip(
        text=wrapped,
        font_size=TEXT_OVERLAY_FONT_SIZE,
        color=TEXT_OVERLAY_COLOR,
        stroke_color=TEXT_OVERLAY_STROKE_COLOR,
        stroke_width=TEXT_OVERLAY_STROKE_WIDTH,
        method="caption",
        size=(int(VIDEO_WIDTH * TEXT_OVERLAY_WIDTH_PERCENT), None),
        text_align="center",
    )

    clip = clip.with_duration(duration)
    clip = clip.with_position(("center", VIDEO_HEIGHT - TEXT_OVERLAY_MARGIN_BOTTOM - clip.h))
    clip = clip.with_effects([
        FadeIn(min(0.3, TRANSITION_DURATION)),
        FadeOut(min(0.3, TRANSITION_DURATION)),
    ])
    return clip


def create_scene_clip(scene: Scene, text_overlay: bool = False) -> CompositeVideoClip | ImageClip:
    base = create_base_image_clip(scene.image_path, scene.duration)

    if not text_overlay:
        return base

    overlay = create_text_overlay_clip(scene.text, scene.duration)
    return CompositeVideoClip([base, overlay], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).with_duration(scene.duration)


def build_video_from_scenes(
    scenes: list[Scene],
    narration_audio_path: Path,
    output_video_path: Path,
    background_music_path: Path | None = None,
    text_overlay: bool = False,
) -> Path:
    if not narration_audio_path.exists():
        raise FileNotFoundError(f"Audio de narracao nao encontrado: {narration_audio_path}")

    clips = [create_scene_clip(scene, text_overlay=text_overlay) for scene in scenes]
    video = concatenate_videoclips(clips, method="compose")

    narration_audio = AudioFileClip(str(narration_audio_path))
    audio_tracks = [narration_audio]

    if background_music_path and background_music_path.exists():
        bgm = AudioFileClip(str(background_music_path))
        bgm = AudioLoop(duration=narration_audio.duration).apply(bgm)
        bgm = bgm.with_volume_scaled(BACKGROUND_MUSIC_VOLUME)
        audio_tracks.append(bgm)

    final_audio = CompositeAudioClip(audio_tracks)
    final_video = video.with_audio(final_audio)

    output_video_path.parent.mkdir(parents=True, exist_ok=True)
    final_video.write_videofile(
        str(output_video_path),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
    )

    return output_video_path