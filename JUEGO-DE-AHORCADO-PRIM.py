# Juego del Ahorcado 
import random 
import pygame 
from pygame import mixer
import time
import math
import os 
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

# Inicializar mixer
pygame.mixer.quit()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Crear la pantalla
pantalla = pygame.display.set_mode((1280, 720))

# Fondo
try:
    fondo = pygame.image.load(resource_path('assets/FOTOS/fondo.png'))
except:
    print("No se encontró fondo.png, usando fondo sólido")
    fondo = pygame.Surface((1280, 720))
    fondo.fill((15, 23, 42))

# Música de fondo
try:
    mixer.music.load(resource_path("assets/MUSICA/Musica-De-Fondo.wav"))
    mixer.music.play(-1)
    mixer.music.set_volume(0.5)
except:
    print("No se pudo cargar la música de fondo")

# Título e icono
pygame.display.set_caption("JUEGO DE AHORCADO")
try:
    icono = pygame.image.load(resource_path('assets/FOTOS/logo.ico'))
    pygame.display.set_icon(icono)
except:
    print("No se pudo cargar el icono")

# Colores
COLOR_FONDO = (15, 23, 42)
COLOR_BOTON_EASY = (255, 0, 0)
COLOR_BOTON_HOVER = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_VERDE = (0, 255, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_AZUL = (100, 150, 255)
COLOR_AMARILLO = (255, 255, 0)
COLOR_AHORCADO = (200, 200, 200)
COLOR_BLANCO = (255, 255, 255)
COLOR_GRIS_CLARO = (200, 200, 200)

# Fuentes
try:
    fuente_montserrat = pygame.font.Font(resource_path('assets/STYLE/Montserrat-Regular.ttf'), 32)
    fuente_montserrat_grande = pygame.font.Font(resource_path('assets/STYLE/Montserrat-Regular.ttf'), 64)
    fuente_montserrat_mediana = pygame.font.Font(resource_path('assets/STYLE/Montserrat-Regular.ttf'), 24)
    fuente_montserrat_pequena = pygame.font.Font(resource_path('assets/STYLE/Montserrat-Regular.ttf'), 20)
    fuente_montserrat_bold = pygame.font.Font(resource_path('assets/STYLE/Montserrat-Bold.ttf'), 32)
except:
    print("No se pudo cargar Montserrat, usando fuentes por defecto")
    fuente_montserrat = pygame.font.Font(None, 32)
    fuente_montserrat_grande = pygame.font.Font(None, 64)
    fuente_montserrat_mediana = pygame.font.Font(None, 24)
    fuente_montserrat_pequena = pygame.font.Font(None, 20)
    fuente_montserrat_bold = pygame.font.Font(None, 32)

fuente = fuente_montserrat
fuente_game_over = fuente_montserrat_grande
fuente_mediana = fuente_montserrat_mediana
fuente_pista = fuente_montserrat_pequena
fuente_letras = pygame.font.Font(None, 28)
fuente_letras_bold = pygame.font.Font(None, 30)
fuente_botones = fuente_montserrat_mediana

# Variables del juego
pausa = False
fuente_pausa = fuente_montserrat_grande
fuente_boton = fuente_montserrat
boton_pausa_rect = pygame.Rect(1220, 10, 32, 32)
boton_reiniciar_rect = pygame.Rect(1180, 10, 32, 32)

valor_puntuacion = 0
intentos_restantes = 8
palabra_actual = ""
pista_actual = ""
letras_adivinadas = []
letras_intentadas = []
progreso_actual = ""
estado_juego = "menu"

DIFICULTAD_ACTUAL = "EASY"
PUNTOS_PARA_DESBLOQUEAR = 50
puntos_acumulados = 0
dificultades_desbloqueadas = ["EASY"]

# Configuración de dificultades
CONFIG_DIFICULTAD = {
    "EASY": {
        "intentos": 8,
        "puntos_ganar": 10,
        "puntos_perder": -2,
        "color": COLOR_AMARILLO,
        "descripcion": "8 intentos - Puntos normales"
    },
    "DARK": {
        "intentos": 6,
        "puntos_ganar": 15, 
        "puntos_perder": -1,
        "color": COLOR_ROJO,
        "descripcion": "6 intentos - +50% puntos"
    },
    "EXTREM": {
        "intentos": 4,
        "puntos_ganar": 20,
        "puntos_perder": 0,
        "color": (255, 0, 128),
        "descripcion": "4 intentos - +100% puntos"
    }
}

# Sistema de efectos
particulas = []
efectos_activos = []
tiempo_inicio = 0

# Variables para control de sonidos
musica_pausada = False
tiempo_fin_sonido = 0

# =============================================================================
# SISTEMA DE SONIDOS CORREGIDO
# =============================================================================

def cargar_sonido(ruta, volumen=1.0):
    try:
        ruta_completa = resource_path(ruta)
        if os.path.exists(ruta_completa):
            sonido = mixer.Sound(ruta_completa)
            sonido.set_volume(volumen)
            print(f"✓ {ruta} cargado (volumen: {volumen})")
            return sonido
        else:
            print(f"✗ {ruta} no encontrado")
            return None
    except Exception as e:
        print(f"✗ Error cargando {ruta}: {e}")
        return None

# CORRECCIÓN: No usar resource_path en las llamadas
print("=== CARGANDO SONIDOS ===")
sonido_correcto = cargar_sonido('assets/MUSICA/correcto.wav', 0.5)
sonido_incorrecto = cargar_sonido('assets/MUSICA/incorrecto.wav', 0.5)
sonido_ganador = cargar_sonido('assets/MUSICA/ganador.wav', 1.0)
sonido_perdedor = cargar_sonido('assets/MUSICA/perdedor.wav', 1.0)

# Crear sonidos silenciosos de respaldo
buffer_silencioso = bytes([0] * 44)
if sonido_correcto is None:
    sonido_correcto = mixer.Sound(buffer=buffer_silencioso)
if sonido_incorrecto is None:
    sonido_incorrecto = mixer.Sound(buffer=buffer_silencioso)
if sonido_ganador is None:
    sonido_ganador = mixer.Sound(buffer=buffer_silencioso)
if sonido_perdedor is None:
    sonido_perdedor = mixer.Sound(buffer=buffer_silencioso)
print("=== SONIDOS LISTOS ===")

def reproducir_sonido_especial(sonido):
    global musica_pausada, tiempo_fin_sonido
    if sonido is not None:
        try:
            if mixer.music.get_busy() and not musica_pausada:
                mixer.music.pause()
                musica_pausada = True
            sonido.play()
            duracion_estimada = 4000 if sonido == sonido_ganador or sonido == sonido_perdedor else 2000
            tiempo_fin_sonido = pygame.time.get_ticks() + duracion_estimada
        except Exception as e:
            print(f"Error reproduciendo sonido especial: {e}")

def reproducir_sonido_normal(sonido):
    if sonido is not None:
        try:
            sonido.play()
        except Exception as e:
            print(f"Error reproduciendo sonido: {e}")

def verificar_reanudar_musica():
    global musica_pausada, tiempo_fin_sonido
    if musica_pausada and pygame.time.get_ticks() > tiempo_fin_sonido:
        try:
            mixer.music.unpause()
            musica_pausada = False
            tiempo_fin_sonido = 0
        except:
            pass

# =============================================================================
# SISTEMA DE DIFICULTAD
# =============================================================================

def verificar_desbloqueo_dificultad():
    global dificultades_desbloqueadas, puntos_acumulados
    if puntos_acumulados >= PUNTOS_PARA_DESBLOQUEAR and "DARK" not in dificultades_desbloqueadas:
        dificultades_desbloqueadas.append("DARK")
        puntos_acumulados -= PUNTOS_PARA_DESBLOQUEAR
        return "DARK"
    elif puntos_acumulados >= PUNTOS_PARA_DESBLOQUEAR and "EXTREM" not in dificultades_desbloqueadas:
        dificultades_desbloqueadas.append("EXTREM") 
        puntos_acumulados -= PUNTOS_PARA_DESBLOQUEAR
        return "EXTREM"
    return None

def cambiar_dificultad(nueva_dificultad):
    global DIFICULTAD_ACTUAL, intentos_restantes
    if nueva_dificultad in dificultades_desbloqueadas:
        DIFICULTAD_ACTUAL = nueva_dificultad
        intentos_restantes = CONFIG_DIFICULTAD[nueva_dificultad]["intentos"]

def mostrar_notificacion_desbloqueo(dificultad_desbloqueada):
    efectos_activos.append({
        "tipo": "notificacion", 
        "dificultad": dificultad_desbloqueada,
        "duracion": 180,
        "y": 500,
        "alpha": 255
    })
    crear_particulas(450, 300, 100, "confeti")
    reproducir_sonido_especial(sonido_ganador)

def dibujar_notificaciones():
    for efecto in efectos_activos[:]:
        if efecto["tipo"] == "notificacion":
            s = pygame.Surface((400, 60), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            texto = fuente_mediana.render(f"¡DESBLOQUEADO: {efecto['dificultad']}!", True, COLOR_VERDE)
            texto_rect = texto.get_rect(center=(200, 30))
            s.blit(texto, texto_rect)
            pantalla.blit(s, (250, efecto["y"]))
            efecto["duracion"] -= 1
            efecto["y"] -= 1
            if efecto["duracion"] <= 0:
                efectos_activos.remove(efecto)

# =============================================================================
# SISTEMA DE PARTÍCULAS
# =============================================================================

class Particula:
    def __init__(self, x, y, color, tipo="confeti"):
        self.x = x
        self.y = y
        self.color = color
        self.tipo = tipo
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -2)
        self.life = random.uniform(60, 120)
        self.size = random.randint(3, 8)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        return self.life > 0
        
    def draw(self, pantalla):
        if self.tipo == "confeti":
            pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.size)

