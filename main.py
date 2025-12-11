import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import base_datos



ventana = tk.Tk()
ventana.title("Biblioteca - Carga de Inventario")
ventana.geometry("1200x900")


# Funcion para manejar posibles errores de la DB
def inicializar_app():
    try:
        # Inicializamos DB al arrancar
        # Creamos aca porque si surge error no lo veremos nunca.
        base_datos.crear_tabla()
        actualizar_tabla()
        entry_autor['values'] = base_datos.listar_autores()
        entry_signatura['values'] = base_datos.listar_signaturas()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo inicializar por falta de DB" + str(e))

ventana.after(200, inicializar_app)


frame_form = tk.Frame(ventana, padx=20, pady=20)
frame_form.pack()

## Etiquetas y campos de entrada

# 1. TITULO
lbl_titulo = tk.Label(frame_form, text = "Titulo Libro", font = ("Arial", 12))
lbl_titulo.grid(row=0, column=0, sticky="e", pady=5)
entry_titulo = tk.Entry(frame_form, font = ("Arial", 12), width=30)
entry_titulo.grid(row=0, column=1,pady=5, padx=5)
entry_titulo.focus()
entry_titulo.bind('<Return>', lambda event: entry_autor.focus())

# 2. AUTOR
lbl_autor = tk.Label(frame_form, text = "Autor", font = ("Arial", 12))
lbl_autor.grid(row=1, column=0, sticky="e", pady=5)
lista_autores = base_datos.listar_autores()
entry_autor = ttk.Combobox(frame_form, font = ("Arial", 12), width=30)
entry_autor['values'] = lista_autores
entry_autor.grid(row=1, column=1, pady=5, padx=5)
entry_autor.bind('<Return>', lambda event: entry_signatura.focus())

# 3. SIGNATURA
lbl_signatura = tk.Label(frame_form, text = "Signatura", font = ("Arial", 12))
lbl_signatura.grid(row=2, column=0, sticky="e", pady=5)
entry_signatura = ttk.Combobox(frame_form, font = ("Arial", 12), width=30)
entry_signatura['values'] = base_datos.listar_signaturas()
entry_signatura.grid(row=2, column=1, pady=5, padx=5)
entry_signatura.bind('<Return>', lambda event: entry_numero_inventario.focus())

# 4. NUM INVENTARIO
lbl_numero_inventario = tk.Label(frame_form, text = "Num de Inv", font = ("Arial", 12))
lbl_numero_inventario.grid(row=3, column=0, sticky="e", pady=5)
entry_numero_inventario = tk.Entry(frame_form, font = ("Arial", 12), width=30)
entry_numero_inventario.grid(row=3, column=1,pady=5, padx=5)
entry_numero_inventario.bind('<Return>', lambda event: guardar())


### Funciones Necesarias ###

def guardar():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    signatura = entry_signatura.get()
    numero_inventario = entry_numero_inventario.get()

    if titulo and autor and numero_inventario and signatura:
        exito = base_datos.guardar_inventario(1, titulo, autor, numero_inventario, signatura)
        
        if exito:
            messagebox.showinfo("Guardar", f"Guardado: {numero_inventario}")
            entry_numero_inventario.delete(0, tk.END)
            entry_numero_inventario.focus()
            actualizar_tabla()
            entry_autor['values'] = base_datos.listar_autores()
    else:
        messagebox.showerror("Error", "Debe completar todos los campos (incluida Signatura)")
        entry_titulo.focus()


def eliminar():
    seleccion = tabla.selection()
    
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar un item de la lista para eliminar")
        return

    datos_fila = tabla.item(seleccion[0]) ['values']
    id_inventario = datos_fila[0]
    titulo = datos_fila[1]

    confirmar = messagebox.askyesno("Confirmar Eliminacion", f"¿Estas seguro de eliminar el libro: {titulo}?")
    
    if confirmar:
        exito = base_datos.eliminar_inventario(id_inventario)
        if exito:
            messagebox.showinfo("Exito!", f"El libro {titulo} ha sido eliminado exitosamente")
            actualizar_tabla()
            limpiar()
            entry_titulo.focus()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el libro")


def seleccionar_registro(event):
    seleccion = tabla.selection()
    if seleccion:
        datos = tabla.item(seleccion[0])['values']
        limpiar()
        entry_titulo.insert(0, datos[1])
        entry_autor.set(datos[2])
        entry_signatura.insert(0, datos[3])
        entry_numero_inventario.insert(0, datos[4])
        entry_titulo.focus()


def actualizar_inventario():
    seccion = tabla.selection()
    if not seccion:
        messagebox.showerror("Error", "Debe seleccionar un item de la lista para actualizar")
        return

    datos_fila = tabla.item(seccion[0]) ['values']
    id_inventario = datos_fila[0]
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    signatura = entry_signatura.get()
    numero_inventario = entry_numero_inventario.get()

    if titulo and autor and signatura and numero_inventario:
        # Corregido: El orden debe ser igual al definido en base_datos.py (signatura antes de numero_inventario)
        exito = base_datos.actualizar_inventario(id_inventario, titulo, autor, signatura, numero_inventario)

        if exito:
            messagebox.showinfo("Exito!", f"El libro {titulo} ha sido actualizado exitosamente")
            actualizar_tabla()
            limpiar()
            entry_titulo.focus()
        else:
            messagebox.showwarning("Error", "No dejes campos vacios")


def limpiar():
    entry_titulo.delete(0, tk.END)
    entry_autor.set("")
    entry_signatura.delete(0, tk.END)
    entry_numero_inventario.delete(0, tk.END)
    entry_titulo.focus()



## Recuadro de Botones
frame_btn = tk.Frame(ventana, padx=20, pady=20)
frame_btn.pack()

btn_guardar = tk.Button(frame_btn, text = "Guardar", command=guardar, bg="#005f73", fg="white", font = ("Arial", 12, "bold"))
btn_guardar.grid(row=0, column=0, pady=20, padx=10)

btn_limpiar = tk.Button(frame_btn, text = "Limpiar Todo", command=limpiar, bg="#005f73", fg="white", font = ("Arial", 12, "bold"))
btn_limpiar.grid(row=0, column=1, pady=20, padx=10)

btn_actualizar = tk.Button(frame_btn, text = "Actualizar", command=actualizar_inventario, bg="#005f73", fg="white", font = ("Arial", 12, "bold"))
btn_actualizar.grid(row=0, column=2, pady=20, padx=10)

btn_eliminar = tk.Button(frame_btn, text = "Eliminar", command=eliminar, bg="#e63946", fg="white", font = ("Arial", 12, "bold"))
btn_eliminar.grid(row=0, column=3, pady=20, padx=10)


## Recuadro de la Tabla
frame_tabla = tk.Frame(ventana, padx=20, pady=20)
frame_tabla.pack()
columnas = ('id', 'titulo', 'autor', 'signatura', 'inventario')
tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings')
tabla.heading('id', text='ID')
tabla.heading('titulo', text='Titulo')
tabla.heading('autor', text='Autor')
tabla.heading('signatura', text='Signatura')
tabla.heading('inventario', text='Num de Inventario')
tabla.pack(fill=tk.BOTH, expand=True)


tabla.bind('<<TreeviewSelect>>', seleccionar_registro)


def actualizar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    
    libros = base_datos.listar_inventario()

    for libros in libros:
        tabla.insert("", tk.END, values=libros)


ventana.mainloop()