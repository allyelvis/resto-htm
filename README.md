Creating a complete automation script for setting up a Django backend with a MySQL database requires multiple steps, including installing dependencies, configuring Django, and setting up the database. Below is a Bash script that outlines the steps necessary to create a simple Django application with a MySQL database.

**Ensure that you have the following prerequisites:**

- A Unix-like system (Linux or macOS).
- Bash shell installed.
- Python 3.x and `pip` installed.
- MySQL server installed and running on your machine.
- MySQL client installed if you need to run MySQL commands for verification (optional).

Here’s the complete automation Bash script:

```bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
DB_NAME="restaurant_db"
DB_USER="root"
DB_PASSWORD="password"
PROJECT_NAME="restaurant_management"
DJANGO_VERSION="3.2"
MYSQL_CLIENT="mysql-connector-python"

# Function to install required packages
install_packages() {
    echo "Updating package list..."
    sudo apt update
    echo "Installing required packages..."
    sudo apt install -y python3-pip python3-dev default-libmysqlclient-dev build-essential
}

# Function to set up MySQL database
setup_database() {
    echo "Setting up MySQL database..."
    mysql -u $DB_USER -p$DB_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
    mysql -u $DB_USER -p$DB_PASSWORD -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
    mysql -u $DB_USER -p$DB_PASSWORD -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '${DB_USER}'@'localhost';"
    mysql -u $DB_USER -p$DB_PASSWORD -e "FLUSH PRIVILEGES;"
    echo "MySQL database setup completed."
}

# Function to create Django project
create_django_project() {
    echo "Creating Django project..."
    pip3 install django==${DJANGO_VERSION} ${MYSQL_CLIENT}
    django-admin startproject $PROJECT_NAME
    cd $PROJECT_NAME

    # Update Django settings for MySQL
    echo "Configuring Django settings..."
    sed -i "s/ENGINE': 'django.db.backends.sqlite3'/ENGINE': 'django.db.backends.mysql'/" $PROJECT_NAME/settings.py
    sed -i "s/NAME': BASE_DIR / 'db.sqlite3'/NAME': '$DB_NAME',/" $PROJECT_NAME/settings.py
    sed -i "s/# 'USER': 'your_username',/'USER': '$DB_USER',/" $PROJECT_NAME/settings.py
    sed -i "s/# 'PASSWORD': 'your_password',/'PASSWORD': '$DB_PASSWORD',/" $PROJECT_NAME/settings.py
    sed -i "s/# 'HOST': 'localhost',/'HOST': 'localhost',/" $PROJECT_NAME/settings.py
    sed -i "s/# 'PORT': '',/'PORT': '',/" $PROJECT_NAME/settings.py

    echo "Django project setup completed."
}

# Function to apply migrations and create superuser
setup_django() {
    echo "Applying migrations..."
    python3 manage.py migrate
    echo "Creating superuser..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DB_USER', 'admin@example.com', '$DB_PASSWORD')" | python3 manage.py shell
    echo "Django setup completed."
}

# Function to run the server
run_server() {
    echo "Starting Django development server..."
    # Use `nohup` to run the server in the background if you wish
    python3 manage.py runserver 0.0.0.0:8000 &
    echo "Django development server is running at http://localhost:8000"
}

# Run all functions
install_packages
setup_database
create_django_project
setup_django
run_server

echo "Restaurant Management System setup complete."
```

### Instructions to Use the Script

1. **Create a Bash Script File**:
   - Open a terminal and create a new script file.
   ```bash
   nano setup_restaurant_management.sh
   ```
   - Copy and paste the script above into the file and save it (Ctrl + X, then Y, then Enter).

2. **Make the Script Executable**:
   - Run the following command to make the script executable:
   ```bash
   chmod +x setup_restaurant_management.sh
   ```

3. **Run the Script**:
   - Execute the script:
   ```bash
   ./setup_restaurant_management.sh
   ```

### Important Notes

- **Database Credentials**: Modify the `DB_NAME`, `DB_USER`, and `DB_PASSWORD` variables at the top of the script to match your MySQL setup.
- **MySQL Server**: Ensure your MySQL server is running before executing the script.
- **Python Version**: The script assumes you are using Python 3.x. Make sure it's properly installed on your system.
- **Django Version**: If you wish to use a different version of Django, modify the `DJANGO_VERSION` variable.
- **Accessing the Development Server**: Once the server starts running, you can navigate to `http://localhost:8000` in your web browser to see your Django application.
- **Error Handling**: The script uses `set -e` to exit immediately on errors. This can be useful for identifying issues during installation/setup.

This script sets up a basic Django project connected to a MySQL database, creates a superuser, and starts the Django development server, providing a foundation for building a restaurant management system further. You can build upon this by adding your models, views, and templates.
