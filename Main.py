from matplotlib.pyplot import figure, show
from mpl_toolkits.mplot3d import Axes3D
from numpy import binary_repr
from random import randint, seed, sample

# Generar una semilla aleatoria para cada ejecución y configurarla
sem = randint(0, int(1e4))  # Genera una semilla entre 0 y 10000

seed(sem)

print('Seed usada:',sem)

# Crear la figura y un conjunto de ejes en 3D
fig = figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

# Parámetros
num_cubos = 8  # Número de cubos a generar (máximo 8 para garantizar octantes únicos)
tam_min = 1    # Tamaño mínimo de los cubos
tam_max = 10   # Tamaño máximo de los cubos (debe ser al menos `tam_min + num_cubos - 1` para permitir valores únicos)

# Generar tamaños únicos y octantes únicos
tamaños = sample(range(tam_min, tam_max + 1), num_cubos)
octantes = [0o0 + i for i in range(8)]
#definimos los octales explicitamente xq range SOLO trabaja con enteros
octantes = sample(octantes, num_cubos) # Selecciona octantes únicos al azar

# Crear la lista de cubos con tamaños y octantes únicos
cubos = [{'tam': tam, 'oct': oct} for tam, oct in zip(tamaños, octantes)]

# Colores y estilos de línea variados
colores = ['b', 'r', 'g', 'purple', 'orange']  # Paleta de colores para cada cubo
estilos = ['-', '--', '-.', ':', (0, (5, 10))]  # Diferentes estilos de línea
anchos = [1.0, 1.5, 2.0, 2.5, 3.0]  # Grosor de las líneas
transparencias = [0.3, 0.5, 0.7, 0.8, 0.9]  # Niveles de transparencia

def dibuja_Cubo(ax, L, octante, color, estilo, ancho, alpha):
    '''Dibuja un cubo desde el origen (0, 0, 0) con un tamaño especificado.
      4--------5
     /|       /|
    7--------6 |
    | |      | |
    | |      | |
    | 0------|-1
    |/       |/
    3--------2
    L: Tamaño del cubo.
    color, estilo, ancho, alpha: Personalización gráfica del cubo.
    # Calculamos la traslación en base al octante'''
    
    offset = [-L if bit == '1' else 0 for bit in bin(octante)[2:].zfill(3)]
    '''NO es traduccion
    #SOLO si el cubo ha de ser retranqueado
    #en caso contrario su direccion será positiva
    # Las esquinas del cubo basado en el tamaño y la traslación'''
    # Esquinas del cubo basado en L y offset
    corners = [[offset[i] + L * int(bit) for i, bit in enumerate(binary_repr(num, width=3))]
               for num in [0, 4, 6, 2, 1, 5, 7, 3]]

    # Definición de las conexiones de las aristas
    conexiones = [[i % 4 for i in range(5)],  # Base inferior (0, 1, 2, 3, 0)
                  [i % 4 + 4 for i in range(5)]] + \
                 [[i, i + 4] for i in range(4)]

    # Crear las aristas del cubo utilizando comprensión de lista
    edges = [[corners[j] for j in conexion] for conexion in conexiones]

    # Dibuja las aristas del cubo
    for edge in edges:
        ax.plot3D(*zip(*edge), color=color, linestyle=estilo, linewidth=ancho, alpha=alpha)

# Dibujar cada cubo con características gráficas diferentes
for i, cubo in enumerate(cubos):
    dibuja_Cubo(ax,cubo['tam'],cubo['oct'], 
        color=colores[i % len(colores)], 
        estilo=estilos[i % len(estilos)], 
        ancho=anchos[i % len(anchos)], 
        alpha=transparencias[i % len(transparencias)])

'''# Dibujar los cubos usando su tamaño y octante
for cubo in cubos:
    dibujar_cubo(ax, cubo['tam'], cubo['oct'])'''

# Configurar etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')  
ax.set_zlabel('Z')

# Calcular el tamaño máximo solo una vez
max_tam = max(cubo['tam'] for cubo in cubos)
lims = [-max_tam, max_tam]

# Ajustar el rango de los ejes
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_zlim(lims)

ax.invert_yaxis()

# Mostrar el gráfico
show()
