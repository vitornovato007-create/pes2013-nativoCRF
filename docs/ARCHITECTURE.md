# Arquitetura proposta

## Princípios
1. ARM64 nativo no Android; não mascarar uma execução Windows por emulação como port nativo.
2. Separar código portável de integrações específicas do Android.
3. Vulkan como primeira opção gráfica; GLES permanece uma possibilidade de fallback.
4. Implementar apenas APIs demonstradas como necessárias pela auditoria.
5. Manter dados originais do usuário fora do controle de versão.

## Componentes

### Android host
Responsável por Activity, ciclo de vida, superfície de janela, permissões, seleção de pasta e integração JNI.

### Runtime core
Inicialização, configuração, logging, gerenciamento de memória e coordenação dos subsistemas.

### Compatibility layer (a definir)
Conjunto mínimo de interfaces compatíveis que o jogo realmente utiliza. Não presumir que uma camada Win32 completa seja necessária ou viável antes de examinar imports e comportamento.

### Graphics
Interface interna independente do backend. Vulkan é o backend-alvo inicial; GLES pode ser implementado depois, se houver benefício comprovado.

### Audio e input
Adaptadores Android para áudio e controles, com interfaces testáveis fora do dispositivo.

### Game data
Validação da instalação fornecida pelo usuário. O projeto não baixa, inclui ou modifica assets proprietários.

## Questão arquitetural crítica

O executável PC é x86 de 32 bits, enquanto o alvo é ARM64. Isso não é resolvido apenas com JNI ou recompilação do launcher. A auditoria deve determinar se existe código-fonte recompilável, uma camada de recompilação binária viável, ou se será necessário reimplementar partes substanciais do jogo. Essa decisão bloqueia qualquer promessa de execução nativa.
