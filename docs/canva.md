# Canva pelo conector (MCP): arte em camadas, texto editável

O Canva não tem app local nem script para controlar. O caminho oficial é o **conector do Canva** no Claude (MCP
`mcp.canva.com`, 46 ferramentas). Ele não tem "criar caixa de texto": o jeito de montar uma arte em camadas é
**importar um arquivo** que o Canva converte em design editável. O Rick monta esse arquivo como PPTX no tamanho exato
da peça, com cada elemento numa camada.

## O fluxo (mesma arte que sairia no ChatGPT, só que separada)

1. **Planejar igual ao motor IA** (`docs/carrossel.md`, `docs/manual_criativo.md`): textos, hierarquia, cores da
   marca, metáfora em foto. A diferença: a IA gera **só a imagem, sem nenhum texto** (fundo, cena, objeto, pessoa).
   Prompt: o mesmo do manual + "no text, no letters, no typography, leave clean space at <área do título>".
2. **Plano JSON** (`plano.json` na pasta da arte; formato completo no cabeçalho de `scripts/canva/montar_pptx.py`):
   camadas de baixo para cima: imagem de fundo, escurecimento/forma, foto recortada, logo, títulos, corpo, botão.
   Texto com fonte que exista no Canva (Anton, Montserrat, Inter, Bebas Neue, League Gothic, Poppins, DM Sans...);
   fonte própria da marca só se ela estiver no Kit de Marca do usuário (senão o Canva troca por outra: avisar).
3. **Montar:** `SKILL_DIR/.venv/bin/python SKILL_DIR/scripts/canva/montar_pptx.py plano.json` gera o PPTX
   (avisa acento/cedilha em caixa alta com entrelinha apertada).
4. **Conferir:** `SKILL_DIR/.venv/bin/python SKILL_DIR/scripts/canva/previa_pptx.py arte.pptx` gera `arte_p01.png`...
   e a folha do carrossel. Olhar cada página (texto cortado, acento encostando, margem 80-90 px, zona segura).
5. **Mandar ao Canva** (o conector só importa de link HTTPS público):
   - Com `gws`: `python3 SKILL_DIR/scripts/canva/link_temporario.py abrir arte.pptx` (Drive do usuário, link aberto)
     > ferramenta `import-design-from-url` do conector com a URL e o título > assim que importar,
     `link_temporario.py fechar <file_id>`. **Perguntar ao usuário antes de abrir o link** (o arquivo fica público
     enquanto o Canva baixa) e nunca deixar aberto.
   - Sem `gws` ou sem o ok: o usuário arrasta o PPTX no Canva (Criar design > Importar arquivo). Mesmo resultado.
6. **Ajustar dentro do Canva pelo conector:** `start-editing-transaction` (devolve os `element_id`) >
   `perform-editing-operations` (trocar texto, trocar imagem com `update_fill`/`insert_fill` usando o `asset_id` do
   `upload-asset-from-url`) > `commit-editing-transaction`. Sem commit nada fica salvo.
7. **Entregar:** link do design (`get-design`) e PNG (`export-design`). Carrossel: `carrossel_entrega.py` nos PNGs.

## O que se sabe do conector (pesquisa de 30/10/2026; conferir com o `tools/list` real ao autorizar)

- Criar/importar: `import-design-from-url` (PPTX, PDF, PSD, AI, Keynote; 20/min), `create-design`, `generate-design`
  (gera por IA, sem controle de camada), `create-design-from-candidate`, `copy-design`, `merge-designs`.
- Editar: `start-editing-transaction` (20/min), `perform-editing-operations` (50/min), `commit-` e
  `cancel-editing-transaction`. Operações confirmadas na documentação: `update_fill` e `insert_fill`. Troca de texto
  existe pelos relatos, mas o esquema exato só aparece com o conector autorizado: registrar aqui quando conferir.
- Imagem: `upload-asset-from-url` (30/min), `create-upload-url`, `remove-background`, `separate-image-layers`
  (Magic Layers: imagem chapada vira camadas), `generate-image`.
- Marca (Pro+): `list-brand-kits`, `search-brand-templates`, `create-design-from-brand-template`, `autofill-design`.
- Saída: `export-design` (20/min), `get-design-thumbnail`, `resize-design` (Pro+).
- Limite geral: 300 chamadas/min por usuário. Transação fica velha se alguém editar no navegador ao mesmo tempo:
  cancelar, começar outra e refazer.

## Armadilhas

- PPTX importado: fonte que o Canva não tem é trocada (muda a largura); sombra e degradê em forma podem sumir; por
  isso efeito pesado vai na IMAGEM (gerada ou preparada antes) e o texto fica limpo.
- Texto com entrelinha < 1,05 e acento em caixa alta encosta na linha de baixo (o montador avisa).
- Imagem maior que a página (fundo ampliado para cortar) entra inteira e o Canva corta na borda: está certo.
- Nada de link público esquecido: `link_temporario.py status` mostra o que ficou aberto.
