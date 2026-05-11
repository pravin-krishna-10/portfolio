from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table 1: Your profile info
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    department = db.Column(db.String(200))
    university = db.Column(db.String(200))
    bio = db.Column(db.Text)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    office = db.Column(db.String(100))
    google_scholar = db.Column(db.String(300))
    github = db.Column(db.String(300))
    linkedin = db.Column(db.String(300))
    profile_image = db.Column(db.String(300))

# Table 2: Your research papers
class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(500))
    journal = db.Column(db.String(300))
    year = db.Column(db.Integer)
    category = db.Column(db.String(50))  # Journal, Conference, Book Chapter
    doi = db.Column(db.String(300))
    abstract = db.Column(db.Text)
    pdf_filename = db.Column(db.String(300))

# Table 3: Your courses
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(20))
    semester = db.Column(db.String(50))
    year = db.Column(db.Integer)
    level = db.Column(db.String(50))  # Undergraduate, Graduate
    description = db.Column(db.Text)
    is_current = db.Column(db.Boolean, default=False)

# Table 4: Your awards
class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    organization = db.Column(db.String(200))
    year = db.Column(db.Integer)
    description = db.Column(db.Text)