def crear_particulas(x, y, cantidad=50, tipo="confeti"):
    colores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for _ in range(cantidad):
        color = random.choice(colores)
        particulas.append(Particula(x, y, color, tipo))

# =============================================================================
# FUNCIONES PRINCIPALES DEL JUEGO
# =============================================================================

# Diccionario de palabras (reducido para ejemplo)
palabras = {
    "PERRO": "El mejor amigo del hombre",
    "GATO": "Animal doméstico que maúlla y caza ratones",
    "PEZ": "Animal que vive en el agua y nada",
    "PAJARO": "Animal con plumas y alas que vuela",
    "VACA": "Animal que da leche",
    "OVEJA": "Animal con lana blanca",
    "CABALLO": "Animal grande que se puede montar",
    "GALLINA": "Pone huevos que comemos",
    "PATO": "Ave que nada en el agua y hace 'cua cua'",
    "RANA": "Animal verde que salta y croa",
    "ELEFANTE": "Animal muy grande con trompa",
    "LEON": "El rey de la selva",
    "TIGRE": "Gato grande con rayas",
    "OSO": "Animal grande que hiberna en invierno",
    "MONO": "Animal que se balancea en los árboles",
    "JIRAFA": "Animal con el cuello muy largo",
    "CANGURO": "Animal que salta y tiene bolsa",
    "PINGUINO": "Ave que no vuela y vive en el hielo",
    "DELFIN": "Animal marino muy inteligente",
    "TORTUGA": "Animal lento con caparazón",
    "CONEJO": "Animal con orejas largas y salta",
    "ARDILLA": "Roedor que come nueces",
    "MARIPOSA": "Insecto con alas coloridas",
    "ABEJA": "Insecto que hace miel",
    "HORMIGA": "Insecto pequeño y trabajador",
    "CARACOL": "Animal lento con concha",
    "ESTRELLA": "Animal marino con forma de estrella",
    "CABRA": "Animal de granja que trepa",
    "CERDO": "Animal de granja que hace 'oink'",
    "RATON": "Roedor pequeño que come queso",
    "SERPIENTE": "Reptil que se arrastra",
    "LAGARTIJA": "Reptil pequeño que corre por las paredes",
    "BALLENA": "El animal más grande del mar",
    "PUERCOESPIN": "Animal con púas afiladas",
    "ERIZO": "Animal pequeño con espinas",
    "ZORRO": "Animal astuto de cola peluda",
    "LOBO": "Animal salvaje que aúlla",
    "CISNE": "Ave blanca muy elegante",
    "BUHO": "Ave que sale de noche y es sabia",
    "PALOMA": "Ave que vive en la ciudad",
    "GOLONDRINA": "Ave que vuelve en primavera",
    "CANARIO": "Pájaro amarillo que canta",
    "LORO": "Ave que repite lo que dices",
    "AGUILA": "Ave con vista muy aguda",
    "FLAMENCO": "Ave rosa con patas largas",
    "PULPO": "Animal marino con ocho brazos",
    "CANGREJO": "Animal que camina de lado",
    "MEDUSA": "Animal marino gelatinoso",
    "CAMALEON": "Reptil que cambia de color",
    "KOALA": "Animal australiano que come eucalipto",

    # Frutas y Comida (50 palabras)
    "MANZANA": "Fruta roja o verde muy común",
    "PLATANO": "Fruta amarilla y alargada",
    "NARANJA": "Fruta cítrica de color naranja",
    "FRESA": "Fruta roja con puntitos",
    "UVA": "Fruta pequeña que crece en racimos",
    "SANDIA": "Fruta grande verde por fuera y roja por dentro",
    "MELON": "Fruta grande y dulce",
    "PERA": "Fruta con forma de lágrima",
    "CEREZA": "Fruta pequeña y roja con hueso",
    "PINA": "Fruta tropical con corona",
    "LIMON": "Fruta amarilla y muy ácida",
    "KIWI": "Fruta marrón por fuera y verde por dentro",
    "MANGO": "Fruta tropical muy dulce",
    "COCO": "Fruta dura con leche inside",
    "ZANAHORIA": "Vegetal naranja que crece bajo tierra",
    "TOMATE": "Fruta roja que usamos en ensalada",
    "LECHUGA": "Verdura verde para ensaladas",
    "PAPA": "Tubérculo que se come frito o cocido",
    "CEBOLLA": "Vegetal que hace llorar al cortarlo",
    "QUESO": "Producto lácteo que se hace con leche",
    "LECHE": "Bebida blanca de la vaca",
    "PAN": "Alimento que se hace con harina",
    "ARROZ": "Grano blanco que se cocina",
    "HUEVO": "Lo pone la gallina, tiene clara y yema",
    "CARNE": "Alimento que viene de los animales",
    "PESCADO": "Animal del mar que comemos",
    "POLLO": "Ave que comemos asada o frita",
    "HELADO": "Postre frío y dulce",
    "CHOCOLATE": "Dulce marrón hecho de cacao",
    "GALLETA": "Dulce crujiente horneado",
    "PASTEL": "Postre dulce para cumpleaños",
    "YOGUR": "Lácteo cremoso y ácido",
    "SOPA": "Comida líquida caliente",
    "PIZZA": "Comida redonda con queso y tomate",
    "HAMBURGUESA": "Comida con pan y carne",
    "SALCHICHA": "Embutido largo para hot dogs",
    "JAMON": "Carne de cerdo curada",
    "AZUCAR": "Endulzante blanco y dulce",
    "MIEL": "Líquido dulce que hacen las abejas",
    "MANTEQUILLA": "Grasa que se unta en el pan",
    "ACEITE": "Líquido para cocinar",
    "SAL": "Condimento blanco y salado",
    "CANELA": "Especia dulce y aromática",
    "VAINILLA": "Sabor para postres",
    "MAIZ": "Grano amarillo en mazorca",
    "TRIGO": "Grano para hacer harina",
    "AVENA": "Cereal para desayuno",
    "NUECES": "Fruto seco con cáscara dura",
    "ALMENDRA": "Fruto seco alargado",
    "CACAHUETE": "Fruto seco que crece bajo tierra",

    # Objetos de la Casa (50 palabras)
    "MESA": "Mueble con patas donde comemos",
    "SILLA": "Asiento con respaldo",
    "CAMA": "Mueble para dormir",
    "ARMARIO": "Mueble para guardar ropa",
    "ESPEJO": "Superficie que refleja tu imagen",
    "VENTANA": "Abertura en la pared con cristal",
    "PUERTA": "Entrada a una habitación",
    "TELEVISION": "Aparato para ver programas",
    "RADIO": "Aparato para escuchar música",
    "TELEFONO": "Dispositivo para hablar a distancia",
    "COMPUTADORA": "Máquina para trabajar y jugar",
    "LIBRO": "Conjunto de hojas con historias",
    "CUADERNO": "Conjunto de hojas para escribir",
    "LAPIZ": "Instrumento para escribir de madera",
    "BOLIGRAFO": "Instrumento para escribir con tinta",
    "GOMA": "Objeto para borrar el lápiz",
    "TIJERAS": "Herramienta para cortar papel",
    "PEGAMENTO": "Sustancia para unir cosas",
    "RELOJ": "Aparato que marca la hora",
    "LAMPARA": "Objeto que da luz",
    "FOCO": "Bombilla que ilumina",
    "ALMOHADA": "Soporte blando para la cabeza",
    "MANTA": "Tela para abrigarse en la cama",
    "TOALLA": "Tela para secarse después de bañarse",
    "CEPILLO": "Objeto para peinar el cabello",
    "PEINE": "Objeto con dientes para el pelo",
    "JABON": "Producto para lavarse las manos",
    "CHAMPU": "Producto para lavar el cabello",
    "PASTA": "Producto para lavar los dientes",
    "CEPILLO": "Objeto para cepillar los dientes",
    "VASO": "Recipiente para beber",
    "PLATO": "Recipiente para comer",
    "TENEDOR": "Utensilio con dientes para comer",
    "CUCHARA": "Utensilio cóncavo para comer",
    "CUCHILLO": "Utensilio con filo para cortar",
    "OLLA": "Recipiente para cocinar",
    "SARTEN": "Recipiente para freír",
    "REFRIGERADOR": "Electrodoméstico que enfría comida",
    "HORNO": "Electrodoméstico para cocinar",
    "LAVADORA": "Máquina para lavar ropa",
    "ESCOBA": "Herramienta para barrer",
    "RECOGEDOR": "Utensilio para recoger la basura",
    "CUBO": "Recipiente para la basura",
    "ASPIRADORA": "Máquina que chupa el polvo",
    "LLAVE": "Objeto para abrir puertas",
    "CANDADO": "Objeto para cerrar con llave",
    "MALETA": "Bolsa para viajar",
    "MOCHILA": "Bolsa para llevar a la escuela",
    "PARAGUAS": "Objeto para protegerse de la lluvia",
    "PARASOL": "Objeto para protegerse del sol",

    # Naturaleza (50 palabras)
    "ARBOL": "Planta grande con tronco y ramas",
    "FLOR": "Parte colorida de las plantas",
    "HOJA": "Parte verde de los árboles",
    "HIERBA": "Planta pequeña del suelo",
    "PIEDRA": "Roca pequeña",
    "MONTAÑA": "Gran elevación de tierra",
    "RIO": "Corriente de agua natural",
    "LAGO": "Gran cuerpo de agua rodeado de tierra",
    "MAR": "Gran extensión de agua salada",
    "OCEANO": "Masa de agua muy grande",
    "PLAYA": "Orilla del mar con arena",
    "DESIERTO": "Lugar seco con mucha arena",
    "BOSQUE": "Lugar con muchos árboles",
    "JARDIN": "Terreno con plantas cultivadas",
    "PARQUE": "Área verde para jugar",
    "SOL": "Estrella que nos da luz y calor",
    "LUNA": "Satélite natural de la Tierra",
    "ESTRELLA": "Punto brillante en el cielo nocturno",
    "NUBE": "Masa de vapor en el cielo",
    "LLUVIA": "Agua que cae del cielo",
    "NIEVE": "Agua congelada que cae en copos",
    "VIENTO": "Aire en movimiento",
    "RAYO": "Descarga eléctrica en una tormenta",
    "ARCOIRIS": "Bandas de colores después de la lluvia",
    "TIERRA": "Planeta donde vivimos",
    "CIELO": "Espacio sobre la Tierra",
    "PASTO": "Hierba verde en el suelo",
    "MUSGO": "Planta verde que crece en piedras",
    "TRONCO": "Parte principal de un árbol",
    "RAIZ": "Parte del árbol bajo tierra",
    "SEMILLA": "Pequeño grano para plantar",
    "FRUTO": "Resultado de una flor",
    "CESPED": "Pasto cortado en jardines",
    "CHARCO": "Pequeña acumulación de agua",
    "CASCADA": "Caída de agua de una montaña",
    "VOLCAN": "Montaña que expulsa lava",
    "ISLA": "Tierra rodeada de agua",
    "PENINSULA": "Tierra rodeada de agua por todos lados menos uno",
    "VALLE": "Terreno entre montañas",
    "CAÑON": "Garganta profunda entre montañas",
    "CUEVA": "Hueco grande en una montaña",
    "ACANTILADO": "Pared rocosa junto al mar",
    "GLACIAR": "Masa de hielo en las montañas",
    "DUNAS": "Montículos de arena en el desierto",
    "OASIS": "Lugar con agua en el desierto",
    "SENDERO": "Camino para caminar en la naturaleza",
    "CAMPO": "Terreno para cultivar",
    "HUERTO": "Terreno para cultivar verduras",
    "INVERNADERO": "Estructura para cultivar plantas",
    "MACETA": "Recipiente para plantas",

    # Profesiones (30 palabras)
    "DOCTOR": "Persona que cura enfermos",
    "ENFERMERO": "Ayuda al doctor a cuidar pacientes",
    "MAESTRO": "Persona que enseña en la escuela",
    "BOMBERO": "Persona que apaga incendios",
    "POLICIA": "Persona que cuida el orden",
    "COCINERO": "Persona que prepara comida",
    "PANADERO": "Persona que hace pan",
    "CARTERO": "Persona que reparte cartas",
    "PILOTO": "Persona que vuela aviones",
    "CONDUCTOR": "Persona que maneja autos",
    "GRANJERO": "Persona que trabaja en el campo",
    "JARDINERO": "Persona que cuida jardines",
    "PINTOR": "Persona que pinta cuadros",
    "MUSICO": "Persona que toca instrumentos",
    "ACTOR": "Persona que actúa en películas",
    "BAILARIN": "Persona que baila",
    "DEPORTISTA": "Persona que practica deportes",
    "ARQUITECTO": "Persona que diseña edificios",
    "INGENIERO": "Persona que construye máquinas",
    "CIENTIFICO": "Persona que hace experimentos",
    "ASTRONAUTA": "Persona que viaja al espacio",
    "BUZO": "Persona que trabaja bajo el agua",
    "MARINERO": "Persona que trabaja en barcos",
    "SOLDADO": "Persona que defiende el país",
    "VETERINARIO": "Doctor de animales",
    "PELUQUERO": "Persona que corta el pelo",
    "MECANICO": "Persona que repara autos",
    "CARPINTERO": "Persona que trabaja con madera",
    "FONTANERO": "Persona que repara tuberías",
    "ELECTRICISTA": "Persona que arregla cables",

    # Deportes (30 palabras)
    "FUTBOL": "Deporte con balón y porterías",
    "BALONCESTO": "Deporte con canasta y balón naranja",
    "TENIS": "Deporte con raqueta y pelota amarilla",
    "NATACION": "Deporte en el agua",
    "CICLISMO": "Deporte con bicicleta",
    "ATLETISMO": "Deporte de correr y saltar",
    "GIMNASIA": "Deporte de hacer acrobacias",
    "BEISBOL": "Deporte con bate y pelota",
    "VOLEIBOL": "Deporte con red y pelota",
    "RUGBY": "Deporte con balón ovalado",
    "HOCKEY": "Deporte con palo y disco",
    "PATINAJE": "Deporte sobre ruedas",
    "SURF": "Deporte sobre olas del mar",
    "ESQUI": "Deporte en la nieve con tablas",
    "SNOWBOARD": "Deporte en la nieve con una tabla",
    "KARATE": "Arte marcial con golpes",
    "JUDO": "Arte marcial con luchas",
    "BOXEO": "Deporte de pelea con guantes",
    "LUCHA": "Deporte de forcejear",
    "TIRO": "Deporte de disparar a un blanco",
    "ARCO": "Deporte con arco y flechas",
    "EQUITACION": "Deporte de montar a caballo",
    "GOLF": "Deporte con palos y hoyos",
    "BOLOS": "Deporte de derribar pinos",
    "BADMINTON": "Deporte con raqueta y volante",
    "TENIS": "Deporte de mesa con pelota pequeña",
    "SALTOS": "Deporte de saltar en trampolín",
    "LEVANTAMIENTO": "Deporte de levantar pesas",
    "CARRERA": "Deporte de correr rápido",
    "MARCHA": "Deporte de caminar rápido",

    # Transporte (30 palabras)
    "AUTO": "Vehículo de cuatro ruedas",
    "BUS": "Vehículo grande para muchas personas",
    "TREN": "Vehículo que va sobre rieles",
    "AVION": "Vehículo que vuela por el aire",
    "BARCO": "Vehículo que flota en el agua",
    "BICICLETA": "Vehículo de dos ruedas con pedales",
    "MOTO": "Vehículo de dos ruedas con motor",
    "CAMION": "Vehículo grande para carga",
    "TAXI": "Auto que se paga por viaje",
    "AMBULANCIA": "Vehículo para llevar enfermos",
    "BOMBEROS": "Vehículo rojo para incendios",
    "POLICIA": "Vehículo de la policía",
    "TRACTOR": "Vehículo para el campo",
    "GRUA": "Vehículo para levantar cosas pesadas",
    "EXCAVADORA": "Máquina para cavar hoyos",
    "SUBTERRANEO": "Tren que va bajo tierra",
    "TREN": "Vehículo con vagones",
    "HELICOPTERO": "Vehículo que vuela con hélices",
    "GLOBO": "Vehículo que vuela con aire caliente",
    "COHETE": "Vehículo que va al espacio",
    "PATINETA": "Tabla con ruedas para patinar",
    "MONOPATIN": "Patineta con manillar",
    "PATINES": "Calzado con ruedas",
    "CARRO": "Vehículo de compras en el supermercado",
    "CARRIOLA": "Vehículo para bebés",
    "SILLA": "Vehículo con ruedas para personas que no pueden caminar",
    "FUNICULAR": "Tren que sube montañas",
    "TRANVIA": "Tren que va por la ciudad",
    "FERRY": "Barco para transportar personas y autos",
    "YATE": "Barco de lujo",

    # Escuela (30 palabras)
    "AULA": "Habitación donde se dan clases",
    "PIZARRA": "Superficie para escribir con tiza",
    "TIZA": "Barra para escribir en la pizarra",
    "BORRADOR": "Objeto para borrar la pizarra",
    "ESCRITORIO": "Mesa del profesor",
    "PUPITRE": "Mesa del estudiante",
    "MOCHILA": "Bolsa para llevar libros",
    "ESTUCHE": "Caja para guardar lápices",
    "REGLA": "Instrumento para medir y trazar líneas",
    "COMPAS": "Instrumento para hacer círculos",
    "CALCULADORA": "Máquina para hacer cuentas",
    "DICCIONARIO": "Libro con significado de palabras",
    "ATLAS": "Libro de mapas",
    "GLOBO": "Esfera con mapa del mundo",
    "MAPAMUNDI": "Mapa de todo el mundo",
    "MICROSCOPIO": "Instrumento para ver cosas pequeñas",
    "TELESCOPIO": "Instrumento para ver cosas lejanas",
    "LABORATORIO": "Lugar para hacer experimentos",
    "BIBLIOTECA": "Lugar con muchos libros",
    "GIMNASIO": "Lugar para hacer deporte",
    "PATIO": "Lugar exterior para jugar",
    "COMEDOR": "Lugar para comer en la escuela",
    "AUDITORIO": "Sala para actuaciones",
    "OFICINA": "Despacho del director",
    "BAÑO": "Lugar para necesidades fisiológicas",
    "CASILLERO": "Armario pequeño para guardar cosas",
    "UNIFORME": "Ropa igual para todos los estudiantes",
    "RECREO": "Tiempo de juego en la escuela",
    "CLASE": "Lección que da el maestro",
    "TAREA": "Trabajo para hacer en casa",

    # Familia y Personas (30 palabras)
    "PADRE": "Hombre que tiene hijos",
    "MADRE": "Mujer que tiene hijos",
    "HIJO": "Niño de unos padres",
    "HIJA": "Niña de unos padres",
    "HERMANO": "Hijo de tus padres",
    "HERMANA": "Hija de tus padres",
    "ABUELO": "Padre de tu padre o madre",
    "ABUELA": "Madre de tu padre o madre",
    "NIETO": "Hijo de tu hijo",
    "NIETA": "Hija de tu hijo",
    "TIO": "Hermano de tu padre o madre",
    "TIA": "Hermana de tu padre o madre",
    "PRIMO": "Hijo de tu tío o tía",
    "PRIMA": "Hija de tu tío o tía",
    "SOBRINO": "Hijo de tu hermano",
    "SOBRINA": "Hija de tu hermano",
    "BEBE": "Niño muy pequeño",
    "NINO": "Persona joven",
    "NINA": "Persona joven femenina",
    "ADULTO": "Persona mayor de edad",
    "ANCIANO": "Persona muy mayor",
    "AMIGO": "Persona con la que te llevas bien",
    "VECINO": "Persona que vive cerca",
    "COMPAÑERO": "Persona que está contigo en clase",
    "MAESTRO": "Persona que enseña",
    "DIRECTOR": "Jefe de la escuela",
    "DOCTOR": "Persona que cura",
    "ENFERMERO": "Persona que ayuda al doctor",
    "BOMBERO": "Persona que apaga fuegos",
    "POLICIA": "Persona que protege",

    # Ropa (30 palabras)
    "CAMISA": "Prenda con botones para el torso",
    "PANTALON": "Prenda para las piernas",
    "VESTIDO": "Prenda femenina de una pieza",
    "FALDA": "Prenda femenina para la cintura",
    "ZAPATOS": "Calzado para los pies",
    "TENIS": "Zapatos deportivos",
    "BOTAS": "Calzado que cubre el tobillo",
    "SANDALIAS": "Calzado abierto para verano",
    "CALCETINES": "Prenda para los pies",
    "ROPA": "Prenda interior",
    "SUETER": "Prenda de abrigo para el torso",
    "CHAQUETA": "Prenda de abrigo con mangas",
    "ABRIGO": "Prenda gruesa para invierno",
    "GORRA": "Prenda para la cabeza con visera",
    "SOMBRERO": "Prenda para la cabeza con ala",
    "GORRO": "Prenda de lana para la cabeza",
    "BUFANDA": "Prenda larga para el cuello",
    "GUANTES": "Prenda para las manos",
    "PIJAMA": "Ropa para dormir",
    "UNIFORME": "Ropa igual para un grupo",
    "TRAJE": "Ropa formal para hombres",
    "CORBATA": "Prenda para el cuello en trajes",
    "CINTURON": "Prenda para sujetar el pantalón",
    "BOLSO": "Accesorio para llevar cosas",
    "MOCHILA": "Bolso para la espalda",
    "PARAGUAS": "Objeto para la lluvia",
    "GAFAS": "Objeto para ver mejor o proteger los ojos",
    "RELOJ": "Objeto para la muñeca con hora",
    "COLLAR": "Adorno para el cuello",
    "PULSERA": "Adorno para la muñeca",

    # Colores (20 palabras)
    "ROJO": "Color de la sangre",
    "AZUL": "Color del cielo",
    "AMARILLO": "Color del sol",
    "VERDE": "Color de las plantas",
    "NARANJA": "Color de la naranja",
    "MORADO": "Color de la uva",
    "ROSA": "Color de la flor del mismo nombre",
    "MARRON": "Color de la tierra",
    "BLANCO": "Color de la nieve",
    "NEGRO": "Color de la noche",
    "GRIS": "Color de las nubes de tormenta",
    "DORADO": "Color del oro",
    "PLATEADO": "Color de la plata",
    "CELESTE": "Color del cielo despejado",
    "TURQUESA": "Color entre azul y verde",
    "VIOLETA": "Color morado oscuro",
    "BEIGE": "Color marrón claro",
    "LILA": "Color morado claro",
    "ESMERALDA": "Color verde brillante",
    "MAGENTA": "Color rosa intenso",

    # Números (10 palabras)
    "UNO": "Primer número",
    "DOS": "Número después del uno",
    "TRES": "Número después del dos",
    "CUATRO": "Número después del tres",
    "CINCO": "Número después del cuatro",
    "SEIS": "Número después del cinco",
    "SIETE": "Número después del seis",
    "OCHO": "Número después del siete",
    "NUEVE": "Número después del ocho",
    "DIEZ": "Número después del nueve",

    # Formas (10 palabras)
    "CIRCULO": "Figura redonda",
    "CUADRADO": "Figura con cuatro lados iguales",
    "TRIANGULO": "Figura con tres lados",
    "RECTANGULO": "Figura con cuatro lados, dos más largos",
    "ESTRELLA": "Figura con puntas",
    "CORAZON": "Figura del símbolo del amor",
    "OVALO": "Figura redonda alargada",
    "ROMBO": "Figura con cuatro lados iguales en diagonal",
    "CRUZ": "Figura con dos líneas que se cortan",
    "ESPIRAL": "Figura que gira en círculos"
}

