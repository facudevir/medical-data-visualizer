# Visualizador de Datos Médicos

Proyecto que genera:
- `catplot.png`: gráfico categórico por `cardio`
- `heatmap.png`: mapa de calor de la correlación

Archivos principales:
- `medical_data_visualizer.py` : funciones `draw_cat_plot()` y `draw_heat_map()`
- `main.py` : script para generar las imágenes
- `medical_examination.csv` : dataset (subir al repo raíz)

Requisitos:
`pip install -r requirements.txt`

Ejecutar:
`python main.py`

Para pruebas unitarias (si existe `test_module.py`):
`python -m pytest` o `python test_module.py`
