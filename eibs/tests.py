import pandas as pd

# Cargar los archivos de Excel
archivo1 = 'A11.xlsx'
archivo2 = 'A22.xlsx'

# Leer los archivos Excel (puedes ajustar las hojas o el rango de datos según sea necesario)
df1 = pd.read_excel(archivo1, skiprows=1)
df2 = pd.read_excel(archivo2, skiprows=1)

# Filtrar las columnas que nos interesan: Perfil (BTHF03), Menús (WSSSID) y Opciones (WSSIDE)
df1_filtered = df1[['BTHF03', 'WSSSID', 'WSSIDE']]
df2_filtered = df2[['BTHF03', 'WSSSID', 'WSSIDE']]

# Unir las tres columnas en un solo identificador único para comparar
df1_filtered['combo'] = df1_filtered['BTHF03'].astype(str) + '-' + df1_filtered['WSSSID'].astype(str) + '-' + df1_filtered['WSSIDE'].astype(str)
df2_filtered['combo'] = df2_filtered['BTHF03'].astype(str) + '-' + df2_filtered['WSSSID'].astype(str) + '-' + df2_filtered['WSSIDE'].astype(str)

# Comparar las opciones que están en el archivo1 pero no en archivo2 (excluidas)
excluidas = df1_filtered[~df1_filtered['combo'].isin(df2_filtered['combo'])]

# Comparar las opciones que están en el archivo2 pero no en archivo1 (incluidas)
incluidas = df2_filtered[~df2_filtered['combo'].isin(df1_filtered['combo'])]

# Crear un archivo Excel con diferentes hojas para incluidas y excluidas
with pd.ExcelWriter('comparacion_opciones.xlsx', engine='openpyxl') as writer:
    excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
    incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

print("Comparación completada. Resultados guardados en 'comparacion_opciones.xlsx' con dos hojas.")
