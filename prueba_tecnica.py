import os
import datetime
import json
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
#Token de GH propio sin revelar
gh_token = os.environ.get("GITHUB_TOKEN")
#Fragmentos de url para estructurar más fácil los requests
url_base = "https://api.github.com"
repo_nombre = "bitcoin-educational-content"
repo_owner = "jramos0"

#Recibe la información como parámetros para generar el .md
def crear_markdown(titulo_archivo, link_archivo, descripcion_archivo):
    content = f"#{titulo_archivo}\n\n**Link: ** {link_archivo}\n\n**Descripción: **{descripcion_archivo}"
    return content

#Crea una nueva rama
def crear_nueva_rama(rama_base, nombre_nueva_rama):
    #Busca el hash de la última rama
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/git/ref/heads/{rama_base}"
    headers = {"Authorization": f"token {gh_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    sha_rama_base = response.json()["object"]["sha"]

    #Crea la nueva rama según el nombre que recibe como parámetro a partir de la rama base
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/git/refs"
    data = {
        "ref": f"refs/heads/{nombre_nueva_rama}",
        "sha": sha_rama_base,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    #Confirmación
    print(f"Se creó la rama '{nombre_nueva_rama}' exitosamente.")

#Crea o actualiza el archivo .md
def crear_o_actualizar_archivo(nombre_rama, direccion_archivo, contenido_archivo, commit):
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/contents/{direccion_archivo}"
    headers = {"Authorization": f"token {gh_token}"}
    #Revisa si el archivo ya existe
    get_response = requests.get(url, headers=headers, params={"ref": nombre_rama})
    if get_response.status_code == 200:
        sha_archivo = get_response.json()["sha"]
    else:
        sha_archivo = None

    #Crea o actualiza el archivo
    data = {
        "message": commit,
        "content": base64.b64encode(contenido_archivo.encode()).decode(),
        "branch": nombre_rama,
    }
    if sha_archivo:
        data["sha"] = sha_archivo

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    #Confirmación
    print(f"Archivo '{direccion_archivo}' creado/actualizado exitosamente en la rama '{nombre_rama}'.")

#Crea el PullRequest
def crear_pull_request(rama_base, rama_head, titulo_pr, contenido_pr):
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/pulls"
    headers = {"Authorization": f"token {gh_token}"}
    data = {
        "title": titulo_pr,
        "body": contenido_pr,
        "head": rama_head,
        "base": rama_base,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    pr_data = response.json()
    print(f"Pull Request creado exitosamente: {pr_data['html_url']}")
    return pr_data

#Muestra la información del PR recién creado
def confirmacion_pr(pr):
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/pulls/{pr['number']}"
    headers = {"Authorization": f"token {gh_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    #Muestra la información importante del PR que se acaba de crear
    pr_info = response.json()
    print(f"Pull Request #{pr_info['number']}\nTítulo: {pr_info['title']}\nDescripción: {pr_info['body']}\nLink: ({pr_info['html_url']})")

#Revisa PullRequests activos
def pull_requests_activos():
    url = f"{url_base}/repos/{repo_owner}/{repo_nombre}/pulls?state=open"
    headers = {"Authorization": f"token {gh_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    pull_requests = response.json()
    #En caso de que no hayan PRs abiertos, corta la ejecución de la función
    if not pull_requests:
        print("No hay Pull Requests abiertos.")
        return
    #Recorre el json de la response y muestra el número, título y link de los PRs abiertos
    print("Pull Requests abiertos:")
    for pr in pull_requests:
        print(f"- #{pr['number']}: {pr['title']} ({pr['html_url']})")

#Recepción de datos y llamadas a las funciones correspondientes (control del programa)
if __name__ == "__main__":
    #Recibe los datos para el .md desde la consola
    titulo = input("Ingrese el título del recurso: ")
    link = input("Ingrese el enlace al recurso: ")
    descripcion = input("Agregue una breve descripción del recurso: ")

    #Declaración de parámetros a usar para los requests
    rama_base = "new-resources"
    nombre_nueva_rama = "features/add-content-" + titulo.replace(' ', '-').replace('/', '_').lower() + datetime.datetime.now().strftime("%m%d%H%M")

    #Llama a los métodos en el orden correspondiente y controla cualquier posible excepción
    try:
        #Crea el contenido para el archivo .md
        content = crear_markdown(titulo, link, descripcion)
        #Crea una nueva rama
        crear_nueva_rama(rama_base, nombre_nueva_rama)
        #Crea el archivo .md
        nombre_archivo = titulo.replace(' ', '-').replace('/', '_').lower() + ".md" #Para darle el formato al nombre y agregar la extensión
        direccion_archivo = f"resources/{nombre_archivo}"
        commit = f"Agregar: {nombre_archivo}"
        crear_o_actualizar_archivo(nombre_nueva_rama, direccion_archivo, content, commit)

        #Crea la descripción del PR
        titulo_pr = f"Agrega el recurso: {titulo}"
        contenido_pr = f"Este PR agrega el recurso: \n\n* **Título: {titulo}**\n* **Link: {link}**\n* **Descripción: {descripcion}**\n"
        #LLama al método para crear el PR
        pr = crear_pull_request(rama_base, nombre_nueva_rama, titulo_pr, contenido_pr)

        #Imprime la información respecto al PR recién creado
        print("---------------------------Información---------------------------")
        confirmacion_pr(pr)

        #En caso de que el usuario quiera ver información referente a todos los pr abiertos en el repo
        respuesta = input("¿Le gustaría ver el listado de todos los PullRequests abiertos? [y/n]")
        if respuesta.lower() == "y":
            pull_requests_activos()
        elif respuesta.lower() == "n":
            print("Hasta la próxima!!")
        else:
            print("Respuesta no válida")
    except requests.exceptions.HTTPError as e:
            print(e)
    except Exception as e:
        print(e)