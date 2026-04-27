from pathlib import Path
from app.models import VideoProject
from app.utils import save_json, save_text


def export_roteiro(project: VideoProject, output_dir: Path) -> Path:
    path = output_dir / "roteiro.txt"
    save_text(path, project.roteiro)
    return path


def export_prompts(project: VideoProject, output_dir: Path) -> Path:
    lines: list[str] = []

    for scene in project.scenes:
        lines.append(f"Cena {scene.index:02d}")
        lines.append(f"Texto: {scene.text}")
        lines.append(f"Duracao: {scene.duration}")
        lines.append(f"Inicio: {scene.start_time}")
        lines.append(f"Fim: {scene.end_time}")
        lines.append(f"Imagem: {scene.image_path}")
        lines.append(f"Prompt: {scene.prompt}")
        lines.append("-" * 80)

    path = output_dir / "prompts.txt"
    save_text(path, "\n".join(lines))
    return path


def export_scenes_json(project: VideoProject, output_dir: Path) -> Path:
    data = {
        "slug": project.slug,
        "theme": project.theme,
        "title": project.title,
        "roteiro": project.roteiro,
        "audio_path": str(project.audio_path) if project.audio_path else None,
        "subtitle_path": str(project.subtitle_path) if project.subtitle_path else None,
        "video_path": str(project.video_path) if project.video_path else None,
        "scenes": [
            {
                "index": scene.index,
                "text": scene.text,
                "duration": scene.duration,
                "start_time": scene.start_time,
                "end_time": scene.end_time,
                "prompt": scene.prompt,
                "image_path": scene.image_path,
            }
            for scene in project.scenes
        ],
    }

    path = output_dir / "cenas.json"
    save_json(path, data)
    return path