def mostrar_info_dificultad():
    config = CONFIG_DIFICULTAD[DIFICULTAD_ACTUAL]
    texto_dificultad = fuente_pista.render(f"DIFICULTAD: {DIFICULTAD_ACTUAL}", True, COLOR_ROJO)
    pantalla.blit(texto_dificultad, (960, 10))
    
    if len(dificultades_desbloqueadas) < 3:
        sig = "DARK" if "DARK" not in dificultades_desbloqueadas else "EXTREM"
        progreso = fuente_pista.render(f"PRÓXIMO: {sig} ({puntos_acumulados}/{PUNTOS_PARA_DESBLOQUEAR})", True, COLOR_TEXTO)
        pantalla.blit(progreso, (960, 40))

def dibujar_ahorcado(intentos_fallidos):
    """Dibuja el ahorcado progresivamente según los intentos fallidos"""
    # Posición y dimensiones de la horca (más a la derecha)
    base_x, base_y = 950, 450
    altura_horca = 200
    ancho_horca = 150
    
    # Color que cambia según intentos
    if intentos_fallidos <= 2:
        color = COLOR_VERDE
    elif intentos_fallidos <= 4:
        color = COLOR_AMARILLO
    else:
        color = COLOR_ROJO
    
    # Dibujar la base (siempre visible)
    pygame.draw.line(pantalla, color, (base_x, base_y), (base_x + 100, base_y), 5)
    pygame.draw.line(pantalla, color, (base_x + 50, base_y), (base_x + 50, base_y - altura_horca), 5)
    pygame.draw.line(pantalla, color, (base_x + 50, base_y - altura_horca), 
                    (base_x + 50 + ancho_horca/2, base_y - altura_horca), 5)
    
    # Dibujar la soga (siempre visible)
    pygame.draw.line(pantalla, color, (base_x + 50 + ancho_horca/2, base_y - altura_horca), 
                    (base_x + 50 + ancho_horca/2, base_y - altura_horca + 30), 5)
    
    # Dibujar progresivamente el cuerpo según los intentos fallidos
    if intentos_fallidos >= 1:
        # Cabeza
        pygame.draw.circle(pantalla, color, 
                          (int(base_x + 50 + ancho_horca/2), int(base_y - altura_horca + 50)), 20, 3)
    
    if intentos_fallidos >= 2:
        # Cuerpo
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 70),
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 130), 3)
    
    if intentos_fallidos >= 3:
        # Brazo izquierdo
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 80),
                        (base_x + 50 + ancho_horca/2 - 30, base_y - altura_horca + 110), 3)
    
    if intentos_fallidos >= 4:
        # Brazo derecho
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 80),
                        (base_x + 50 + ancho_horca/2 + 30, base_y - altura_horca + 110), 3)
    
    if intentos_fallidos >= 5:
        # Pierna izquierda
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 130),
                        (base_x + 50 + ancho_horca/2 - 25, base_y - altura_horca + 170), 3)
    
    if intentos_fallidos >= 6:
        # Pierna derecha
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2, base_y - altura_horca + 130),
                        (base_x + 50 + ancho_horca/2 + 25, base_y - altura_horca + 170), 3)
        
        # Cara triste (cuando está completamente ahorcado)
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2 - 8, base_y - altura_horca + 45),
                        (base_x + 50 + ancho_horca/2 - 2, base_y - altura_horca + 45), 2)
        pygame.draw.line(pantalla, color, 
                        (base_x + 50 + ancho_horca/2 + 8, base_y - altura_horca + 45),
                        (base_x + 50 + ancho_horca/2 + 2, base_y - altura_horca + 45), 2)
        pygame.draw.arc(pantalla, color, 
                       (base_x + 50 + ancho_horca/2 - 10, base_y - altura_horca + 50, 20, 15),
                       3.14, 6.28, 2)
        
