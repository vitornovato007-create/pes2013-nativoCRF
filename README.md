# PES 2013 Nativo CRF

Projeto experimental para investigar e desenvolver uma forma de executar **Pro Evolution Soccer 2013** em Android ARM64, reutilizando os dados de uma instalação legítima da versão PC, sem depender de Winlator ou de uma sessão Windows.

> **Estado:** estrutura inicial / pesquisa e auditoria. Ainda não existe um runtime jogável. O repositório não contém arquivos do jogo, executáveis proprietários ou DLLs extraídas.

## Objetivo técnico

Construir, por etapas, um runtime Android nativo ARM64. A meta é reaproveitar componentes open-source compatíveis e implementar as camadas de integração necessárias, em vez de tentar converter o executável Windows diretamente.

- Android ARM64 como plataforma-alvo inicial.
- Vulkan como backend gráfico principal, com OpenGL ES como alternativa futura.
- Uso eficiente de CPU, RAM e GPU.
- Preservar os arquivos originais do usuário; nunca distribuir dados proprietários do PES.
- Diagnóstico e testes automatizados desde o início.

## Importante: estratégia de compatibilidade

O executável original do PES 2013 é um programa Windows x86 de 32 bits. Android ARM64 não executa esse binário nativamente. Um port real exige identificar e substituir ou implementar as interfaces Win32, Direct3D 9, áudio, entrada, sistema de arquivos e demais dependências.

Este projeto **não promete** compatibilidade apenas por copiar `pes2013.exe` para o Android. A viabilidade será determinada pela auditoria técnica e por protótipos incrementais. Não usaremos Wine/Winlator/Box64 como solução final do objetivo nativo.

## Arquitetura planejada

| Camada | Responsabilidade |
|---|---|
| Android app | APK, ciclo de vida, permissões e interface |
| Runtime | Inicialização, configuração, logs e gerenciamento de recursos |
| Compatibility layer | APIs Win32 necessárias, apenas as efetivamente identificadas |
| Graphics | Abstração gráfica; Vulkan primeiro, GLES como fallback |
| Audio / Input | Áudio e controles Android |
| Game data | Seleção e validação dos arquivos fornecidos pelo usuário |

## Estrutura

- `app/`: aplicação Android e código JNI/C++.
- `native/`: runtime e componentes portáveis.
- `docs/`: auditoria, arquitetura, decisões e plano de testes.
- `tests/`: testes de host e testes nativos.
- `tools/`: scripts auxiliares de análise.
- `third_party/`: dependências externas documentadas; sem cópias vendorizadas até a revisão de licenças.

## Primeiras etapas

1. Inventariar o executável PC e suas dependências, sem incluir arquivos proprietários no Git.
2. Mapear chamadas Win32, Direct3D 9, DirectSound/XAudio, DirectInput/XInput e formatos de dados usados.
3. Avaliar projetos open-source reutilizáveis e suas licenças.
4. Definir uma fatia mínima de runtime Android ARM64 e validar o toolchain.
5. Prototipar subsistemas isolados antes de tentar iniciar o jogo.

Veja [docs/ROADMAP.md](docs/ROADMAP.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) e [docs/TECHNICAL_AUDIT.md](docs/TECHNICAL_AUDIT.md).

## Build

A estrutura inicial ainda não produz um APK jogável. Os arquivos de build serão ampliados depois da auditoria e da escolha das dependências. O workflow manual de auditoria de assets está em `.github/workflows/pes-asset-audit.yml`; ele não foi executado.

## Dados do jogo e direitos autorais

Forneça seus próprios arquivos de uma cópia legítima do PES 2013. Não envie para este repositório executáveis, DLLs proprietárias, imagens, áudio, bancos de dados ou outros assets do jogo. A Konami não é afiliada a este projeto.
