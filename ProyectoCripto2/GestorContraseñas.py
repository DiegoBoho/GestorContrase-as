import flet as ft
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Función para encriptar una contraseña utilizando AES
# Toma una contraseña y una llave como parámetros y devuelve la contraseña encriptada en formato base64
def encriptador(contraseña, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(contraseña.encode('utf-8'))
    print("cipher"+str(ciphertext)+"tag"+str(tag))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

# Función para desencriptar una contraseña previamente encriptada
# Toma la contraseña encriptada en base64 y la llave, y devuelve la contraseña desencriptada en texto plano
def desencriptador(encrypted_password, key):
    encrypted_data = base64.b64decode(encrypted_password)
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

# Función que define y gestiona la interfaz de administración de contraseñas
# Se encarga de la lógica para añadir, desencriptar y eliminar contraseñas
def administradorContraseñas(page, llaveEncriptacion):
    # Campos de entrada para usuario y contraseña, y la lista de contraseñas
    nombreUsuario_input = ft.TextField(label="Usuario")
    contraseña_input = ft.TextField(label="Contraseña", password=True)
    contraseña_list = ft.ListView(expand=True)

    # Función interna para encriptar y añadir una nueva contraseña a la lista
    def encriptarAgregarContraseñas(e):
        nombreUsuario = nombreUsuario_input.value
        contraseña = contraseña_input.value
        if nombreUsuario and contraseña:
            encrypted_password = encriptador(contraseña, llaveEncriptacion)

            # Texto para mostrar la contraseña desencriptada al usuario
            decrypted_text = ft.Text("")

            # Crear un item de lista con opciones para desencriptar y eliminar
            list_item = ft.ListTile(
                leading=ft.Icon(ft.icons.ALBUM),
                title=ft.Text(nombreUsuario, width=150),
                subtitle=ft.Text(encrypted_password, width=200),
                trailing=ft.Column(
                    [
                        ft.TextButton("Desencriptar", on_click=lambda _, pw=encrypted_password: desencriptador_accion(
                            pw, decrypted_text)),
                        ft.TextButton("Eliminar", on_click=lambda _: eliminar_contraseña_accion(list_item))
                    ],
                    spacing=10  # Espacio entre botones
                )
            )

            # Añadir el item a la lista de contraseñas y actualizar la página
            contraseña_list.controls.append(ft.Column([list_item, decrypted_text]))
            page.update()

            # Limpiar campos de entrada
            nombreUsuario_input.value = ""
            contraseña_input.value = ""
            page.update()

    # Función interna para desencriptar una contraseña y mostrarla en la interfaz
    def desencriptador_accion(encrypted_password, label):
        decrypted_password = desencriptador(encrypted_password, llaveEncriptacion)
        label.value = decrypted_password
        page.update()

    # Función interna para eliminar un elemento de la lista de contraseñas
    def eliminar_contraseña_accion(item):
        # Elimina el item de la lista
        for control in contraseña_list.controls:
            if isinstance(control, ft.Column) and control.controls[0] == item:
                contraseña_list.controls.remove(control)
                break
        page.update()

    # Botón para encriptar y agregar una nueva contraseña
    botonEncriptar = ft.ElevatedButton("Encriptar y Agregar", on_click=encriptarAgregarContraseñas)

    # Añadir controles de la página a la interfaz
    page.controls.extend([
        nombreUsuario_input,
        contraseña_input,
        botonEncriptar,
        contraseña_list
    ])
    page.update()

# Vista de login de la aplicación
# Muestra la interfaz de login y permite la autenticación del usuario
def menuIngreso(page):
    # Genera una llave de encriptación aleatoria para la sesión
    llaveEncriptacion = get_random_bytes(16)
    page.title = "Login"

    # Campos de entrada para usuario y contraseña
    nombreUsuario_input = ft.TextField(label="Usuario")
    contraseña_input = ft.TextField(label="Contraseña", password=True)

    # Acción de autenticación al presionar el botón de login
    def ingresoAccion(e):
        if nombreUsuario_input.value == "admin" and contraseña_input.value == "1234":  # Ejemplo de credenciales
            # Si las credenciales son correctas, muestra la interfaz de administración de contraseñas
            page.controls.clear()
            administradorContraseñas(page, llaveEncriptacion)
        else:
            # Muestra un mensaje de error si las credenciales no coinciden
            page.controls.append(ft.Text("Usuario o contraseña incorrectos"))
            page.update()

    # Botón para iniciar sesión
    login_button = ft.ElevatedButton("Login", on_click=ingresoAccion)

    # Añadir controles de login a la interfaz
    page.controls.extend([
        nombreUsuario_input,
        contraseña_input,
        login_button
    ])
    page.update()

# Función principal que inicia la aplicación
# Llama a la vista de login para comenzar el flujo de la aplicación
def main(page: ft.Page):
    menuIngreso(page)

# Iniciar la aplicación llamando a la función main
ft.app(target=main)
