import re


def normalize_roteiro(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_roteiro_blocks(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def validate_roteiro(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("O roteiro nao pode estar vazio.")

    words = text.split()
    if len(words) < 20:
        raise ValueError("O roteiro e muito curto. Envie um texto maior para gerar um video.")