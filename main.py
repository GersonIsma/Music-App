import os
import re
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración: usa variable de entorno para la conexión
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de canción
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    embed_url = db.Column(db.String(200), nullable=False)

from flask import Flask, render_template, request, redirect, url_for
# (ya tienes otros imports, no es necesario repetirlos)

# ... Tu clase Song y configuraciones ya están arriba

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']
        video_url = request.form['youtube_url']

        # Procesar enlace YouTube
        video_id = extract_youtube_id(video_url)
        embed_url = f"https://www.youtube.com/embed/{video_id}" if video_id else ""

        new_song = Song(title=title, artist=artist, album=album, genre=genre, embed_url=embed_url)
        db.session.add(new_song)
        db.session.commit()
        return redirect('/')
    return render_template('add_song.html')


@app.route('/edit/<int:song_id>', methods=['GET', 'POST'])
def edit(song_id):
    song = Song.query.get_or_404(song_id)
    if request.method == 'POST':
        song.title = request.form['title']
        song.artist = request.form['artist']
        song.album = request.form['album']
        song.genre = request.form['genre']
        video_url = request.form['youtube_url']
        song.embed_url = f"https://www.youtube.com/embed/{extract_youtube_id(video_url)}"
        db.session.commit()
        return redirect('/')
    return render_template('edit_song.html', song=song)


@app.route('/delete/<int:song_id>', methods=['POST'])
def delete(song_id):
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/')

def extract_youtube_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else ""

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto de Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port)
