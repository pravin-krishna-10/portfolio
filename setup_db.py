from app import app
from models import db, Profile, Publication, Course, Award

with app.app_context():
    # Create all tables (safe to run again - won't delete existing data)
    db.create_all()

    # ===== YOUR PROFILE =====
    # Check if profile already exists
    if not Profile.query.first():
        profile = Profile(
            name='Pravin',
            designation='Assistant Professor',
            department='Your Department',
            university='Your University',
            bio='I am an Assistant Professor specializing in... Write your full bio here. Talk about your research interests, your journey, and what drives your academic work.',
            email='pravin@university.edu',
            phone='+91 XXXXX XXXXX',
            office='Room XXX, Department Building',
            google_scholar='https://scholar.google.com/citations?user=YOUR_ID',
            github='https://github.com/your-username',
            linkedin='https://linkedin.com/in/your-profile'
        )
        db.session.add(profile)
        print("Profile added!")

    # ===== YOUR PUBLICATIONS =====
    if Publication.query.count() == 0:
        papers = [
            Publication(
                title='Your First Paper Title Here',
                authors='Pravin, A. Co-Author, B. Co-Author',
                journal='Journal Name, Vol. XX, No. X, pp. 1-15',
                year=2025,
                category='Journal',
                doi='https://doi.org/10.xxxx/xxxxx',
                abstract='Write a brief abstract of your paper here.'
            ),
            Publication(
                title='Your Second Paper Title Here',
                authors='Pravin, C. Co-Author',
                journal='Conference Name 2024, pp. 100-110',
                year=2024,
                category='Conference',
                doi='https://doi.org/10.xxxx/xxxxx',
                abstract='Write a brief abstract of your paper here.'
            ),
            Publication(
                title='Your Third Paper Title Here',
                authors='Pravin, D. Co-Author, E. Co-Author',
                journal='Another Journal Name, Vol. XX',
                year=2024,
                category='Journal',
                doi='',
                abstract='Write a brief abstract of your paper here.'
            ),
            Publication(
                title='Your Fourth Paper Title Here',
                authors='Pravin, F. Co-Author',
                journal='Book Title, Publisher Name, Chapter 5',
                year=2023,
                category='Book Chapter',
                doi='',
                abstract=''
            ),
        ]
        db.session.add_all(papers)
        print(f"{len(papers)} publications added!")

    # ===== YOUR COURSES =====
    if Course.query.count() == 0:
        courses = [
            Course(
                course_name='Your Current Course Name',
                course_code='CS 501',
                semester='Spring',
                year=2026,
                level='Graduate',
                description='Brief description of what this course covers.',
                is_current=True
            ),
            Course(
                course_name='Another Current Course',
                course_code='CS 201',
                semester='Spring',
                year=2026,
                level='Undergraduate',
                description='Brief description of what this course covers.',
                is_current=True
            ),
            Course(
                course_name='A Past Course',
                course_code='CS 301',
                semester='Fall',
                year=2025,
                level='Undergraduate',
                description='Brief description of this course.',
                is_current=False
            ),
        ]
        db.session.add_all(courses)
        print(f"{len(courses)} courses added!")

    # ===== YOUR AWARDS =====
    if Award.query.count() == 0:
        awards = [
            Award(
                title='Your Award Title',
                organization='Awarding Organization',
                year=2024,
                description='Brief description of the award.'
            ),
            Award(
                title='Another Achievement',
                organization='Another Organization',
                year=2023,
                description=''
            ),
        ]
        db.session.add_all(awards)
        print(f"{len(awards)} awards added!")

    # Save everything to database
    db.session.commit()
    print("\nDatabase initialized successfully!")
    print("You can now update all this data through the admin panel at /admin")