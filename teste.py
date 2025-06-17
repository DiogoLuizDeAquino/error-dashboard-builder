import pandas as pd

# Leitura do CSV
df = pd.read_csv('data/Request_2025_06_16.csv')
df['completedDate'] = pd.to_datetime(df['completedDate'], errors='coerce')
df['status'] = df['status'].str.strip().str.upper()

# Filtro por período (2021 a 2025) e apenas falhas
df_failed = df[
    (df['status'] == 'FAILURE') &
    (df['completedDate'] >= '2021-01-01') &
    (df['completedDate'] <= '2025-12-31')
]

# Quantidade de falhas no período
total_failures_periodo = len(df_failed)

print(f"Total de falhas entre 2021 e 2025: {total_failures_periodo}")
