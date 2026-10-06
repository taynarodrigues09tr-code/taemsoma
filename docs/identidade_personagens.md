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

## Referências oficiais recebidas

As pranchas de Sophia e Matheus foram recebidas em `referencias_oficiais_sophia_matheus.zip` e extraídas sem modificar os PNGs:

- `referencias/personagens/sophia/prancha_oficial.png`
- `referencias/personagens/matheus/prancha_oficial.png`

Ambas as fichas estão com `status_visual: aprovado`. Cada prancha está em `referencias_aprovadas` e no registro `referencia_principal`, com caminho, origem e SHA-256. O verificador detecta mudanças nos bytes dos arquivos; uma substituição futura exige revisão deliberada da ficha e do hash.

Sophia usa macacão roxo com estampas artísticas, camiseta rosa-clara, laços rosa e tênis rosa. Sua prancha substitui a proposta azul-petróleo e a orientação anterior de cores discretas. Matheus usa macacão curto verde com dinossauro no peito e pegadas, camiseta creme com pequenos dinossauros e tênis azuis. As propostas anteriores de figurino foram substituídas pelos visuais oficiais.

O cabelo de Matheus tem mechas levemente onduladas na prancha; use essa forma como referência, mantendo o cabelo curto de base lisa e sem cachos definidos. As idades oficiais continuam 9 e 4 anos. Sophia deve ser claramente mais alta; as pranchas isoladas não definem uma escala numérica conjunta.

Não inclua títulos, legendas, quadros ou decoração do layout nas futuras cenas. O programa confere integridade e registros, mas não avalia automaticamente a consistência das imagens geradas.

## Fotografias pessoais futuras

Estas pranchas são desenhos 3D oficiais, não fotografias. Caso fotografias sejam fornecidas depois, guarde-as em `referencias/fotografias/sophia/` ou `referencias/fotografias/matheus/`. Essas pastas continuam ignoradas pelo Git, exceto pelos marcadores `.gitkeep`.

Registre fotografias em `ficha_visual.referencias_fotograficas` somente após o arquivo existir, usando um objeto com `arquivo` (caminho relativo ao projeto) e `descricao`. Elas são insumos de desenvolvimento e não substituem automaticamente as pranchas oficiais.
