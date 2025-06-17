import matplotlib.pyplot as plt
import matplotlib.cm as cm
from analise import analisar_falhas
import pandas as pd
import os

# Parâmetros
csv_path = 'data/WF_failures_2025_06_17.csv'
start_filter = pd.to_datetime('2024-06-17')
end_filter = pd.to_datetime('2025-06-17')
margem_erro_percentual = 30

# Executando a análise
resultados = analisar_falhas(csv_path, start_filter, end_filter, margem_erro_percentual)

# Verifica se a pasta de imagens existe, se não, cria uma
output_dir = 'generated_images'
os.makedirs(output_dir, exist_ok=True)

# ======================GRÁFICO DE BARRAS======================
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
ax.bar(x, sem_margem, width, color='#008000', label='Without Margin')
ax.bar([p + width for p in x], com_margem, width, color="#64E54A", label='With margin of error 30%')

ax.set_xlabel('Period')
ax.set_ylabel('Mean of Failure')
ax.set_title('Compare the averages - (1 year period)')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(labels)
ax.legend()

plt.tight_layout()
output_path_barras = os.path.join(output_dir, 'dashboard.png')
plt.savefig(output_path_barras)
plt.close()

# ======================GRÁFICO DE LINHA======================
fig, ax = plt.subplots()

ax.plot(labels, sem_margem, marker='o', linestyle='-', color='#008000', label='Without Margin')
ax.plot(labels, com_margem, marker='o', linestyle='--', color="#64E54A", label='With Error Margin (30%)')

ax.set_xlabel('Period')
ax.set_ylabel('Mean of Failure')
ax.set_title('Line Chart - (1 year period)')
ax.legend()

plt.tight_layout()
output_path_linha = os.path.join(output_dir, 'dashboard_line.png')
plt.savefig(output_path_linha)
plt.close()

# ======================GRÁFICO DE PIZZA======================
top_10_df = resultados['top_10_robos']

# Verifica se o DataFrame não está vazio
if not top_10_df.empty:
    labels_pizza = top_10_df['workflowName']
    sizes_pizza = top_10_df['total_falhas']

    fig, ax = plt.subplots(figsize=(8, 8))
    colors_pizza = plt.cm.tab10.colors  # Usando uma paleta de até 10 cores

    ax.pie(
        sizes_pizza,
        labels=labels_pizza,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors_pizza
    )

    ax.set_title('Top 10 Workflows with Most Failures - (1 year period)')
    ax.axis('equal')  # Deixar a pizza circular

    output_path_pizza = os.path.join(output_dir, 'dashboard_pizza.png')
    plt.savefig(output_path_pizza, bbox_inches='tight')
    plt.close()

    print(f"Saved pie chart: {output_path_pizza}")
else:
    print("No failures found for the selected period. Skipping pie chart.")

# ====================== FINAL ======================
print(f"Saved bar chart: {output_path_barras}")
print(f"Saved line chart: {output_path_linha}")
