from flask import Flask, render_template, request, session, redirect, url_for
from spotify_utils import (
    traducir_a_consulta, modo_sorprendeme, buscar_canciones,
    crear_playlist, obtener_playlists_usuario, agregar_a_playlist,
    obtener_historial
)

app = Flask(__name__)
app.secret_key = "una_clave_secreta_para_sesiones"


@app.route("/", methods=["GET", "POST"])
def index():
    """Página principal con búsqueda y botón de sorpréndeme."""
    if request.method == "POST":
        # Detectar si es modo "Sorpréndeme"
        if "sorprendeme" in request.form:
            consulta = modo_sorprendeme()
            entrada = f"✨ {consulta}"
        else:
            entrada = request.form.get("entrada", "").strip()
            if not entrada:
                return render_template("index.html", error="Escribe algo para buscar.")
            consulta = traducir_a_consulta(entrada)

        # Guardamos SOLO la consulta (texto corto), no las canciones
        session['consulta'] = consulta
        session['entrada'] = entrada
        return redirect(url_for('preview'))

    return render_template("index.html", error=None)


@app.route("/preview", methods=["GET", "POST"])
def preview():
    """Página de previsualización: busca las canciones AQUÍ, no en la sesión."""
    consulta = session.get('consulta', '')
    entrada = session.get('entrada', '')

    if not consulta:
        return redirect(url_for('index'))

    # Volvemos a buscar las canciones (rápido, y evita meterlas en la cookie)
    canciones = buscar_canciones(consulta, limite_total=50)

    if request.method == "POST":
        uris_seleccionadas = request.form.getlist("seleccionadas")
        accion = request.form.get("accion")

        if not uris_seleccionadas:
            return render_template("preview.html",
                                   canciones=canciones,
                                   entrada=entrada,
                                   playlists=obtener_playlists_usuario(),
                                   mensaje="⚠️ No seleccionaste ninguna canción.")

        if accion == "nueva":
            nombre = request.form.get("nombre_playlist", f"IA: {entrada}")
            url = crear_playlist(nombre, uris_seleccionadas)
            return render_template("preview.html",
                                   canciones=canciones,
                                   entrada=entrada,
                                   playlists=[],
                                   mensaje=f"✅ ¡Playlist creada! <a href='{url}' target='_blank'>Abrir en Spotify</a>")

        elif accion == "existente":
            playlist_id = request.form.get("playlist_existente")
            if playlist_id:
                agregar_a_playlist(playlist_id, uris_seleccionadas)
                return render_template("preview.html",
                                       canciones=canciones,
                                       entrada=entrada,
                                       playlists=[],
                                       mensaje="✅ ¡Canciones añadidas a la playlist!")

    return render_template("preview.html",
                           canciones=canciones,
                           entrada=entrada,
                           playlists=obtener_playlists_usuario(),
                           mensaje=None)


@app.route("/historial")
def historial():
    """Página que muestra el historial de playlists creadas."""
    registros = obtener_historial()
    return render_template("historial.html", registros=registros)


if __name__ == "__main__":
    app.run(debug=True, port=5000)