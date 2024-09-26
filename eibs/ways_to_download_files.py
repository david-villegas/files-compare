'''
Estas son 3 maneras de generar la descarga de un archivo una vez generado el reporte a través de DJANGO
utilizando el sistema de archivos del S.O.
'''
# A través de import os y settings de Django
import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
import os

# Crear un archivo Excel en el sistema de archivos
file_name = 'comparacion_opciones.xlsx'
file_path = os.path.join(settings.MEDIA_ROOT, file_name)  # Guardar en la carpeta 'media'

with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
    incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

# Generar la URL de descarga
file_url = os.path.join(settings.MEDIA_URL, file_name)

return render(request, 'comparar_excel.html', {'file_url': file_url})

return render(request, 'comparar_excel.html') # cierre de la función

###########################################################################################################################

#Otra manera de hacerlo con Sistema de Archivos
from django.core.files.storage import FileSystemStorage

# Guardar los resultados en un archivo Excel
output_file = 'resultados_comparacion.xlsx'
changes.to_excel(output_file, index=False)

# Almacenar el archivo en el sistema de archivos
fs = FileSystemStorage()
filename = fs.save(output_file, open(output_file, 'rb'))
file_url = fs.url(filename)

return render(request, 'eibs/comparar.html', {'file_url': file_url})

return render(request, 'eibs/comparar.html') # cierre de la función

###########################################################################################################################
# Esta es Descarga Directa sin almacenar en el sistema de archivos del S.O.

from io import BytesIO

# Crear un archivo Excel en memoria con diferentes hojas para incluidas y excluidas
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    excluidas.to_excel(writer, sheet_name='Opciones Excluidas', index=False)
    incluidas.to_excel(writer, sheet_name='Opciones Incluidas', index=False)

# Preparar el archivo para la descarga
output.seek(0)
response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
response['Content-Disposition'] = 'attachment; filename=comparacion_opciones.xlsx'

return response

return render(request, 'comparar_excel.html') # cierre de la función
