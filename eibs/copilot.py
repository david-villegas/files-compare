# ESTE ES EL CÓDIGO QUE FUNCIONO A LA PERFECCIÓN

import pandas as pd

# Leer los archivos, saltando la primera celda
file1 = pd.read_excel('A1.xlsx', skiprows=1)
file2 = pd.read_excel('A2.xlsx', skiprows=1)

# Crear un conjunto de perfiles y menús para cada archivo
perfiles_menus1 = file1.groupby('BTHF03')['WSSSID'].apply(set).reset_index()
perfiles_menus2 = file2.groupby('BTHF03')['WSSSID'].apply(set).reset_index()

# Merge de los dos dataframes para comparar
merged = pd.merge(perfiles_menus1, perfiles_menus2, on='BTHF03', how='outer', suffixes=('_file1', '_file2'))

# Identificar cambios en los menús
merged['added_menus'] = merged.apply(lambda row: row['WSSSID_file2'] - row['WSSSID_file1'] if pd.notna(row['WSSSID_file1']) and pd.notna(row['WSSSID_file2']) else set(), axis=1)
merged['removed_menus'] = merged.apply(lambda row: row['WSSSID_file1'] - row['WSSSID_file2'] if pd.notna(row['WSSSID_file1']) and pd.notna(row['WSSSID_file2']) else set(), axis=1)

# Filtrar perfiles con cambios
changes = merged[(merged['added_menus'].apply(len) > 0) | (merged['removed_menus'].apply(len) > 0)]

# Guardar los resultados en un archivo Excel
changes.to_excel('resultados_comparacion.xlsx', index=False)

print("Comparación completada y resultados guardados en 'resultados_comparacion.xlsx'")