def dividir_texto(texto, max_caracteres):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        if len(linea_actual + " " + palabra) <= max_caracteres:
            if linea_actual:
                linea_actual += " " + palabra
            else:
                linea_actual = palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    
    if linea_actual:
        lineas.append(linea_actual)
    
    return lineas

def iniciar_juego():
    global palabra_actual, pista_actual, letras_adivinadas, letras_intentadas, progreso_actual, intentos_restantes, tiempo_inicio
    lista_palabras = list(palabras.keys())
    palabra_actual = random.choice(lista_palabras)
    pista_actual = palabras[palabra_actual]
    letras_adivinadas = []
    letras_intentadas = []
    intentos_restantes = CONFIG_DIFICULTAD[DIFICULTAD_ACTUAL]["intentos"]
    tiempo_inicio = time.time()
    actualizar_progreso()

def actualizar_progreso():
    global progreso_actual
    progreso_actual = ""
    for letra in palabra_actual:
        if letra in letras_adivinadas:
            progreso_actual += letra + " "
        else:
            progreso_actual += "_ "
    return progreso_actual

def procesar_letra(letra):
    global intentos_restantes, valor_puntuacion, puntos_acumulados, letras_adivinadas, letras_intentadas
    
    if letra in letras_intentadas:
        return False
    
    letras_intentadas.append(letra)
    
    if letra in palabra_actual:
        letras_adivinadas.append(letra)
        actualizar_progreso()
        reproducir_sonido_normal(sonido_correcto)
        crear_particulas(450, 200, 10, "brillo")
        
        if all(l in letras_adivinadas for l in palabra_actual):
            puntos_ganados = CONFIG_DIFICULTAD[DIFICULTAD_ACTUAL]["puntos_ganar"]
            valor_puntuacion += puntos_ganados
            puntos_acumulados += puntos_ganados
            
            dificultad_desbloqueada = verificar_desbloqueo_dificultad()
            if dificultad_desbloqueada:
                crear_particulas(450, 300, 100, "confeti")
                reproducir_sonido_especial(sonido_ganador)
            
            reproducir_sonido_especial(sonido_ganador)
            crear_particulas(450, 150, 100, "confeti")
            return "ganador"
        return True
    else:
        intentos_restantes -= 1
        penalizacion = CONFIG_DIFICULTAD[DIFICULTAD_ACTUAL]["puntos_perder"]
        if penalizacion < 0:
            valor_puntuacion = max(0, valor_puntuacion + penalizacion)
        
        reproducir_sonido_normal(sonido_incorrecto)
        efectos_activos.append({"tipo": "shake", "duracion": 20})
        
        if intentos_restantes <= 0:
            reproducir_sonido_especial(sonido_perdedor)
            return "perdedor"
        return False

