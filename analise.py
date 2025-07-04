import pandas as pd
import numpy as np

def analisar_falhas(csv_path, start_filter, end_filter, margem_erro_percentual):
    # Leitura e tratamentos
    df = pd.read_csv(csv_path)
    df['completedDate'] = pd.to_datetime(df['completedDate'], errors='coerce')
    df['status'] = df['status'].str.strip().str.upper()

    # Filtrar apenas falhas dentro do período
    df_failed = df[
        (df['status'] == 'FAILURE') &
        (df['completedDate'] >= start_filter) &
        (df['completedDate'] <= end_filter)
    ]

    total_failures = len(df_failed)
    start_date = df_failed['completedDate'].min()
    end_date = df_failed['completedDate'].max()

    total_days = (end_date - start_date).days + 1
    total_weeks = np.ceil(total_days / 7)
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1

    mean_daily_real = total_failures / total_days if total_days > 0 else 0
    mean_weekly_real = total_failures / total_weeks if total_weeks > 0 else 0
    mean_monthly_real = total_failures / total_months if total_months > 0 else 0

    failures_ajustadas = total_failures * (1 - margem_erro_percentual / 100)
    mean_daily_corrigida = failures_ajustadas / total_days if total_days > 0 else 0
    mean_weekly_corrigida = failures_ajustadas / total_weeks if total_weeks > 0 else 0
    mean_monthly_corrigida = failures_ajustadas / total_months if total_months > 0 else 0

    # Top 10 workflows que mais apresentam falhas
    top_10_robos = (
    df_failed['workflowName']
    .value_counts()
    .head(10)
    .reset_index(name='total_falhas')
    .rename(columns={'index': 'workflowName'})
)

    resultados = {
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'total_failures': total_failures,
        'mean_daily_real': mean_daily_real,
        'mean_weekly_real': mean_weekly_real,
        'mean_monthly_real': mean_monthly_real,
        'mean_daily_corrigida': mean_daily_corrigida,
        'mean_weekly_corrigida': mean_weekly_corrigida,
        'mean_monthly_corrigida': mean_monthly_corrigida,
        'margem_erro_percentual': margem_erro_percentual,
        'top_10_robos': top_10_robos
    }

    return resultados
