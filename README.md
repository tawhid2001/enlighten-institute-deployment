# Enlighten School - Backend

The **Enlighten School** backend is built with Django and Django REST Framework (DRF), providing a robust API for managing course enrollment, lesson progress, and user roles (students and teachers). This backend serves as the core of the Enlighten School e-learning platform.

## Features

- **User Authentication**: Separate registration and login for students and teachers.
- **Course Management**: Teachers can create, update, and manage course and lesson content.
- **Lesson Tracking**: Students can view lesson progress and track course completion.
- **Enrollment**: Students can enroll in courses and view their enrolled courses.
- **Progress Tracking**: Comprehensive progress tracking for both students and teachers.

## Technologies

- **Backend Framework**: Django, Django REST Framework (DRF)
- **Database**: superbase (PostgreSQL)
- **Authentication**: DRF Token Authentication
- **Deployment**: Vercel (for live API)

## Live Demo

The live backend API can be accessed here: [Enlighten School Live API](https://enlighten-institute-deployment.vercel.app/)

## Important URLs and Endpoints

### Authentication

- **Login**: `POST /api/auth/login/`  
- **Registration**: `POST /api/auth/registration/`  
- **Account Confirmation**: `GET /api/auth/registration/account_confirm_email/<str:key>/`

### Course Endpoints

- **Course List**: `GET /api/course/courselist/`
- **Course Detail**: `GET /api/course/courselist/<int:pk>/`
- **Enroll in Course**: `POST /api/enrollment/enroll/`

### Lesson Endpoints

- **Lesson List for a Course**: `GET /api/course/<int:course_id>/lessons/`
- **Lesson Detail**: `GET /api/course/lesson/<int:pk>/`
- **Lesson Progress**: `GET /api/lessonprogress/`

### Student Progress Endpoints

- **Course Progress**: `GET /api/course_progress/<int:course_id>/`
- **My Enrollments**: `GET /api/my-enrollments/`
- **Enrolled Students in Course**: `GET /api/students/<int:course_id>/`

## Local Setup

To set up the Enlighten School backend locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tawhid2001/enlighten-institute-deployment.git
   cd enlighten-institute-deployment
