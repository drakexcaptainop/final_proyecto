# para correr la pagina
1) instalar las dependencias en el archivo requirements.txt
2) navegar a la carpeta final_proyecto/proyecto_veterinaria
3) en una consola dentro de carpeta final_proyecto/proyecto_veterinaria ejecutar `python manage.py makemigrations`
4) en una consola dentro de carpeta final_proyecto/proyecto_veterinaria ejecutar `python manage.py migrate`
5) en una consola dentro de final_proyecto/proyecto_veterinaria ejecutar `python manage.py runserver`
6) abrir localhost:8000/main


#Para ejecutar sonar-scanner
- Añadir una variable de entorno llamada SONAR_TOKEN donde su valor es su token de SonarQube
- Tambien se puede añadir directamente el token dentro del archivo sonar-project.properties

# En caso de quere generar una llave de api
1) navegar a la carpeta final_proyecto/proyecto_veterinaria
2) en una consola dentro de final_proyecto/proyecto_veterinaria ejecutar `python manage.py shell`
3) copiar y pegar el codigo `from rest_framework_api_key.models import APIKey; api_key_obj, raw_key = APIKey.objects.create_key(name="test"); print(raw_key)`
4) la llave impresa es la llave de la api, uso ilimitado
