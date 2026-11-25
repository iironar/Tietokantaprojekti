## About the repository

This application is supposed to be auction for vehicles created for another course, now repurposed to showcase cybersecurity flaws for cybersecurity part VII

## Installation and Setup

Before installing the application, make sure you have installed Python 3
This project uses SQLite, which is included in Python 3

### 1. Clone the repository

Clone the repository anywhere you want and move inside the source directory.

You can also copypaste these commands

```bash
git clone https://github.com/iironar/Tietokantaprojekti.git
cd Tietokantaprojekti
```

### 2. Create a virtual environment

Create a Python virtual environment using the following commands.

**Linux and macOS:**

```bash
python3 -m venv venv
```

**Windows:**

```powershell
py -m venv venv
```

### 3. Activate the virtual environment

**Linux and macOS:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

### 4. Install dependencies

Install Flask inside the virtual environment:

```bash
python -m pip install flask
```

### 5. Initialize the database

Run the following commands from the project's root directory:

```bash
python -c "import sqlite3; c=sqlite3.connect('database.db'); c.executescript(open('schema.sql', encoding='utf-8').read()); c.close()"
```

```bash
python -c "import sqlite3; c=sqlite3.connect('database.db'); c.executescript(open('init.sql', encoding='utf-8').read()); c.close()"
```

These commands create the database and execute the needed SQL statements in the initialization files.

### 6. Run the application

Start the Flask application:

```bash
flask --app app run
```

The application will be available in your browser at:

http://127.0.0.1:5000

When you are finished, you can deactivate the virtual environment using:

```bash
deactivate
```

 
 
