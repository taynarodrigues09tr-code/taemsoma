# Identidade de Sophia e Matheus

As fichas são a fonte permanente de identidade para todas as cenas futuras. Não há integração com Higgsfield nesta etapa.

## Onde guardar cada informação

- `personagens/sophia.json` e `personagens/matheus.json`: identidade, personalidade, aparência e relação entre os irmãos.
- `identidade/regras_consistencia.json`: conceito do canal, estilo compartilhado e regras de continuidade.
- `referencias/personagens/sophia/` e `referencias/personagens/matheus/`: imagens de referência aprovadas, quando existirem. As pastas estão vazias por enquanto.

## O que já está definido

Sophia tem 9 anos, pele parda, olhos castanhos grandes e expressivos e cabelo castanho-escuro curto e cacheado, com cachos bem definidos. É curiosa, observadora, criativa, inteligente e determinada; ama desenhar e atividades artísticas. Matheus tem 4 anos, pele clara, olhos castanhos e cabelo loiro curto e liso. É energético, espontâneo, engraçado, aventureiro e muito curioso. Sophia é a irmã mais velha e claramente mais alta; Matheus é o irmão menor. São irmãos e protagonistas de aventuras educativas baseadas em descobertas do cotidiano.

O conceito é **aprender brincando**. O visual será animação 3D estilizada, moderna, colorida, expressiva e com identidade própria. Os gestos nas fichas são orientações iniciais de atuação, não decisões sobre a aparência.

## Como completar uma ficha

1. Consulte `ficha_visual.definido`: são os atributos já estabelecidos e que devem permanecer entre cenas.
2. Escolha os valores de `ficha_visual.pendente` com calma, incluindo o modelo visual final, a paleta exata, os calçados e acessórios. As características oficiais já estão em `definido`; não devem ser substituídas por decisões de cena.
3. Ao decidir um campo, retire seu nome de `pendente` e registre o mesmo nome com seu valor em `decisoes_aprovadas`. Exemplo de formato: `"roupa_base": "descrição da roupa escolhida"`.
4. Guarde imagens aprovadas na pasta do personagem e registre seus caminhos relativos em `referencias_aprovadas`. Exemplo de caminho: `referencias/personagens/sophia/frente.png`. Não registre arquivos que ainda não existem.
5. Quando não houver pendências e as referências estiverem aprovadas, altere `status_visual` de `em_definicao` para `aprovado`. A aprovação é uma decisão humana; o programa só confere os registros.
6. Em mudanças permanentes posteriores, aumente `versao`, revise as referências e mantenha o histórico no Git.

Uma futura cena deverá usar a ficha completa e as regras compartilhadas. Pode variar expressão, pose, ação, cenário, iluminação e enquadramento. Trajes temáticos devem ser registrados para aquela cena e não alteram a roupa base. Se uma imagem contradisser a ficha, revise a imagem antes de usá-la como referência.

## Como conferir

Na pasta do projeto, execute:

```bash
python3 ferramentas/verificar_projeto.py
python3 -m unittest discover -s testes -v
```

O verificador detecta conflitos de decisões, relações incorretas entre os irmãos, estilo incompatível, referências ausentes e aprovação incompleta. Ele permite fichas em definição para continuarmos o planejamento. Não compara imagens, não gera cenas e não garante consistência visual automaticamente.

O próximo passo é receber fotografias, desenvolver os modelos 3D e revisar as referências visuais, incluindo uma vista conjunta para fixar a diferença de escala.

## Roupas como assinatura visual

Sophia usa macacão moderno de pequena artista, com bolsos para materiais e detalhes gráficos sutis, sem excesso de cores. Matheus usa macacão infantil moderno com dinossauro gráfico, sem virar fantasia. Essas diretrizes são oficiais e permanentes.

`proposta_de_design` descreve uma primeira opção de cores e acabamento: azul-petróleo e creme para Sophia; verde-sálvia e creme para Matheus. São propostas, não referências aprovadas. As fichas continuam com `status_visual: em_definicao` até a aprovação do modelo final. Uma roupa temporária deve ser justificada pelo episódio e nunca muda idade, pele, olhos, cabelo ou proporções físicas.

## Como receber fotografias oficiais

Guarde as fotos nos diretórios locais:

- `referencias/fotografias/sophia/`
- `referencias/fotografias/matheus/`

Use nomes simples como `frente.jpg`, `perfil.jpg` e `corpo_inteiro.jpg`. Estas pastas têm arquivos marcadores `.gitkeep` para existir no GitHub; as fotografias ficam ignoradas pelo Git e não serão enviadas automaticamente. Ainda não recebemos fotografias.

Registre cada foto em `ficha_visual.referencias_fotograficas` na ficha correspondente, apenas depois de o arquivo existir. Exemplo para Sophia:

```json
[
  {
    "arquivo": "referencias/fotografias/sophia/frente.jpg",
    "descricao": "Fotografia oficial de referência, vista de frente."
  }
]
```

Os caminhos são relativos à pasta do projeto. Fotografias ajudam a desenvolver o personagem, mas não aprovam automaticamente a versão 3D. As imagens 3D aprovadas continuam nas pastas `referencias/personagens/` e na lista `referencias_aprovadas`. Revise qualquer divergência com a ficha; não substitua os traços oficiais automaticamente. O verificador confere caminhos e existência, não o conteúdo ou formato das imagens.
