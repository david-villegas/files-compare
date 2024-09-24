import pandas as pd


# Leer los archivos Excel
df1 = pd.read_excel('A11.xlsx')
df2 = pd.read_excel('A22.xlsx')

# Agrupar por perfil y obtener los IDs de menú únicos en cada archivo
grouped1 = df1.groupby('BTHF03')['WSSSID'].unique()
grouped2 = df2.groupby('BTHF03')['WSSSID'].unique()

# Encontrar los perfiles que tienen nuevos o menos menús
perfiles_nuevos_menus = grouped2[~grouped2.isin(grouped1)].index
perfiles_menos_menus = grouped1[~grouped1.isin(grouped2)].index

# Imprimir los resultados
print("Perfiles a los que se les agregaron nuevos menús:")
print(perfiles_nuevos_menus)

print("\nPerfiles a los que se les quitaron menús:")
print(perfiles_menos_menus)

'''

import pandas as pd

def comparar_archivos_excel(archivo1, archivo2, hoja='Reporte Perfiles eIBS'):
  """Compara dos archivos Excel y genera un nuevo archivo con las diferencias en los perfiles.

  Args:
    archivo1: Nombre del primer archivo Excel.
    archivo2: Nombre del segundo archivo Excel.
    hoja: Nombre de la hoja en ambos archivos (opcional).

  Returns:
    None
  """

  # Leer los archivos Excel, saltando la primera fila
  df1 = pd.read_excel(archivo1, sheet_name=hoja, header=1)
  df2 = pd.read_excel(archivo2, sheet_name=hoja, header=1)

  # Agrupar por perfil y obtener los IDs de menú únicos en cada archivo
  grouped1 = df1.groupby('BTHF03')['WSSSID'].unique()
  grouped2 = df2.groupby('BTHF03')['WSSSID'].unique()

  # Encontrar los perfiles que tienen nuevos o menos menús
  perfiles_nuevos_menus = grouped2[~grouped2.isin(grouped1)].index
  perfiles_menos_menus = grouped1[~grouped1.isin(grouped2)].index

  # Crear un DataFrame con los resultados
  resultados = pd.DataFrame({'Perfil': perfiles_nuevos_menus.tolist() + perfiles_menos_menus.tolist(),
                             'Cambio': ['Nuevo menú'] * len(perfiles_nuevos_menus) + ['Menú eliminado'] * len(perfiles_menos_menus)})

  # Guardar los resultados en un nuevo archivo Excel
  resultados.to_excel('resultados_comparacion.xlsx', index=False)

# Ejemplo de uso:
comparar_archivos_excel('A1.xlsx', 'A2.xlsx')
'''