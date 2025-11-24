# medical_data_visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1) Importar los datos medical_examination.csv y asignarlos a df
df = pd.read_csv("medical_examination.csv")

# 2) Añadir columna 'overweight'
# calcular IMC: peso (kg) / (altura (m))**2
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 3) Normalizar cholesterol y gluc (0 = bueno, 1 = malo)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():
    """
    4-8) Dibujar la gráfica categórica:
       - Crear DataFrame para la gráfica usando pd.melt con las columnas:
         cholesterol, gluc, smoke, alco, active, overweight
       - Agrupar para obtener conteos por cardio, variable y valor
       - Usar sns.catplot para dibujar barras (un panel por cardio)
    Devuelve: fig (matplotlib.figure.Figure)
    """
    # 4) Crear df_cat con melt
    df_cat = pd.melt(df,
                     id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 5-6) Agrupar y formatear para contar los valores por cardio/variable/value
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7) Crear el gráfico: barras (y=total, hue=value, col=cardio)
    sns.set_style("whitegrid")
    g = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar',
        height=5,
        aspect=1
    )

    g.set_axis_labels("variable", "total")
    g.set_titles("cardio = {col_name}")
    g._legend.set_title("value")

    # 8) Obtener la figura y devolverla
    fig = g.fig
    return fig

def draw_heat_map():
    """
    9-15) Dibujar mapa de calor:
      - Limpiar datos según criterios
      - Calcular matriz de correlación
      - Crear máscara para triángulo superior
      - Dibujar heatmap con sns.heatmap
    Devuelve: fig (matplotlib.figure.Figure)
    """
    # 10) Limpiar datos
    df_heat = df.copy()

    # Filtrar: ap_lo <= ap_hi
    df_heat = df_heat[df_heat['ap_lo'] <= df_heat['ap_hi']]

    # Filtrar por percentiles para height y weight (2.5% - 97.5%)
    height_low = df_heat['height'].quantile(0.025)
    height_high = df_heat['height'].quantile(0.975)
    weight_low = df_heat['weight'].quantile(0.025)
    weight_high = df_heat['weight'].quantile(0.975)

    df_heat = df_heat[(df_heat['height'] >= height_low) & (df_heat['height'] <= height_high)]
    df_heat = df_heat[(df_heat['weight'] >= weight_low) & (df_heat['weight'] <= weight_high)]

    # 11) Calcular matriz de correlación
    corr = df_heat.corr()

    # 12) Generar máscara para triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 13) Configurar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # 14) Dibujar heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        linewidths=.5,
        vmax=0.3,
        center=0,
        square=True,
        cbar_kws={"shrink": .5},
        ax=ax
    )

    # 15) Devolver figura
    return fig

# Si se ejecuta como script, generar y guardar las figuras (para desarrollo)
if __name__ == "__main__":
    cat_fig = draw_cat_plot()
    cat_fig.savefig("catplot.png")

    heat_fig = draw_heat_map()
    heat_fig.savefig("heatmap.png")
    print("Figuras guardadas: catplot.png, heatmap.png")
