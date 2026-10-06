"""Confere a estrutura dos personagens e roteiros, sem serviços externos."""
import json
import hashlib
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
    regras = ler_objeto(RAIZ / "identidade/regras_consistencia.json")
    if regras.get("versao") != 2:
        raise ValueError("Versão de regras de consistência não suportada.")
    estilo = texto(regras.get("estilo", {}), "id")
    personagens = list((RAIZ / "personagens").glob("*.json"))
    roteiros = list((RAIZ / "roteiros").glob("*.json"))
    if not personagens or not roteiros:
        raise ValueError("É necessário pelo menos um personagem e um roteiro.")
    nomes = set()
    fichas = {}
    for caminho in personagens:
        dados = ler_objeto(caminho)
        nome = texto(dados, "nome")
        if nome in nomes:
            raise ValueError(f"Personagem duplicado: {nome}.")
        nomes.add(nome)
        texto(dados, "personalidade")
        texto(dados, "aparencia")
        ident = texto(dados, "id")
        if ident in fichas:
            raise ValueError(f"Identificador duplicado: {ident}.")
        fichas[ident] = dados
        if type(dados.get("versao")) is not int or dados["versao"] < 1:
            raise ValueError(f"{nome}: versão inválida.")
        ficha = dados.get("ficha_visual")
        if not isinstance(ficha, dict) or not isinstance(ficha.get("definido"), dict):
            raise ValueError(f"{nome}: ficha visual inválida.")
        if ficha["definido"].get("estilo") != estilo:
            raise ValueError(f"{nome}: estilo incompatível com o canal.")
        pendentes = ficha.get("pendente")
        aprovadas = ficha.get("decisoes_aprovadas")
        if not isinstance(pendentes, list) or any(not isinstance(p, str) or not p.strip() for p in pendentes):
            raise ValueError(f"{nome}: campos pendentes inválidos.")
        if not isinstance(aprovadas, dict) or any(not isinstance(v, str) or not v.strip() for v in aprovadas.values()):
            raise ValueError(f"{nome}: decisões aprovadas inválidas.")
        if set(pendentes) & set(aprovadas):
            raise ValueError(f"{nome}: uma decisão não pode estar pendente e aprovada.")
        referencias = ficha.get("referencias_aprovadas")
        if not isinstance(referencias, list):
            raise ValueError(f"{nome}: referências inválidas.")
        pasta = (RAIZ / "referencias/personagens" / ident).resolve()
        for referencia in referencias:
            if not isinstance(referencia, str):
                raise ValueError(f"{nome}: referência deve ser um caminho.")
            arquivo = (RAIZ / referencia).resolve()
            if not arquivo.is_relative_to(pasta) or not arquivo.is_file():
                raise ValueError(f"{nome}: referência inexistente ou fora da pasta do personagem.")
        status = dados.get("status_visual")
        if status not in {"em_definicao", "aprovado"}:
            raise ValueError(f"{nome}: status visual inválido.")
        if status == "aprovado" and (pendentes or not referencias):
            raise ValueError(f"{nome}: aprovação exige decisões completas e referências.")
        principal = ficha.get("referencia_principal", {})
        if status == "aprovado":
            if principal.get("status_arquivo") != "disponivel" or principal.get("arquivo") not in referencias:
                raise ValueError(f"{nome}: referência principal não está disponível ou registrada.")
            original = (RAIZ / principal["arquivo"]).read_bytes()
            if not original.startswith(b"\x89PNG\r\n\x1a\n") or hashlib.sha256(original).hexdigest() != principal.get("sha256"):
                raise ValueError(f"{nome}: integridade da referência principal inválida.")
        fotos = ficha.get("referencias_fotograficas")
        if not isinstance(fotos, list):
            raise ValueError(f"{nome}: lista de fotografias inválida.")
        pasta_fotos = (RAIZ / "referencias/fotografias" / ident).resolve()
        if ficha.get("pasta_fotografias") != f"referencias/fotografias/{ident}":
            raise ValueError(f"{nome}: pasta de fotografias inválida.")
        for foto in fotos:
            if not isinstance(foto, dict):
                raise ValueError(f"{nome}: registro de fotografia inválido.")
            arquivo = (RAIZ / texto(foto, "arquivo")).resolve()
            texto(foto, "descricao")
            if not arquivo.is_relative_to(pasta_fotos) or not arquivo.is_file():
                raise ValueError(f"{nome}: fotografia inexistente ou fora da pasta do personagem.")
    oficial = {
        "sophia": (9, "parda", "castanho-escuro", "cacheado", "claramente_mais_alta"),
        "matheus": (4, "clara", "loiro", "liso", "claramente_mais_baixo"),
    }
    if set(fichas) != set(oficial):
        raise ValueError("Os protagonistas oficiais devem ser Sophia e Matheus.")
    for ident, (idade, pele, cor, textura, altura) in oficial.items():
        definido = fichas[ident]["ficha_visual"]["definido"]
        cabelo = definido.get("cabelo", {})
        if (type(definido.get("idade_anos")) is not int
                or definido.get("idade_anos") != idade
                or definido.get("tom_de_pele") != pele
                or definido.get("olhos", {}).get("cor") != "castanhos"
                or cabelo.get("cor") != cor or cabelo.get("textura") != textura
                or cabelo.get("comprimento") != "curto"
                or definido.get("altura_relativa") != altura):
            raise ValueError(f"{ident}: características físicas oficiais alteradas.")
        texto(definido, "proporcoes_gerais")
        roupa = definido.get("roupa_principal", {})
        if roupa.get("tipo") != "macacao":
            raise ValueError(f"{ident}: a roupa principal deve ser um macacão.")
        texto(roupa, "diretriz")
        texto(roupa, "assinatura")
    relacao_visual = regras.get("relacao_visual", {})
    if relacao_visual.get("mais_velha") != "sophia" or relacao_visual.get("menor") != "matheus":
        raise ValueError("Relação visual oficial entre irmãos inválida.")
    for ident, dados in fichas.items():
        relacao = dados.get("relacao", {})
        irmao = relacao.get("irmao_id")
        if relacao.get("tipo") != "irmaos" or irmao == ident or irmao not in fichas:
            raise ValueError(f"{ident}: relação entre irmãos inválida.")
        if fichas[irmao].get("relacao", {}).get("irmao_id") != ident:
            raise ValueError(f"{ident}: relação entre irmãos deve ser recíproca.")
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
