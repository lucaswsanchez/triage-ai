"""Retrieval over the KB. BM25 today, behind an interface so embeddings can replace it later."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Protocol

from rank_bm25 import BM25Okapi

from app.kb import Article, Chunk

_TOKEN = re.compile(r"[a-z0-9]+(?:[-'][a-z0-9]+)*")

STOPWORDS = frozenset(
    """
    a an and are as at be been but by can could do does for from has have hi hello how i i'm
    if in is it its me my no not of on or our please so that the their them then there this
    to was we were what when where which who why will with would you your thanks thank since
    am any all also just get got still now today one some
    el la los las un una unos unas y o de del al en con por para que se no mi mis me lo le
    les es son esta este estoy hola gracias favor como cuando donde porque pero ya muy hay
    """.split()
)

# Small Spanish -> English IT glossary. The KB is written in English, so without it
# BM25 cannot match Spanish tickets. Its effect is measured in the evaluation.
GLOSSARY: dict[str, str] = {
    "contrasena": "password",
    "clave": "password",
    "bloqueada": "locked",
    "bloqueado": "locked",
    "bloqueo": "locked",
    "cuenta": "account",
    "usuario": "user account",
    "correo": "email outlook",
    "correos": "email outlook",
    "mail": "email",
    "mails": "email",
    "buzon": "mailbox",
    "compartido": "shared",
    "compartida": "shared",
    "carpeta": "folder",
    "permisos": "permissions access",
    "permiso": "permissions access",
    "acceso": "access",
    "impresora": "printer",
    "imprimir": "print printer",
    "imprime": "print printer",
    "lenta": "slow",
    "lento": "slow",
    "computadora": "computer laptop",
    "pc": "computer",
    "notebook": "laptop",
    "pantalla": "monitor screen",
    "camara": "camera",
    "microfono": "microphone audio",
    "sonido": "audio sound",
    "escuchan": "audio hear",
    "reunion": "meeting teams",
    "red": "network",
    "conecta": "connect",
    "conectar": "connect",
    "conexion": "connection",
    "unidad": "drive",
    "instalar": "install software",
    "programa": "software",
    "actualizacion": "update windows",
    "actualizaciones": "update windows",
    "robada": "stolen",
    "robado": "stolen",
    "robaron": "stolen",
    "perdi": "lost",
    "perdida": "lost",
    "perdido": "lost",
    "sospechoso": "suspicious phishing",
    "enlace": "link",
    "ingreso": "onboarding new hire",
    "ingresa": "onboarding new hire",
    "nuevo": "new",
    "nuevos": "new",
    "empleado": "employee",
    "empleados": "employees",
    "baja": "offboarding leaver",
    "renuncia": "offboarding leaver",
    "sincroniza": "sync",
    "sincronizar": "sync",
    "recuperacion": "recovery",
    "autenticacion": "authentication mfa",
    "codigo": "code",
    "celular": "phone",
    "telefono": "phone",
}


def _fold(text: str) -> str:
    """Lowercase and strip accents so 'contraseña' and 'contrasena' match."""
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in normalized if not unicodedata.combining(c))


def _stem(token: str) -> str:
    """Very light English stemming: enough to match 'printers'/'printer', 'syncing'/'sync'."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in _TOKEN.findall(_fold(text)):
        if raw in STOPWORDS:
            continue
        expansion = GLOSSARY.get(raw)
        words = expansion.split() if expansion else [raw]
        tokens.extend(_stem(w) for w in words)
    return tokens


@dataclass(frozen=True)
class RetrievedArticle:
    article: Article
    score: float
    best_section: str
    snippet: str


class Retriever(Protocol):
    def search(self, query: str, top_k: int = 3) -> list[RetrievedArticle]: ...


class BM25Retriever:
    """BM25 over section-level chunks; scores are aggregated per article (max chunk score)."""

    def __init__(self, articles: list[Article]) -> None:
        self._articles = {a.id: a for a in articles}
        self._chunks: list[Chunk] = []
        corpus: list[list[str]] = []
        for article in articles:
            header = f"{article.title} {' '.join(article.tags)} {article.category}"
            for chunk in article.chunks:
                self._chunks.append(chunk)
                # Title and tags are repeated in every chunk so each section keeps its context.
                corpus.append(tokenize(f"{header} {header} {chunk.section} {chunk.text}"))
        self._bm25 = BM25Okapi(corpus)

    @property
    def articles(self) -> dict[str, Article]:
        return self._articles

    def search(self, query: str, top_k: int = 3) -> list[RetrievedArticle]:
        tokens = tokenize(query)
        if not tokens:
            return []
        scores = self._bm25.get_scores(tokens)
        best: dict[str, tuple[float, Chunk]] = {}
        for chunk, score in zip(self._chunks, scores, strict=True):
            current = best.get(chunk.article_id)
            if current is None or score > current[0]:
                best[chunk.article_id] = (float(score), chunk)
        ranked = sorted(best.items(), key=lambda kv: kv[1][0], reverse=True)
        results: list[RetrievedArticle] = []
        for article_id, (score, chunk) in ranked[:top_k]:
            if score <= 0:
                break
            results.append(
                RetrievedArticle(
                    article=self._articles[article_id],
                    score=round(score, 3),
                    best_section=chunk.section,
                    snippet=chunk.text[:600],
                )
            )
        return results
