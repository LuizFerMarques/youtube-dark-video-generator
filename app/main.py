from pathlib import Path

from app.cli import build_parser
from app.config import PROJETOS_DIR, TEXT_OVERLAY_ENABLED_DEFAULT
from app.models import VideoProject
from app.utils import slugify, ensure_dir, read_text
from app.services.roteiro_service import normalize_roteiro, validate_roteiro
from app.services.scene_service import build_scenes
from app.services.prompt_service import attach_prompts
from app.services.tts_service import generate_narration
from app.services.subtitle_service import generate_srt
from app.services.asset_service import bind_scene_images, validate_scene_images
from app.services.export_service import (
    export_roteiro,
    export_prompts,
    export_scenes_json,
)
from app.services.video_service import build_video_from_scenes


def resolve_text_overlay_flag(enable_flag: bool, disable_flag: bool) -> bool:
    if disable_flag:
        return False
    if enable_flag:
        return True
    return TEXT_OVERLAY_ENABLED_DEFAULT


def build_project(
    theme: str,
    title: str,
    roteiro: str,
    voice: str | None = None,
    background_music_path: str | None = None,
    text_overlay: bool = False,
    image_extension: str | None = None,
) -> VideoProject:
    roteiro = normalize_roteiro(roteiro)
    validate_roteiro(roteiro)

    slug = slugify(title)
    project_dir = ensure_dir(PROJETOS_DIR / slug)
    output_dir = ensure_dir(project_dir / "saida")

    scenes = build_scenes(roteiro)
    scenes = attach_prompts(scenes, theme)
    scenes = bind_scene_images(
        scenes=scenes,
        slug=slug,
        projetos_dir=PROJETOS_DIR,
        extension=image_extension,
    )

    narration_path = output_dir / "narracao.mp3"
    subtitle_path = output_dir / "legendas.srt"
    video_path = output_dir / "video_final.mp4"

    project = VideoProject(
        slug=slug,
        theme=theme,
        title=title,
        roteiro=roteiro,
        scenes=scenes,
        audio_path=narration_path,
        subtitle_path=subtitle_path,
        video_path=video_path,
    )

    export_roteiro(project, output_dir)
    export_prompts(project, output_dir)
    export_scenes_json(project, output_dir)

    generate_narration(project.roteiro, narration_path, voice_name=voice)
    generate_srt(project.scenes, subtitle_path)

    validate_scene_images(project.scenes)

    bgm_path = Path(background_music_path) if background_music_path else None

    build_video_from_scenes(
        scenes=project.scenes,
        narration_audio_path=project.audio_path,
        output_video_path=project.video_path,
        background_music_path=bgm_path,
        text_overlay=text_overlay,
    )

    export_scenes_json(project, output_dir)
    return project


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    roteiro = args.roteiro_text
    if args.roteiro_file:
        roteiro = read_text(Path(args.roteiro_file))

    text_overlay = resolve_text_overlay_flag(
        enable_flag=args.text_overlay,
        disable_flag=args.no_text_overlay,
    )

    project = build_project(
        theme=args.theme,
        title=args.title,
        roteiro=roteiro,
        voice=args.voice,
        background_music_path=args.background_music,
        text_overlay=text_overlay,
        image_extension=args.image_extension,
    )

    print("\nProjeto gerado com sucesso.")
    print(f"Titulo: {project.title}")
    print(f"Slug: {project.slug}")
    print(f"Cenas: {len(project.scenes)}")
    print(f"Audio: {project.audio_path}")
    print(f"Legenda: {project.subtitle_path}")
    print(f"Video: {project.video_path}")


if __name__ == "__main__":
    main()