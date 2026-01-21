# House Price Estimator

A minimal Django application that estimates house prices from user input.

Features:
- Square meter, rooms, floor, building age inputs
- Simple price estimation algorithm
- Bootstrap-based responsive UI

Quick start (Windows PowerShell):

```powershell
# create a virtual environment
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# run migrations (no models used except auth default)
python manage.py migrate

# runserver
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

How the estimator works
- The app uses a small heuristic-based estimator:
	- base price per square meter: 2000 (configurable in code)
	- rooms increase value (+3% per room)
	- higher floors increase value (+2% per floor)
	- older buildings decrease value (-1% per year)
	- multiplier is clamped to a reasonable range so results don't go negative

Notes
- This is a demo app intended for illustration and does not use any machine learning model or real market data. Treat results as simple heuristics for prototyping.

Changes in UI
- The app now uses a refreshed design named "Home Price Prediction Robot" with a modern, minimalist layout.
- Uses Poppins font and blue/turquoise accent colors; form inputs and buttons include rounded corners, subtle shadows, and animation.
- A light-weight JavaScript file is included to submit the form via AJAX and animate the estimate result box for a smooth user experience.

Accessibility & Progressive enhancement
- JavaScript is optional: the server still renders results for non-JS clients. When JS is enabled, the form will POST via fetch and display results without a page reload.