def mostrar_puntuacion(x, y):
    puntuacion = fuente_montserrat_bold.render("PUNTAJE : " + str(valor_puntuacion), True, COLOR_ROJO)
    pantalla.blit(puntuacion, (x, y))

def mostrar_intentos(x, y):
    intentos = fuente_montserrat_bold.render("INTENTOS : " + str(intentos_restantes), True, COLOR_TEXTO)
    pantalla.blit(intentos, (x, y))

def mostrar_pista():
    pygame.draw.rect(pantalla, COLOR_FONDO, (50, 100, 800, 80))
    pygame.draw.rect(pantalla, (50, 50, 150), (50, 100, 800, 80), 2)
    
    titulo_pista = fuente_pista.render("Pista:", True, COLOR_BLANCO)
    pantalla.blit(titulo_pista, (60, 105))
    
    lineas_pista = dividir_texto(pista_actual, 60)
    
    for i, linea in enumerate(lineas_pista):
        pista_texto = fuente_pista.render(linea, True, COLOR_TEXTO)
        pantalla.blit(pista_texto, (150, 105 + i * 25))

def mostrar_palabra():
    offset_x, offset_y = 0, 0
    for efecto in efectos_activos[:]:
        if efecto["tipo"] == "shake":
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            efecto["duracion"] -= 1
            if efecto["duracion"] <= 0:
                efectos_activos.remove(efecto)
    
    palabra_texto = fuente.render(progreso_actual, True, COLOR_TEXTO)
    palabra_rect = palabra_texto.get_rect(center=(450 + offset_x, 200 + offset_y))
    pantalla.blit(palabra_texto, palabra_rect)

