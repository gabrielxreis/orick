# Canva: arte montada DENTRO do Canva, camada por camada (conector MCP)

Regra do Gabriel (31/10/2026): no motor Canva, tudo é feito no Canva. Nada de PowerPoint, PPTX ou PDF intermediário.
Sem o app do Canva na máquina: perguntar e instalar (`python3 SKILL_DIR/scripts/detectar_apps.py instalar_canva`:
Homebrew no Mac, winget no Windows, ou a página oficial). Sem o conector do Canva no Claude: pedir para autorizar
(`/mcp` ou Conectores do app); sem ele não há como montar.

Referência técnica completa (ferramentas, operações, estrutura dos elementos, app desktop): `docs/canva_api.md`.

## Fluxo PRINCIPAL (31/10/2026, Gabriel: montado peça por peça no Canva "fica feio"): ChatGPT faz, Canva edita

1. **Foto da pessoa no Gemini (Nano Banana)**, com a ficha e as fotos reais de referência (o ChatGPT erra o rosto).
   Padrão; o usuário pode escolher outro gerador.
2. **Arte inteira no ChatGPT** com essa foto anexada + referências aprovadas + briefing (`docs/carrossel.md`,
   `docs/manual_criativo.md`): é onde sai bonita. Uma página por mensagem; conferir acento e rosto.
3. **Canva deixa editável:** subir o PNG (`create-upload-url` + POST cru -> `mediaId`) > `separate-image-layers`
   (Magic Layers) > `get-separate-image-layers-job` até `completed` > `read-design`. Testado na capa do carrossel
   de suporte e resistência do X-Trader: os 8 textos viraram texto editável já na fonte condensada certa, botões e
   blocos viraram elementos, o fundo ficou limpo; `replace_text` troca a palavra mantendo fonte, cor e lugar.
4. Conferir lado a lado (miniatura do Canva x PNG do ChatGPT). Perde: degradê e brilho dentro do texto (vira cor
   chapada). Tamanho sai o do PNG (ex.: 1122x1402): `resize-design` para 1080x1350 se precisar.
5. Carrossel: uma página por vez no Magic Layers e `merge-designs` na ordem. Salvar edição só com o ok do usuário.

O caminho "kit de fontes + montar camada por camada" (abaixo) fica para quando não houver arte do ChatGPT
(ex.: template de série com texto trocado em lote).

## Por que assim

- O conector cria e edita elementos (texto, forma, imagem, página), mas **não escolhe a família da fonte**: texto
  novo nasce na fonte padrão do Canva. **Trocar o texto de um elemento existente mantém a fonte dele.**
- Por isso cada marca tem um **kit de fontes no Canva**: um design com caixas de texto já na fonte certa, uma por estilo.
- Arquivo local não vira design (PPTX é recusado, PDF fica só em Uploads); imagem sobe e vira camada.

## Kit de fontes da marca (uma vez por marca)

Design "Rick Kit - <Marca>", no tamanho da peça (1080x1350), na pasta "Rick" do Canva, com caixas de texto nomeadas
pelo estilo e já na fonte da marca: 3x `titulo`, 2x `subtitulo`, 3x `corpo`, 2x `destaque`, 1x `botao`, 1x `rodape`
(sobra caixa: o Rick apaga as que não usar). Fontes da marca vêm do `design-<marca>.md`.
Como criar: o Rick cria com `add_text` (texto = nome do estilo) e o usuário escolhe a fonte de cada caixa no app do
Canva (ou o Rick faz pela tela do app, com permissão de computer use: clicar no texto > seletor de fonte > digitar
o nome > Enter). Conferir com `read-design`: cada caixa com o `fontRef` da fonte certa. Guardar o `design_id` do kit
e o mapa das caixas no `design-<marca>.md` (seção "Canva").
Conta Pro com Kit de Marca e modelo de marca: dá para usar `create-design-from-brand-template` + `autofill-design`.

## Montar uma peça

1. **Planejar igual ao motor IA** (`docs/carrossel.md`, `docs/manual_criativo.md`). A IA gera **só a imagem, sem
   nenhum texto** (fundo, cena, objeto, pessoa); prompt com "no text, no letters, no typography, leave clean space".
2. **Plano** `plano.json` (camadas de baixo para cima; formato em `scripts/canva/canva_ops.py`): imagem (`fundo: true`
   para o fundo da página), forma (retangulo, arredondado, elipse; cor, opacidade, raio, borda), texto com `estilo`
   (a caixa do kit), tamanho, cor, negrito, alinhar, entrelinha. Palavra em outra cor = texto separado.
3. **Subir as imagens:** para cada arquivo, `create-upload-url` e `curl -X POST -H "Content-Type: application/octet-stream"
   --data-binary @arquivo "<url>"` -> `mediaId`. Guardar em `midias.json`.
4. **Base:** `copy-design` do kit da marca (uma cópia por página do carrossel); `read-design` com
   `open_transaction: true` e `design_content` -> `page_id` e os `locator_id` das caixas -> `kit.json`.
5. **Operações:** `python3 SKILL_DIR/scripts/canva/canva_ops.py plano.json --kit kit.json --midias midias.json --pagina N`
   e aplicar com `edit-design` (`finalize: keep_open`), em lotes de até ~20 operações. Olhar a miniatura que volta a
   cada chamada (texto cortado, acento encostando, margem 80-90 px, zona segura). Ajustar com `position_element`,
   `resize_element`, `format_text`.
6. **Mostrar e só então salvar:** mostrar a miniatura ao usuário; `commit` só com o ok dele (regra do conector).
7. **Carrossel:** `merge-designs` das páginas na ordem. **Entregar:** link do design + `export-design` (PNG); folha
   com `carrossel_entrega.py` nos PNGs.

## Armadilhas (testadas)

- `create-design` NÃO faz base em branco (gera um post pronto) e "Instagram Post (Portrait)" sai 1080x1440: usar o kit.
- `update_fill` no `locator_id` da PÁGINA troca o fundo e cobre a página sozinho (corta o excesso).
- `format_text` formata o elemento inteiro; `add_text` sem `width` não quebra linha; texto: `resize_element` só width.
- Fonte padrão do `add_text` (`fontRef YACgEZ1cb1Q`) é mais larga que fontes condensadas: título quebra em 2 linhas.
- Transação fica velha se o usuário mexer no mesmo design no app/navegador: `cancel` e refazer.
- Nunca subir arquivo para hospedagem pública só para o `import-design-from-url` (a ferramenta proíbe).
