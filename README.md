How to Run the Project
Follow these steps to set up and run the Django project locally:

1. Clone the Repository
bash
Copy
Edit
git clone <your-github-repo-url>
cd OnlineGroceryStore
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Environment Variables (if needed)
Create a .env file and add necessary configurations (e.g., database credentials, API keys).

5. Apply Migrations
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
6. Create a Superuser (For Admin Access)
bash
Copy
Edit
python manage.py createsuperuser
Follow the prompts to set up a username and password.

7. Run the Development Server
bash
Copy
Edit
python manage.py runserver
The project will be available at:
http://127.0.0.1:8000/

8. Test API Endpoints
Use Postman or curl to test authentication, product management, and other endpoints.

