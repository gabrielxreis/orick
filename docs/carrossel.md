# Carrossel (o método do Rick)

Ler antes de qualquer carrossel. Aprendido de um carrossel educativo de 7 páginas aprovado de primeira por um cliente
(mercado financeiro, 28/10/2026) e generalizado aqui. O estilo vale para qualquer nicho que ensina alguma coisa:
finanças, igreja, saúde, imigração, curso. Preset pronto: [`presets/carrossel-educativo`](../presets/carrossel-educativo/README.md).

## 0. Antes de tudo: a marca manda

1. Ler `<Marca>/design/design-<marca>.md` e qualquer guia de estilo da pasta `design/`. **Se a marca exige um motor
   (ex.: "carrossel desta marca só na IA de imagem X, é o que o cliente gosta"), seguir isso à risca, sem plano B.**
2. Paleta, fontes, logo, rodapé e @ sempre os da marca. Nunca copiar marca de referência nem preset de outro cliente.
3. Sem referência da marca? Pedir 3 a 6 carrosséis que o cliente gosta, ou propor o preset `carrossel-educativo`.

## 0b. Escolher o TIPO antes de montar

| Tipo | Função | Estrutura |
|---|---|---|
| **Educativo** | explicar, listar, entregar método | gancho, valor cedo, resumo útil, uma ação (seções 1-2) |
| **Campanha publicitária** | valorizar produto e construir marca | produto completo > produto em uso > produto com o universo da marca (seção 3b) |
| **Motion/painel** | mostrar sistema, rotina, conexões | capa, módulos, conexão e CTA animados (motor C) |

Não obrigar uma campanha de 3 páginas a virar aula de 10 slides: o pedido e a função da peça mandam.

**Estruturas do educativo** (a de 7 páginas abaixo é uma "método/conceitos"):
| Estrutura | Sequência | Objetivo |
|---|---|---|
| Lista | promessa, itens, lista resumida | salvar |
| Antes/depois | resultado, ponto inicial, etapas, conclusão | mostrar transformação |
| Mito/realidade | crença, correção sustentada, reenquadramento | compartilhar |
| Método | promessa, partes do processo, método completo | referência aplicável |

Quantidade de páginas sai do conteúdo real (6-10 é ponto de partida, não meta). Não inventar números, casos ou
resultados para o gancho. Capa: promessa concreta e motivo para deslizar (6-12 palavras), não só o nome do assunto.
Última página: síntese útil sozinha + UMA ação.

## 1. Planejar o texto (mostrar antes de desenhar)

- Usar a `ig-carousel-planner` (se instalada) ou este roteiro. Mostrar ao usuário uma linha por página
  (tipo, título, destaque, foto/metáfora) e só desenhar depois do ok.
- **Sequência de 7 páginas que funcionou:**
  | Pág. | Papel | O que vai |
  |---|---|---|
  | 1 | Capa / gancho | pessoa da marca (ou cena icônica) + frase que promete o aprendizado + 3 chips com os temas |
  | 2 | Metáfora geral | uma cena do dia a dia que explica o assunto inteiro |
  | 3-5 | Conceitos | um conceito por página, cada um com SUA metáfora em foto + exemplo concreto |
  | 6 | Fixação | "Guarde isso!" + lista com ícone por item + frase final de efeito |
  | 7 | Conversão | frase de fechamento + produto/logo + CTA ("Acesse o link da bio") + pílula com o link |
- **Texto curto:** título até 4-6 palavras, corpo até 2 frases (3 linhas). Uma ideia por página.
- **Título em dois pesos de cor:** a palavra-chave gigante na cor de destaque (gradiente) e o resto em branco menor,
  ou o inverso (frase em branco, palavra-chave no meio).
- **Corpo com um trecho destacado** na cor fria (azul/ciano) em negrito.
- **Exemplo concreto** numa caixa (borda fina na cor da marca, "Exemplo:" em negrito) ou numa barra vertical.
- **Metáfora em foto:** cada conceito vira uma cena reconhecível (bola quicando = preço entre chão e teto, rede do
  trapezista = suporte, bloqueio de vôlei = resistência, salto com vara = rompimento). A pessoa da marca aparece na
  capa, na fixação e na conversão; nas metáforas, não.
- Sem travessão nos textos (o rótulo "PÁGINA 3 — TEMA" é elemento gráfico, não frase). Português com acento certo.

## 2. Sistema visual (grade fixa em todas as páginas)

Formato 4:5 (1080x1350). Medidas do original:
1. **Foto ocupa a página toda**, assunto do lado direito; lado esquerdo escurecido por vinheta diagonal para o texto.
   Luz cinematográfica (golden hour, contraluz quente, sombras frias: teal & orange), profundidade rasa.
