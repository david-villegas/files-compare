import pandas as pd

# Función para leer el archivo ignorando la primera fila
def leer_archivo(ruta_archivo):
    # Leer el archivo saltando la primera fila (celda vacía)
    df = pd.read_excel(ruta_archivo, skiprows=1)
    return df

# Función para comparar los archivos y obtener perfiles con cambios en los menús
def comparar_archivos(archivo1, archivo2):
    # Leer los archivos
    df1 = leer_archivo(archivo1)
    df2 = leer_archivo(archivo2)

    # Agrupar los menús por perfil en cada archivo
    grupos1 = df1.groupby('BTHF03')['WSSSID'].apply(list).reset_index()
    grupos2 = df2.groupby('BTHF03')['WSSSID'].apply(list).reset_index()

    # Comparar los menús de cada perfil
    perfiles_unicos = pd.merge(grupos1, grupos2, on='BTHF03', how='outer', suffixes=('_archivo1', '_archivo2'))
    perfiles_cambiados = []

    for idx, row in perfiles_unicos.iterrows():
        menues1 = set(row['WSSSID_archivo1']) if pd.notna(row['WSSSID_archivo1']) else set()
        menues2 = set(row['WSSSID_archivo2']) if pd.notna(row['WSSSID_archivo2']) else set()

        # Verificar si hay cambios
        if menues1 != menues2:
            perfiles_cambiados.append({
                'Perfil': row['BTHF03'],
                'Menús en archivo1': menues1,
                'Menús en archivo2': menues2,
                'Menús quitados': menues1 - menues2,
                'Menús añadidos': menues2 - menues1
            })

    return pd.DataFrame(perfiles_cambiados)

# Función para guardar los resultados en un nuevo archivo Excel
def guardar_resultados(df, nombre_archivo_salida):
    df.to_excel(nombre_archivo_salida, index=False)

# Ejemplo de uso
archivo1 = 'A1.xlsx'
archivo2 = 'A2.xlsx'
resultado = comparar_archivos(archivo1, archivo2)

# Guardar los resultados en un archivo de salida
guardar_resultados(resultado, 'resultados_comparacion.xlsx')

print("La comparación ha finalizado y el archivo de resultados ha sido generado.")
