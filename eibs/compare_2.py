import pandas as pd

# Leer los archivos Excel
df1 = pd.read_excel('A1.xlsx')
df2 = pd.read_excel('A2.xlsx')

# Comparar por fila (ejemplo)
diferencias = df1[~df1.isin(df2)]

# Guardar las diferencias en un nuevo archivo
diferencias.to_excel('diferencias.xlsx', index=False)