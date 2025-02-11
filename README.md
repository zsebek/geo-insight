launch backend with
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
launch frontend with
streamlit run .\main.py

- add root dir for manual debugging

https://github.com/EvickaStudio/GeoGuessr-API

project-name/


Keys go in J_COOKIE = "9RdYNUrRX

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



│-- backend/               # Backend API and visualization logic
│   │-- models/            # Database models
│   │-- routes/            # API endpoints
│   │-- services/          # Business logic for visualizations
│   └── main.py            # Entry point (FastAPI) or manage.py (Django)
│
│-- frontend/              # Frontend code (if applicable)
│-- scripts/               # Utility scripts
│-- README.md              # Documentation

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


# GeoInsight

GeoInsight is a web application that analyses your GeoGuessr games and provides you with metrics and 
visualizations to better understand your style of play. 

The web application can be accessed [here](https://geo-insight.streamlit.app/).

If you want to install GeoInsight on your local machine, follow the instructions below.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed the latest version of Python. 
* You have a Windows/Linux/Mac machine.

## Installing GeoInsight

To install GeoInsight, follow these steps:

Clone the repository onto your machine:

```
git clone https://github.com/SafwanSipai/geo-insight.git 
```

## Using GeoInsight

To use GeoInsight, follow these steps:

1. Go to the root of the folder (geo-insight) that was created when the repository was cloned.

2. Create a python virtual environment using the command: `python -m venv <env-name>`

3. Install the required libraries/dependencies: `pip install requirements.txt`

4. Activate the python environment (run the following commands in the root folder):

    | Platform | Command                |
    | :--------| :------------------------- |
    | bash/zsh | `source <env-name>/bin/activate` |
    | PowerShell | `<env-name>\Scripts\Activate.ps1` |
    | cmd.exe | `<env-name>\Scripts\activate.bat` |

5. Inside the terminal, run the command: `streamlit run app.py`

6. The web application will open in your browser.

## Getting your `_ncfa` cookie

1. Open your web browser and navigate to the GeoGuessr website.

2. Log in to your GeoGuessr account using your credentials.

3. Once logged in, open the developer tools in your web browser. You can usually do this by right-clicking on the webpage and selecting "Inspect" or by pressing Ctrl+Shift+I (Cmd+Option+I on Mac).

4. In the developer tools window, navigate to the "Network" tab.

5. With the network tab open, refresh the GeoGuessr webpage to capture the network traffic.

6. Use the filter on the top-left of the network tab to search for 'stats'.

7. Click on the 'stats' request to open it and view its details.

8. In the request headers section, locate the "_ncfa" cookie.

    ![alt text](images/ncfa1.PNG)

9. Copy the value of the "_ncfa" cookie (everything after the '=' sign until the ';', do not copy the ';').

    ![alt text](images/ncfa2.PNG)

10. Now, you can paste the copied "_ncfa" token into text box of the web application, where indicated.

## Security and Privacy

GeoInsight is completely secure for use. It DOES NOT establish any connections to a database, ensuring that neither the _ncfa cookie nor the associated data fetched through it is retained or stored anywhere. Upon exiting the web application, this data is promptly deleted. 

You are welcome to review the code yourself to confirm this assurance.

## Acknowledgement 

* [Geoguessr API guide](https://efisha.com/2022/04/18/geoguessr-api-endpoints/)

* [Fetching the _ncfa cookie](https://github.com/EvickaStudio/GeoGuessr-API?tab=readme-ov-file#authentication)