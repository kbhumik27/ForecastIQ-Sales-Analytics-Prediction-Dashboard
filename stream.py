import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
def load_css(dark_mode=False):
    # Define theme variables based on mode
    if dark_mode:
        theme_vars = {
            'primary_color': '#2E86AB',
            'secondary_color': '#A23B72',
            'success_color': '#10B981',
            'warning_color': '#F59E0B',
            'error_color': '#EF4444',
            'text_primary': '#F9FAFB',
            'text_secondary': '#D1D5DB',
            'bg_primary': '#1F2937',
            'bg_secondary': '#111827',
            'border_color': '#374151',
            'shadow': '0 1px 3px 0 rgba(255, 255, 255, 0.1), 0 1px 2px 0 rgba(255, 255, 255, 0.06)',
            'chart_bg': '#1F2937',
            'grid_color': 'rgba(255,255,255,0.1)'
        }
    else:
        theme_vars = {
            'primary_color': '#2E86AB',
            'secondary_color': '#A23B72',
            'success_color': '#10B981',
            'warning_color': '#F59E0B',
            'error_color': '#EF4444',
            'text_primary': '#1F2937',
            'text_secondary': '#6B7280',
            'bg_primary': '#FFFFFF',
            'bg_secondary': '#F9FAFB',
            'border_color': '#E5E7EB',
            'shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
            'chart_bg': '#FFFFFF',
            'grid_color': 'rgba(0,0,0,0.1)'
        }
    
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base styling with theme variables */
    .stApp {{
        background-color: {theme_vars['bg_secondary']} !important;
        color: {theme_vars['text_primary']} !important;
    }}
    
    .main .block-container {{
        background-color: {theme_vars['bg_secondary']} !important;
        color: {theme_vars['text_primary']} !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {theme_vars['bg_primary']} !important;
    }}
    
    .css-1lcbmhc {{
        background-color: {theme_vars['bg_primary']} !important;
        border-right: 1px solid {theme_vars['border_color']} !important;
    }}
    
    /* Input widgets */
    .stSelectbox > div > div {{
        background-color: {theme_vars['bg_primary']} !important;
        color: {theme_vars['text_primary']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
    }}
    
    .stMultiSelect > div > div {{
        background-color: {theme_vars['bg_primary']} !important;
        color: {theme_vars['text_primary']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
    }}
    
    .stDateInput > div > div {{
        background-color: {theme_vars['bg_primary']} !important;
        color: {theme_vars['text_primary']} !important;
        border: 1px solid {theme_vars['border_color']} !important;
    }}
    
    /* Main app styling */
    .main {{
        font-family: 'Inter', sans-serif;
        background-color: {theme_vars['bg_secondary']} !important;
        color: {theme_vars['text_primary']} !important;
    }}
    
    /* Header styling */
    .header-container {{
        background: linear-gradient(135deg, {theme_vars['primary_color']}, {theme_vars['secondary_color']});
        padding: 2rem 1rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: {theme_vars['shadow']};
    }}
    
    .header-title {{
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }}
    
    .header-subtitle {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 0;
    }}
    
    /* Metric cards */
    .metric-card {{
        background-color: {theme_vars['bg_primary']};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {theme_vars['border_color']};
        box-shadow: {theme_vars['shadow']};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }}
    
    .metric-title {{
        color: {theme_vars['text_secondary']};
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .metric-value {{
        color: {theme_vars['text_primary']};
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }}
    
    .metric-change {{
        font-size: 0.875rem;
        font-weight: 500;
    }}
    
    .metric-change.positive {{
        color: {theme_vars['success_color']};
    }}
    
    .metric-change.negative {{
        color: {theme_vars['error_color']};
    }}
    
    /* Chart containers */
    .chart-container {{
        background-color: {theme_vars['bg_primary']};
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid {theme_vars['border_color']};
        box-shadow: {theme_vars['shadow']};
        margin-bottom: 1.5rem;
    }}
    
    .chart-title {{
        color: {theme_vars['text_primary']};
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {theme_vars['primary_color']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}
    
    .stButton > button:hover {{
        background-color: {theme_vars['secondary_color']} !important;
        transform: translateY(-1px) !important;
    }}
    
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {{
        color: {theme_vars['text_primary']} !important;
    }}
    
    p, span, div {{
        color: {theme_vars['text_primary']} !important;
    }}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .header-title {{
            font-size: 2rem;
        }}
        
        .metric-value {{
            font-size: 1.5rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Theme toggle function
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Load CSS with theme
load_css(st.session_state.dark_mode)

# Apply theme
theme_vars = {
    'text_primary': '#F9FAFB' if st.session_state.dark_mode else '#1F2937',
    'chart_bg': '#1F2937' if st.session_state.dark_mode else '#FFFFFF',
    'grid_color': 'rgba(255,255,255,0.1)' if st.session_state.dark_mode else 'rgba(0,0,0,0.1)'
}

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Sales Forecasting Dashboard</h1>
    <p class="header-subtitle">Advanced Analytics & Machine Learning Insights</p>
</div>
""", unsafe_allow_html=True)

# Theme toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col3:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", 
                 help="Toggle dark/light mode",
                 key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Generate sample data for demonstration
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2011, 1, 1)
    end_date = datetime(2011, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate sample sales data
    countries = ['United Kingdom', 'Germany', 'France', 'Spain', 'Netherlands']
    stock_codes = [f'SKU{i:03d}' for i in range(1, 51)]
    
    data = []
    for date in date_range:
        for country in countries:
            for _ in range(np.random.randint(5, 15)):
                stock_code = np.random.choice(stock_codes)
                quantity = np.random.randint(1, 100)
                unit_price = np.random.uniform(1, 50)
                
                data.append({
                    'InvoiceDate': date,
                    'Country': country,
                    'StockCode': stock_code,
                    'Quantity': quantity,
                    'UnitPrice': unit_price,
                    'Revenue': quantity * unit_price
                })
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

# Calculate metrics
total_revenue = df['Revenue'].sum()
total_quantity = df['Quantity'].sum()
avg_order_value = df['Revenue'].mean()
mae = 15.42  # Your calculated MAE
quantity_sold_w39 = 45623  # Your calculated quantity for week 39

# Sidebar filters
st.sidebar.header("📊 Filters")
countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['Country'].unique(),
    default=df['Country'].unique()[:3]
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['InvoiceDate'].min(), df['InvoiceDate'].max()),
    min_value=df['InvoiceDate'].min(),
    max_value=df['InvoiceDate'].max()
)

# Filter data based on selections
filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['InvoiceDate'] >= pd.to_datetime(date_range[0])) &
    (df['InvoiceDate'] <= pd.to_datetime(date_range[1]))
]

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-value">${total_revenue:,.0f}</div>
        <div class="metric-change positive">↗ 12.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Quantity</div>
        <div class="metric-value">{total_quantity:,}</div>
        <div class="metric-change positive">↗ 8.3%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Model MAE</div>
        <div class="metric-value">{mae:.2f}</div>
        <div class="metric-change negative">↘ 3.2%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Week 39 Forecast</div>
        <div class="metric-value">{quantity_sold_w39:,}</div>
        <div class="metric-change positive">↗ 15.7%</div>
    </div>
    """, unsafe_allow_html=True)

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Revenue Trend by Country</h3>', unsafe_allow_html=True)
    
    # Revenue trend chart
    revenue_trend = filtered_df.groupby(['InvoiceDate', 'Country'])['Revenue'].sum().reset_index()
    fig_revenue = px.line(
        revenue_trend,
        x='InvoiceDate',
        y='Revenue',
        color='Country',
        title='',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_revenue.update_layout(
        plot_bgcolor=theme_vars['chart_bg'],
        paper_bgcolor=theme_vars['chart_bg'],
        font=dict(color=theme_vars['text_primary']),
        xaxis=dict(showgrid=True, gridcolor=theme_vars['grid_color']),
        yaxis=dict(showgrid=True, gridcolor=theme_vars['grid_color']),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_revenue, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Sales Distribution by Country</h3>', unsafe_allow_html=True)
    
    # Sales distribution pie chart
    country_sales = filtered_df.groupby('Country')['Quantity'].sum().reset_index()
    fig_pie = px.pie(
        country_sales,
        values='Quantity',
        names='Country',
        title='',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(
        plot_bgcolor=theme_vars['chart_bg'],
        paper_bgcolor=theme_vars['chart_bg'],
        font=dict(color=theme_vars['text_primary']),
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Full width charts
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<h3 class="chart-title">Model Performance & Forecast Analysis</h3>', unsafe_allow_html=True)

# Create subplots for model performance
fig_performance = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Prediction vs Actual', 'Weekly Forecast Trend'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}]]
)

# Generate sample prediction data
np.random.seed(42)
actual_values = np.random.normal(100, 25, 100)
predicted_values = actual_values + np.random.normal(0, mae, 100)

# Prediction vs Actual scatter plot
fig_performance.add_trace(
    go.Scatter(
        x=actual_values,
        y=predicted_values,
        mode='markers',
        name='Predictions',
        marker=dict(color='#2E86AB', size=8, opacity=0.6)
    ),
    row=1, col=1
)

# Perfect prediction line
min_val, max_val = min(actual_values), max(actual_values)
fig_performance.add_trace(
    go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        name='Perfect Prediction',
        line=dict(color='#EF4444', dash='dash')
    ),
    row=1, col=1
)

# Weekly forecast trend
weeks = list(range(35, 45))
forecast_values = [np.random.randint(40000, 50000) for _ in weeks]
forecast_values[4] = quantity_sold_w39  # Week 39 value

fig_performance.add_trace(
    go.Scatter(
        x=weeks,
        y=forecast_values,
        mode='lines+markers',
        name='Weekly Forecast',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10)
    ),
    row=1, col=2
)

# Highlight week 39
fig_performance.add_trace(
    go.Scatter(
        x=[39],
        y=[quantity_sold_w39],
        mode='markers',
        name='Week 39 Forecast',
        marker=dict(color='#F59E0B', size=15, symbol='star')
    ),
    row=1, col=2
)

fig_performance.update_layout(
    height=400,
    plot_bgcolor=theme_vars['chart_bg'],
    paper_bgcolor=theme_vars['chart_bg'],
    font=dict(color=theme_vars['text_primary']),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig_performance.update_xaxes(showgrid=True, gridcolor=theme_vars['grid_color'])
fig_performance.update_yaxes(showgrid=True, gridcolor=theme_vars['grid_color'])

st.plotly_chart(fig_performance, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Model Information Section
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Model Configuration</h3>', unsafe_allow_html=True)
    
    model_config = {
        'Algorithm': 'Random Forest Regressor',
        'Features': 'Country, StockCode, Month, Year, DayOfWeek, Day, Week',
        'Max Bins': '4,000',
        'Training Period': 'Jan 2011 - Sep 25, 2011',
        'Test Period': 'Sep 26, 2011 - Dec 31, 2011',
        'Evaluation Metric': 'Mean Absolute Error (MAE)'
    }
    
    for key, value in model_config.items():
        st.markdown(f"**{key}:** {value}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">Key Insights</h3>', unsafe_allow_html=True)
    
    insights = [
        f"📊 Model achieved MAE of {mae:.2f} units",
        f"🎯 Week 39 forecast: {quantity_sold_w39:,} units",
        f"📈 Total revenue: ${total_revenue:,.0f}",
        f"🌍 Top performing country: {filtered_df.groupby('Country')['Revenue'].sum().idxmax()}",
        f"📦 Average order value: ${avg_order_value:.2f}",
        f"🔄 Model processes {len(df):,} daily transactions"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style="text-align: center; color: var(--text-secondary); font-size: 0.875rem; margin-top: 2rem;">
    <p>🚀 Powered by PySpark ML & Streamlit | Built with ❤️ for Data Science</p>
</div>
""", unsafe_allow_html=True)

# Close dark mode div
if st.session_state.dark_mode:
    st.markdown('</div>', unsafe_allow_html=True)