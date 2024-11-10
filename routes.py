from flask import render_template, redirect, url_for, request, flash
from app import app, db
from models import Photo
from forms import PhotoForm
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads' #variable por si cambia algun dia la carpeta de carga
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    photos = Photo.query.all()
    return render_template('index.html', photos=photos)

# Ruta para crear una nueva foto
@app.route('/add', methods=['GET', 'POST'])
def add_photo():
    form = PhotoForm()  # Crea una instancia del formulario
    if form.validate_on_submit():
        image_file = request.files['image']  # Obteniene el archivo de la imagen

        if image_file and allowed_file(image_file.filename):
            # Usa secure_filename para obtener un nombre de archivo seguro
            filename = secure_filename(image_file.filename)
            # Guarda la imagen en el directorio de uploads
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Crea una nueva foto a partir de los datos del formulario
            new_photo = Photo(
                title=form.title.data,
                description=form.description.data,
                image='uploads/' + filename  # Guarda solo el nombre del archivo
            )
            db.session.add(new_photo)  # Agrega la foto a la base de datos
            db.session.commit()  # Confirma los cambios
            return redirect(url_for('index'))  # Vuelve a la página inicial
    return render_template('photo_form.html', form=form)

# Ruta para editar una foto existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_photo(id):
    photo = Photo.query.get_or_404(id)  # Toma la foto por el ID
    form = PhotoForm(obj=photo)  # Carga los datos de la foto

    if form.validate_on_submit():
        # Actualiza los campos de la foto
        photo.title = form.title.data
        photo.description = form.description.data

        # Verifica si se cargó una nueva imagen
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                # Usa secure_filename para asegurarse de que el nombre del archivo es seguro
                filename = secure_filename(image_file.filename)
                # Guardar la imagen en la carpeta uploads
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Actualiza la imagen en la base de datos (guardar solo el nombre del archivo)
                photo.image = 'uploads/' + filename  # Guarda la ruta de la imagen

        db.session.commit()  # Confirma los cambios en la base de datos
        return redirect(url_for('index'))  # Vuelve a la pagina inicial

    return render_template('photo_form.html', form=form)  # Vuelve a mostrar el formulario si hay errores

# Ruta para eliminar una foto
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_photo(id):
    photo = Photo.query.get_or_404(id)  # Toma la foto por id
    db.session.delete(photo)  # Elimina la foto
    db.session.commit()  # Confirma los cambios
    return redirect(url_for('index'))  # Vuelve a la página principal