# Roadmap

Este roadmap é orientativo. Cada fase depende dos resultados e dos critérios de saída da fase anterior.

## Fase 0 — Auditoria e viabilidade
- [ ] Identificar versão, arquitetura e imports do executável PES 2013.
- [ ] Inventariar DLLs e APIs exigidas, separando componentes redistribuíveis e proprietários.
- [ ] Mapear Direct3D 9, Win32, áudio, input, threads, memória e arquivos.
- [ ] Avaliar projetos open-source candidatos e licenças.
- [ ] Publicar relatório de viabilidade com riscos e lacunas.

**Saída:** mapa de dependências verificável e arquitetura aprovada.

## Fase 1 — Base Android ARM64
- [ ] Configurar projeto Android/NDK/CMake.
- [ ] Criar aplicação mínima com JNI.
- [ ] Validar inicialização, ciclo de vida e logging em dispositivo ARM64.
- [ ] Medir baseline de CPU, RAM e GPU.

**Saída:** APK de diagnóstico nativo, sem executar o jogo ainda.

## Fase 2 — Subsistemas isolados
- [ ] Camada de arquivos e caminhos.
- [ ] Input Android para abstração de controles.
- [ ] Áudio Android.
- [ ] Contexto gráfico Vulkan e apresentação de frame.
- [ ] Backend OpenGL ES opcional.

**Saída:** protótipos testáveis independentemente.

## Fase 3 — Compatibilidade do jogo
- [ ] Implementar somente APIs comprovadamente necessárias.
- [ ] Definir estratégia para chamadas x86/Win32 incompatíveis com ARM64.
- [ ] Validar carregamento de dados e recursos sem redistribuir assets.

**Saída:** prova técnica de execução de uma fatia real do jogo.

## Fase 4 — Primeiro cenário jogável
- [ ] Inicializar subsistemas em conjunto.
- [ ] Renderizar uma cena real.
- [ ] Integrar áudio e controles.
- [ ] Instrumentar estabilidade, memória e desempenho.

**Saída:** primeiro teste jogável documentado, se a viabilidade permitir.

## Critérios de qualidade
- Nenhum workflow ou build remoto deve ser iniciado sem autorização explícita do mantenedor.
- Não declarar suporte funcional sem teste reproduzível.
- Medir consumo de RAM e desempenho em hardware real.
- Toda dependência deve ter origem, versão/commit e licença documentados.
