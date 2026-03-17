from flask import Flask, jsonify
from config import Config
from extensions import db

from routes.user_routes import user_bp
from routes.course_routes import course_bp
from routes.enrollment_routes import enrollment_bp
from routes.rating_routes import rating_bp
from routes.recommendation_routes import recommendation_bp
from routes.audit_log_routes import audit_log_bp
from routes.data_quality_routes import data_quality_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)
app.register_blueprint(rating_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(audit_log_bp)
app.register_blueprint(data_quality_bp)

@app.route('/')
def home():
    return jsonify({"message": "API is running!"})

if __name__ == '__main__':
    app.run(debug=True)