# Namakkal City Public Grievance Redressal (PGR) System

A Django-based Public Grievance Redressal application designed for Namakkal City to facilitate public complaint registration, status tracking, OTP verification, and administrative dashboard management.

## Features

- **Public Features:**
  - Citizen complaint registration.
  - OTP verification flow for secure registration.
  - Quick complaint status checking via tracking/complaint number.
  - Responsive home page and public contact page.
- **Admin & Agent Dashboard:**
  - Complete complaints list view with detailed statistics.
  - Ward/Area management and dynamic filtering.
  - Conversation log tracking.
  - Notification template manager and status tracking.
  - Campaign creation and monitoring.
  - Agent and department administration.
  - Local news/updates publishing panel.
  - Export complaints data directly to Excel.

## Getting Started

### Prerequisites

- Python 3.10+
- Pip (Python Package Manager)

### Installation & Setup

1. **Clone/Navigate to the Repository:**
   ```bash
   cd namakkal-city
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   Ensure you have Django and other necessary packages installed.
   ```bash
   pip install django openpyxl
   ```

4. **Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Seed the database:**
   To set up default zones, wards, areas, status types, and the default admin user:
   ```bash
   python seed_pgr.py
   ```
   *Default Admin credentials created:*
   - **Username:** `admin`
   - **Password:** `admin123`

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.
