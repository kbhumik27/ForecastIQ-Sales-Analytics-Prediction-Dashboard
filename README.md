# 📊 ForecastIQ – Sales Analytics & Prediction Dashboard

ForecastIQ is a Streamlit-powered interactive dashboard designed for advanced sales forecasting, KPI visualization, and business intelligence. Built using PySpark, Plotly, and scikit-learn, it simulates and forecasts e-commerce sales data with support for theme toggling (light/dark), model insights, and interactive charts.

![ForecastIQ Banner](https://your-image-or-gif-link-if-any)

## 🚀 Features

- 📈 **Real-time Data Filtering**: Filter by country and date using an intuitive sidebar.
- 🎯 **Sales Forecasting**: Weekly sales prediction using a trained Random Forest model.
- 🌍 **Multi-country Support**: Simulates data for UK, France, Germany, Spain, and Netherlands.
- 💡 **KPI Metrics**: Total Revenue, Quantity Sold, MAE, Week-specific Forecasts.
- 🌙 **Dark/Light Mode Toggle**: Built-in CSS theming for a better viewing experience.
- 📊 **Interactive Charts**: Revenue trends, country-wise distribution, and model performance.

## 📌 Demo

> Coming Soon: Live demo hosted on Streamlit Cloud or Tiber Developer Cloud.

## 🛠️ Tech Stack

- **Frontend**: Streamlit, HTML/CSS (custom styling), Plotly
- **Backend**: Python, Pandas, NumPy
- **ML/ETL**: PySpark, scikit-learn (Random Forest), Data Generation
- **Visualization**: Plotly Express, Plotly Graph Objects, Subplots

## 📂 Project Structure

```bash
📁 ForecastIQ/
│
├── 📄 app.py              # Main Streamlit dashboard
├── 📁 data/               # (Optional) Real datasets or preprocessed files
├── 📁 assets/             # Icons, images, or logo if any
├── 📄 requirements.txt    # Python dependencies
├── 📄 README.md           # Project overview (this file)
