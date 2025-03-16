
from cryptography.fernet import Fernet

# Clave generada (guárdala en un lugar seguro)
key = b'hLE4Ni7Yl5I9ru0n8iczCseAuOwDaaHv21xL-9mi2dE='
cipher_suite = Fernet(key)

def encrypt_data(data):
    """
    Cifra los datos proporcionados.
    
    Parámetros:
        data (str o bytes): Los datos que se desean cifrar.
    
    Retorna:
        bytes: Los datos cifrados.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')  # Convierte el string a bytes si es necesario
    encrypted_data = cipher_suite.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data):
    """
    Descifra los datos proporcionados.
    
    Parámetros:
        encrypted_data (bytes): Los datos cifrados que se desean descifrar.
    
    Retorna:
        str: Los datos descifrados en formato string.
    """
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')  # Convierte los bytes a string

# Ejemplo de uso (puedes eliminarlo después de probar)
if __name__ == "__main__":
    # Cifrar un dato de ejemplo
    texto_plano = "Hola, esto es un secreto."
    texto_cifrado = encrypt_data(texto_plano)
    print("Texto cifrado:", texto_cifrado)

    # Descifrar el dato
    texto_descifrado = decrypt_data(texto_cifrado)
    print("Texto descifrado:", texto_descifrado)


