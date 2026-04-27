from app.config import DEFAULT_THEME_STYLE
from app.models import Scene


KEYWORD_MAP = {
    "oração": "person praying, hands together, sacred atmosphere",
    "oracao": "person praying, hands together, sacred atmosphere",
    "deus": "heavenly light, divine presence, spiritual environment",
    "jesus": "biblical atmosphere, sacred symbolism, emotional scene",
    "bíblia": "open bible, golden light, cinematic composition",
    "biblia": "open bible, golden light, cinematic composition",
    "fé": "person with hopeful expression, sunrise, spiritual strength",
    "fe": "person with hopeful expression, sunrise, spiritual strength",
    "milagre": "divine light breaking through clouds, powerful symbolic scene",
    "jejum": "person in contemplative silence, spiritual discipline, introspective atmosphere",
    "arrependimento": "person kneeling in repentance, emotional and reverent atmosphere",
    "cruz": "cross silhouette, dramatic sky, sacred light",
    "céu": "heavenly sky, powerful light rays, majestic atmosphere",
    "ceu": "heavenly sky, powerful light rays, majestic atmosphere",
    "escuridão": "dark background, contrast with divine light, intense atmosphere",
    "escuridao": "dark background, contrast with divine light, intense atmosphere",
    "esperança": "sunrise, peaceful mountains, golden light, emotional hope",
    "esperanca": "sunrise, peaceful mountains, golden light, emotional hope",
}


def build_prompt(scene_text: str, theme: str) -> str:
    lowered = scene_text.lower()

    matched_fragments = [
        visual for keyword, visual in KEYWORD_MAP.items() if keyword in lowered
    ]

    if not matched_fragments:
        matched_fragments.append(f"symbolic visual representation of {theme}")

    visual_part = ", ".join(dict.fromkeys(matched_fragments))
    return f"{visual_part}, {DEFAULT_THEME_STYLE}"


def attach_prompts(scenes: list[Scene], theme: str) -> list[Scene]:
    for scene in scenes:
        scene.prompt = build_prompt(scene.text, theme)
    return scenes