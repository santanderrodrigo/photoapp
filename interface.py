import fotoapp

imagen = None

def main():
    global imagen  # Accedemos a la variable imagen definida fuera de la función.

    while True:
        print('*******************************')
        print("¡Bienvenido a FotoAPP!")
        print('2023 - Developed by Rodrigo Santander')
        print('*******************************\n')

        if imagen is None:
            print("1. Cargar una imagen y seleccionar red social para redimensionar")
        else:
            print("1. Cargar otra imagen y seleccionar red social para redimensionar")
            print("2. Ver histograma")
            print("3. Ecualizar histograma")
            print("4. Previsualizar filtros")
            print("5. Aplicar filtro")
            print("6. Guardar la imagen")
            print("7. Descartar la imagen")
            print("8. Bocetar persona")
            print("9. Previsualizar")

        print("10. Salir")

        opcion = input("Selecciona una opción: ")

        if imagen is None:
            opciones_disponibles = ("1", "10")
        else:
            opciones_disponibles = ("1", "2", "3", "4", "5", "6", "7", "8", "9","10")

        if opcion in opciones_disponibles:
            if opcion == "1":
                # Cargar una imagen y seleccionar red social para redimensionar
                ruta_imagen = input("Ingresa la ruta de la imagen: ")
                print(fotoapp.getSocial())
                while True:
                    red_social = input('ingrese el nombre de la red social: ').capitalize().strip()
                    if red_social in fotoapp.getSocial():
                        break
                    print('Selección inválida')

                imagen = fotoapp.redimensionar_imagen(ruta_imagen, red_social)
                if not imagen == fotoapp.emptyImage():
                    print("Imagen cargada y redimensionada correctamente para", red_social)
                else:
                    print("Error al importar la imagen.")
                    imagen = None

            elif opcion == "2":
                # Ver histograma
                fotoapp.histograma(imagen)

            elif opcion == "3":
                # Ecualizar histograma
                imagen = fotoapp.ecualizar_histograma(imagen)
                print("Histograma ecualizado.")

            elif opcion == "4":
                # Previsualizar filtros
                print(fotoapp.getFilters())
                while True:
                    filtro_elegido = input("Selecciona un filtro : ").upper().strip()
                    if filtro_elegido in fotoapp.getFilters():
                        break
                    print('Selección inválida')
                preview_filters = fotoapp.filters_preview(imagen, filtro_elegido)
                preview_filters.show()

            elif opcion == "5":
                # Aplicar filtro
                print(fotoapp.getFilters())
                while True:
                    filtro_elegido = input("Selecciona un filtro : ").upper().strip()
                    if filtro_elegido in fotoapp.getFilters():
                        break
                    print('Selección inválida')
                imagen = fotoapp.aplicar_filtro(imagen, filtro_elegido)
                print("Filtro aplicado.")

            elif opcion == "6":
                # Guardar la imagen
                imagen.save('imagen_editada.jpg')
                print("Imagen guardada correctamente.")
                print('imagen_editada.jpg')

            elif opcion == "7":
                # Descartar la imagen
                imagen = None
                print("Imagen descartada.")

            elif opcion == "8":
                fotoapp.imagePreview(imagen)
                entrada = input('Ud es una IA y debe indicarnos si hay una persona en la imagen siguiente, escribe "S" para Sí: ').upper().strip()
                if entrada == "S" or  entrada == "SI" or entrada == "SÍ":
                    print('Nuestra IA profesional ha detectado una persona.')
                    fotoapp.crear_boceto_persona(imagen)
                    print('Se ha guardado la imagen como "boceto_persona.png"')
                else:
                    print('Nuestra IA avanzada no detectó una persona, prueba cargando otra imagen y ejecutando nuevamente la función')
            elif opcion == "9":
                fotoapp.imagePreview(imagen)

            elif opcion == "10":
                # Salir
                print("¡Hasta luego!")
                break

        else:
            print("Opción no válida. Por favor, elige una opción válida.")

if __name__ == "__main__":
    main()
