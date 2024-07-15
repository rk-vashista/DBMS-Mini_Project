# Job Portal Application

This Job Portal Application is a web-based platform designed to facilitate the process of job searching and application for both job seekers and employers. Built with Flask, a Python web framework, it offers a simple yet effective interface for managing job postings, applying for jobs, and administering job applications.

## Features

- **Job Listings**: Browse available job listings with detailed descriptions, requirements, and application procedures.
- **Job Application**: Apply for jobs directly through the portal with an easy-to-use form.
- **Admin Dashboard**: For employers and administrators, manage job postings, view applications, and edit or delete job listings.
- **Responsive Design**: Accessible on various devices, ensuring a seamless experience for all users.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/job-portal.git
   ```
2. Navigate to the project directory:
   ```sh
   cd job-portal
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     .\dbproj\Scripts\activate
     ```
   - On Unix or MacOS:
     ```sh
     source dbproj/Scripts/activate
     ```
5. Set up the environment variables by creating a `.env` file based on the `.env.example` provided.

6. Run the Flask application:
   ```sh
   python app.py
   ```

## Usage

- Visit `http://localhost:5000` to view the job listings.
- To apply for a job, click on the job listing and fill out the application form.
- Access the admin dashboard at `http://localhost:5000/admin` with the credentials provided in your `.env` file.

## Contributing

Contributions to the Job Portal Application are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
