# Manual criativo (o básico que o Rick aplica em toda peça)

Regras gerais de criação de imagem, capa e carrossel, destiladas do manual de um criador que trabalha com o /ogab
(30/10/2026) e das correções que ele fez. Aqui ficam só os princípios que servem para qualquer marca; identidade,
personagem, bordões e hashtags de cada cliente ficam na pasta do cliente. Complementa
`docs/composicao_e_tipografia.md` (enquadramento, hierarquia, zonas) e `docs/carrossel.md` (método de carrossel).

## 1. Ordem de prioridade

1. Pedido atual do usuário.
2. Correção mais recente sobre o mesmo assunto e contexto.
3. Identidade e referências aprovadas da marca atendida.
4. Preferências pessoais registradas do usuário.
5. Orientações gerais (este manual, presets, skills).

- Regra de um cliente nunca vira regra de outro. Correção de UMA peça ("sobe o título", "troca o vermelho por azul")
  não vira paleta ou padrão geral.
- Instrução antiga que já foi corrigida não volta.
- Distinguir: correção direta do usuário, caso específico, orientação de guia. Não inventar preferência para tapar lacuna.
- Ao registrar algo novo na pasta da marca, anotar com data e contexto ("[CASO] 29/10, campanha X"), sem apagar o que mudou.

## 2. Gosto que dá certo (padrão quando a marca não diz o contrário)

- Visual com intenção e peso de marca: **poucas palavras e espaço negativo**.
- Headline com respiro: nada espremido, colado na lateral ou escondido pela interface.
- Sofisticação vem dos **overlays** (véu escuro, brilho controlado, sombra suave, profundidade), não de letra
  gasta/rachada. "Textura" pedida pelo usuário não quer dizer letra desgastada: perguntar ou usar letra limpa.
- **Cor natural na foto:** balanço de branco neutro. A cor da marca entra em detalhes (palavra, traço, objeto),
  nunca pintando a cena inteira (pele, ambiente, objetos alaranjados = erro). Fundo gráfico com glow da marca é uma
  coisa; fotografia é outra.
- Produto em peça publicitária: **grande, inteiro, valorizado pela composição**. Um item isolado não representa uma
  coleção: mostrar o conjunto.
- Tipografia de marca clássica/premium precisa de **peso e caráter**; fina e genérica parece amadora.

## 3. Construir a imagem: ideia antes do efeito

Antes de escolher efeito, escrever em uma frase o que a imagem comunica e definir:
1. Assunto principal. 2. Ação visível. 3. Emoção ou contraste. 4. Objeto ou ambiente que torna o assunto
reconhecível. 5. Espaço reservado para headline, recorte ou montagem.

Exemplo: "excesso de ofertas" virou um vendedor soterrado de produtos e sem nenhum comprador. A cena conta a ideia
sem parágrafo na arte.

**Contexto específico e correto:** lugar, instituição e objeto reconhecíveis (assunto do Brasil = mapa do Brasil e
Congresso, nunca referência dos EUA). App ou marca citada pode virar símbolo criativo (WhatsApp = balões verdes,
celulares, duplo check) em vez de print chapado; logo oficial quando a marca precisa aparecer.

## 4. Pedir imagem por IA (quando o usuário autorizou gerar)

- Escrever **"fotografia realista, não ilustração"** quando tem que parecer foto, inclusive em cena sem pessoa
  (tende a sair ilustrada).
- Sempre no pedido: luz coerente com o ambiente, balanço de branco neutro, perspectiva e escala coerentes,
  materiais/reflexos/sombras plausíveis, ação e expressão específicas, **sem texto legível e sem logos inventados**
  quando a cena vai ser composta depois.
- **Pessoa real (personagem da marca):** anexar ficha + rosto + corpo em toda geração; descrição escrita sozinha não
  basta. Perdeu semelhança depois de várias mensagens: reanexar. Conferir óculos, barba, formato do rosto, corpo e
  roupa em cada cena. Nunca afinar o corpo nem trocar o rosto por um "executivo genérico".
- Arquétipo (ex.: "bobo da corte") é direção de expressão, não fantasia em toda imagem. Acessório de personagem só
  quando tem função (no gancho, por exemplo).
- A pessoa da marca não precisa estar em toda cena: aparece onde a reação, a lição ou a chamada dela têm função.
- **Fisheye/grande-angular** chama atenção em gancho (perspectiva próxima, expressão teatral). Pedir **sem vinheta
  e sem bordas pretas** quando o usuário não quer o escurecido.
- **Plano aberto para título:** do joelho para cima, personagem menor na metade de baixo, terço superior livre e
  folga dos dois lados. Close dramático e plano aberto têm funções diferentes: escolher pelo uso.
