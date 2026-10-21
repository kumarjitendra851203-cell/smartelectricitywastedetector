# ⚡ Smart Energy Analyzer

### AI-Powered Electricity Consumption & Waste Detection System

An intelligent energy analysis application that helps users understand electricity consumption, detect unusual energy usage, estimate potential electricity waste, and forecast future energy bills using data analysis and machine learning.

## 🚀 Overview

**Smart Energy Analyzer** is a Python-based application with a Streamlit interface and a high-performance C++ engine for rolling Z-score calculations.

The application analyzes electricity consumption data, identifies unusual usage patterns, visualizes daily and hourly consumption, and predicts future energy usage and estimated bills.

## ✨ Features

- 📊 **Energy Dashboard** — Visualize daily electricity consumption and usage patterns.
- 📂 **CSV Upload** — Upload your own electricity consumption dataset.
- 🔍 **Data Validation** — Identify invalid rows and display the reasons for rejection.
- 🚨 **Anomaly Detection** — Detect unusual electricity usage using Z-score analysis or Isolation Forest.
- ⚡ **Energy Waste Estimation** — Calculate additional energy consumption and estimated cost associated with detected anomalies.
- 📈 **Consumption Forecasting** — Predict future electricity usage using Ridge Regression.
- 💰 **Bill Estimation** — Estimate electricity bills using flat-rate or tiered pricing.
- 🕒 **Hourly Analysis** — Analyze consumption patterns by hour and day of the week.
- 🔥 **Heatmap Visualization** — Explore weekday-versus-hour electricity usage.
- ⚙️ **C++ Acceleration** — Use a C++ rolling Z-score engine when a compatible compiler is available.
- 🔄 **NumPy Fallback** — Continue analysis with NumPy if the C++ engine cannot be compiled.
- 🧪 **Automated Tests** — Run unit tests to check application functionality.

> **Note:** Electricity bills are estimates, and detected anomalies indicate unusual usage rather than confirmed electricity waste.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main application and analysis |
| C++ | High-performance rolling Z-score engine |
| Streamlit | Interactive web interface |
| Pandas | Data processing and manipulation |
| NumPy | Numerical calculations and fallback engine |
| scikit-learn | Isolation Forest and Ridge Regression |
| Matplotlib | Charts and visualizations |

## 📁 Project Structure

```text
Smart-Energy-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── tests/
│   └── ...
└── C++ engine source files
```

*Update the structure above to match the actual files in your repository.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart-Energy-Analyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install a C++ Compiler (Optional)

Install a compatible compiler such as GCC/G++ and ensure `g++` is available in your system PATH.

The application can use the NumPy fallback if the C++ engine is unavailable.

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 🧪 Run Tests

Execute the project's unit tests with:

```bash
python -m unittest discover -s tests
```

## 📊 How It Works

1. Load the demo dataset or upload a supported CSV file.
2. Validate the input data and inspect any rejected rows.
3. Explore electricity usage through daily charts, hourly profiles, and heatmaps.
4. Detect unusual consumption using the available anomaly detection methods.
5. Review estimated additional energy consumption and associated cost.
6. Forecast future electricity consumption and view the estimated bill.

## 🎯 Project Objectives

- Improve awareness of electricity consumption.
- Identify unusual energy usage patterns.
- Support data-driven energy management.
- Explore machine learning for energy forecasting.
- Demonstrate Python and C++ integration in a practical project.

## 🔮 Future Enhancements

- Real-time smart meter integration.
- Device-level energy monitoring.
- User authentication and personalized dashboards.
- Electricity tariff configuration by region.
- Email or mobile alerts for unusual consumption.
- Historical reports and downloadable PDF summaries.
- Cloud deployment and database integration.

*These are planned enhancements, not claims about existing functionality.*

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Test your code.
5. Submit a pull request.

## ⚠️ Disclaimer

This application provides analytical estimates based on the supplied data. Anomaly detection does not prove that electricity was wasted, and predicted bills may differ from actual utility bills.

## 👨‍💻 Developer

**Jitendra Kumar**  
CSE — Artificial Intelligence & Data Science

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

*Built with Python, C++, data analytics, and machine learning.*
