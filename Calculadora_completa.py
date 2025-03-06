import re
from tkinter import *
import tkinter as tk
import math

resultado_operacion = 0
ultima_op = True
root = tk.Tk()
root.title("Calculadora")
root.geometry("325x470")
root.config(bg="black")
root.resizable(False,False)

texto1 = Label(root, font=("Arial 14"), text="≡   Estándar", bg="black", fg="white")
texto1.place(x=1, y=10, width=150, height=15)

caja = Text(root, bg="black", fg="white", relief="flat", font=("Arial 20"))
caja.place(x=20, y=85, width=350, height=40)

posiciones = [(2, 128),(63,128),(124, 128),(185,128),(246, 128),(307,128),(2, 168),(83, 168),(164, 168),
              (245, 168), (2, 218), (83, 218), (164, 218), (245, 218),(2, 268), (83, 268), (164, 268),
              (245, 268), (2, 318), (83, 318), (164, 318), (245, 318),(2, 368), (83, 368), (164, 368),
              (245, 368), (2, 418), (83, 418), (164, 418), (245, 418)]

nombres_botones = ["MC","MR","M+","M-","MS","Mv","%", "CE", "C", "<--", "1/x", "x²", "√x",
                   "÷", "7", "8", "9", "x", "4", "5", "6", "-","1", "2", "3", "+", "+/-", "0", ".", "="]


def insertar_valor(valor):
    global ultima_op
    operaciones = ["+", "-", "x", "÷"]
    if ultima_op and valor in operaciones:
        caja.insert(END, valor)
        ultima_op = False
    elif ultima_op:
        caja.delete("1.0", END)
        ultima_op = False
    validar = caja.get("end-2c", "end-1c")
    if valor in operaciones and validar in operaciones:
        caja.delete("end-2c", "end-1c")
    contenido = caja.get("1.0", tk.END).strip().split()
    if contenido == "0":
        caja.delete("1.0", END)
    caja.insert(END, valor)

def limpiar(borrar):
    caracterrr = {
        "CE": lambda: caja.delete("1.0", END),
        "C": lambda: caja.delete("1.0", END),
        "<--": lambda: caja.delete("end-2c",END)
    }
    if borrar in caracterrr:
        caracterrr[borrar]()

def caraceteres(valor):
    return {
        "1/x": lambda x: 1 / x if x != 0 else "Error",
        "x²": lambda x: x ** 2,
        "√x": lambda x: math.sqrt(x) if x >= 0 else "Error",
        "+/-": lambda x: x*-1,
        "%": lambda x: x / 100
    }.get(valor)

def realizar_operacion(valor):
    global resultado_operacion, ultima_op
    contenido = caja.get("1.0", "end-1c").strip()
    if not contenido:
        return

    try:
        if valor in ["1/x", "x²", "√x", "+/-", "%"]:
            operadores_buscar = ['+', '-', 'x', '÷']
            # Aquí buscamos la última aparición de los operadores a buscar con rfind combinado con el for
            # Con la función max lo que hacemos es obtener la posición del operador más a la derecha
            last_operator_pos = max((contenido.rfind(op) for op in operadores_buscar), default=-1)
            # Aquí lo que hacemos es obtener el número que está después del operador
            # Si no se encuentra, con else solo obtenemos el valor de contenido
            # El : después del +1 indica que buscamos lo que está adelante del operador
            operando = contenido[last_operator_pos + 1:] if last_operator_pos != -1 else contenido
            # Aquí obtenemos los valores que están atrás del operador (incluyendo el operador)
            nueva_base = contenido[:last_operator_pos + 1] if last_operator_pos != -1 else ""

            if valor == "%":
                if last_operator_pos == -1:
                    # Si no hay operador, calculamos el porcentaje directo
                    num = float(contenido) / 100
                    resultado_operacion = str(num)
                    insertar_resultado()
                else:
                    # Obtener el operador y los operandos
                    operador = contenido[last_operator_pos]
                    #todo lo que esta a la izquierda del operqdor
                    izquierda = contenido[:last_operator_pos]
                    #todo lo qie esta a la derecha
                    derecha = contenido[last_operator_pos + 1:]

                    # Calculamos el porcentaje basado en el operador
                    num_izq = eval(izquierda.replace('x', '*').replace('÷', '/'))
                    num_der = float(derecha)
                    porcentaje = (num_izq * num_der) / 100

                    # Aplicamos las oiperaciones
                    if operador == '+':
                        resultado = num_izq + porcentaje
                    elif operador == '-':
                        resultado = num_izq - porcentaje
                    elif operador == 'x':
                        resultado = num_izq * porcentaje
                    elif operador == '÷':
                        resultado = num_izq / porcentaje if porcentaje != 0 else "Error"

                    resultado_operacion = str(resultado)
                    insertar_resultado()
            else:
                # Evaluar el operando actual
                operando_eval = operando.replace('x', '*').replace('÷', '/')
                #con re.sub buscamos el numero que esta dentro de la raiz y lo  remplazamos en math
                operando_eval = re.sub(r'√(\d+\.?\d*)', r'math.sqrt(\1)', operando_eval)
                num = eval(operando_eval)

                # Aplicar la operación unaria
                operacion = caraceteres(valor)
                # Aquí le asignamos el valor de operación si operación no da error
                resultado = operacion(num) if operacion else "Error"

                # Si se encuentra un valor como raíz, se actualiza al instante
                nueva_expresion = nueva_base + str(resultado)
                caja.delete("1.0", tk.END)
                caja.insert("1.0", nueva_expresion)
                resultado_operacion = nueva_expresion
                ultima_op = True

        elif valor == "=":
            # Evaluar la expresión completa
            expresion = contenido.replace("x", "*").replace("÷", "/")
            expresion = re.sub(r'√(\d+\.?\d*)', r'math.sqrt(\1)', expresion)
            resultado = eval(expresion)
            resultado_operacion = str(resultado)
            insertar_resultado()

    except Exception as e:
        resultado_operacion = "Error"
        insertar_resultado()

def insertar_resultado():
    global ultima_op
    ultima_op = True
    caja.delete("1.0", tk.END)
    caja.insert("1.0", resultado_operacion)


for nombre, (x, y) in zip(nombres_botones, posiciones):
    if nombre == "=":
        boton = tk.Button(root, text=nombre, command=lambda v=nombre: realizar_operacion(v), bg="#D3A4D3", relief="flat", fg = "white")
    elif nombre in ["CE", "C", "<--"]:
        boton = tk.Button(root, text=nombre, command=lambda v=nombre: limpiar(v), bg="#2B211E", fg = "white")
    elif nombre in ["1/x", "x²", "√x", "+/-", "%"]:
        boton = tk.Button(root, text=nombre, command=lambda v=nombre: realizar_operacion(v), bg="#2B211E", fg = "white")
    elif nombre in ["MC","MR","M+","M-","MS","Mv"]:
        boton = tk.Button(root, text=nombre, command=None, bg="black", fg= "white", relief="flat")
        boton.place(x=x, y=y, width=40, height=40)
    else:
        boton = tk.Button(root, text=nombre, command=lambda v=nombre: insertar_valor(v), bg="#2B211E",fg = "white")
    boton.place(x=x, y=y, width=80, height=50)

root.mainloop()