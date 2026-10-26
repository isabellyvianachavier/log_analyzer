import pandas as pd

df = pd.read_csv(
    "data/access.log",
    names=["data_hora", "evento", "usuario", "ip"],
    comment="#",
    skipinitialspace=True,
    encoding="utf-8",
)

df["data_hora"] = pd.to_datetime(df["data_hora"])
print(df.dtypes)

falhas = df[df["evento"] == "LOGIN_FAILED"]
print(falhas)
print(len(falhas))

falhas_por_ip = falhas["ip"].value_counts()
falhas_por_usuario = falhas["usuario"].value_counts()

print(falhas_por_ip)
print(falhas_por_usuario)