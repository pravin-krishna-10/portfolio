from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Profile, Publication, Course, Award
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ---- PUBLIC ROUTES (what visitors see) ----

# Home page
@app.route('/')
def index():
    profile = Profile.query.first()
    recent_papers = Publication.query.order_by(Publication.year.desc()).limit(3).all()
    total_publications = Publication.query.count()
    total_courses = Course.query.count()
    total_awards = Award.query.count()
    return render_template('index.html',
                           profile=profile,
                           recent_papers=recent_papers,
                           total_publications=total_publications,
                           total_courses=total_courses,
                           total_awards=total_awards)

# Publications page
@app.route('/publications')
def publications():
    category = request.args.get('category', 'all')
    if category != 'all':
        papers = Publication.query.filter_by(category=category).order_by(Publication.year.desc()).all()
    else:
        papers = Publication.query.order_by(Publication.year.desc()).all()
    return render_template('publications.html', papers=papers, category=category)

# Teaching page
@app.route('/teaching')
def teaching():
    profile = Profile.query.first()
    current_courses = Course.query.filter_by(is_current=True).all()
    past_courses = Course.query.filter_by(is_current=False).order_by(Course.year.desc()).all()
    return render_template('teaching.html',
                           profile=profile,
                           current_courses=current_courses,
                           past_courses=past_courses)

# About page
@app.route('/about')
def about():
    profile = Profile.query.first()
    awards = Award.query.order_by(Award.year.desc()).all()
    return render_template('about.html', profile=profile, awards=awards)

# Contact page
@app.route('/contact')
def contact():
    profile = Profile.query.first()
    return render_template('contact.html', profile=profile)


# ---- ADMIN ROUTES (for you to manage content) ----

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    publications = Publication.query.order_by(Publication.year.desc()).all()
    courses = Course.query.all()
    awards = Award.query.all()
    profile = Profile.query.first()
    return render_template('admin/dashboard.html',
                           publications=publications,
                           courses=courses,
                           awards=awards,
                           profile=profile)

# Add a new publication
@app.route('/admin/add-publication', methods=['GET', 'POST'])
def add_publication():
    if request.method == 'POST':
        paper = Publication(
            title=request.form['title'],
            authors=request.form['authors'],
            journal=request.form['journal'],
            year=int(request.form['year']),
            category=request.form['category'],
            doi=request.form.get('doi', ''),
            abstract=request.form.get('abstract', '')
        )

        # Handle PDF upload
        if 'pdf' in request.files:
            pdf = request.files['pdf']
            if pdf.filename != '':
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
                pdf.save(pdf_path)
                paper.pdf_filename = pdf.filename

        db.session.add(paper)
        db.session.commit()
        flash('Publication added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_publication.html')

# Edit a publication
@app.route('/admin/edit-publication/<int:id>', methods=['GET', 'POST'])
def edit_publication(id):
    paper = Publication.query.get_or_404(id)
    if request.method == 'POST':
        paper.title = request.form['title']
        paper.authors = request.form['authors']
        paper.journal = request.form['journal']
        paper.year = int(request.form['year'])
        paper.category = request.form['category']
        paper.doi = request.form.get('doi', '')
        paper.abstract = request.form.get('abstract', '')

        if 'pdf' in request.files:
            pdf = request.files['pdf']
            if pdf.filename != '':
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
                pdf.save(pdf_path)
                paper.pdf_filename = pdf.filename

        db.session.commit()
        flash('Publication updated!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/edit_publication.html', paper=paper)

# Delete a publication
@app.route('/admin/delete-publication/<int:id>')
def delete_publication(id):
    paper = Publication.query.get_or_404(id)
    db.session.delete(paper)
    db.session.commit()
    flash('Publication deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# Add a new course
@app.route('/admin/add-course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course = Course(
            course_name=request.form['course_name'],
            course_code=request.form['course_code'],
            semester=request.form['semester'],
            year=int(request.form['year']),
            level=request.form['level'],
            description=request.form.get('description', ''),
            is_current='is_current' in request.form
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_course.html')

# Delete a course
@app.route('/admin/delete-course/<int:id>')
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# Add a new award
@app.route('/admin/add-award', methods=['GET', 'POST'])
def add_award():
    if request.method == 'POST':
        award = Award(
            title=request.form['title'],
            organization=request.form['organization'],
            year=int(request.form['year']),
            description=request.form.get('description', '')
        )
        db.session.add(award)
        db.session.commit()
        flash('Award added!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_award.html')

# Delete an award
@app.route('/admin/delete-award/<int:id>')
def delete_award(id):
    award = Award.query.get_or_404(id)
    db.session.delete(award)
    db.session.commit()
    flash('Award deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# Update profile
@app.route('/admin/update-profile', methods=['GET', 'POST'])
def update_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile(name='')
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        profile.name = request.form['name']
        profile.designation = request.form['designation']
        profile.department = request.form['department']
        profile.university = request.form['university']
        profile.bio = request.form['bio']
        profile.email = request.form['email']
        profile.phone = request.form.get('phone', '')
        profile.office = request.form.get('office', '')
        profile.google_scholar = request.form.get('google_scholar', '')
        profile.github = request.form.get('github', '')
        profile.linkedin = request.form.get('linkedin', '')
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/update_profile.html', profile=profile)


if __name__ == '__main__':
    app.run(debug=True)