- **Charge/caricatura:** escolher conscientemente entre charge de jornal (colorida, cabeça grande, corpo pequeno,
  traço bem-humorado) e cabeça aumentada com acabamento realista. Para recortar: corpo inteiro, fundo branco liso,
  sem cenário, texto ou logo. Fundo branco não é transparência: se a entrega precisa de alfa, recortar
  (Selecionar assunto) e conferir. Objetos e pose carregam a metáfora.

## 5. Edição pontual: preservar a base

Quando o pedido é local ("troca só essa pessoa", "só essa palavra em laranja", "só o upscale"):
- Identificar exatamente o que muda e mudar **só isso**.
- Preservar enquadramento, outras pessoas, fundo, objetos, cores e luz.
- Integrar escala, perspectiva, sombra e contato com o ambiente.
- Conferir que nada mudou fora da área pedida. Não aproveitar a edição para redesenhar.
- No Photoshop isso é natural (camada nova, máscara); na IA de imagem, usar o prompt E (abaixo).

## 6. Upscale e originais

- Preferir o original em alta (site oficial, assessoria, banco) a print de notícia.
- Upscale (Real-ESRGAN x4plus no fluxo do /ogab) e conferir o **tamanho real do arquivo**: "4K" no prompt não prova
  resolução. Melhorar a imagem não recupera detalhe que não existe nem comprova autenticidade.

## 7. Headline e margens

- Poucas palavras, impacto, hierarquia clara. Passou de 2-3 palavras e apertou: quebrar em 2 linhas.
- **Margem lateral mínima de 80-90 px** para headline em arte de 1080 px de largura.
- Headline numa linha só quando cabe com respiro; nunca reduzir até ficar ilegível.
- **Caixa alta mantém acento:** "CASA PRÓPRIA", "PREÇO", "ATENÇÃO". Conferir sempre (fonte sem glifo acentuado
  = trocar a fonte ou usar `faixas` com outra fonte só na letra).
- Palavra-chave forte em condensada, com o tratamento da marca (degradê, placa inclinada, sombra suave) só nela;
  não espalhar degradê pelo texto todo.
- **Reels 1080x1920, zona conservadora do texto principal:** x 70-1010, y 250-1480, longe da coluna de ícones à
  direita e da legenda embaixo. Conferir com a zona desenhada antes de entregar. Não aplicar esses números ao
  carrossel 1080x1350: adaptar ao formato.
- Capa que abre vídeo: legível já no primeiro quadro.

## 8. Viral é objetivo, não promessa

Padrões que ajudam: gancho forte ligado ao que a pessoa VÊ, humor e ironia (quando é a voz da marca), personagem
conhecido, contraste (medo x humor, surpresa x conflito, universos diferentes, antes x depois), objeto concreto e
gesto claro em vez de texto. Perguntas de revisão:
1. Em um segundo dá para entender o assunto?
2. Tem surpresa, tensão, utilidade ou desejo?
3. A imagem ilustra a ideia específica ou só enfeita?
4. O título promete o que o conteúdo entrega?
5. Há motivo concreto para salvar ou mandar para alguém?
6. A personalidade aparece sem atrapalhar a clareza?

Nunca prometer viralização nem reapresentar métrica antiga como atual.

## 9. Fatos e transparência

- Política, eleição, tribunal, pesquisa e notícia: confirmar em fonte confiável antes de produzir. Sem confirmação,
  avisar e esperar.
- Separar fato, opinião, hipótese, metáfora e campanha fictícia. Não inventar números, casos, depoimentos ou nomes
  para deixar o gancho mais forte.
- Montagem gerada nunca vira "foto documental" de um acontecimento. Campanha fictícia é identificada como conceitual
  ("Concept Campaign").
- Conteúdo sintético segue as regras vigentes do canal (rótulo de IA da plataforma etc.).

## 10. Processo em 10 etapas (qualquer peça)

1. **Pacote de referência:** identidade, logo oficial (transparente), fontes, fotos/ficha do personagem, artes
   aprovadas, correções anteriores. Faltou algo indispensável: dizer exatamente o quê.
2. **Briefing:** conta, objetivo, público, idioma, formato, nº de páginas, assunto, ação principal, texto obrigatório,
   o que deve ser preservado. Se o pedido já responde, não perguntar de novo.
3. **Verificar o conteúdo** (fatos e fontes).
4. **Conceituar:** ideia central e narrativa visual; tipo de peça; papel de cada página.
5. **Escrever:** headlines curtas, destaques, apoio, chamada, no idioma e na voz do cliente. Mostrar o mapa.
6. **Aprovar a direção visual na 1ª página** (ou composição-chave) antes de propagar um erro para a sequência.
7. **Construir a sequência** usando a página aprovada como referência; variar cena e composição.
8. **Revisar visualmente** todas as páginas, também em tamanho de celular: grafia, recortes, mãos, rostos,
   produtos, sombras, logos, margens, navegação.
