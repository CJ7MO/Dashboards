import requests
import os
#descargar archivo csv desde una URL
path= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%202/data/FuelConsumptionCo2.csv"
#url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv'
response = requests.get(path)

#el archivo se guardara en el directorio actual del proyecto
cwd = os.getcwd()
filename = 'FuelConsumptionCo2.csv'
filepath = os.path.join(cwd, filename)

# Verifique el estado de la respuesta HTTP
if response.status_code == 200:
    # Si la respuesta es exitosa (código 200), guarde el contenido en un archivo
    with open(filepath, 'wb') as f:
        f.write(response.content)
else:
    # Si la respuesta es fallida, imprima el código de estado de la respuesta
    print('Error al descargar el archivo: ', response.status_code)