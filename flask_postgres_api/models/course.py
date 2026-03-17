from extensions import db
from sqlalchemy import CheckConstraint

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False) 

    __table_args__ = (
        CheckConstraint('length(description) >= 10', name='check_description_min_length'),
        CheckConstraint('length(title) >= 3', name='check_title_min_length'),
    )

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description
        }