# Auditoria técnica — PES 2013 PC para Android ARM64

## Status
Pendente de amostras técnicas verificáveis. Nenhum executável do jogo foi fornecido ou analisado nesta etapa.

## Itens a coletar
- Versão exata do PES 2013 e patch instalado.
- Arquitetura e cabeçalho PE de `pes2013.exe`.
- Imports estáticos e DLLs carregadas dinamicamente.
- Dependências de Direct3D 9 e extensões utilizadas.
- APIs Win32: janela, threads, sincronização, arquivos, registro, memória e temporizadores.
- Áudio: DirectSound, XAudio ou middleware de terceiros.
- Entrada: DirectInput, XInput ou outros dispositivos.
- Formatos e padrões de acesso aos arquivos `img` e demais dados.
- Proteções/DRM: apenas identificar requisitos; não contornar mecanismos de proteção.
- Requisitos de CPU, RAM, GPU e comportamento em dispositivos de referência.

## Matriz de risco inicial

| Área | Risco | Observação |
|---|---|---|
| x86 32-bit → ARM64 | Crítico | Exige código-fonte, recompilação binária ou reimplementação compatível |
| Win32 | Alto | APIs efetivamente usadas ainda desconhecidas |
| Direct3D 9 | Alto | Tradução para Vulkan/GLES exige análise de recursos e estado gráfico |
| Áudio | Médio/alto | Middleware e APIs ainda não identificados |
| Input | Médio | Provável necessidade de mapeamento para Android |
| Arquivos do jogo | Médio | Formatos e caminhos precisam ser inventariados |
| RAM/GPU | Alto | Medições reais necessárias |

## Método
1. Obter metadados e hashes localmente, sem publicar os binários.
2. Extrair imports e dependências com ferramentas de análise PE.
3. Reproduzir inicialização em ambiente de referência apenas para observação técnica.
4. Registrar cada API observada, evidência, frequência e prioridade.
5. Classificar dependências por licença e possibilidade de reutilização.
6. Atualizar arquitetura e roadmap com base nos resultados.

## Registro de evidências

| ID | Evidência | Resultado | Estado |
|---|---|---|---|
| AUD-001 | Executável PC original | Ainda não fornecido | Pendente |
| AUD-002 | Inventário de DLLs | Ainda não fornecido | Pendente |
| AUD-003 | Captura de APIs gráficas | Ainda não fornecida | Pendente |
