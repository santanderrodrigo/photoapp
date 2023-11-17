try:
    from PIL import Image, ImageFilter
    import cv2
    import matplotlib.pyplot as plt
    import numpy as np
    from urllib.parse import urlparse
    import requests
    from io import BytesIO
    import os
except ImportError as e:
    missing_modules = []
    if 'Image' not in dir():
        missing_modules.append("PIL (Pillow)")
    if 'cv2' not in dir():
        missing_modules.append("OpenCV (cv2)")
    if 'plt' not in dir():
        missing_modules.append("Matplotlib (plt)")
    if 'np' not in dir():
        missing_modules.append("NumPy (np)")
    if 'urlparse' not in dir():
        missing_modules.append("urllib.parse (urlparse)")
    if 'requests' not in dir():
        missing_modules.append("requests")
    if 'os' not in dir():
        missing_modules.append("os")
    if 'BytesIO' not in dir():
        missing_modules.append("io.BytesIO")
    print(f"Faltan las siguientes importaciones: {', '.join(missing_modules)}")


dimensiones_recomendadas = {
        "Youtube": (1280, 720),
        "Instagram": (1080, 1080),
        "Twitter": (1200, 675),
        "Facebook": (1200, 630)
    }
# Lista de nombres de filtros disponibles
filtros_disponibles = {
        "ORIGINAL": "Original",
        "BLUR": "Blur",
        "CONTOUR": "Contour",
        "DETAIL": "Detail",
        "EDGE_ENHANCE": "Edge Enhance",
        "EDGE_ENHANCE_MORE": "Edge Enhance More",
        "EMBOSS": "Emboss",
        "FIND_EDGES": "Find Edges",
        "SHARPEN": "Sharpen",
        "SMOOTH": "Smooth"
    }
def getSocial()->list:
    '''retorna una lista con los nombres de las redes sociales admitidas'''
    redes = []
    for red in dimensiones_recomendadas:
        redes.append(red)
    return redes

def getFilters()->list:
    '''retorna una lista con los nombres de los filtros admitidas'''
    filtros = []
    for filtro in filtros_disponibles:
        if not filtro == "ORIGINAL":
            filtros.append(filtro)
    return  filtros

def emptyImage()->Image:
    '''Esta función retorna una imagen en negro a partir de un array de ceros'''
    # Tamaño de la imagen
    ancho = 640
    alto = 480

    # Crear una matriz NumPy completamente negra
    imagen_negra = np.zeros((alto, ancho, 3), dtype=np.uint8)

    # Guardar la imagen negra en un archivo
    return Image.fromarray(imagen_negra)

def abrir_imagen(path: str)->Image:
    '''retorna la imagen a partir del path/url, en caso de error devuelve una imagen en negro'''
    parsed_url = urlparse(path)

    # Comprobar si la URL tiene un esquema (http, https, etc.) y un netloc (dominio)
    if parsed_url.scheme and parsed_url.netloc:
        try:
            response = requests.get(path)
            if response.status_code == 200:
                imagen_bytes = BytesIO(response.content)
                imagen = Image.open(imagen_bytes)
                return imagen
            else:
                print(f"No se pudo descargar la imagen desde la URL. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Ocurrió un error al abrir la imagen desde la URL: {e}")
    else:
        # Abrir la imagen
        try:
            imagen = Image.open(path)
            return imagen
        except Exception as e:
            print(f"Ocurrió un error al abrir la imagen desde la URL: {e}")

    return emptyImage()


def redimensionar_imagen(ruta_imagen:str, palabra_clave:str)->Image:
    '''retorna la imagen definida por ruta_imagen redimensionada para la red social elegida en el parametro palabra clave'''

    try:
        imagen = abrir_imagen(ruta_imagen)
        # Obtener las dimensiones recomendadas para la palabra clave
        dimensiones = dimensiones_recomendadas.get(palabra_clave)

        if dimensiones:
            # Redimensionar la imagen sin distorsión
            imagen.thumbnail(dimensiones)

            # Guardar la imagen redimensionada
            #imagen.save('temp_image.jpg')
            #print(f'La imagen se ha redimensionado correctamente para {palabra_clave}')
            return  imagen
        else:
            print('Palabra clave no válida. Las opciones son Youtube, Instagram, Twitter o Facebook.')

    except Exception as e:
        print(f'Ocurrió un error: {e}')

    #si llegamos hasta acá debemos retornar una imagen en en negro ya que algo falló
    return emptyImage()

