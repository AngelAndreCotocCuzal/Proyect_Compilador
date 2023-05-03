import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWidgets import *
import re
from PyQt5.uic import loadUiType
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
from compilador import Compiler


# Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')
# QWidget = loadUiType('interfaz.ui')
Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')


class VentanaPrincipal(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.boton_buscar_archivo.clicked.connect(self.buscar_archivo)
        self.openFile.clicked.connect(self.create)

        # Seleccionar el archivo a compilar
    def create(self) -> None:
        # Obtener la dirección del archivo
        file_name = QFileDialog.getOpenFileName(self, 'Select Program', 'D:/', 'File (*.txt)')[0]

        # Si se escoge un archivo, entonces...
        if file_name != '':
            # print(file_name)

            # Conseguir el nombre del archivo (de C:/dirección/de/archivo.txt a solamente archivo.txt)
            def get_name(string):
                def invertir_cadena(chain):
                    return chain[::-1]

                cadena_invertida = invertir_cadena(string)
                counter = 0
                letter = ''
                new_string = ''
                while letter != '/':
                    new_string += letter
                    letter = cadena_invertida[counter]
                    counter += 1

                name = invertir_cadena(new_string)
                return name

            # Cambiar el texto de lineText por el nombre del archivo (la barra al lado del botón "Abrir Archivo")
            self.fileName.setText(get_name(file_name))

            # Llamado del método "update_file_text_edit"
            self.update_fileContent_text_edit(file_name)

            # Llamado del metodo "compile"
            self.compile(file_name)

    # Cambiar textEdit "Texto" por el contenido del archivo
    def update_fileContent_text_edit(self, file):
        # Se abre el archivo en modo de lectura como f
        with open(file, 'r') as f:
            # Se leen los contenidos del archivo
            contents = f.read()

            # En el textEdit llamado "fileContent" se colocan los contenidos del archivo
            self.fileContent.setText(contents)

            f.close()

    # Cambiar el textEdit "Valores" por los valores encontrados en el archivo
    def update_fileValues_text_edit(self, values):
        self.fileValues.setText(values)

    # Cambiar el textEdit "Lista de Componentes" por los componentes del archivo
    def update_fileComponentes_text_edit(self, components):
        self.fileComponents.setText(components)

    # Compilar archivo
    def compile(self, file):
        compiled = Compiler(file)
        data = compiled.parse()
        data2 = f"Total de Operadores: {compiled.countOperatorPrint} \n " \
                f"Total de Palabras Reservadas: {compiled.countReserverdWordPrint} \n " \
                f"Total de Identificadores: {compiled.countIdentifierPrint} \n " \
                f"Total de Signos: {compiled.countSignPrint} "
        # self.update_fileComponentes_text_edit(data2)
        self.update_fileValues_text_edit(data)

    # Crear elementos de la interfaz gráfica
    # self.label_archivo = QLabel('Archivo:')
    # self.texto_archivo = QLineEdit()
    #self.boton_buscar_archivo = QPushButton('Buscar archivo')
    #self.tabla_tokens = QTableWidget()
    #self.tabla_tokens.setColumnCount(4)
    #self.tabla_tokens.setHorizontalHeaderLabels(['Tipo', 'Token', 'Cantidad', 'Líneas'])
    #self.label_errores = QLabel('Errores léxicos:')
    #self.texto_errores = QLabel()

    # Añadir los elementos a un layout vertical
    #layout_vertical = QVBoxLayout()
    #layout_vertical.addWidget(self.label_archivo)
    #layout_vertical.addWidget(self.texto_archivo)
    #layout_vertical.addWidget(self.boton_buscar_archivo)
    #layout_vertical.addWidget(self.tabla_tokens)
    #layout_vertical.addWidget(self.label_errores)
    #layout_vertical.addWidget(self.texto_errores)

    # Establecer el layout para la ventana principal
    #self.setLayout(layout_vertical)

    # Conectar el botón de buscar archivo con la función correspondiente


    def buscar_archivo(self):
        print("estas en buscar archivo")
        # Abrir un diálogo para buscar el archivo
        archivo, _ = QFileDialog.getOpenFileName(self, 'Buscar archivo', '', 'Archivos de texto (*.txt)')

        # Mostrar el nombre del archivo en el campo correspondiente
        self.texto_archivo.setText(archivo)

        # Llamar a la función de análisis léxico con el archivo seleccionado
        self.analizar_lexico(archivo)

    def analizar_lexico(self, archi):
        # Lista de tokens reconocidos
        tokens = {
            r'\bentero\b': 'Palabra reservada',
            r'\bdecimal\b': 'Palabra reservada',
            r'\bbooleano\b': 'Palabra reservada',
            r'\bcadena\b': 'Palabra reservada',
            r'\bsi\b': 'Palabra reservada',
            r'\bsino\b': 'Palabra reservada',
            r'\bmientras\b': 'Palabra reservada',
            r'\bhacer\b': 'Palabra reservada',
            r'\bverdadero\b': 'Palabra reservada',
            r'\bfalso\b': 'Palabra reservada',
            r'\+': 'Operador',
            r'-': 'Operador',
            r'\*': 'Operador',
            r'/': 'Operador',
            r'%': 'Operador',
            r'=': 'Operador',
            r'==': 'Operador',
            r'<': 'Operador',
            r'>': 'Operador',
            r'>=': 'Operador',
            r'<=': 'Operador',
            r'\(': 'Signo',
            r'\)': 'Signo',
            r'\{': 'Signo',
            r'\}': 'Signo',
            r'\"': 'Signo',
            r';': 'Signo',
            r'\b\d+\b': 'Numero',
            r'\b\d+\.\d+\b': 'Flotante',
            r'\b[a-z]+\b': 'Identificador',
            r'\b[a-z]+\b': 'Identificador'
        }

        # Abre el archivo de entrada y lee su contenido
        #archivo = 'archivo.txt'
        archivo = archi

        with open(archivo, 'r') as f:
            contenido = f.read()

        # Separa el contenido en líneas
        lineas = contenido.split('\n')
        # Analiza cada línea y busca los tokens reconocidos
        tabla_tokens = {}
        for num_linea, linea in enumerate(lineas):
            for patron, tipo in tokens.items():
                for match in re.finditer(patron, linea):
                    token = match.group()
                    if tipo not in tabla_tokens:
                        tabla_tokens[tipo] = {}
                    if token not in tabla_tokens[tipo]:
                        tabla_tokens[tipo][token] = {'lineas': [], 'cantidad': 0}
                    tabla_tokens[tipo][token]['lineas'].append(num_linea + 1)
                    if tipo == 'Identificador':
                        cantidad_letras = len(token)
                        tabla_tokens[tipo][token]['cantidad'] = cantidad_letras

        # Borra el contenido de la tabla
        self.tabla_tokens.setRowCount(0)

        # Agrega los tokens encontrados a la tabla
        for tipo, tokens in tabla_tokens.items():
            for token, data in tokens.items():
                cantidad = data['cantidad'] if tipo == 'Identificador' else len(data['lineas'])
                lineas = data['lineas']
                fila = self.tabla_tokens.rowCount()
                self.tabla_tokens.insertRow(fila)
                self.tabla_tokens.setItem(fila, 0, QTableWidgetItem(tipo))
                self.tabla_tokens.setItem(fila, 1, QTableWidgetItem(token))
                self.tabla_tokens.setItem(fila, 2, QTableWidgetItem(str(cantidad)))
                self.tabla_tokens.setItem(fila, 3, QTableWidgetItem(str(lineas)))


        tokens_error = {
            'decimal': r'\bdecimal\b',
            'booleano': r'\bbooleano\b',
            'cadena': r'\bcadena\b',
            'si': r'\bsi\b',
            'sino': r'\bsino\b',
            'mientras': r'\bmientras\b',
            'hacer': r'\bhacer\b',
            'verdadero': r'\bverdadero\b',
            'falso': r'\bfalso\b',
            'operador': r'[\+\-\*/%=<>]=?|\(|\)|\{|\}|\"|;',
            'numero': r'\d+(\.\d+)?',
            'identificador': r'[a-zA-Z]+',
        }

        # Variables para almacenar los tokens y errores léxicos
        tokens_encontrados = {}
        errores_lexicos = []

        # Lectura del archivo
        with open(archivo, 'r') as f:
            lineas = f.readlines()

        # Análisis léxico
        for i, linea in enumerate(lineas):
            # Eliminación de espacios en blanco y saltos de línea
            linea = linea.strip()

            # Búsqueda de tokens en la línea
            for tipo, patron in tokens_error.items():
                for token in re.findall(patron, linea):
                    # Agregar el token encontrado al diccionario de tokens
                    if tipo in tokens_encontrados:
                        tokens_encontrados[tipo]['cantidad'] += 1
                    else:
                        tokens_encontrados[tipo] = {'tipo': tipo, 'cantidad': 1}

                    # Reemplazar el token encontrado en la línea para evitar detectarlo dos veces
                    linea = linea.replace(token, '', 1)

            # Búsqueda de errores léxicos
            if re.search(r'[^\w\s]', linea):
                errores_lexicos.append({'linea': i + 1, 'error': linea})

        # Impresión de los errores léxico
        texto = ''
        contador = 0
        for error in errores_lexicos:
            for clave, valor in error.items():
                if contador == 2:
                    texto += '\n'
                    contador = 0
                texto += f'{clave}: {valor}\n'
                contador += 1

            self.texto_errores.setText(texto)



if __name__ == '__main__':
    # Crear la aplicación y la ventana principal
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())
