from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.

def comparar_archivos(request):
    if request.method == 'POST' and request.FILES['archivo1'] and request.FILES['archivo2']:
        archivo1 = request.FILES['archivo1']
        archivo2 = request.FILES['archivo2']

        # Leer los archivos, saltando la primera celda
        df1 = pd.read_excel(archivo1, skiprows=1)
        df2 = pd.read_excel(archivo2, skiprows=1)

        # Crear un conjunto de perfiles y menús para cada archivo
        perfiles_menus1 = df1.groupby('BTHF03')['WSSSID'].apply(set).reset_index()
        perfiles_menus2 = df2.groupby('BTHF03')['WSSSID'].apply(set).reset_index()

        # Merge de los dos dataframes para comparar
        merged = pd.merge(perfiles_menus1, perfiles_menus2, on='BTHF03', how='outer', suffixes=('_A1', '_A2'))

        # Identificar cambios en los menús
        merged['agregados'] = merged.apply(lambda row: row['WSSSID_A2'] - row['WSSSID_A1'] if pd.notna(row['WSSSID_A1']) and pd.notna(row['WSSSID_A2']) else set(), axis=1)
        merged['eliminados'] = merged.apply(lambda row: row['WSSSID_A1'] - row['WSSSID_A2'] if pd.notna(row['WSSSID_A1']) and pd.notna(row['WSSSID_A2']) else set(), axis=1)

        # Filtrar perfiles con cambios
        changes = merged[(merged['agregados'].apply(len) > 0) | (merged['eliminados'].apply(len) > 0)]

        # Guardar los resultados en un archivo Excel
        output_file = 'resultados_comparacion.xlsx'
        changes.to_excel(output_file, index=False)

        # Almacenar el archivo en el sistema de archivos
        fs = FileSystemStorage()
        filename = fs.save(output_file, open(output_file, 'rb'))
        file_url = fs.url(filename)

        return render(request, 'eibs/comparar.html', {'file_url': file_url})

    return render(request, 'eibs/comparar.html')

def index(request):
    return render(request, 'eibs/index.html')
