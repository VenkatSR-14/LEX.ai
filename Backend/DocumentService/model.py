from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    file_blob = db.Column(db.LargeBinary, nullable=True)
    file_contents_generated = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Document {self.filename} (User: {self.user_id})>'
