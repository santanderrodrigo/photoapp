import unittest
from unittest.mock import patch
from io import StringIO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from fotoapp import getSocial, getFilters, emptyImage, abrir_imagen, redimensionar_imagen, ecualizar_histograma, aplicar_filtro, filters_preview, crear_boceto_persona_, imagePreview, crear_boceto_persona, histograma
'''
Este modulo es para hacer una bateria de pruebas muy básicas sobre las funciones de fotoapp.py
Me gustaría poder desarrollarlo más, ya que es algo que siempre me gusta realizar testing sobre 
mis propias aplicaciones.
'''
class TestFunctions(unittest.TestCase):
    def test_getSocial(self):
        '''debe devolver una lista con al menos un elemento'''
        redes = getSocial()
        self.assertTrue(isinstance(redes, list) and len(redes) > 0)

    def test_getFilters(self):
        '''debe devolver una lista con al menos un elemento'''
        filtros = getFilters()
        self.assertTrue(isinstance(filtros, list) and len(filtros) > 0)

    def test_emptyImage(self):
        '''debe devolver una imagen'''
        imagen = emptyImage()
        self.assertIsInstance(imagen, Image.Image)

    def test_abrir_imagen(self):
        '''debe devolver una imagen como respuesta'''
        # Mock para simular entrada de usuario
        with patch('builtins.input', return_value='testset/testpersona1.jpg'):
            imagen = abrir_imagen(input("Ingrese la ruta de la imagen: "))
            self.assertIsInstance(imagen, Image.Image)

    def test_abrir_imagen_erronea(self):
        '''debe devolver una imagen en negro emptyImage'''
        # Mock para simular entrada de usuario
        with patch('builtins.input', return_value='3asd32a1sd31a2sf.jpg'):
            imagen = abrir_imagen(input("Ingrese la ruta de la imagen: "))
            self.assertTrue(isinstance(imagen, Image.Image) and imagen == emptyImage())

    def test_redimensionar_imagen(self):
        '''debe devolver una imagen mas chica que la imagen original'''
        imagen_path = 'testset/largetest.jpg'
        palabra_clave = 'Youtube'
        imagen = abrir_imagen(imagen_path)
        imagen_redimensionada = redimensionar_imagen(imagen_path, palabra_clave)
        ancho_img1, alto_img1 = imagen.size
        ancho_img2, alto_img2 = imagen_redimensionada.size
        self.assertFalse((ancho_img1 * alto_img1)  ==(ancho_img2 * alto_img2))

    def test_ecualizar_histograma(self):
        '''deberiamos verificar si la imagen está ecualizada y si nos devuelve una imagen'''
        #ToDo -> chequear equalizacion
        imagen_original = Image.open('testset/testpersona1.jpg')
        imagen_ecualizada = ecualizar_histograma(imagen_original)
        self.assertIsInstance(imagen_ecualizada, Image.Image)

    def test_aplicar_filtro(self):
        imagen_original = Image.open('testset/testpersona1.jpg')
        # ToDo -> chequear que ambas imágenes sean diferentes para validar la aplicacion del filtro,
        #  ... investigar ...
        filtro_elegido = 'BLUR'
        imagen_filtrada = aplicar_filtro(imagen_original, filtro_elegido)
        self.assertIsInstance(imagen_filtrada, Image.Image)

    def test_filters_preview(self):
        ''''debe retornar un plt y mostrar el plot'''
        imagen_original = Image.open('testset/testpersona1.jpg')
        filtro_elegido = 'BLUR'
        plt = filters_preview(imagen_original, filtro_elegido)
        # minimo nos aseguramos que nos retorne algo
        #ToDo
        self.assertIsNotNone(plt)

    def test_crear_boceto_persona(self):
        ''''debe retornar un plt, guardar la imagen y mostrar el plt'''
        imagen_original = Image.open('testset/testpersona1.jpg')
        plt = crear_boceto_persona(imagen_original)
        #minimo nos aseguramos que nos retorne algo
        # ToDo
        self.assertIsNotNone(plt)


if __name__ == '__main__':
    unittest.main()