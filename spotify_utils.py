import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from google import genai

load_dotenv()

PERMISOS = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=PERMISOS,
    open_browser=True,
    cache_path=".cache"
))

cliente_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ARCHIVO_HISTORIAL = "historial.json"


def traducir_a_consulta(texto_usuario):
    """Traduce lenguaje natural a consulta de Spotify."""
    prompt = f"""Eres un experto en música de Spotify. Convierte la petición del usuario en una consulta de búsqueda válida.
Reglas:
1. Si es un artista: artist:"nombre"
2. Si es un género: genre:nombre
3. Devuelve SOLO la consulta, sin explicaciones.
Ejemplos: "Bad Bunny" -> artist:"Bad Bunny"; "rock clásico" -> genre:classic rock

Petición: {texto_usuario}
Consulta:"""
    interaccion = cliente_gemini.interactions.create(model="gemini-3.6-flash", input=prompt)
    return interaccion.output_text.strip()


def modo_sorprendeme():
    """Pide a Gemini que invente una consulta creativa pero SEGURA para Spotify."""
    prompt = """Inventa UNA consulta de búsqueda para la API de Spotify que SIEMPRE devuelva resultados.

REGLAS ESTRICTAS:
1. Usa SOLO UNO de estos formatos simples:
   - genre:nombre_genero          (ej: genre:jazz, genre:synthpop, genre:lofi)
   - artist:"nombre artista"      (ej: artist:"Daft Punk")
   - Una palabra clave suelta     (ej: lofi, chill, jazz)

2. NUNCA combines genre + year, genre + artist, ni uses comillas dentro de genre:.
3. Usa SIEMPRE géneros universales y conocidos: pop, rock, jazz, hip-hop, electronic, classical, reggae, blues, soul, funk, latin, indie, metal, punk, folk, country, ambient, lofi, house, techno, trap, r&b, disco, salsa, bossa nova.
4. Elige algo variado y sorprendente, pero SEGURO.

RESPONDE SOLO CON LA CONSULTA, sin explicaciones ni comillas extras.

Ejemplos válidos:
genre:synthpop
artist:"Tame Impala"
genre:bossa nova
lofi hip hop

Consulta:"""
    interaccion = cliente_gemini.interactions.create(model="gemini-3.6-flash", input=prompt)
    return interaccion.output_text.strip().strip('"').strip("'")


def buscar_canciones(consulta, limite_total=50):
    """
    Busca canciones en Spotify con la consulta dada.
    Si no hay resultados, intenta automáticamente con versiones más simples.
    Devuelve info completa: título, artista, álbum, imagen y preview.
    """
    # Intento 1: la consulta original tal cual
    canciones = _buscar_canciones_interno(consulta, limite_total)

    # Intento 2: sin comillas y sin filtros de año (los que más fallan)
    if not canciones:
        consulta_simple = consulta.replace('"', '')
        if 'year:' in consulta_simple:
            consulta_simple = consulta_simple.split('year:')[0]
        consulta_simple = consulta_simple.strip()
        print(f"⚠️ Sin resultados para '{consulta}'. Probando con: '{consulta_simple}'")
        canciones = _buscar_canciones_interno(consulta_simple, limite_total)

    # Intento 3: solo la primera palabra clave (último recurso)
    if not canciones:
        palabras = consulta.replace('genre:', '').replace('artist:', '').replace('"', '').split()
        palabra_clave = palabras[0] if palabras else "pop"
        print(f"⚠️ Sin resultados. Probando solo con: '{palabra_clave}'")
        canciones = _buscar_canciones_interno(palabra_clave, limite_total)

    return canciones


def _buscar_canciones_interno(consulta, limite_total=50):
    """Función interna que ejecuta la búsqueda real en Spotify."""
    canciones = []
    uris_vistos = set()
    offset = 0
    limit = 10

    while len(canciones) < limite_total:
        try:
            resultados = sp.search(q=consulta, type='track', limit=limit, offset=offset)
        except Exception as e:
            print(f"❌ Error en la búsqueda: {e}")
            break

        pistas = resultados['tracks']['items']
        if not pistas:
            break

        for pista in pistas:
            if pista['uri'] in uris_vistos:
                continue
            uris_vistos.add(pista['uri'])

            # Extraer la imagen más pequeña (o la más grande si prefieres)
            imagenes = pista['album'].get('images', [])
            imagen_url = imagenes[-1]['url'] if imagenes else None

            canciones.append({
                'uri': pista['uri'],
                'nombre': pista['name'],
                'artista': pista['artists'][0]['name'],
                'album': pista['album']['name'],
                'imagen': imagen_url,
                'preview': pista.get('preview_url')
            })

        offset += limit

    return canciones[:limite_total]


def crear_playlist(nombre, uris, publica=False):
    """Crea una playlist y la registra en el historial."""
    if not uris:
        return None

    playlist = sp._post("me/playlists", payload={
        "name": nombre,
        "public": publica,
        "description": "Creada con IA 🎧"
    })
    playlist_id = playlist['id']

    for i in range(0, len(uris), 100):
        sp._post(f"playlists/{playlist_id}/items", payload={"uris": uris[i:i+100]})

    url = playlist['external_urls']['spotify']
    guardar_en_historial(nombre, url, len(uris))
    return url


def guardar_en_historial(nombre, url, num_canciones):
    """Guarda el registro de una playlist creada en un archivo JSON."""
    historial = []

    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, 'r', encoding='utf-8') as f:
            try:
                historial = json.load(f)
            except json.JSONDecodeError:
                historial = []

    from datetime import datetime
    historial.append({
        'nombre': nombre,
        'url': url,
        'canciones': num_canciones,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    with open(ARCHIVO_HISTORIAL, 'w', encoding='utf-8') as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)


def obtener_historial():
    """Lee el historial desde el archivo JSON."""
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []
    with open(ARCHIVO_HISTORIAL, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def obtener_playlists_usuario():
    """Obtiene las playlists del usuario para el selector de 'añadir a existente'."""
    playlists = sp.current_user_playlists(limit=50)
    return [{'id': p['id'], 'nombre': p['name']} for p in playlists['items']]


def agregar_a_playlist(playlist_id, uris):
    """Añade canciones a una playlist existente."""
    for i in range(0, len(uris), 100):
        sp._post(f"playlists/{playlist_id}/items", payload={"uris": uris[i:i+100]})