def mostrar_teclado():
    offset_x, offset_y = 0, 0
    for efecto in efectos_activos:
        if efecto["tipo"] == "shake":
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            break
    
    alfabeto = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S"],
        ["T", "U", "V", "W", "X", "Y", "Z"]
    ]
    
    ancho_cuadro = 50
    alto_cuadro = 50
    espacio_horizontal = 10
    espacio_vertical = 10
    inicio_x = 50
    inicio_y = 300
    
    for fila_idx, fila in enumerate(alfabeto):
        for col_idx, letra in enumerate(fila):
            x = inicio_x + col_idx * (ancho_cuadro + espacio_horizontal) + offset_x
            y = inicio_y + fila_idx * (alto_cuadro + espacio_vertical) + offset_y
            
            if letra in letras_adivinadas:
                color = COLOR_VERDE
                color_fondo = (0, 100, 0)
            elif letra in letras_intentadas:
                color = COLOR_ROJO
                color_fondo = (100, 0, 0)
            else:
                color = (200, 200, 200)
                color_fondo = (50, 50, 50)
            
            pygame.draw.rect(pantalla, color_fondo, (x, y, ancho_cuadro, alto_cuadro))
            pygame.draw.rect(pantalla, color, (x, y, ancho_cuadro, alto_cuadro), 3)
            
            letra_texto = fuente_letras_bold.render(letra, True, color)
            letra_rect = letra_texto.get_rect(center=(x + ancho_cuadro // 2, y + alto_cuadro // 2))
            pantalla.blit(letra_texto, letra_rect)

def dibujar_boton_reiniciar():
    color_boton = COLOR_BOTON_HOVER if boton_reiniciar_rect.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)
    color_icono = (200, 200, 200) if boton_reiniciar_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_reiniciar_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_reiniciar_rect, 2, border_radius=6)
    
    centro_x = boton_reiniciar_rect.centerx
    centro_y = boton_reiniciar_rect.centery
    radio = 8
    
    pygame.draw.circle(pantalla, color_icono, (centro_x, centro_y), radio, 2)
    
    inicio_x = centro_x + 4
    inicio_y = centro_y - 4
    
    puntos_flecha = [
        (inicio_x, inicio_y),
        (inicio_x - 3, inicio_y - 3),
        (inicio_x - 6, inicio_y)
    ]
    pygame.draw.polygon(pantalla, color_icono, puntos_flecha)

