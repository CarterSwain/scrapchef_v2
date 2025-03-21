ScrapChef 🧑‍🍳✨

(Testing Auto Deployment)

An AI-powered recipe generator that helps users create unique dishes based on available ingredients.

DEPLOYED @ https://scrapchefapp.com 

Features:

- AI Recipe Generation: Users enter ingredients, and the OpenAI API generates unique recipes.
- Save & Explore Recipes: Logged-in users can save recipes to their profile and explore recipes saved by others.
- User Preferences: Customize dietary preferences and exclude certain ingredients.
- Authentication: Sign up and log in via Django Admin or Google Auth (Django Allauth).
- Tailwind CSS Styling: Clean and modern UI with responsive design.


Tech Stack:

- Backend: Django (Monolith Architecture)
- Frontend: Django Templates + Tailwind CSS
- Database: PostgreSQL (local & production)
- AI Integration: OpenAI API
- Auth: Django Allauth (Google & Admin)
- Hosting: Google Cloud


Installation & Setup:

1. Clone the Repository:

git clone https://github.com/yourusername/ScrapChef.git
cd ScrapChef

2. Create & Activate Virtual Environment:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

3. Install Dependencies:

pip install -r requirements.txt

4. Set Up Environment Variables:

OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_django_secret
DATABASE_URL=your_postgres_db_url
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
ALLOWED_HOSTS=localhost,127.0.0.1

5. Apply Migrations & Run Server:

python manage.py migrate
python manage.py runserver


Usage:

- Log in or sign up using Google Auth.
- Enter ingredients and generate a unique recipe.
- Save recipes to your profile and explore community favorites.


Contributing:

- Fork the repo
- Create a feature branch: git checkout -b feature-name
- Commit changes: git commit -m "Add new feature"
- Push and open a pull request


License:

- MIT License