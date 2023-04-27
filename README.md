The RMS (Recruitment Management System) is a web-based application built with Django that allows companies to manage their recruitment process efficiently. The system has several features that enable companies to streamline their recruitment process and hire the best candidates for their job openings.

## Features

### Authentication

The system has an authentication system that allows users to register and login to the system. Once a user logs in, they can access the system's features based on their user role.

### User Roles

There are three user roles in the system: 

1. Administrator: An administrator can manage the system's settings, manage job openings, view applicant details, and manage users.

2. Hiring Manager: A hiring manager can create job openings, view applicant details, and manage users assigned to the job openings they created.

3. Applicant: An applicant can apply for job openings and view their application status.

### Job Openings

The system allows administrators and hiring managers to create job openings with all the necessary details such as job title, description, salary, and required skills. Once a job opening is created, it becomes visible to applicants who can apply for the job.

### Applicant Management

The system allows administrators and hiring managers to view applicant details such as their resume, application status, and other relevant information. They can also change the status of an applicant's application, schedule interviews, and send emails to applicants.

### User Management

The system allows administrators to manage users, including creating new users, editing user details, and assigning user roles. Hiring managers can only manage users assigned to the job openings they created.

## Installation

To run the RMS application on your local machine, follow these steps:

1. Clone the repository to your local machine using Git or download the zip file and extract it to a folder.

2. Navigate to the folder containing the `requirements.txt` file and run the following command to install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and set the necessary environment variables. You should set the `SECRET_KEY` and database details such as `DATABASE_URL` and `DATABASE_NAME`.

4. Run the following command to migrate the database:

    ```
    python manage.py migrate
    ```

5. Create a superuser account by running the following command:

    ```
    python manage.py createsuperuser
    ```

6. Run the application by running the following command:

    ```
    python manage.py runserver
    ```

7. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Usage

### Login

To access the system, you need to log in using your credentials. If you don't have an account, you can register as a new user.

### Dashboard

Once you log in, you'll be redirected to the dashboard, where you can see an overview of the system's features based on your user role. The dashboard shows job openings, applicants, and users, depending on your user role.

### Job Openings

To create a new job opening, click on the "Create Job Opening" button on the dashboard. Fill in the necessary details such as job title, description, salary, and required skills.

### Applicants

To
 