2. **Rótulo de página** no canto superior esquerdo (x ~150, y ~95): "PÁGINA N — TEMA", pequeno, caixa alta,
   espaçado, cinza a 40%, com traço curto na cor da marca embaixo (80 x 4 px).
3. **Título** condensado ultrapesado em caixa alta (Bebas Neue / Anton / Druk), entrelinha 0,85, ponto final.
4. **Corpo** em sans geométrica (Montserrat), 34-38 px.
5. **Gráfico sobre a foto** quando o assunto pede: pontos com brilho ligados por linha tracejada, números, seta.
   O gráfico conversa com a foto (sobe junto com o avião, segue a bola).
6. **Assinatura nas bordas:** blocos de pixels "glitch" nas duas cores da marca saindo da borda esquerda em cima
   (x 0-65, y 30-360) e da direita embaixo (x 990-1080, y 860-1280), com retângulo de contorno branco fino deslocado.
7. **Rodapé fixo** (y ~1250, faixa escura subindo do preto): logo à esquerda | seta → no centro | divisor fino |
   #assinatura ou @ à direita.
8. **Duas temperaturas sempre:** cor quente = palavra-chave/marca; cor fria = solução/destaque; vermelho = erro, queda.

## 3. Três motores (padrão: IA de imagem; outro só pela marca ou pelo pedido)

| Motor | Quando | Sai |
|---|---|---|
| **B. IA de imagem** (ChatGPT/gpt-image, Nano Banana), **padrão do Rick** | sempre que a marca não pede outro motor e o usuário não escolheu Photoshop/Canva | PNG por página, não editável |
| **A. Photoshop** (opção) | o usuário pede PSD editável, a marca tem fotos próprias, vai virar template/série | PSD com uma prancheta por página + PNG |
| **C. HTML do /ogab** (`instagram/carrossel`) ou **carrossel de motion** (`instagram/carrossel_motion`) | tipográfico rápido sem foto / carrossel animado em vídeo | PNG/PDF ou MP4 por página |

Fotos das metáforas por IA (motor A ou B) **só perguntando antes** (o que vai ser gerado e o custo).

### A. Photoshop

1. `arte.jsx` com `Y.doc(1080, 1350*N)` + `Y.fatiar` (panorâmico) **ou** um documento por página reaproveitando um
   `pagina()` comum (rodapé, rótulo, glitch e vinheta numa função; só foto, título, corpo e caixa mudam).
2. Árvore por página (de baixo para cima): `FOTO` (smart object, `Y.colocar` + encaixar à direita) > `VINHETA`
   (`Y.degrade` preto diagonal 0-75%) > `GRAFICO` > `GLITCH` (`Y.retangulo` em colunas + `Y.grao`, contorno branco
   `so_contorno`) > `TEXTO` (rótulo, título com `faixas` para a palavra-chave em gradiente via `Y.efeitos`, corpo
   com `faixas` no destaque, caixa de exemplo) > `RODAPE`.
3. Montar com `montar.py`, conferir cada página com os olhos e `conferir_arte.py` (contraste, zona segura).
4. Série: depois do primeiro aprovado, `virar_template.py` + `lote.py` trocam só os textos e as fotos.

### B. IA de imagem (processo validado: 7 páginas aprovadas de primeira)

1. Conversa nova no ChatGPT (modo Chat) ou no Gemini, pelo navegador logado do usuário.
2. **Primeira mensagem com tudo anexado:** as páginas de referência aprovadas (capa, metáfora, conceito, analogia,
   fixação, conversão) + a ficha do personagem da marca (dizer qual imagem é a ficha).
3. **Briefing único com o carrossel inteiro**, nesta ordem: formato 4:5 e "EXATAMENTE no mesmo estilo das
   referências"; como a pessoa é; o sistema visual com os hex, fontes, blocos glitch, rótulo e rodapé;
   "Textos em português do Brasil, com acentos corretos, sem inventar nem mudar palavras"; página por página
   (foto/metáfora, título dividido nas duas cores, corpo com o trecho destacado, caixa, gráfico); fechar com
   "Gere UMA página por vez, começando pela PÁGINA 1 agora". Guardar o briefing como `briefing.txt` na pasta.
4. **Uma página por mensagem:** "Agora a PÁGINA N — TEMA, exatamente como no briefing (resumo). Rótulo do topo:
   'PÁGINA N — TEMA'." Repetir o rótulo evita número errado; com a pessoa, repetir "fiel à ficha anexada".