def ecualizar_histograma(imagen:Image)->Image:
    '''Recibe una imagen como parametro y la retorna con el histograma equalizado'''
    if not isinstance(imagen, np.ndarray):
        if not isinstance(imagen, Image.Image):
            print('Imagen inválida o corrupta')
            return emptyImage()
        else:
            #convertimos la imagen en un array de np
            imagen = np.array(imagen)

    if len(imagen.shape) == 2: #asumimos que solo posee ancho y alto, por lo que es escala de grises
        # Si es una imagen monocromática (escala de grises)
        canal_b = imagen
        canal_g = imagen
        canal_r = imagen
    else:
        if len(imagen.shape) == 4: #asumimos que es RGBA
            # Dividir la imagen en sus canales de color (BGR)
            imagen = cv2.cvtColor(imagen, cv2.COLOR_RGBA2RGB)

        #separamos en canales RGB
        canal_b, canal_g, canal_r = cv2.split(imagen)

    # Ecualizar el histograma de cada canal de color
    canal_b_ecualizado = cv2.equalizeHist(canal_b)
    canal_g_ecualizado = cv2.equalizeHist(canal_g)
    canal_r_ecualizado = cv2.equalizeHist(canal_r)

    # Combinar los canales ecualizados para obtener la imagen ecualizada en color
    imagen_ecualizada = cv2.merge((canal_b_ecualizado, canal_g_ecualizado, canal_r_ecualizado))

    return Image.fromarray(imagen_ecualizada)

def aplicar_filtro_y_mostrar_preview(imagen: Image, filtro_elegido:str)->Image:
    ''''''
    imagen_filtrada = aplicar_filtro(imagen,filtro_elegido)
    imagen_filtrada.save(f'{filtro_elegido}.jpg')
    previews_image = filters_preview(imagen,filtro_elegido)
    previews_image.savefig('previsualizacion_filtros.png')

def aplicar_filtro(imagen: Image, filtro_elegido:str)->Image:
    '''Aplica el filtro_elegido sobre la imagen y retorna la imagen con el filtro aplicado'''
    if not isinstance(imagen, Image.Image):
        print('Imagen inválida o corrupta')
        return emptyImage()

    # Aplicar el filtro seleccionado
    if filtro_elegido in filtros_disponibles:
        imagen_filtrada = imagen.filter(getattr(ImageFilter, filtro_elegido))

        # Guardar la imagen filtrada
        #imagen_filtrada.save(f'{filtro_elegido}_filtrada.jpg')
        return imagen_filtrada

    else:
        print("Filtro no válido. Los filtros disponibles son:", getFilters())
        return emptyImage()
def filters_preview(imagen_original:Image, filtro_elegido:str)->plt:
    '''Retorna un matplotlib plot con todas las previsualñizaciones de todos los filtros disponibles
    marcando en rojo el filtro seleccionado como parametro filtro_elegido'''

    if not isinstance(imagen_original, Image.Image):
        print('Imagen inválida o corrupta')
        return emptyImage()

    if filtro_elegido in filtros_disponibles:
        #copiamos la imagen para no trabajr sobre ella misma y modificarla durante el preview
        imagen = imagen_original.copy()
        imagen.thumbnail((200, 200))

        imagen_filtrada = imagen.filter(getattr(ImageFilter, filtro_elegido))

        # Mostrar la imagen original y la imagen filtrada en una sola figura
        plt.figure(figsize=(15, 15))
        plt.subplot(3, 4, 1)
        plt.title(filtros_disponibles["ORIGINAL"])
        plt.imshow(imagen)
        plt.axis("off")

        for i, filtro in enumerate(filtros_disponibles.keys()):
            if filtro != "ORIGINAL":
                plt.subplot(3, 4, i +1)
                plt.title(filtros_disponibles[filtro], color='red' if filtro == filtro_elegido else 'black')
                plt.imshow(imagen.filter(getattr(ImageFilter, filtro)))
                plt.axis("off")

        # Guardar la figura que muestra las imágenes originales y filtradas
        #plt.savefig('imagenes_filtradas.png')
        # Mostrar la figura
        #plt.show()
        return plt
    else:
        print("Filtro no válido. Los filtros disponibles son:", getFilters())
        # Crear una figura y ejes vacíos
        fig, ax = plt.subplots()
        return plt

def plotpreview(plot):
    # Mostrar la imagen
    plot.show()

def imagePreview(imagen_original):
    if not isinstance(imagen_original, Image.Image):
        print('Imagen inválida o corrupta')
        return emptyImage()
    # Cargar la imagen en escala de grises
    imagen = np.array(imagen_original)

    # Mostrar la imagen
    plt.imshow(imagen)
    plt.axis('off')  # Para ocultar los ejes si lo prefieres
    plt.show()

