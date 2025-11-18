# 📚 Referência Rápida de Filtros

## Filtros Passa-Baixa (Suavização)

| Filtro | Efeito | Quando Usar |
|--------|--------|-------------|
| **Média 3x3** | Suavização leve, remove ruído | Redução de ruído mantendo detalhes |
| **Média 5x5** | Suavização forte, mais desfoque | Ruído intenso, efeito blur |
| **Gaussiano** | Suavização natural, preserva bordas | Melhor qualidade, pré-processamento |

## Filtros Passa-Alta (Detecção de Bordas)

| Filtro | Efeito | Quando Usar |
|--------|--------|-------------|
| **Laplaciano** | Bordas em todas direções | Contornos completos, detalhes finos |
| **Sobel X** | Destaca bordas verticais | Detecção de linhas verticais |
| **Sobel Y** | Destaca bordas horizontais | Detecção de linhas horizontais |
| **Sobel XY** | Bordas em todas direções | Detecção geral de bordas |

## Transformações Morfológicas

| Operação | Efeito | Quando Usar |
|----------|--------|-------------|
| **Erosão** | Reduz objetos, remove ruído branco | Remover pontos isolados |
| **Dilatação** | Aumenta objetos, preenche buracos | Conectar componentes próximos |
| **Abertura** | Remove ruído externo | Limpar fundo, suavizar bordas |
| **Fechamento** | Preenche buracos internos | Reconstruir objetos fragmentados |
| **Gradiente** | Extrai contornos | Detecção de bordas |

## Conversão de Cor

| Conversão | Efeito | Quando Usar |
|-----------|--------|-------------|
| **Grayscale** | Tons de cinza | Simplificar processamento |
| **HSV** | Separação cor/brilho | Segmentação por cor |
| **Canais RGB** | Separação R, G, B | Análise individual de cores |

## Limiarização

| Método | Efeito | Quando Usar |
|--------|--------|-------------|
| **Binária** | Preto e branco fixo | Iluminação uniforme |
| **Adaptativa Mean** | Limiar por região | Iluminação variável |
| **Adaptativa Gaussian** | Limiar ponderado | Melhor qualidade |
| **Otsu** | Limiar automático | Histograma bimodal |

## Histogramas

| Técnica | Efeito | Quando Usar |
|---------|--------|-------------|
| **Equalização** | Aumenta contraste global | Imagens com baixo contraste |
| **CLAHE** | Equalização local adaptativa | Variação de iluminação |
