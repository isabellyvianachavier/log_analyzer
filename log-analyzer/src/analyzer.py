import sys
from pathlib import Path

import pandas as pd

LIMITE_FALHAS = 5
COLUNAS = ["data_hora", "evento", "usuario", "ip"]
CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "data" / "access.log"


def ler_logs(caminho):
    """
    Lê o arquivo de logs e retorna um DataFrame limpo.
    """

    df = pd.read_csv(
        caminho,
        names=COLUNAS,
        comment="#",
        skipinitialspace=True,
        encoding="utf-8",
        on_bad_lines="skip",
    )

    # Converte data/hora; valores inválidos viram NaT e a linha é descartada
    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
    df = df.dropna()

    # Remove espaços sobrando no fim dos campos de texto
    for coluna in ["evento", "usuario", "ip"]:
        df[coluna] = df[coluna].str.strip()

    return df


def analisar_logs(df):
    """
    Analisa o DataFrame e retorna as informações coletadas.
    """

    falhas = df[df["evento"] == "LOGIN_FAILED"]
    sucessos = df[df["evento"] == "LOGIN_SUCCESS"]

    return {
        "total_eventos": len(df),
        "total_sucessos": len(sucessos),
        "total_falhas": len(falhas),
        "falhas_por_usuario": falhas["usuario"].value_counts(),
        "falhas_por_ip": falhas["ip"].value_counts(),
    }


def encontrar_maiores_falhas(falhas_por_usuario, falhas_por_ip):
    """
    Encontra o usuário e o IP com maior número de falhas.
    Retorna None quando não há nenhuma falha.
    """

    usuario_mais_falhas = None
    ip_mais_falhas = None

    if not falhas_por_usuario.empty:
        usuario_mais_falhas = falhas_por_usuario.idxmax()

    if not falhas_por_ip.empty:
        ip_mais_falhas = falhas_por_ip.idxmax()

    return usuario_mais_falhas, ip_mais_falhas


def detectar_ips_suspeitos(falhas_por_ip):
    """
    Identifica IPs com LIMITE_FALHAS ou mais falhas (>=).
    """

    return falhas_por_ip[falhas_por_ip >= LIMITE_FALHAS]


def gerar_relatorio(analise, usuario_mais_falhas, ip_mais_falhas, ips_suspeitos):
    """
    Exibe o relatório final no terminal.
    """

    print("================================")
    print("         LOG ANALYZER")
    print("================================")

    print("\nResumo:")
    print(f"Total de eventos: {analise['total_eventos']}")
    print(f"Logins bem-sucedidos: {analise['total_sucessos']}")
    print(f"Logins malsucedidos: {analise['total_falhas']}")

    print("\nFalhas por usuário:")
    for usuario, quantidade in analise["falhas_por_usuario"].items():
        print(f"{usuario} → {quantidade}")

    print("\nFalhas por IP:")
    for ip, quantidade in analise["falhas_por_ip"].items():
        print(f"{ip} → {quantidade}")

    print("\nUsuário com mais falhas:")
    if usuario_mais_falhas is None:
        print("Nenhuma falha registrada.")
    else:
        print(f"{usuario_mais_falhas} → {analise['falhas_por_usuario'][usuario_mais_falhas]}")

    print("\nIP com mais falhas:")
    if ip_mais_falhas is None:
        print("Nenhuma falha registrada.")
    else:
        print(f"{ip_mais_falhas} → {analise['falhas_por_ip'][ip_mais_falhas]}")

    print(f"\nIPs potencialmente suspeitos (limite: {LIMITE_FALHAS} ou mais falhas):")
    if ips_suspeitos.empty:
        print("Nenhum IP atingiu o limite de falhas.")
    else:
        for ip, quantidade in ips_suspeitos.items():
            print(f"{ip} → {quantidade} tentativas malsucedidas")


def main():

    # Permite: python src/analyzer.py data/outro.log
    if len(sys.argv) > 1:
        caminho_logs = Path(sys.argv[1])
    else:
        caminho_logs = CAMINHO_PADRAO

    try:
        df = ler_logs(caminho_logs)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_logs}")
        return

    analise = analisar_logs(df)

    usuario_mais_falhas, ip_mais_falhas = encontrar_maiores_falhas(
        analise["falhas_por_usuario"],
        analise["falhas_por_ip"],
    )

    ips_suspeitos = detectar_ips_suspeitos(analise["falhas_por_ip"])

    gerar_relatorio(analise, usuario_mais_falhas, ip_mais_falhas, ips_suspeitos)


if __name__ == "__main__":
    main()