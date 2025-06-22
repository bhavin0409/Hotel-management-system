# Hotel Management System

This is a Django-based Hotel Management System for managing hotel operations such as room bookings, customer profiles, food menus, employee management, and more.

## Features

- Customer registration and login
- Room listing, booking, and management
- Food menu and category management
- Employee and designation management
- Admin dashboard for hotel operations
- Responsive UI with Bootstrap

## Project Structure

```
management/
├── hotelpro/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── management/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── static/
│   ├── css/
│   ├── images/
│   └── ...
├── db.sqlite3
├── manage.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd management
   ```

2. **Install dependencies:**
   ```sh
   pip install -r hotelpro/requirements.txt
   ```

3. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

4. **Create a superuser (admin):**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

6. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Static Files

- Static files (CSS, JS, images) are located in the `static/` directory.
- Media uploads are stored in the `media/` directory.

## License

This project is for educational purposes.

---

**Developed with