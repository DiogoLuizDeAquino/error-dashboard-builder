import matplotlib.pyplot as plt
from analise import analisar_falhas
import pandas as pd
import os as os

# Parâmetros
csv_path = 'data/WF_failures_2025_06_17.csv'
start_filter = pd.to_datetime('2025-06-09')
end_filter = pd.to_datetime('2025-06-17')
margem_erro_percentual = 30

# Executando a análise
resultados = analisar_falhas(csv_path, start_filter, end_filter, margem_erro_percentual)

# Exemplo de um gráfico de barras comparando as médias
labels = ['Day', 'Week', 'Month']
sem_margem = [
    resultados['mean_daily_real'],
    resultados['mean_weekly_real'],
    resultados['mean_monthly_real']
]
com_margem = [
    resultados['mean_daily_corrigida'],
    resultados['mean_weekly_corrigida'],
    resultados['mean_monthly_corrigida']
]

x = range(len(labels))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x, sem_margem, width, label='Without Margin')
ax.bar([p + width for p in x], com_margem, width, label='With margin of error 30%')

ax.set_xlabel('Period')
ax.set_ylabel('Mean of Failure')
ax.set_title('Compare the averages - Failure per Period')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(labels)
ax.legend()

plt.tight_layout()

#Verifica se a pasta de imagens existe, se não, cria uma.
output_dir = 'generated_images'
os.makedirs(output_dir, exist_ok= True)

#Salva o dashboard gerado na pasta.
output_path = os.path.join(output_dir, 'dashboard.png')

plt.savefig(output_path)

fig, ax = plt.subplots()

ax.plot(labels, sem_margem, marker='o', linestyle='-', color='blue', label='Without Margin')
ax.plot(labels, com_margem, marker='o', linestyle='--', color='orange', label='With Error Margin (30%)')

ax.set_xlabel('Period')
ax.set_ylabel('Mean of Failure')
ax.set_title('Failure Trend (Line Chart)')
ax.legend()

plt.tight_layout()
output_path_onda = os.path.join(output_dir, 'dashboard_line.png')
plt.savefig(output_path_onda)
plt.close()

print(f"Saved images: {output_path}")