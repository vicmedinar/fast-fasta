import os
from tkinter import Tk, filedialog

# Permitir al usuario seleccionar el archivo desde cualquier directorio
Tk().withdraw()  # Oculta la ventana principal de Tkinter
ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo FASTA")
if not ruta_archivo:
    raise FileNotFoundError("No se seleccionó ningún archivo.")

# Leer el archivo FASTA
with open(ruta_archivo) as file:
    nombres = []  # Lista para guardar los nombres de las secuencias
    secuencias = []  # Lista para guardar las secuencias de nucleótidos
    secuencia_actual = ''  # Variable temporal para guardar la secuencia actual

    for linea in file:
        if linea.startswith('>'):  # Si es un nombre de secuencia.
            if secuencia_actual:
                secuencias.append(secuencia_actual)
                secuencia_actual = ''  # Reiniciar la secuencia
            nombre = linea.strip().replace('_', ' ').strip()
            nombres.append(nombre)
        else:
            secuencia_actual += linea.strip()  # Añadir nucleótidos

    if secuencia_actual:  # Añadir la última secuencia si no está vacía
        secuencias.append(secuencia_actual)

# Diccionario del código genético
codigo_genetico = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
    'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
}

# Crear y escribir el archivo de resultados
nombre_salida = "resultados_fasta.txt"
with open(nombre_salida, "w") as salida:
    for i, nombre in enumerate(nombres):
        # Calcular el conteo de nucleótidos
        conteo_A = secuencias[i].count('A')
        conteo_T = secuencias[i].count('T')
        conteo_C = secuencias[i].count('C')
        conteo_G = secuencias[i].count('G')

        # Calcular porcentajes
        purinas = conteo_A + conteo_G
        pirimidinas = conteo_C + conteo_T
        nucleotidos = conteo_A + conteo_G + conteo_C + conteo_T
        por_purinas = (purinas / nucleotidos) * 100
        por_pirimidinas = (pirimidinas / nucleotidos) * 100

        # Escribir los resultados
        salida.write(f"Nombre: {nombre}\n")
        salida.write(f"Conteo de nucleótidos - A: {conteo_A}, T: {conteo_T}, C: {conteo_C}, G: {conteo_G}\n")
        salida.write(f"Porcentaje - Purinas: {por_purinas:.2f}%, Pirimidinas: {por_pirimidinas:.2f}%\n")
        salida.write("Marcos de lectura:\n")
        for marco in range(3):
            secuencia_aminoacidos = ''
            for j in range(marco, len(secuencias[i]) - 2, 3):
                codon = secuencias[i][j:j + 3]
                aminoacido = codigo_genetico.get(codon, '?')
                secuencia_aminoacidos += aminoacido
            salida.write(f"Marco {marco + 1}: {secuencia_aminoacidos}\n")
        salida.write("-" * 40 + "\n")

print(f"Resultados exportados a {nombre_salida}")

