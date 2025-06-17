import pandas as pd
import numpy as np

# Parâmetros
start_filter = pd.to_datetime('2025-06-09')
end_filter = pd.to_datetime('2025-06-17')
margem_erro_percentual = 30  # Exemplo: 30% de margem de erro

# Leitura e alguns tratamentos dos dados
df = pd.read_csv('data/WF_failures_2025_06_17.csv')
df['completedDate'] = pd.to_datetime(df['completedDate'], errors='coerce')
df['status'] = df['status'].str.strip().str.upper()

# Filtrar falhas apenas no período desejado
df_failed = df[
    (df['status'] == 'FAILURE') &
    (df['completedDate'] >= start_filter) &
    (df['completedDate'] <= end_filter)
]

# Total de falhas
total_failures = len(df_failed)

# Intervalo de datas do período filtrado
start_date = df_failed['completedDate'].min()
end_date = df_failed['completedDate'].max()

# Total de dias, semanas e meses dentro do intervalo
total_days = (end_date - start_date).days + 1
total_weeks = np.ceil(total_days / 7)
total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

# Cálculo das médias sem margem
mean_daily_real = (total_failures / total_days) 
mean_weekly_real = (total_failures / total_weeks)
mean_monthly_real = (total_failures / total_months)

# Aplicando margem de erro (reduzindo o total de falhas antes das médias)
failures_ajustadas = total_failures * (1 - margem_erro_percentual / 100)

mean_daily_corrigida = (failures_ajustadas / total_days)
mean_weekly_corrigida = (failures_ajustadas / total_weeks)
mean_monthly_corrigida = (failures_ajustadas / total_months)

# Impressão dos resultados
print(f"Período analisado: {start_date.date()} até {end_date.date()} ({total_days} dias)")
print(f"Total de falhas analisadas: {total_failures}")
print(f"Média de falhas por dia (sem margem): {mean_daily_real:.2f}")
print(f"Média de falhas por semana (sem margem): {mean_weekly_real:.2f}")
print(f"Média de falhas por mês (sem margem): {mean_monthly_real:.2f}")

print("\n Após aplicar margem de erro de {}%:".format(margem_erro_percentual))
print(f"Média ajustada por dia: {mean_daily_corrigida:.2f}")
print(f"Média ajustada por semana: {mean_weekly_corrigida:.2f}")
print(f"Média ajustada por mês: {mean_monthly_corrigida:.2f}")
