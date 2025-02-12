launch backend with
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
launch frontend with
streamlit run .\main.py

- root dir is z sandbox for manual debugging

https://github.com/EvickaStudio/GeoGuessr-API

project-name/


Named keys user_cookies = "9RdYNUrRX

Launch.json for backend
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Backend CurFile",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend"
            },
            "console": "integratedTerminal"
        }
    ]
}


* [Geoguessr API guide](https://efisha.com/2022/04/18/geoguessr-api-endpoints/)

* [Fetching the _ncfa cookie](https://github.com/EvickaStudio/GeoGuessr-API?tab=readme-ov-file#authentication)\



1. Install PostgreSQL (on Mac)
brew install postgresql
brew services start postgresql

🔹 Install on Windows (Using pgAdmin or WSL)
17.2
Download & install PostgreSQL from postgresql.org
Run pgAdmin or psql to manage the database.
https://www.postgresql.org/download/
db superuser (default)
un: postgres
pw: geocoach

2. Start and Enable PostgreSQL on mac
sudo systemctl start postgresql
sudo systemctl enable postgresql

* on windows, launch pgAdmin app

3️⃣ Create a PostgreSQL Database & User
Open PostgreSQL CLI (psql):

sudo -u postgres psql
Then run the following:

-- Create a new database
CREATE DATABASE geoguessr_dev;

-- Create a new user
CREATE USER Zach WITH PASSWORD 'geocoach';
GRANT ALL PRIVILEGES ON DATABASE geoguessr_dev TO Zach;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO Zach;

CREATE USER Jason WITH PASSWORD 'geocoach';
GRANT ALL PRIVILEGES ON DATABASE geoguessr_dev TO Jason;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO Jason;

Exit psql:
\q

Figure out SQL for generating tables.


🔹 Option 1: Using pgAdmin GUI
1️⃣ Open pgAdmin
Open pgAdmin and connect to your PostgreSQL server.
Expand Databases → geoguessr_dev.
2️⃣ Create the games Table
Navigate to Schemas → public → Tables.
Right-click Tables → Click Create → Click Table.
Set the table name as games.
3️⃣ Define Columns
Under the "Columns" tab, click "Add" and add the following fields:

Column Name	Data Type	Primary Key?	Constraints
id	SERIAL	✅ Yes	Auto-increment
map_slug	VARCHAR(255)	❌ No	-
map_name	TEXT	❌ No	-
points	INTEGER	❌ No	-
game_token	VARCHAR(255)	❌ No	UNIQUE
game_mode	VARCHAR(50)	❌ No	-
raw_payload	JSONB	❌ No	Stores full JSON
Click Save to create the table.


│-- backend/               # Backend API and visualization logic
│   │-- models/            # Database models
│   │-- routes/            # API endpoints
│   │-- services/          # Business logic for visualizations
│   └── main.py            # Entry point (FastAPI) or manage.py (Django)
│
│-- frontend/              # Frontend code (if applicable)
│-- scripts/               # Utility scripts
│-- README.md              # Documentation

for database setup
create each table by hand too if you want
make sure id is serial, points are integer, and otherwise text


# Backend Visualization Development Guide (For Zach)
1. Getting Started
1.1. Install Required Software
Ensure you have:

VSCode (with the Python extension)
Python 3.8+ (Check with python --version)
pip & virtualenv (Check with pip --version)
Matplotlib, Pandas, NumPy (for visualization)
1.2. Set Up the Project in VSCode
Clone the Repository


git clone https://github.com/your-org/project-name.git
cd project-name
Open the Project in VSCode
You will mainly work inside backend/visualizations/.

2.1. Writing your analysis
cd backend/visualizations/
touch zach_plot.py
Example zach_plot.py:
import matplotlib.pyplot as plt
import numpy as np

# Pull in some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create the plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, label="Sine Wave")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("Sample Visualization")
plt.legend()
plt.grid()

# Save the plot
plt.savefig("output.png")
plt.show()


Run the script in VSCode Terminal:
python zach_plot.py
This will generate output.png.

3. Viewing and Debugging Plots in VSCode
Install the Python extension in VSCode.
Use the interactive window to run Python code and see live plots.
Open output.png in VSCode to check results.
4. Next Steps: Converting to an API
Once you're happy with your visualization:

I'll help turn your script into a backend API.
We’ll model the data and integrate it into the frontend.

git checkout -b zach-visualization
git add backend/visualizations/zach_plot.py
git commit -m "Initial visualization script"
git push origin zach-visualization



# Creating API Endpoints
from fastapi import APIRouter
from backend.services.visualization_service import generate_chart_data

router = APIRouter()

@router.get("/visualizations/{chart_type}")
async def get_chart_data(chart_type: str):
    return generate_chart_data(chart_type)


Implement the logic in backend/services/visualization_service.py:\
def generate_chart_data(chart_type):
    if chart_type == "bar":
        return {"labels": ["A", "B", "C"], "values": [10, 20, 30]}
    elif chart_type == "line":
        return {"points": [1, 2, 3, 4, 5], "values": [5, 10, 15, 20, 25]}
    else:
        return {"error": "Unknown chart type"}
