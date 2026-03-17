from extensions import db

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    confidence_score = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "confidence_score": self.confidence_score
        }