def dibujar_boton_pausa():
    color_boton = (200, 200, 200) if boton_pausa_rect.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)
    color_icono = (200, 200, 200) if boton_pausa_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_TEXTO
    
    pygame.draw.rect(pantalla, color_boton, boton_pausa_rect, border_radius=6)
    pygame.draw.rect(pantalla, color_icono, boton_pausa_rect, 2, border_radius=6)
    
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 8, boton_pausa_rect.y + 6, 4, 20))
    pygame.draw.rect(pantalla, color_icono, (boton_pausa_rect.x + 20, boton_pausa_rect.y + 6, 4, 20))

def mostrar_pantalla_final(mensaje, color):
    pantalla.fill(COLOR_FONDO)
    
    centro_x = 640
    
    texto_resultado = fuente_montserrat_bold.render(mensaje, True, color)
    texto_rect = texto_resultado.get_rect(center=(centro_x, 150))
    pantalla.blit(texto_resultado, texto_rect)
    
    palabra_texto = fuente.render(f"LA PALABRA ERA: {palabra_actual}", True, COLOR_TEXTO)
    palabra_rect = palabra_texto.get_rect(center=(centro_x, 250))
    pantalla.blit(palabra_texto, palabra_rect)
    
    puntuacion_texto = fuente.render(f"PUNTUACIÓN TOTAL: {valor_puntuacion}", True, COLOR_TEXTO)
    puntuacion_rect = puntuacion_texto.get_rect(center=(centro_x, 300))
    pantalla.blit(puntuacion_texto, puntuacion_rect)
    
    boton_ancho = 250
    boton_alto = 60
   
    boton_rect = pygame.Rect(centro_x - boton_ancho // 2, 450, boton_ancho, boton_alto)
    
    color_boton = COLOR_BOTON_HOVER if boton_rect.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON_EASY
    
    pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=8)
    pygame.draw.rect(pantalla, COLOR_TEXTO, boton_rect, 2, border_radius=8)
    
    texto_reiniciar = fuente_botones.render("JUGAR DE NUEVO", True, COLOR_TEXTO)
    texto_rect = texto_reiniciar.get_rect(center=boton_rect.center)
    pantalla.blit(texto_reiniciar, texto_rect)
    
    return boton_rect

def mostrar_pausa():
    s = pygame.Surface((1280, 720))
    s.set_alpha(200)
    s.fill(COLOR_FONDO)
    pantalla.blit(s, (0, 0))

    centro_x = 640

    texto_pausa = fuente_pausa.render("PAUSA", True, COLOR_TEXTO)
    texto_rect = texto_pausa.get_rect(center=(centro_x, 250))
    pantalla.blit(texto_pausa, texto_rect)
    
    pygame.draw.polygon(pantalla, COLOR_TEXTO, [
        (centro_x - 40, 350),
        (centro_x - 40, 400),  
        (centro_x + 10, 375)
    ], 0)
    
    texto_continuar = fuente_boton.render("CLICK PARA CONTINUAR", True, COLOR_TEXTO)
    texto_rect = texto_continuar.get_rect(center=(centro_x, 450))
    pantalla.blit(texto_continuar, texto_rect)
   
    tiempo = pygame.time.get_ticks() / 1000
    titulo = fuente_montserrat_bold.render("AHORCADO", True, COLOR_ROJO)
    titulo_rect = titulo.get_rect(center=(centro_x, 100))
    
    surf_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    surf_temp.blit(titulo, (0, 0))
    surf_temp.set_alpha(200 + int(math.sin(tiempo * 3) * 55))
    pantalla.blit(surf_temp, titulo_rect)

def dibujar_selector_dificultad(x, y):
    titulo = fuente_montserrat_bold.render("SELECCIONA DIFICULTAD", True, COLOR_TEXTO)
    pantalla.blit(titulo, (x, y))
    
    for i, dificultad in enumerate(["EASY", "DARK", "EXTREM"]):
        boton = pygame.Rect(x + i * 120, y + 40, 100, 40)
        
        if dificultad in dificultades_desbloqueadas:
            color_fondo = COLOR_BLANCO
            if boton.collidepoint(pygame.mouse.get_pos()):
                color_fondo = (220, 220, 220)
            
            if DIFICULTAD_ACTUAL == dificultad:
                pygame.draw.rect(pantalla, color_fondo, boton, border_radius=8)
                pygame.draw.rect(pantalla, COLOR_ROJO, boton, 3, border_radius=8)
            else:
                pygame.draw.rect(pantalla, color_fondo, boton, border_radius=8)
                pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton, 2, border_radius=8)
            
            texto = fuente_pista.render(dificultad, True, (0, 0, 0))
            texto_rect = texto.get_rect(center=boton.center)
            pantalla.blit(texto, texto_rect)
            
        else:
            pygame.draw.rect(pantalla, (50, 50, 50), boton, border_radius=8)
            pygame.draw.rect(pantalla, (100, 100, 100), boton, 2, border_radius=8)
            
            texto = fuente_pista.render("BLOQUEADO", True, (150, 150, 150))
            texto_rect = texto.get_rect(center=boton.center)
            
            if texto_rect.width > boton.width - 10:
                fuente_pequena = pygame.font.Font(None, 16)
                texto = fuente_pequena.render("BLOQUEADO", True, (150, 150, 150))
                texto_rect = texto.get_rect(center=boton.center)
            
            pantalla.blit(texto, texto_rect)
            
            candado_x = boton.centerx
            candado_y = boton.y + 15
            pygame.draw.rect(pantalla, (150, 150, 150), (candado_x - 6, candado_y, 12, 8))
            pygame.draw.arc(pantalla, (150, 150, 150), (candado_x - 5, candado_y - 3, 10, 6), 3.14, 6.28, 2)

