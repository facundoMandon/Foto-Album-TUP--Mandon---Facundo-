from app import db

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=False)  # Ruta o URL de la imagen

    def __repr__(self):
        return f"Photo('{self.title}', '{self.description}')"
