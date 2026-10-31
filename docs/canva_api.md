# Canva: engenharia reversa (conector MCP + app desktop)

Levantado e testado em 30-31/10/2026 numa conta real (conector oficial do Canva no Claude + app Canva 1.126.2 no Mac).
Este é o "photoshop_api.md" do Canva: o que existe, o formato de cada comando e o que foi testado de verdade.

## 1. Resumo: onde estão os comandos de edição

- **O app desktop NÃO tem API de edição.** É um Electron que só carrega o editor do canva.com (seção 5). Toda edição
  passa pelo editor web, e o único jeito oficial e estável de comandá-lo de fora é o **conector MCP**.
- O conector edita **camada por camada**: criar texto, forma (SVG), imagem, página; mover, redimensionar, girar,
  opacidade, ordem das camadas, cor, tamanho e peso do texto, trocar texto e imagem, apagar, agrupar.
- **Não existe campo de família da fonte.** `add_text` cria sempre na fonte padrão do Canva (`fontRef`
  `YACgEZ1cb1Q,0`, 16 px, preto). **`replace_text` MANTÉM a fonte do elemento** (testado): por isso a montagem usa um
  **kit de fontes da marca** (seção 4).
- Arquivo local NÃO vira design pelo conector: `create-upload-url` recusa PPTX ("Unsupported file format PPTX") e o
  PDF sobe só como arquivo em Uploads, não como design. `import-design-from-url` aceita só URL pública, e a própria
  ferramenta proíbe hospedar arquivo gerado em terceiros para criar a URL. Imagem (JPG/PNG) sobe e vira `mediaId`.

## 2. Ferramentas do conector (as que o Rick usa)

| Ferramenta | Para quê | Observações testadas |
|---|---|---|
| `create-upload-url` | URL de upload de uso único | depois: `POST` dos bytes crus, `Content-Type: application/octet-stream` (sem multipart/base64). Resposta `{"mediaId":"MAH..."}` (imagem) ou `{"fileId":"..."}` (documento). URL vale uma vez e expira |
| `read-design` | ler o design em camadas | `filter.fields`: design_metadata, page_metadata, design_content, thumbnails, presenter_notes. `open_transaction: true` abre edição e devolve `transaction_id` |
| `edit-design` | aplicar operações | `transaction_id`, `page_index` (começa em 1), `operations` e `finalize`: `keep_open` (aplica), `commit` (salva, sem operations), `cancel` (descarta). Cada chamada devolve a miniatura e o documento atualizado |
| `copy-design` | duplicar (ex.: o kit da marca) | |
| `merge-designs` | juntar designs (páginas do carrossel) | |
| `create-design` | design novo por IA a partir de briefing | NÃO cria em branco: "em branco" foi ignorado (veio um post pronto). "Instagram Post (Portrait)" saiu 1080x1440 |
| `export-design` | PNG/JPG/PDF/PPTX/MP4 | conferir antes com `get-export-formats` |
| `search-designs`, `list-folder-items`, `create-folder`, `move-item-to-folder` | achar e organizar | |
| `list-brand-kits`, `search-brand-templates`, `create-design-from-brand-template`, `autofill-design` | marca (plano Pro+) | modelo de marca preenchido mantém as fontes |
| `separate-image-layers` | imagem chapada vira design em camadas (Magic Layers) | **fluxo principal**: arte do ChatGPT vira design editável (textos com fonte detectada, elementos e fundo limpo). Só com `mediaId` (upload antes); job: `get-separate-image-layers-job` |
| `remove-background`, `generate-image` | imagem | |
| `help` | dúvida de produto do Canva | |

Limites: 300 chamadas/min por usuário; `edit-design` (antigo perform-editing-operations) ~50/min; upload 30/min.

## 3. Operações do `edit-design` (esquema real)

Unidades em px da página; `locator_id` vem do `read-design` (formato `PAGEID-ELEMENTID`); `page_id` é o id da página.

- **Texto:** `add_text {page_id, text, top, left, width?, rotation?, opacity?}` (com width quebra linha) ·
  `replace_text {locator_id, text}` (mantém fonte e estilo) · `find_and_replace_text {locator_id, find_text, replace_text}` ·
  `format_text {locator_id, formatting:{font_size 1-800, color "#RRGGBB", font_weight normal|bold,
  font_style normal|italic, line_height 0.5-2.5, text_align start|center|end, decoration, strikethrough, link,
  list_level, list_marker}}` (vale para o elemento INTEIRO, sem trecho) · `update_text_anchoring {start|center|end}`
- **Forma:** `insert_shape {page_id, top, left, width, height, path (SVG só M L H V C S A Z), view_box_width,
  view_box_height, color, opacity, corner_rounding 0-1000, stroke_color, stroke_weight, rotation}` ·
  `replace_shape` · `recolor_element {locator_id, color}` · `update_stroke_properties`
