# 🎵 Spotify IA

Aplicación web que crea y mejora playlists de Spotify usando inteligencia artificial. Escribe lo que quieres escuchar en lenguaje natural —por ejemplo, **"Bad Bunny"**, **"rock clásico"**, **"música para estudiar"** o **"una playlist para viajar de noche"**— y la IA traduce tu petición a una búsqueda útil para Spotify.

La app te muestra una previsualización de canciones con título, artista, álbum, portada y preview de 30 segundos. Después puedes seleccionar qué canciones incluir y confirmar si quieres crear una playlist nueva o añadirlas a una playlist existente.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.x-green?style=flat-square)
![Spotify](https://img.shields.io/badge/Spotify-Web%20API-1DB954?style=flat-square)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square)

---

## ✨ Funcionalidades

- **Búsqueda con lenguaje natural**: escribe una idea, artista, género, emoción o actividad, y Gemini la convierte en una consulta compatible con Spotify.
- **Previsualización antes de confirmar**: revisa las canciones encontradas antes de crear o modificar playlists.
- **Selección manual de canciones**: marca o desmarca cada canción antes de enviarla a Spotify.
- **Portadas y datos de álbum**: cada resultado muestra título, artista, álbum e imagen.
- **Previews de 30 segundos**: escucha fragmentos usando el `preview_url` disponible en Spotify.
- **Crear playlist nueva**: define el nombre de la playlist y créala directamente en tu cuenta.
- **Añadir a playlist existente**: selecciona una playlist de tu cuenta y agrega canciones nuevas.
- **Modo "Sorpréndeme"**: deja que la IA genere una búsqueda creativa automáticamente.
- **Historial local**: guarda un registro de playlists creadas en `historial.json`.
- **Compatibilidad con endpoints actuales de Spotify**: usa endpoints como `/me/playlists` y `/playlists/{id}/items`.

---

## 🛠️ Stack técnico

- **Backend**: Python 3.11+ con Flask
- **Cliente de Spotify**: Spotipy
- **IA**: Google Gemini mediante el SDK oficial `google-genai`
- **Frontend**: HTML5 + CSS embebido con tema oscuro inspirado en Spotify
- **Persistencia local**:
  - `.env` para credenciales
  - `historial.json` para el historial de playlists

---

## 📁 Estructura recomendada

```text
Spotify-IA/
│
├── app.py
├── .env
├── historial.json
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── preview.html
│   └── historial.html
│
└── static/
    ├── style.css
    └── app.js
```

La estructura puede variar según tu implementación, pero se recomienda separar las plantillas, estilos y lógica principal para mantener el proyecto ordenado.

---

## 🚀 Instalación paso a paso

### 1. Requisitos previos

Necesitas tener instalado:

- Python 3.11 o superior.
- Una cuenta de Spotify.
- Una API Key de Google Gemini.
- Git, si vas a clonar el repositorio.

> Spotify Premium no es obligatorio para crear playlists. Puede ser necesario solo si más adelante agregas control de reproducción en dispositivos.

---

### 2. Clona el repositorio

```bash
git clone https://github.com/CastriDani/Spotify-IA.git
cd Spotify-IA
```

---

### 3. Crea un entorno virtual

#### En Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### En macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Sabrás que el entorno virtual está activo cuando veas `(venv)` al inicio de la terminal.

---

### 4. Instala las dependencias

```bash
pip install flask spotipy python-dotenv google-genai
```

También puedes crear un archivo `requirements.txt` con este contenido:

```txt
flask
spotipy
python-dotenv
google-genai
```

Y luego instalar con:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuración de Spotify Developer

### 1. Crea una app en Spotify Developer Dashboard

1. Ve a Spotify Developer Dashboard.
2. Inicia sesión con tu cuenta.
3. Haz clic en **Create app**.
4. Completa los campos:

```text
App name: Spotify IA
App description: Aplicación local para crear playlists con IA
Website: puede dejarse vacío si es un proyecto local
Redirect URI: http://127.0.0.1:8888/callback
API/SDKs: Web API
```

5. Pulsa **Add** después de escribir el Redirect URI.
6. Marca la aceptación de términos.
7. Guarda la app.

> El Redirect URI debe coincidir exactamente en Spotify Dashboard y en tu archivo `.env`.

---

### 2. Copia tus credenciales

Desde la app creada en Spotify Developer Dashboard, copia:

```text
Client ID
Client Secret
```

Estos datos se usarán en el archivo `.env`.

---

### 3. Añade tu cuenta como usuario autorizado

Mientras la app esté en modo desarrollo, solo las cuentas autorizadas podrán usarla.

1. Entra a tu app en Spotify Developer Dashboard.
2. Ve a **User Management**.
3. Añade el nombre y correo de tu cuenta de Spotify.
4. Guarda los cambios.

---

## 🤖 Configuración de Gemini

1. Entra a Google AI Studio.
2. Crea una nueva API Key.
3. Copia la clave generada.
4. Guárdala en el archivo `.env`.

---

## ⚙️ Variables de entorno

Crea un archivo llamado `.env` en la raíz del proyecto:

```env
SPOTIPY_CLIENT_ID=tu_client_id_aqui
SPOTIPY_CLIENT_SECRET=tu_client_secret_aqui
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

GEMINI_API_KEY=tu_api_key_de_gemini_aqui
GEMINI_MODEL=gemini-2.5-flash

SPOTIFY_MARKET=CO
```

Importante:

- No uses comillas.
- No dejes espacios alrededor del signo `=`.
- No subas este archivo a GitHub.

---

## ▶️ Ejecución

Con el entorno virtual activo, ejecuta:

```bash
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5000
```

La primera vez que realices una acción con Spotify, se abrirá el navegador para autorizar la app. Después de aceptar, Spotify redirigirá al callback configurado y la aplicación continuará el proceso.

---

## 📖 Cómo usar la app

1. Escribe lo que quieres escuchar en lenguaje natural.

Ejemplos:

```text
Bad Bunny
Rock clásico
Música para estudiar
Reggaetón viejo para una noche con amigos
Playlist tranquila para programar de noche
```

2. Revisa la previsualización de canciones.
3. Escucha los previews disponibles.
4. Marca o desmarca las canciones que quieras incluir.
5. Elige una de las dos opciones:
   - Crear una playlist nueva.
   - Añadir a una playlist existente.
6. Pulsa **Confirmar y ejecutar**.
7. Abre la playlist creada o actualizada en Spotify.
8. Consulta el historial desde la sección correspondiente.

---

## 🧪 Ejemplos de prompts

```text
Crea una playlist de salsa romántica.
```

```text
Quiero música para concentrarme mientras programo.
```

```text
Hazme una playlist para viajar en carretera.
```

```text
Sorpréndeme con música indie para una tarde lluviosa.
```

```text
Crea una playlist con música urbana, pero evita canciones demasiado explícitas.
```

---

## 🧯 Errores comunes

### Error: `INVALID_CLIENT`

Revisa que estas variables estén bien escritas en `.env`:

```env
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=
```

No deben tener espacios ni comillas.

---

### Error: `INVALID_REDIRECT_URI`

Verifica que el Redirect URI sea exactamente el mismo en Spotify Developer Dashboard y en `.env`:

```text
http://127.0.0.1:8888/callback
```

---

### Error: `404 Not Found` en `/callback`

Esto puede pasar si Flask está usando el mismo puerto que el callback o si la ruta no está manejada por Spotipy.

Configuración recomendada:

```text
Aplicación Flask: http://127.0.0.1:5000
Callback Spotify: http://127.0.0.1:8888/callback
```

---

### No aparecen previews

No todas las canciones de Spotify tienen `preview_url`. Si una canción no tiene preview disponible, la app puede mostrarla sin reproductor.

---

### No aparecen canciones suficientes

Prueba con términos más generales o en inglés:

```text
reggaeton
latin pop
rock
salsa
lofi
electronic
```

---

## 🔒 Seguridad

No subas archivos sensibles al repositorio.

Agrega un archivo `.gitignore` con al menos:

```gitignore
.env
venv/
__pycache__/
.spotify_cache
historial.json
*.pyc
```

El archivo `.env` contiene credenciales privadas y nunca debe compartirse públicamente.

---

## 💡 Mejoras futuras

- Modo ambiente: estudio, gym, viaje, dormir, fiesta o trabajo.
- Filtro para evitar canciones explícitas.
- Evitar duplicados antes de añadir canciones a una playlist existente.
- Sistema de canciones bloqueadas.
- Perfiles musicales locales.
- Ordenamiento inteligente de canciones según energía o estado de ánimo.
- Portadas automáticas para playlists.
- Integración con Ollama para una versión de IA local.
- Automatización con n8n.
- Control por voz con Whisper local.

---

## 📌 Estado del proyecto

Proyecto funcional en entorno local para crear y actualizar playlists de Spotify usando IA generativa.

---

## 👤 Autor

Desarrollado por **CastriDani**.

Repositorio:

```text
https://github.com/CastriDani/Spotify-IA
```
