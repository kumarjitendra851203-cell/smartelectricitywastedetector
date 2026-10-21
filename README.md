# Smart Energy Analyzer

Python (main) + C++ (fast rolling z-score engine) + Streamlit UI + Pandas / scikit-learn / Matplotlib.

## Run
    pip install -r requirements.txt
    streamlit run app.py
C++ engine `g++` se auto-compile hota hai; g++ na ho to NumPy fallback chalta hai (sidebar me engine dikhta hai).

## Features
- Demo data ya apni CSV (rows validate hoti hain, galat rows reason ke saath dikhti hain)
- Overview: daily chart, hourly profile, weekday x hour heatmap
- Anomalies: C++ z-score ya Isolation Forest, events table, extra kWh/cost
- Forecast: Ridge (trend + weekday), 95% range, predicted bill (flat / tiered)
- Bills sirf estimate hain.

## Tests
    python -m unittest discover -s tests
