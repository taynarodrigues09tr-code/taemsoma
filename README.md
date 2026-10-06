# Taemsoma — histórias de Sophia e Matheus

Projeto para criar vídeos animados infantis para YouTube, com cenas geradas no Higgsfield.

Esta primeira versão organiza o trabalho. Ainda não gera vídeos, não acessa o Higgsfield e não publica no YouTube.

## Como o projeto está organizado

- `personagens/`: descrição dos personagens para manter sua aparência e personalidade consistentes.
- `roteiros/`: histórias divididas em cenas. O exemplo inicial é uma sugestão editável.
- `docs/`: orientações para as próximas etapas.
- `videos/`: lugar para guardar vídeos localmente; esses arquivos não são enviados ao GitHub.
- `ferramentas/`: ferramentas simples para conferir os arquivos do projeto.

## Configuração básica

Usamos Python 3.12 ou superior. Neste início, não é necessário instalar bibliotecas, criar contas adicionais ou fornecer chaves de acesso.

No ambiente na nuvem, abra o terminal e execute:

```bash
cd /workspace/taemsoma
python3 ferramentas/verificar_projeto.py
```

O resultado esperado é `Projeto inicial válido: 2 personagens e 1 roteiro.` Isso verifica os arquivos de planejamento, não a geração de vídeos.

## Por onde começar

1. Leia `personagens/sophia.json` e `personagens/matheus.json`. As descrições são sugestões; podemos adaptá-las às suas ideias.
2. Leia `roteiros/primeira_historia.json` para ver como dividimos uma história em cenas.
3. Consulte `docs/proximos_passos.md`. Vamos fazer uma pequena etapa de cada vez.

## O que é o GitHub?

O GitHub guarda os arquivos e o histórico do projeto. Um **commit** é um registro de alterações; um **push** envia esses registros para o GitHub. Os arquivos preparados no ambiente só aparecem no site depois desse envio.

Não coloque senhas ou chaves de acesso nos arquivos. Se precisarmos de uma integração, configuraremos as credenciais nas configurações seguras do ambiente.
