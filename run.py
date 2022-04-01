from flask import Flask, render_template, send_file, g, request, jsonify, session, escape, redirect
from passlib.hash import pbkdf2_sha256
import os
from db import Database
import mimetypes

mimetypes.add_type('application/javascript', '.mjs')
app = Flask(__name__, static_folder='public', static_url_path='')
app.secret_key = b'lkj98t&%$3rhfSwu3D'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/mypalettes')
def api_mypalettes():
    if 'user' in session:
        user_id = session['user']['user_id']
        response = get_db().get_user_palettes(user_id)
        return jsonify(response)
    else:
        return jsonify('Error: User not authenticated')

@app.route('/api/myuser')
def api_myuser():
    if 'user' in session:
        user_id = session['user']['user_id']
        response = get_db().get_user(user_id)
        return jsonify(response)
    else:
        return jsonify('Error: User not authenticated')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', 'course', path))


@app.route('/create_palette', methods=['GET', 'POST'])
def create_palette():
    if request.method == 'POST':
        if 'user' in session:
            uid = session['user']['user_id'];
        name = request.form['name']
        image = request.form['image']
        c1 = request.form['h1']
        c2 = request.form['h2']
        c3 = request.form['h3']
        c4 = request.form['h4']
        c5 = request.form['h5']
        c6 = request.form['h6']

        if uid and name and c1 and c2 and c3 and c4 and c5 and c6 and image:
            get_db().create_palette(uid, name, c1, c2, c3, c4, c5, c6, image)

    return render_template('profile.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        typed_password = request.form['password']
        photo = request.form['profile-photo']
        print(photo)
        if name and username and typed_password and photo:
            encrypted_password = pbkdf2_sha256.encrypt(typed_password, rounds=200000, salt_size=16)
            get_db().create_user(name, username, encrypted_password, photo)
            return redirect('/login')
    return render_template('create_user.html')

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'POST':
        user_id = session['user']['user_id']
        name = request.form['name']
        photo = request.form['profile-photo']
        if name:
            get_db().update_user_name(name, user_id)
        if photo:
            get_db().update_user_photo(photo, user_id)
        if name or photo:
            return redirect('/profile')
    return render_template('edit_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        typed_password = request.form['password']
        if username and typed_password:
            user = get_db().get_user_username(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['encrypted_password']):
                    session['user'] = user
                    user_data = get_db().get_user_username(username);
                    return render_template('profile.html', user_data=user_data)
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif username and not typed_password:
            message = "Missing password, please try again"
        elif not username and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/<name>')
def generic(name):
    if 'user' in session:
        return render_template(name + '.html')
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
