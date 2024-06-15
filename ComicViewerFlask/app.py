from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from pathlib import Path
from main import ComicLibrary
from segment_panels import segment_panels

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['COMICS_FOLDER'] = Path('static/uploads/')  # Set the path to your comics directory

library = ComicLibrary(app.config['COMICS_FOLDER'])

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    comics_by_series = library.get_comics_by_series()
    return render_template('index.html', comics_by_series=comics_by_series)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'pass':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/comic/<int:comic_id>')
def view_comic(comic_id):
    comic = library.get_comic_by_id(comic_id)
    if not comic:
        abort(404)
    pages = library.get_pages_by_series(comic['series'])
    next_comic = library.get_next_comic(comic_id)
    prev_comic = library.get_previous_comic(comic_id)
    next_comic_id = next_comic['id'] if next_comic else None
    prev_comic_id = prev_comic['id'] if prev_comic else None

    segment = request.args.get('segment', 'false').lower() == 'true'
    panel_images = []

    if segment:
        image_path = Path(app.root_path) / 'static' / comic['path']
        panel_images = segment_panels(image_path)

    return render_template(
        'comic.html', 
        series=comic['series'], 
        pages=pages, 
        current_comic_id=comic_id, 
        next_comic_id=next_comic_id, 
        prev_comic_id=prev_comic_id, 
        panel_images=panel_images,
        segment=segment
    )

@app.route('/next_comic/<int:comic_id>')
def next_comic(comic_id):
    next_comic = library.get_next_comic(comic_id)
    if next_comic:
        return redirect(url_for('view_comic', comic_id=next_comic['id'], segment=request.args.get('segment', 'false')))
    return redirect(url_for('index'))

@app.route('/previous_comic/<int:comic_id>')
def previous_comic(comic_id):
    prev_comic = library.get_previous_comic(comic_id)
    if prev_comic:
        return redirect(url_for('view_comic', comic_id=prev_comic['id'], segment=request.args.get('segment', 'false')))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
