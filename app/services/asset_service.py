from pathlib import Path
from app.config import DEFAULT_IMAGE_EXTENSION
from app.models import Scene
from app.utils import ensure_dir


def get_project_root(slug: str, projetos_dir: Path) -> Path:
    return ensure_dir(projetos_dir / slug)


def get_project_images_dir(slug: str, projetos_dir: Path) -> Path:
    return ensure_dir(get_project_root(slug, projetos_dir) / "imagens")


def expected_scene_image_path(
    slug: str,
    projetos_dir: Path,
    scene_index: int,
    extension: str | None = None,
) -> Path:
    ext = extension or DEFAULT_IMAGE_EXTENSION
    return get_project_images_dir(slug, projetos_dir) / f"cena_{scene_index:02d}{ext}"


def bind_scene_images(
    scenes: list[Scene],
    slug: str,
    projetos_dir: Path,
    extension: str | None = None,
) -> list[Scene]:
    for scene in scenes:
        scene.image_path = str(expected_scene_image_path(slug, projetos_dir, scene.index, extension))
    return scenes


def validate_scene_images(scenes: list[Scene]) -> None:
    missing = [scene.image_path for scene in scenes if not Path(scene.image_path).exists()]
    if missing:
        raise FileNotFoundError(
            "As imagens abaixo nao foram encontradas:\n" + "\n".join(missing)
        )