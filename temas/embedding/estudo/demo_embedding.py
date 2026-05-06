"""Demo simples de embeddings pré-treinados para apresentação.

Uso:
    python temas/embedding/estudo/demo_embedding.py
    python temas/embedding/estudo/demo_embedding.py --model glove-wiki-gigaword-100 --topn 5

Na primeira execução, o `gensim` faz download do modelo escolhido.
O exemplo usa um modelo em inglês porque ele é compacto e costuma funcionar
bem para analogias clássicas de embeddings.
"""

from __future__ import annotations

import argparse
import sys
from typing import Iterable, Sequence

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Dependência ausente: instale as bibliotecas do projeto com "
        "`pip install -r requirements.txt`."
    ) from exc


DEFAULT_MODEL = "glove-wiki-gigaword-100"
DEMO_WORDS = ("father", "mother", "uncle", "aunt", "king", "man", "woman", "queen")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mostra vetores de palavras e faz contas com embeddings pré-treinados."
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Nome do modelo no gensim.downloader. Padrão: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--topn",
        type=int,
        default=5,
        help="Quantidade de resultados exibidos em cada analogia.",
    )
    return parser.parse_args()


def load_model(model_name: str):
    try:
        import gensim.downloader as api
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Biblioteca ausente: instale as dependências com "
            "`pip install -r requirements.txt`."
        ) from exc

    print(f"Carregando modelo '{model_name}'...")
    print("Se for a primeira vez, o gensim vai baixar o modelo automaticamente.\n")
    return api.load(model_name)


def require_words(model, words: Iterable[str], model_name: str) -> None:
    missing = [word for word in words if word not in model]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"O modelo '{model_name}' não contém as palavras: {joined}")


def preview_vector(vector: np.ndarray, size: int = 8) -> str:
    return ", ".join(f"{value:+.3f}" for value in vector[:size])


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Não é possível calcular cosseno com vetor nulo.")
    return float(np.dot(vector_a, vector_b) / (norm_a * norm_b))


def print_section(title: str) -> None:
    print("=" * 80)
    print(title)
    print("=" * 80)


def print_embedding_preview(model, words: Sequence[str]) -> None:
    print_section("1) Cada palavra vira um vetor")
    dimension = model.vector_size
    print(f"Dimensão do embedding: {dimension}\n")

    for word in words:
        vector = model[word]
        print(
            f"{word:>8} -> [{preview_vector(vector)} ...] "
            f"(mostrando só as 8 primeiras posições)"
        )
    print()


def compare_relations(model, left_a: str, left_b: str, right_a: str, right_b: str) -> None:
    print_section("2) Relações também viram vetores")
    left_relation = model[left_a] - model[left_b]
    right_relation = model[right_a] - model[right_b]
    similarity = cosine_similarity(left_relation, right_relation)

    print(f"Relação 1: {left_a} - {left_b}")
    print(f"Relação 2: {right_a} - {right_b}\n")
    print(f"cos({left_a} - {left_b}, {right_a} - {right_b}) = {similarity:.4f}")
    print("Quanto mais perto de 1, mais parecida é a direção dessas duas relações.\n")


def format_analogy(positive: Sequence[str], negative: Sequence[str]) -> str:
    pieces = []
    for word in positive:
        pieces.append(word)
    for word in negative:
        pieces.append(f"- {word}")
    return " + ".join(pieces).replace("+ - ", "- ")


def run_analogy(
    model,
    *,
    positive: Sequence[str],
    negative: Sequence[str],
    expected: str | None = None,
    topn: int = 5,
) -> None:
    query = format_analogy(positive, negative)
    results = model.most_similar(positive=list(positive), negative=list(negative), topn=topn)

    print(f"Conta vetorial: {query}")
    if expected:
        print(f"Palavra esperada: {expected}")
    print("Resultado do modelo:")
    for index, (word, score) in enumerate(results, start=1):
        marker = "  <==" if expected and word == expected else ""
        print(f"{index:>2}. {word:<12} similaridade={score:.4f}{marker}")
    print()


def main() -> None:
    args = parse_args()
    model = load_model(args.model)
    require_words(model, DEMO_WORDS, args.model)

    print_section("Modelo carregado")
    print(f"Vocabulário aproximado: {len(model):,} palavras")
    print(f"Dimensão dos vetores: {model.vector_size}\n")

    print_embedding_preview(model, ("father", "mother", "uncle", "aunt"))
    compare_relations(model, "father", "mother", "uncle", "aunt")

    print_section("3) Fazendo contas com embeddings")
    run_analogy(
        model,
        positive=("father", "aunt"),
        negative=("mother",),
        expected="uncle",
        topn=args.topn,
    )
    run_analogy(
        model,
        positive=("king", "woman"),
        negative=("man",),
        expected="queen",
        topn=args.topn,
    )

    print_section("Leitura para o público")
    print("O modelo nunca recebeu uma regra escrita como 'tio = pai + tia - mãe'.")
    print("Mesmo assim, a geometria do espaço vetorial captura esse padrão.")
    print("É isso que torna embeddings tão úteis em busca, recomendação e IA generativa.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nExecução interrompida pelo usuário.")
