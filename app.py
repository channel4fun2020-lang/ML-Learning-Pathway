import os
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ml_pathway.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(db.Model):
    """User model for authentication and profile management"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('ExerciseSubmission', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Module(db.Model):
    """Learning module model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    module_number = db.Column(db.Integer, nullable=False, unique=True)
    duration_weeks = db.Column(db.Integer)
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    
    # Relationships
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.module_number}: {self.title}>'


class Lesson(db.Model):
    """Individual lesson within a module"""
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    lesson_order = db.Column(db.Integer)
    video_url = db.Column(db.String(500))
    
    # Relationships
    exercises = db.relationship('Exercise', backref='lesson', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'


class Exercise(db.Model):
    """Coding exercises for hands-on learning"""
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    starter_code = db.Column(db.Text)
    expected_output = db.Column(db.Text)
    difficulty = db.Column(db.String(20))  # Easy, Medium, Hard
    points = db.Column(db.Integer, default=10)
    
    # Relationships
    submissions = db.relationship('ExerciseSubmission', backref='exercise', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Exercise {self.title}>'


class ExerciseSubmission(db.Model):
    """User submissions for exercises"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Submission User {self.user_id} Exercise {self.exercise_id}>'


class UserProgress(db.Model):
    """Track user progress through modules"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    progress_percentage = db.Column(db.Float, default=0)
    completed_lessons = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    module = db.relationship('Module', backref='user_progress')
    
    def __repr__(self):
        return f'<Progress User {self.user_id} Module {self.module_id}>'


class Quiz(db.Model):
    """Assessment quizzes for each module"""
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    passing_score = db.Column(db.Integer, default=70)
    
    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'


class QuizQuestion(db.Model):
    """Quiz questions"""
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20))  # multiple_choice, short_answer
    options = db.Column(db.Text)  # JSON for multiple choice
    correct_answer = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<Question {self.id}>'


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    modules = Module.query.order_by(Module.module_number).all()
    return render_template('index.html', modules=modules)


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing progress"""
    user_progress = UserProgress.query.filter_by(user_id=current_user.id).all()
    stats = {
        'modules_started': len(user_progress),
        'modules_completed': sum(1 for p in user_progress if p.completed_at),
        'total_points': 0  # Calculate from submissions
    }
    return render_template('dashboard.html', progress=user_progress, stats=stats)


@app.route('/module/<int:module_id>')
def module_detail(module_id):
    """Display module details and lessons"""
    module = Module.query.get_or_404(module_id)
    lessons = Lesson.query.filter_by(module_id=module_id).order_by(Lesson.lesson_order).all()
    return render_template('module.html', module=module, lessons=lessons)


@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    """Display lesson content"""
    lesson = Lesson.query.get_or_404(lesson_id)
    exercises = Exercise.query.filter_by(lesson_id=lesson_id).all()
    return render_template('lesson.html', lesson=lesson, exercises=exercises)


@app.route('/exercise/<int:exercise_id>')
@login_required
def exercise_detail(exercise_id):
    """Display exercise with code editor"""
    exercise = Exercise.query.get_or_404(exercise_id)
    previous_submission = ExerciseSubmission.query.filter_by(
        user_id=current_user.id,
        exercise_id=exercise_id
    ).first()
    return render_template('exercise.html', exercise=exercise, submission=previous_submission)


@app.route('/api/exercise/<int:exercise_id>/submit', methods=['POST'])
@login_required
def submit_exercise(exercise_id):
    """API endpoint to submit exercise solution"""
    exercise = Exercise.query.get_or_404(exercise_id)
    data = request.get_json()
    code = data.get('code')
    
    # TODO: Add code execution and validation
    is_correct = False
    feedback = "Submission received. Code evaluation pending."
    
    submission = ExerciseSubmission(
        user_id=current_user.id,
        exercise_id=exercise_id,
        code=code,
        is_correct=is_correct,
        feedback=feedback
    )
    
    db.session.add(submission)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'feedback': feedback,
        'points_awarded': exercise.points if is_correct else 0
    })


@app.route('/quiz/<int:quiz_id>')
@login_required
def quiz_detail(quiz_id):
    """Display quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz=quiz)


@app.route('/resources')
def resources():
    """Learning resources page"""
    resources = {
        'books': [
            {'title': 'Hands-On Machine Learning', 'author': 'Aurélien Géron'},
            {'title': 'Deep Learning', 'author': 'Goodfellow, Bengio, Courville'},
            {'title': 'Pattern Recognition and Machine Learning', 'author': 'Christopher M. Bishop'},
        ],
        'websites': [
            {'name': 'Kaggle', 'url': 'https://www.kaggle.com'},
            {'name': 'Papers with Code', 'url': 'https://paperswithcode.com'},
            {'name': 'ArXiv', 'url': 'https://arxiv.org'},
        ],
        'tools': [
            {'name': 'TensorFlow', 'url': 'https://www.tensorflow.org'},
            {'name': 'PyTorch', 'url': 'https://pytorch.org'},
            {'name': 'Scikit-learn', 'url': 'https://scikit-learn.org'},
        ]
    }
    return render_template('resources.html', resources=resources)


@app.route('/community')
def community():
    """Community and support page"""
    return render_template('community.html')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
