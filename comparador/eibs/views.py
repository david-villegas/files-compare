from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import os

# Create your views here.
def index(request):
    return render(request, 'eibs/index.html')


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


def comparar_opciones(request):
    if request.method == 'POST' and request.FILES['archivo1'] and request.FILES['archivo2']:
        archivo1 = request.FILES['archivo1']
        archivo2 = request.FILES['archivo2']

        # Leer los archivos, saltando la primera celda
        df1 = pd.read_excel(archivo1, skiprows=1)
        df2 = pd.read_excel(archivo2, skiprows=1)

        # Filtrar las columnas que nos interesan: Perfil (BTHF03), Menús (WSSSID) y Opciones (WSSIDE)
        df1_filtered = df1[['BTHF03', 'WSSSID', 'WSSIDE']]
        df2_filtered = df2[['BTHF03', 'WSSSID', 'WSSIDE']]

        # Unir las tres columnas en un solo identificador único para comparar
        df1_filtered['identificador'] = df1_filtered['BTHF03'].astype(str) + '-' + df1_filtered['WSSSID'].astype(str) + '-' + df1_filtered['WSSIDE'].astype(str)
        df2_filtered['identificador'] = df2_filtered['BTHF03'].astype(str) + '-' + df2_filtered['WSSSID'].astype(str) + '-' + df2_filtered['WSSIDE'].astype(str)

        # Comparar las opciones que están en el archivo1 pero no en archivo2 (excluidas)
        excluidas = df1_filtered[~df1_filtered['identificador'].isin(df2_filtered['identificador'])]

        # Comparar las opciones que están en el archivo2 pero no en archivo1 (incluidas)
        incluidas = df2_filtered[~df2_filtered['identificador'].isin(df1_filtered['identificador'])]

        # Almacenar el archivo en el sistema de archivos
        output_file = 'resultados_comparacion.xlsx'

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
            incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

        fs = FileSystemStorage()
        filename = fs.save(output_file, open(output_file, 'rb'))
        file_url = fs.url(filename)

        return render(request, 'eibs/opciones.html', {'file_url': file_url})

################################# MODO 1 GENERAR DESCARGA DE REPORTE ################################

        # # Crear un archivo Excel con diferentes hojas para incluidas y excluidas
        # with pd.ExcelWriter('comparacion_opciones.xlsx', engine='openpyxl') as writer:
        #     excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
        #     incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

        #  # Crear un archivo Excel en memoria con diferentes hojas para incluidas y excluidas
        # output = BytesIO()
        # with pd.ExcelWriter(output, engine='openpyxl') as writer:
        #     excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
        #     incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

        # # Preparar el archivo para la descarga
        # output.seek(0)
        # response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=comparacion_opciones.xlsx'

        # return response

################################# MODO 2 GENERAR DESCARGA DE REPORTE ################################
         # Crear un archivo Excel en el sistema de archivos
        # file_name = 'comparacion_opciones.xlsx'
        # file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # Guardar en la carpeta 'media'

        # with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        #     excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
        #     incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

        # # Generar la URL de descarga
        # file_url = os.path.join(settings.MEDIA_URL, file_name)

        # return render(request, 'eibs/opciones.html', {'file_url': file_url})

    return render(request, 'eibs/opciones.html')