9. **Legenda** coerente com as imagens e o idioma.
10. **Exportar e entregar:** ordem, dimensões reais, arquivos individuais (nunca um mosaico, sem mockup de celular
    salvo pedido), prompts e versão aprovada guardados. Publicar só com instrução explícita.

## 11. Prompts portáteis (IA de imagem)

Campos entre colchetes são preenchidos antes; nunca aparecem na arte.

**A. Cena fotográfica com a pessoa da marca**
```text
Crie uma fotografia realista vertical [formato] usando as referências anexadas de rosto e corpo de [pessoa].
Preserve identidade, formato do rosto, cabelo/barba, corpo e [acessório-assinatura]. Roupa conforme a ficha.
Ideia da cena: [uma frase]. Ação: [gesto e objeto]. Expressão: [emoção concreta].
Ambiente: [local específico e contexto correto]. Enquadramento: [close ou plano aberto, pela função].
Reservar espaço para [headline/recorte] em [região].
Cor natural, balanço de branco neutro, luz coerente com o ambiente, pele e materiais realistas.
Cor da marca apenas em [detalhe pontual]. Fotografia realista, não ilustração. Sem texto legível e sem logos inventados.
```

**B. Gancho fisheye sem vinheta**
```text
Fotografia realista vertical 9:16, lente fisheye grande-angular, sem vinheta e sem bordas pretas.
Personagem conforme as referências anexadas, reconhecível, com [expressão teatral] e [ação clara].
Cenário: [contexto que explica o assunto]. Profundidade, foco no personagem e espaço para headline.
Cor natural, luz realista. Sem textos ou marcas inventadas.
```

**C. Plano aberto com área para título**
```text
Refaça a cena em vertical 9:16 e plano mais aberto. Mesmo personagem das referências.
Do joelho para cima, personagem menor, centralizado na metade inferior. Terço superior livre e folga dos dois lados.
Ambiente [descrever], suavemente desfocado. Fotografia realista, cor natural, sem texto e sem logos.
```

**D. Charge recortável**
```text
Use a foto anexada como referência da pessoa. Charge de jornal colorida, cabeça grande e corpo pequeno,
traço bem-humorado, personagem reconhecível e de corpo inteiro. Pose: [ação]. Expressão: [emoção].
Objeto: [metáfora visual]. Fundo branco liso, sem cenário, para recortar. Sem texto e sem logos.
```

**E. Mudar só um elemento**
```text
Edite a imagem-base anexada. Altere somente [elemento exato], usando [referência anexada].
Preserve todo o restante: enquadramento, fundo, outras pessoas, objetos, cores, luz e posição dos elementos.
Integre a alteração com escala, perspectiva e sombras coerentes. Não redesenhe a imagem nem acrescente texto.
```

**F. Campanha de produto em 3 páginas** e **G. briefing de carrossel educativo**: em `docs/carrossel.md`.

## 12. Checklist (somar ao de `composicao_e_tipografia.md`)

- **Antes:** conta, público, idioma e objetivo definidos; identidade certa; fotos/logo anexadas; fatos confirmados;
  correções recentes consideradas.
- **Imagem:** ideia reconhecível rápido; cor natural; fisheye sem vinheta quando pedido; personagem fiel (rosto,
  corpo, acessório, roupa); sem fantasia por automatismo; produto com forma, escala e reflexo coerentes; mãos e
  contatos sem erro; edição pontual preservou a base; logos oficiais e sem deformação.
- **Texto:** folga nas laterais, topo e rodapé; legível no celular; acentos, nomes e caixa corretos; nenhuma palavra
  cortada; overlays refinados e letra limpa; texto gerado por IA conferido palavra por palavra; CTA e hashtags da
  conta certa.
- **Entrega:** arquivos abertos depois de exportar; dimensões reais; páginas individuais ordenadas e nomeadas;
  publicação só se autorizada.

## 13. Ficha de marca nova

Quando uma marca chega sem `design-<marca>.md`, abrir com esta ficha e preencher com o usuário/referências:

```yaml
marca:
conta:
idioma:
publico:
objetivo:
paleta:
fontes:
logo_oficial:
personagem_e_referencias:
tom_de_voz:
bordoes:
cta:
hashtags:
referencias_aprovadas:
correcoes_recentes:
elementos_obrigatorios:
elementos_proibidos:
formato:
quantidade_de_paginas:
```
