# Log Analyzer

Analisador de logs de acesso em Python que identifica tentativas de login
malsucedidas e IPs potencialmente suspeitos. Projeto de estudo que combina
programação, análise de dados com Pandas e conceitos básicos de cibersegurança.

## O que ele faz

- Lê um arquivo de logs (`data/access.log`) com Pandas
- Conta logins bem-sucedidos e malsucedidos
- Mostra falhas por usuário e por IP
- Aponta IPs com 5 ou mais falhas (`LIMITE_FALHAS`)

## Formato dos logs

```
data_hora,evento,usuario,ip
2026-09-28 08:16:45,LOGIN_FAILED,user02,192.168.0.15
```

Linhas começando com `#` e linhas em branco são ignoradas.

## Como executar

```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/analyzer.py
```

Para analisar outro arquivo: `python src/analyzer.py data/teste_limite.log`

## Estrutura

```
log-analyzer/
├── data/
├── src/analyzer.py
├── requirements.txt
└── README.md
```

## Próximos passos

- Detecção por janela de tempo (ex.: 5 falhas em 10 minutos)
- Gráficos com matplotlib
- Testes automatizados com pytest

## Autora

Isa, estudante de ADS na FIAP.