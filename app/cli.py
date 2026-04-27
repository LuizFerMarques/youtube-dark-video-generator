import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="youtube_dark_factory",
        description="Gera videos dark a partir de roteiro, audio e imagens."
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Titulo do video."
    )
    parser.add_argument(
        "--theme",
        required=True,
        help="Tema base do video."
    )

    grupo_roteiro = parser.add_mutually_exclusive_group(required=True)
    grupo_roteiro.add_argument(
        "--roteiro-file",
        help="Caminho para um arquivo TXT contendo o roteiro."
    )
    grupo_roteiro.add_argument(
        "--roteiro-text",
        help="Texto do roteiro passado diretamente no terminal."
    )

    parser.add_argument(
        "--voice",
        help="Nome da voz do edge-tts. Ex: pt-BR-AntonioNeural"
    )
    parser.add_argument(
        "--background-music",
        help="Caminho da musica de fundo."
    )
    parser.add_argument(
        "--text-overlay",
        action="store_true",
        help="Exibe texto da cena sobre a imagem."
    )
    parser.add_argument(
        "--no-text-overlay",
        action="store_true",
        help="Desabilita texto na tela mesmo se estiver ativado por padrao."
    )
    parser.add_argument(
        "--image-extension",
        default=None,
        help="Extensao esperada das imagens. Ex: .png, .jpg"
    )

    return parser