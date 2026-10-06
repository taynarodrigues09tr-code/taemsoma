"""Confere a estrutura dos personagens e roteiros, sem serviços externos."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def ler_objeto(caminho):
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    if not isinstance(dados, dict):
        raise ValueError(f"{caminho.name}: o conteúdo deve ser um objeto JSON.")
    return dados


def texto(dados, campo):
    valor = dados.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"Campo obrigatório ausente ou vazio: {campo}.")
    return valor


def verificar():
    personagens = list((RAIZ / "personagens").glob("*.json"))
    roteiros = list((RAIZ / "roteiros").glob("*.json"))
    if not personagens or not roteiros:
        raise ValueError("É necessário pelo menos um personagem e um roteiro.")
    nomes = set()
    for caminho in personagens:
        dados = ler_objeto(caminho)
        nome = texto(dados, "nome")
        if nome in nomes:
            raise ValueError(f"Personagem duplicado: {nome}.")
        nomes.add(nome)
        texto(dados, "personalidade")
        texto(dados, "aparencia")
    for caminho in roteiros:
        dados = ler_objeto(caminho)
        texto(dados, "titulo")
        texto(dados, "status")
        texto(dados, "objetivo")
        elenco = dados.get("personagens")
        if not isinstance(elenco, list) or not elenco:
            raise ValueError(f"{caminho.name}: informe os personagens.")
        if any(not isinstance(nome, str) or nome not in nomes for nome in elenco):
            raise ValueError(f"{caminho.name}: personagem sem descrição cadastrada.")
        cenas = dados.get("cenas")
        if not isinstance(cenas, list) or not cenas:
            raise ValueError(f"{caminho.name}: informe pelo menos uma cena.")
        for numero, cena in enumerate(cenas, start=1):
            if not isinstance(cena, dict) or type(cena.get("numero")) is not int or cena["numero"] != numero:
                raise ValueError(f"{caminho.name}: numere as cenas em sequência a partir de 1.")
            texto(cena, "descricao")
            texto(cena, "narracao")
    print(f"Projeto inicial válido: {len(personagens)} personagens e {len(roteiros)} roteiro.")


if __name__ == "__main__":
    try:
        verificar()
    except (OSError, ValueError) as erro:
        raise SystemExit(f"Erro na verificação: {erro}") from None