def crear_boceto_persona(imagen_original,persona=True)->plt:
    if persona == False:
        print('No hay persona, ignorando boceto.')
        return emptyImage()

    if not isinstance(imagen_original, Image.Image):
        print('Imagen inválida o corrupta')
        return emptyImage()
    # Cargar la imagen en escala de grises
    imagen = np.array(imagen_original)

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar el detector de bordes Canny
    bordes = cv2.Canny(gris, 50, 150)

    # Visualizar la imagen original y la imagen con los bordes resaltados
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title('Imagen Original')

    plt.subplot(1, 2, 2)
    plt.imshow(bordes, cmap='gray')
    plt.title('Bordes Resaltados')

    # Guardar la figura que muestra la imagen original y el boceto
    plt.savefig('boceto_persona.png')

    return plt

def histograma(imagen: Image):

    imagen = np.array(imagen)
    hist, bins = np.histogram(imagen.flatten(), 256, [0, 256])

    # cumulative distribution function
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()

    plt.plot(cdf_normalized, color='b')
    plt.hist(imagen.flatten(), 256, [0, 256], color='r')
    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), loc='upper left')
    plt.show()

def tp_rutina(path_files = "",darkImage = 'darktest.jpg',lightimage= 'lightest.jpg',personTest= 'testpersona.jpg'):
    '''esta funcion hace un testeo rapido de las funciones de la libreria con las imagenes definidas'''
    # Rutina de pedidos del TP
    ########### PASO 1 ##################
    '''leer la imagen y redimencionarla'''
    print('Cargando imagen oscura...')
    ruta = path_files + darkImage  # Reemplaza con la ruta de tu imagen oscura
    print ("RUTA: ", ruta)
    print('Redimensionando para Instagram la imagen oscura')
    imagen = redimensionar_imagen(ruta, 'Instagram')

    print('\r Histograma \r')
    histograma(imagen)

    ########### PASO 2 ##################
    '''Ecualizar una imagen oscura'''
    print('\r Ecualizando imagen \r')
    imagen_ecualizada = ecualizar_histograma(imagen)
    # Mostrar la imagen original y la imagen ecualizada en una figura
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Imagen Oscura Original")
    plt.imshow(imagen)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Imagen Oscura Ecualizada")
    plt.imshow(imagen_ecualizada)
    plt.axis("off")

    # Guardar la figura que muestra ambas imágenes
    plt.savefig('imagen_original_vs_ecualizada_DARK.png')

    # Mostrar la figura
    plt.show()

    '''leer la imagen y redimencionarla'''
    print('Cargando imagen clara...')
    ruta2 = path_files + lightimage  # Reemplaza con la ruta de tu imagen oscura
    print('Redimensionando para Instagram la imagen clara')
    imagen2 = redimensionar_imagen(ruta2, 'Instagram')

    print('\r Histograma \r')
    histograma(imagen2)
    '''Ecualizar una imagen clara'''
    print('\r Ecualizando imagen \r')
    imagen_ecualizada = ecualizar_histograma(imagen2)
    # Mostrar la imagen original y la imagen ecualizada en una figura
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Imagen Clara Original")
    plt.imshow(imagen2)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Imagen Clara Ecualizada")
    plt.imshow(imagen_ecualizada)
    plt.axis("off")

    # Guardar la figura que muestra ambas imágenes
    plt.savefig('imagen_original_vs_ecualizada_LIGHT.png')

    # Mostrar la figura
    plt.show()

    ########### PASO 3 ##################

    aplicar_filtro_y_mostrar_preview(imagen, 'BLUR')
    aplicar_filtro_y_mostrar_preview(imagen2, 'BLUR')
    '''
    #aplique los 9 filtros de Pillow, indicar el seleccionado, guardar la imagen 
    print('\r Generando previsualización de los filtros para imagen oscura\r')
    previsualizacion_filtros = filters_preview(imagen, 'BLUR')
    previsualizacion_filtros.savefig('previsualizacion_filtros_darktest.png')
    # Mostrar la figura
    previsualizacion_filtros.show()

    #a la imagen clara
    #aplique los 9 filtros de Pillow, indicar el seleccionado, guardar la imagen
    print('\r Generando previsualización de los filtros para imagen clara\r')
    previsualizacion_filtros = filters_preview(imagen2, 'BLUR')
    previsualizacion_filtros.savefig('previsualizacion_filtros_lightest.png')
    # Mostrar la figura
    previsualizacion_filtros.show()
    '''


    ########### PASO 4 ##################
    '''leer la imagen y redimencionarla
    detectar contornos de una persona usando el filtro sobel'''
    print('\r Generando boceto de persona \r')
    ruta3 = path_files  +personTest  # Reemplaza con la ruta de tu imagen oscura
    imagen_persona = redimensionar_imagen(ruta3, 'Instagram')
    boceto1 = crear_boceto_persona(imagen_persona,True)
    plotpreview(boceto1)

#tp_rutina('testset/','darktest1.webp','lighttest1.webp','testpersona1.jpg')
#tp_rutina('testset/','darktest2.webp','lighttest2.webp','testpersona2.webp')