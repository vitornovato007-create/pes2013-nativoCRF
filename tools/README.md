# Ferramentas de auditoria PES 2013

## pes_asset_inspector.py

Inspeção estática e somente leitura dos pacotes IMG AFS e arquivos SFD.
O script lê o índice AFS, verifica limites e sobreposições, coleta pequenas
amostras de cabeçalho e procura marcadores Sofdec/MPEG em uma janela limitada.
Não extrai, modifica, executa nem envia assets do jogo.

### Executar localmente

Requer Python 3.9+ e não precisa de dependências externas.

    python tools/pes_asset_inspector.py /caminho/para/pasta/img
    python tools/pes_asset_inspector.py dt04.img dt05_a.img pes12ci.sfd --json relatorio.json

### Testes

    python -m unittest discover -s tools -p "test_*.py" -v

## GitHub Actions

O workflow .github/workflows/pes-asset-audit.yml testa os scripts em pull
requests e também pode ser iniciado manualmente.

IMPORTANTE: GitHub Actions não consegue ler arquivos que estão somente no
seu celular ou PC. Não envie os arquivos proprietários ao repositório.
O workflow só examina assets se eles já estiverem presentes em game-data/
no checkout. Para analisar os arquivos reais sem publicá-los, execute o
script localmente e compartilhe apenas o relatório JSON revisado.
