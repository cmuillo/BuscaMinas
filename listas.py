

def aplanar(lista):
    if not lista:
        return []
    primero = lista[0]
    resto = lista[1:]
    if isinstance(primero, list):
        aplanar(primero)
    else:
        print(primero)
    aplanar(resto)


# Prueba
entrada = ["foto.png", ["docs", "tarea.docs", "2pdf.pdf","video.mp4"]]

print("Entrada:", entrada)
aplanar(entrada)

