# Registros de decisões (ADR)

## ADR-0001 — Objetivo de execução
**Status:** aceito como objetivo, sujeito à viabilidade técnica.

Buscar execução Android ARM64 nativa sem Winlator/Wine/Box64 como solução final.

## ADR-0002 — Backend gráfico
**Status:** direção inicial.

Vulkan será investigado como backend principal. OpenGL ES será considerado como alternativa. A decisão final depende dos requisitos gráficos identificados e da compatibilidade dos dispositivos.

## ADR-0003 — Estratégia de implementação
**Status:** híbrida.

Reutilizar bibliotecas open-source quando tecnicamente compatíveis e licenciadas para o uso pretendido; desenvolver adaptadores e componentes específicos quando necessário. Nenhuma dependência será incorporada antes de revisar manutenção, arquitetura e licença.