- **Imagem/vídeo:** `insert_fill {page_id, asset_type image|video, asset_id (mediaId), alt_text, top, left, width,
  height, opacity, rotation}` · `update_fill {locator_id, asset_type, asset_id, alt_text}` (no `locator_id` DA PÁGINA
  troca o fundo e cobre a página sozinho, testado) · `crop_media` · `flip_media`
- **Geral:** `position_element {locator_id, top, left}` · `resize_element {locator_id, width, height?,
  preserve_aspect_ratio}` (texto: só width) · `rotate_element` · `update_opacity` · `layer_element {front|back}` ·
  `delete_element` · `group_elements` / `ungroup_elements` · `update_line_properties`
- **Página:** `add_page {width, height, background_color, title}` · `reorder_page` · `replace_speaker_notes` ·
  `update_title` · `update_autofill_field` (rotular elemento para autofill)
- Página "responsive" (docs/sites) aceita só update_title, replace_text, update_fill, delete_element, find_and_replace_text.

Regras do conector: comparar a miniatura de antes e depois a cada chamada; **só dar `commit` com o ok do usuário
depois de mostrar a prévia**; transação fica velha se alguém editar no navegador ao mesmo tempo (cancelar e refazer).

## 4. Estrutura que o `read-design` devolve (o "DOM" do Canva)

```json
{"pages":[{"type":"fixed","id":"PB3K7BZ8Hm6VVkZJ","dimensions":{"width":1080,"height":1440},
  "background":{"media":{"type":"image","mediaId":"MAH...","imageBox":{"top":0,"left":0,"width":1080,"height":1440}}},
  "elements":[
    {"id":"LB8X...","type":"text","top":50.6,"left":64.2,"width":219.7,"height":359.7,"rotation":0,"opacity":1,
     "textRegions":[{"characters":"seu","formatting":{"fontSize":300.4,"fontWeight":"normal","fontStyle":"normal",
       "color":"#1b1b1b","textAlign":"start","lineHeight":0.70,"letterSpacing":0.02,"fontRef":"YAEp7Jy5cNk,0"}}],
     "locator_id":"PB3K7BZ8Hm6VVkZJ-LB8X..."},
    {"type":"rect","fill":{"media":{"type":"image","mediaId":"MAH..."}}, "...": "imagem num quadro"},
    {"type":"shape","viewBox":{...},"paths":[{"d":"M0 0 H1080 V1440 H0 Z","fill":{"color":{"type":"solid","color":"#000000"}},"cornerRounding":0}]}
  ]}]}
```

- Um texto pode ter vários `textRegions` (trechos com estilo diferente, ex.: palavra colorida). O conector LÊ os
  trechos, mas `format_text` só formata o elemento inteiro: palavra em outra cor = outro elemento de texto.
- `fontRef` = id interno da fonte no Canva (`YACgEZ1cb1Q,0` = padrão). Não dá para escrever; só herdar via kit.

## 5. App desktop (Canva.app 1.126.2, com.canva.canvaeditor)

- Electron (Mac App Store, sandbox). `Contents/Resources/app.asar` com `dist/main.js` (6,7 MB), `preload.js` e
  páginas internas (`desktop_chrome_v2`, `desktop_offline_fallback`, `desktop_recording`). O editor vem do canva.com.
- Deep link: `canva://` (abrir pelo sistema: `open "canva://..."`). Abre arquivos por associação (`open -a Canva arquivo`).
- Ponte página <-> app: `window.ElectronBridge` (`requestMessagePort`, `onPageBuildIdentityReady`) num barramento
  de mensagens (`ElectronMessageBus`). Serviços que o app oferece ao editor (RPC), sem nenhum de edição:
  `BaseNavigationService` (navigateToEditor, navigateToHome, navigateToDesignViewer...), `TabManagementService`
  (createTab, getTabs, focusTab, closeTab...), `DownloadService` (downloadFileByUrl, startBatchDownload...),
  `LocalExportService` (localExport2), `FileDropService`, `MenuBarService`, `ThemeService`, `WindowManagementService`,
  `SessionService`, `AppUpdateService`, `RecordingService`, `NotificationService`, `HostCapabilitiesService`.
- Travas: fuses do Electron com RunAsNode, NODE_OPTIONS e `--inspect` DESLIGADOS; integridade do asar LIGADA; sandbox
  do macOS. Porta de depuração do Chromium (`--remote-debugging-port`) não testada (o app já estava aberto).
- Conclusão: para editar, conector MCP. O app serve para o usuário ver e mexer; ajuste fino que o conector não faz
  (ex.: trocar a família da fonte de um elemento) é feito no app pela tela (computer use: app com permissão total),
  clicando no texto > seletor de fonte > digitar o nome > Enter, e conferindo pela miniatura do `read-design`.
- APIs internas do canva.com (as que o editor usa por baixo) NÃO são usadas: não são públicas, mudam sem aviso e os
  termos do Canva proíbem acesso automatizado fora das APIs oficiais (risco de bloquear a conta do usuário).
