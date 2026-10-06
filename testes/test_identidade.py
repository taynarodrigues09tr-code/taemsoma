"""Testa falhas de consistência em cópias temporárias do projeto."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from ferramentas import verificar_projeto as verificador


class IdentidadeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        for pasta in ("personagens", "roteiros", "identidade", "referencias"):
            shutil.copytree(verificador.RAIZ / pasta, self.raiz / pasta)
        alteracao = patch.object(verificador, "RAIZ", self.raiz)
        alteracao.start()
        self.addCleanup(alteracao.stop)

    def alterar_sophia(self, alterar):
        caminho = self.raiz / "personagens/sophia.json"
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        alterar(dados)
        caminho.write_text(json.dumps(dados), encoding="utf-8")

    def test_fichas_oficiais_validas(self):
        with contextlib.redirect_stdout(io.StringIO()):
            verificador.verificar()

    def test_decisao_pendente_e_aprovada(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["pendente"].append("arquivo_referencia_principal"))
        self.alterar_sophia(lambda d: d["ficha_visual"]["decisoes_aprovadas"].update(arquivo_referencia_principal="Arquivo"))
        with self.assertRaisesRegex(ValueError, "pendente e aprovada"):
            verificador.verificar()

    def test_aprovacao_incompleta(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["decisoes_aprovadas"].pop("modelo_visual_final"))
        self.alterar_sophia(lambda d: d["ficha_visual"]["pendente"].append("modelo_visual_final"))
        with self.assertRaisesRegex(ValueError, "aprovação exige"):
            verificador.verificar()

    def test_referencia_inexistente(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["referencias_aprovadas"].append("referencias/personagens/sophia/ausente.png"))
        with self.assertRaisesRegex(ValueError, "referência inexistente"):
            verificador.verificar()

    def test_estilo_incompativel(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["definido"].update(estilo="outro"))
        with self.assertRaisesRegex(ValueError, "estilo incompatível"):
            verificador.verificar()

    def test_irmao_inexistente(self):
        self.alterar_sophia(lambda d: d["relacao"].update(irmao_id="desconhecido"))
        with self.assertRaisesRegex(ValueError, "relação entre irmãos inválida"):
            verificador.verificar()

    def test_idade_oficial_alterada(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["definido"].update(idade_anos=4))
        with self.assertRaisesRegex(ValueError, "características físicas oficiais alteradas"):
            verificador.verificar()

    def test_altura_invertida(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["definido"].update(altura_relativa="claramente_mais_baixo"))
        with self.assertRaisesRegex(ValueError, "características físicas oficiais alteradas"):
            verificador.verificar()

    def test_fotografia_fora_da_pasta(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["referencias_fotograficas"].append({"arquivo": "README.md", "descricao": "Frente"}))
        with self.assertRaisesRegex(ValueError, "fotografia inexistente ou fora"):
            verificador.verificar()

    def test_fotografia_local_valida(self):
        caminho = self.raiz / "referencias/fotografias/sophia/frente.jpg"
        caminho.write_bytes(b"arquivo de teste, sem avaliacao visual")
        self.alterar_sophia(lambda d: d["ficha_visual"]["referencias_fotograficas"].append({"arquivo": "referencias/fotografias/sophia/frente.jpg", "descricao": "Frente"}))
        with contextlib.redirect_stdout(io.StringIO()):
            verificador.verificar()

    def test_imagem_oficial_modificada(self):
        caminho = self.raiz / "referencias/personagens/sophia/prancha_oficial.png"
        caminho.write_bytes(caminho.read_bytes() + b"alteracao")
        with self.assertRaisesRegex(ValueError, "integridade da referência principal inválida"):
            verificador.verificar()

    def test_principal_nao_registrada(self):
        self.alterar_sophia(lambda d: d["ficha_visual"]["referencia_principal"].update(arquivo="ausente.png"))
        with self.assertRaisesRegex(ValueError, "referência principal não está disponível ou registrada"):
            verificador.verificar()
