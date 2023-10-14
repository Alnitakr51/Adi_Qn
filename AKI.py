
import tkinter as tk
from tkinter import messagebox
import json
import os

personajes = [
    {"nombre": "Cissney", "genero": "Femenino", "color_cabello": "Rojo", "ojos": "Cafes"},
    {"nombre": "Zack", "genero": "Masculino", "color_cabello": "Negro", "ojos": "Azules"},
    {"nombre": "Cloud", "genero": "Masculino", "color_cabello": "Rubio", "ojos": "Azules"},
    {"nombre": "Aerith", "genero": "Femenino", "color_cabello": "Cafe", "ojos": "Verdes"}
]

respuestas = {
    "color_cabello": None,
    "ojos": None,
    "genero": None
}

preguntas = {
    "color_cabello": [("Blanco", "color de cabello Blanco"),("Negro", "color de cabello negro"), ("Rubio", "color de cabello rubio"), ("Rojo", "color de cabello rojo"), ("Cafe", "color de cabello cafe")],
    "ojos": [("Azules", "color de ojos azules"), ("Cafes", "color de ojos cafes"), ("Verdes", "color de ojos verdes")],
    "genero": [("Masculino", "genero masculino"), ("Femenino", "genero femenino")]
}

archivo_json = "personajes.json"

def guardar_personajes():
    with open(archivo_json, "w") as archivo:
        json.dump(personajes, archivo)

def cargar_personajes():
    global personajes
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as archivo:
            personajes = json.load(archivo)

def responder_si(caracteristica, pregunta_actual, ventana_preguntas):
    respuestas[caracteristica] = preguntas[caracteristica][pregunta_actual][0]
    ventana_preguntas.destroy()

def iniciar_preguntas(caracteristica):
    def mostrar_pregunta(pregunta_actual):
        if pregunta_actual < len(preguntas[caracteristica]):
            pregunta, desc = preguntas[caracteristica][pregunta_actual]
            ventana_pregunta.config(text=f"Tu personaje tiene {desc}?")
            boton_si.config(command=lambda: responder_si(caracteristica, pregunta_actual, ventana_preguntas))
            boton_no.config(command=lambda: responder_no(pregunta_actual))

    def responder_no(pregunta_actual):
        mostrar_pregunta(pregunta_actual + 1)

    pregunta_actual = 0
    ventana_preguntas = tk.Toplevel(ventana)
    ventana_preguntas.title(f"Preguntas - {caracteristica}")
    ventana_preguntas.configure(bg="white")
    ventana_pregunta = tk.Label(ventana_preguntas, text="", fg="black")
    ventana_pregunta.pack(pady=10)

    boton_si = tk.Button(ventana_preguntas, text="Si", bg="green", fg="white")
    boton_si.pack(side=tk.LEFT, padx=10, pady=10)

    boton_no = tk.Button(ventana_preguntas, text="No", bg="red", fg="white")
    boton_no.pack(side=tk.LEFT, padx=10, pady=10)

    mostrar_pregunta(pregunta_actual)

def verificar_coincidencia():
    for caracteristica in respuestas:
        if respuestas[caracteristica] is None:
            messagebox.showinfo("Resultado", f"Debes responder todas las preguntas.")
            return

    personajes_coincidentes = []
    for personaje in personajes:
        coincide = all(personaje[caracteristica] == respuestas[caracteristica] for caracteristica in respuestas)
        if coincide:
            personajes_coincidentes.append(personaje["nombre"])

    if not personajes_coincidentes:
        mensaje_nuevo_personaje = messagebox.askyesno("Resultado", "No se encontraron personajes que coincidan Quieres agregar uno nuevo?")
        if mensaje_nuevo_personaje:
            agregar_nuevo_personaje()
    else:
        messagebox.showinfo("Resultado", f"Personajes que coinciden: {', '.join(personajes_coincidentes)}.")

def agregar_nuevo_personaje():
    def guardar_nuevo_personaje():
        nombre_nuevo = entrada_nombre_nuevo.get().capitalize()
        color_cabello_nuevo = entrada_color_cabello_nuevo.get()
        color_ojos_nuevo = entrada_color_ojos_nuevo.get()
        genero_nuevo = entrada_genero_nuevo.get()

        if nombre_nuevo and color_cabello_nuevo and color_ojos_nuevo and genero_nuevo:
            personajes.append({"nombre": nombre_nuevo, "color_cabello": color_cabello_nuevo, "ojos": color_ojos_nuevo, "genero": genero_nuevo})
            messagebox.showinfo("Exito", f"nuevo personaje '{nombre_nuevo}' agregado con exito.")
            ventana_nuevo_personaje.destroy()
            guardar_personajes()
        else:
            messagebox.showinfo("Error", "Completa todos los campos para agregar un nuevo personaje.")

    ventana_nuevo_personaje = tk.Toplevel(ventana)
    ventana_nuevo_personaje.title("Agregar Nuevo Personaje")
    ventana_nuevo_personaje.configure(bg="white")

    tk.Label(ventana_nuevo_personaje, text="Nombre:", fg="black").pack(pady=5)
    entrada_nombre_nuevo = tk.Entry(ventana_nuevo_personaje)
    entrada_nombre_nuevo.pack(pady=5)

    tk.Label(ventana_nuevo_personaje, text="Color de cabello:", fg="black").pack(pady=5)
    entrada_color_cabello_nuevo = tk.Entry(ventana_nuevo_personaje)
    entrada_color_cabello_nuevo.pack(pady=5)

    tk.Label(ventana_nuevo_personaje, text="Color de ojos:", fg="black").pack(pady=5)
    entrada_color_ojos_nuevo = tk.Entry(ventana_nuevo_personaje)
    entrada_color_ojos_nuevo.pack(pady=5)

    tk.Label(ventana_nuevo_personaje, text="Genero:", fg="black").pack(pady=5)
    entrada_genero_nuevo = tk.Entry(ventana_nuevo_personaje)
    entrada_genero_nuevo.pack(pady=5)

    boton_guardar_nuevo = tk.Button(ventana_nuevo_personaje, text="Guardar", command=guardar_nuevo_personaje, bg="blue", fg="white")
    boton_guardar_nuevo.pack(pady=10)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Adivina Quien")
ventana.configure(bg="white")

# Botones para iniciar preguntas por sección
boton_pregunta_cabello = tk.Button(ventana, text="Preguntar Color Cabello", command=lambda: iniciar_preguntas("color_cabello"), bg="green", fg="white")
boton_pregunta_cabello.pack(side=tk.LEFT, padx=10, pady=10)

boton_pregunta_ojos = tk.Button(ventana, text="Preguntar Color Ojos", command=lambda: iniciar_preguntas("ojos"), bg="orange", fg="white")
boton_pregunta_ojos.pack(side=tk.LEFT, padx=10, pady=10)

boton_pregunta_genero = tk.Button(ventana, text="Preguntar Genero", command=lambda: iniciar_preguntas("genero"), bg="purple", fg="white")
boton_pregunta_genero.pack(side=tk.LEFT, padx=10, pady=10)

boton_verificar = tk.Button(ventana, text="Verificar", command=verificar_coincidencia, bg="blue", fg="white")
boton_verificar.pack(pady=10)

# Cargar los personajes desde el archivo JSON si existe
cargar_personajes()

ventana.mainloop()
