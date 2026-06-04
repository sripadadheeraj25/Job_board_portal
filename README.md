# Job Board Portal

A full-stack job board web application built with Python and Django that connects employers and job seekers.

## Live Demo

https://job-board-portal-zpjn.onrender.com

## Features

- Role-based registration — Employer and Job Seeker
- Employers can post, edit, and delete job listings
- Job seekers can search and filter jobs by keyword, location, and type
- Apply to jobs with resume upload (PDF)
- View resume directly from the applicants list
- Employer dashboard with applicant counts per job
- Update application status — Shortlisted, Hired, Rejected
- Seeker dashboard to track all applications and status
- Save and bookmark jobs for later
- Withdraw application if status is still Applied
- Email notification to employer on new application
- Pagination on job listings
- Responsive UI with Bootstrap 5
- Django Admin panel for site management

## Tech Stack

- **Backend:** Python, Django 6.0
- **Database:** PostgreSQL (Supabase)
- **File Storage:** Cloudinary
- **Frontend:** Django Templates, Bootstrap 5
- **Deployment:** Render

## Setup Instructions

1. Clone the repository
```
git clone https://github.com/sripadadheeraj25/Job_board_portal.git
cd Job_board_portal
```

2. Create and activate virtual environment
```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create a `.env` file in the root folder
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```
python manage.py createsuperuser
```

7. Start the server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.