def dibujar_menu_principal():
    pantalla.fill(COLOR_FONDO)
    
    centro_x = 640
    
    tiempo = pygame.time.get_ticks() / 1000
    titulo = fuente_montserrat_bold.render("AHORCADO", True, COLOR_ROJO)
    titulo_rect = titulo.get_rect(center=(centro_x, 100))
    
    surf_temp = pygame.Surface(titulo.get_size(), pygame.SRCALPHA)
    surf_temp.blit(titulo, (0, 0))
    surf_temp.set_alpha(200 + int(math.sin(tiempo * 3) * 55))
    pantalla.blit(surf_temp, titulo_rect)
    
    boton_ancho = 200
    boton_alto = 60
    boton_jugar = pygame.Rect(centro_x - boton_ancho // 2, 300, boton_ancho, boton_alto)
    
    color_boton = COLOR_ROJO if boton_jugar.collidepoint(pygame.mouse.get_pos()) else (200, 0, 0)
    
    pygame.draw.rect(pantalla, color_boton, boton_jugar, border_radius=12)
    pygame.draw.rect(pantalla, COLOR_ROJO, boton_jugar, 3, border_radius=12)
    
    texto_jugar = fuente_montserrat_bold.render("JUGAR", True, (255, 255, 255))
    texto_rect = texto_jugar.get_rect(center=boton_jugar.center)
    pantalla.blit(texto_jugar, texto_rect)
    
    # CORREGIDO: Posición correcta del selector de dificultad
    selector_ancho = 360
    dibujar_selector_dificultad(centro_x - selector_ancho // 2, 200)
    
    instrucciones = [
        "-HAZ CLIC EN LAS LETRAS O USA EL TECLADO",
        "-ADIVINA LA PALABRA ANTES DE COMPLETAR EL AHORCADO",
        "-CONSIGUE 50 PUNTOS PARA DESBLOQUEAR NUEVAS DIFICULTADES",
        "-¡BUENA SUERTE!"
    ]
    
    for i, linea in enumerate(instrucciones):
        texto = fuente_pista.render(linea, True, COLOR_TEXTO)
        texto_rect = texto.get_rect(center=(centro_x, 400 + i * 25))
        pantalla.blit(texto, texto_rect)
    
    if random.random() < 0.05:
        crear_particulas(centro_x, 150, 5, "confeti")
    
    return boton_jugar

# =============================================================================
# BUCLE PRINCIPAL DEL JUEGO CORREGIDO
# =============================================================================

jugando = True
reloj = pygame.time.Clock()

while jugando:
    mouse_pos = pygame.mouse.get_pos()
    
    # Actualizar partículas
    particulas = [p for p in particulas if p.update()]
    
    # Verificar si debe reanudar la música después de sonidos especiales
    verificar_reanudar_musica()
    
    # Dibujar según el estado del juego
    if estado_juego == "menu":
        boton_jugar = dibujar_menu_principal()
        
    elif estado_juego == "jugando" and not pausa:
        pantalla.fill(COLOR_FONDO)
        pantalla.blit(fondo, (0, 0))
        
        mostrar_puntuacion(10, 10)
        mostrar_intentos(10, 50)
        mostrar_info_dificultad()
        mostrar_pista()
        mostrar_palabra()
        
        intentos_fallidos = CONFIG_DIFICULTAD[DIFICULTAD_ACTUAL]["intentos"] - intentos_restantes
        dibujar_ahorcado(intentos_fallidos)
        mostrar_teclado()
        dibujar_boton_reiniciar()
        dibujar_boton_pausa()
        
    elif estado_juego == "ganador":
        boton_reiniciar_centro = mostrar_pantalla_final("¡GANASTE!", COLOR_ROJO)
        
    elif estado_juego == "perdedor":
        boton_reiniciar_centro = mostrar_pantalla_final("PERDISTE", COLOR_ROJO)
    
    # Dibujar partículas
    for particula in particulas:
        particula.draw(pantalla)
    
    # Mostrar pantalla de pausa si está pausado
    if pausa and estado_juego == "jugando":
        mostrar_pausa()
    
    # Manejar eventos - CORREGIDO: Todo dentro del bucle de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado_juego == "menu":
                if boton_jugar.collidepoint(mouse_pos):
                    estado_juego = "jugando"
                    iniciar_juego()
                
                # CORREGIDO: Posición correcta para los botones de dificultad
                for i, dificultad in enumerate(["EASY", "DARK", "EXTREM"]):
                    boton = pygame.Rect(460 + i * 120, 240, 100, 40)  # 640-180=460 para centrar
                    if boton.collidepoint(mouse_pos) and dificultad in dificultades_desbloqueadas:
                        cambiar_dificultad(dificultad)
                        
            elif pausa:
                pausa = False
                try:
                    mixer.music.unpause()
                except:
                    pass
                
            elif boton_pausa_rect.collidepoint(mouse_pos) and estado_juego == "jugando":
                pausa = True
                try:
                    mixer.music.pause()
                except:
                    pass
                
            elif boton_reiniciar_rect.collidepoint(mouse_pos) and estado_juego == "jugando":
                iniciar_juego()
            
            elif estado_juego in ["ganador", "perdedor"]:
                if boton_reiniciar_centro.collidepoint(mouse_pos):
                    estado_juego = "jugando"
                    iniciar_juego()
            
            elif not pausa and estado_juego == "jugando":
                alfabeto = [
                    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                    ["K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S"],
                    ["T", "U", "V", "W", "X", "Y", "Z"]
                ]

                ancho_cuadro = 50  
                alto_cuadro = 50   
                espacio_horizontal = 10
                espacio_vertical = 10
                inicio_x = 50
                inicio_y = 300

                for fila_idx, fila in enumerate(alfabeto):
                    for col_idx, letra in enumerate(fila):
                        x = inicio_x + col_idx * (ancho_cuadro + espacio_horizontal)
                        y = inicio_y + fila_idx * (alto_cuadro + espacio_vertical)
                        rect_letra = pygame.Rect(x, y, ancho_cuadro, alto_cuadro)

                        if rect_letra.collidepoint(mouse_pos) and letra not in letras_intentadas:
                            resultado = procesar_letra(letra)
                            if resultado == "ganador":
                                estado_juego = "ganador"
                            elif resultado == "perdedor":
                                estado_juego = "perdedor"
        
        # CORREGIDO: Detección de teclas dentro del bucle de eventos
        if evento.type == pygame.KEYDOWN:
            # Tecla ESC para pausar
            if evento.key == pygame.K_ESCAPE and estado_juego == "jugando":
                pausa = not pausa
                if pausa:
                    try:
                        mixer.music.pause()
                    except:
                        pass
                else:
                    try:
                        mixer.music.unpause()
                    except:
                        pass
            
            # Tecla ENTER para reiniciar en pantallas de ganador/perdedor
            if evento.key == pygame.K_RETURN and estado_juego in ["ganador", "perdedor"]:
                estado_juego = "jugando"
                iniciar_juego()
                
            # Detección de letras para el juego
            if not pausa and estado_juego == "jugando":
                letra = evento.unicode.upper()
                if letra.isalpha() and len(letra) == 1:
                    resultado = procesar_letra(letra)
                    if resultado == "ganador":
                        estado_juego = "ganador"
                    elif resultado == "perdedor":
                        estado_juego = "perdedor"

    pygame.display.update()
    reloj.tick(60)
                
pygame.quit()