5. **Conferir cada página antes da próxima:** acento (Ç, Ã, Ê, É), palavra trocada, rótulo, destaque no lugar,
   rosto. Errou: pedir de novo só aquela página dizendo o que corrigir.
6. Baixar (sai ~1122x1402), renomear `01_capa.png` ... `07_conversao.png`.
7. Logo de marca citada (banco, bolsa, órgão) que a IA desenhou torta: trocar pela oficial no Photoshop.

### 3b. Campanha publicitária de produto (3 páginas, aprovada num caso real de 29/10/2026)

1. **Página 1:** conjunto completo do produto (com estojo/embalagem), apresentação de impacto.
2. **Página 2:** produto em uso (mesa posta, mão, ambiente), produto ainda em destaque.
3. **Página 3:** produto + embalagem + fechamento de marca, com UMA ação no rodapé (ícone de seguir no centro).
- Seta/"swipe" discreta nas páginas 1 e 2. Rodapé consistente; logo do estúdio + "Concept Campaign" quando é
  campanha conceitual (marca fictícia).
- Fotografia publicitária realista dominante, materiais táteis, poucas palavras, tipografia com peso e caráter.
- Testar a direção na página 1, aprovar e usar como referência das outras (mesmo desenho, material e acabamento do
  produto; só a composição muda).
- Erros que o cliente corrigiu: um item isolado em vez da coleção; tipografia fraca para marca clássica; faltou a
  assinatura do estúdio no rodapé.
- Não inventar alegações, preços, datas ou endereços. Entregar 3 arquivos separados (sem mosaico, sem mockup de
  celular). Importar no Canva só se pedirem, avisando que a imagem importada não vira texto editável.

Prompt (IA de imagem):
```text
Criar três artes individuais de carrossel 4:5 para [marca], em [idioma]. Usar a identidade e logo oficiais anexadas.
Produto como protagonista, grande, identificável, totalmente visível e com desenho consistente.
Fotografia publicitária realista, materiais e reflexos plausíveis, tipografia [direção da marca], poucas palavras e
margens amplas. Página 1: conjunto completo, apresentação de impacto. Página 2: contexto de uso, produto em destaque.
Página 3: produto com embalagem e fechamento de marca. Nas duas primeiras, indicação discreta de arrastar; na
terceira, uma ação principal no rodapé. Não inventar alegações, datas, preços ou endereços.
Usar a primeira página aprovada como referência das demais. Arquivos separados, sem mosaico e sem mockup.
```

Briefing de carrossel educativo (para planejar com IA ou mostrar ao usuário):
```text
Tema: [tema]. Público: [público]. Conta: [conta]. Idioma: [idioma].
Objetivo principal: [salvar/compartilhar/comentar/seguir]. Estrutura: [lista/transformação/mitos/método].
Escreva primeiro o mapa slide a slide, com função, headline, destaque e ideia visual. Uma ideia por página.
Capa com promessa clara; conteúdo forte cedo; encerramento com síntese útil.
Não invente números, casos ou resultados. Não preencha páginas com repetição.
Use a identidade anexada e preserve respiro em todas as headlines.
```

### C. HTML / motion do /ogab

Seguir `~/.claude/skills/ogab/instagram/carrossel/CARROSSEL.md` (slides tipográficos na marca, PNG/PDF) ou
`~/.claude/skills/ogab/instagram/carrossel_motion/CARROSSEL_MOTION.md` (cada página vira um vídeo de ~6,5 s que se
monta sozinho). Precisa do /ogab instalado.

## 4. Entregar

1. Pasta `<Marca>/design/carrosseis/<AAAA-MM-DD>_<tema>/` com as páginas, o briefing/arte.jsx e o PSD (motor A).
2. `python3 SKILL_DIR/scripts/carrossel_entrega.py <pasta>` gera `instagram_1080x1350/*.jpg` (corte central,
   sem distorcer) e `folha_carrossel.jpg` (todas numeradas, para mostrar de uma vez).
3. Mostrar a folha ao usuário. Se a marca tem pasta no Drive, subir lá (design > carrosseis).
4. Legenda do post pela `ig-caption-writer` + `ig-humanizer` (se instaladas), salva em `legenda_post.txt`.

## 5. Cuidados

- Nada de promessa de resultado em nicho regulado (finanças, saúde, imigração): seguir as regras da marca.
- Celebridade ou cena de filme na capa: ok em orgânico informativo; em anúncio pago só com o ok do usuário.
  Melhor ainda: a própria pessoa da marca no lugar (funcionou e evita imagem de terceiro).
- O que mudou de aprendizado vai para o `docs/diario.md` e, se for da marca, para o `design-<marca>.md`.
