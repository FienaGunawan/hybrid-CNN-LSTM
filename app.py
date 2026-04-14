import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import logging
from datetime import datetime
import traceback

import backend as backend

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
os.makedirs('logs', exist_ok=True)
log_file = f'logs/app_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("="*80)
logger.info("Stock Price Prediction Application Started")
logger.info(f"Log file: {log_file}")
logger.info("="*80)


st.set_page_config(
    page_title='Stock Price Prediction',
    layout='wide',
)


CSS = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary-dark: #1a1f2e;
        --primary-blue: #2563eb;
        --primary-navy: #1e3a8a;
        --success-green: #059669;
        --success-light: #10b981;
        --danger-red: #dc2626;
        --danger-light: #ef4444;
        --warning-amber: #d97706;
        --info-blue: #0284c7;
        --neutral-gray: #64748b;
        --bg-light: #f8fafc;
        --bg-white: #ffffff;
        --text-dark: #1e293b;
        --text-gray: #475569;
        --border-light: #e2e8f0;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    }

    html, body, .stApp {
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-dark);
        line-height: 1.6;
    }

    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }

    .block-container {
        padding-top: 0.5rem;
        padding-left: 20px;
        padding-right: 20px;
        max-width: 1400px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}

    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
    }

    .header {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-navy) 100%);
        box-shadow: var(--shadow-lg);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid var(--primary-blue);
        border-radius: 12px;
    }

    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 0 2rem;
    }

    .header h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .header h1 i {
        color: var(--success-light);
        font-size: 2rem;
    }

    .header .subtitle {
        color: #cbd5e1;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }

    .header-badge {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: white;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .card {
        background: var(--bg-white);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: var(--shadow-lg);
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--bg-light);
    }

    .card-header h2 {
        color: var(--text-dark);
        font-size: 1.4rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
    }

    .card-header i {
        color: var(--primary-blue);
        font-size: 1.5rem;
    }

    .form-label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-dark);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .form-label i {
        color: var(--primary-blue);
        font-size: 1rem;
    }

    .stButton > button {
        padding: 0.9rem 2.2rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-navy) 100%);
        color: #000000;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .stDownloadButton > button {
        padding: 0.9rem 2.2rem;
        border: none;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-navy) 100%);
        color: #000000;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        width: 100%;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
    }

    div[data-testid="stForm"] {
        background: var(--bg-white);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        transition: all 0.3s ease;
    }

    div[data-testid="stForm"]:hover {
        box-shadow: var(--shadow-lg);
    }

    div[data-baseweb="select"] > div {
        border: 2px solid var(--border-light);
        border-radius: 8px;
        background: var(--bg-white);
    }

    div[data-baseweb="select"] > div:hover {
        border-color: var(--neutral-gray);
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.25rem;
        margin-bottom: 1.5rem;
    }

    .stat-card {
        background: var(--bg-light);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--neutral-gray);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        transform: translate(40%, -40%);
    }

    .stat-card.primary {
        border-left-color: var(--primary-blue);
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }

    .stat-card.positive {
        border-left-color: var(--success-green);
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }

    .stat-card.negative {
        border-left-color: var(--danger-red);
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    }

    .stat-card.info {
        border-left-color: var(--info-blue);
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }

    .stat-card.warning {
        border-left-color: var(--warning-amber);
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
    }

    .stat-card.danger {
        border-left-color: var(--danger-red);
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    }

    .stat-label {
        font-size: 0.75rem;
        color: var(--text-gray);
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--text-dark);
        font-family: 'Courier New', monospace;
    }

    .stat-change {
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-weight: 700;
    }

    .stat-change.positive { color: var(--success-green); }
    .stat-change.negative { color: var(--danger-red); }

    .stat-info {
        font-size: 0.8rem;
        color: var(--text-gray);
        margin-top: 0.5rem;
        font-weight: 600;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid var(--border-light);
        text-align: center;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--text-gray);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--text-dark);
        font-family: 'Courier New', monospace;
    }

    .metric-value.excellent { color: var(--success-green); }
    .metric-value.good { color: var(--success-light); }
    .metric-value.fair { color: var(--warning-amber); }
    .metric-value.poor { color: var(--danger-red); }

    .metric-desc {
        font-size: 0.7rem;
        color: var(--text-gray);
        margin-top: 0.25rem;
        font-weight: 600;
    }

    .table-container table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border-light);
    }

    .table-container th, .table-container td {
        padding: 1rem;
        text-align: left;
    }

    .table-container th {
        background: var(--primary-dark);
        color: white;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }

    .table-container td {
        border-bottom: 1px solid var(--border-light);
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }

    .table-container tr:last-child td {
        border-bottom: none;
    }

    .table-container tbody tr:hover {
        background: var(--bg-light);
    }

    div[data-testid="stPlotlyChart"] > div {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        background: white;
    }

    div[data-testid="stPlotlyChart"] {
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .alert {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-left: 4px solid;
    }

    .alert-success {
        background: #d1fae5;
        color: #065f46;
        border-left-color: var(--success-green);
    }

    .alert-error {
        background: #fee2e2;
        color: #991b1b;
        border-left-color: var(--danger-red);
    }

    .section-caption {
        color: var(--text-gray);
        font-size: 0.85rem;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }

    .footer {
        background: var(--primary-dark);
        padding: 2rem 0;
        margin-top: 3rem;
        text-align: center;
        border-top: 3px solid var(--primary-blue);
        border-radius: 12px;
    }

    .footer p {
        margin: 0.5rem 0;
        color: #94a3b8;
        font-size: 0.9rem;
    }

    .footer p:first-child {
        color: white;
        font-weight: 700;
        font-size: 1rem;
    }

    @media (max-width: 768px) {
        .header h1 {
            font-size: 1.3rem;
        }
        .stats-grid {
            grid-template-columns: 1fr;
        }
        .card {
            padding: 1.5rem;
        }
    }
</style>
"""


st.markdown(CSS, unsafe_allow_html=True)


TICKER_LABELS = {
    'BIRD.JK': 'BIRD.JK - Blue Bird',
    'BPTR.JK': 'BPTR.JK - Batavia Prosperindo',
    'GIAA.JK': 'GIAA.JK - Garuda Indonesia',
    'LRNA.JK': 'LRNA.JK - Eka Sari Lorena',
    'PURA.JK': 'PURA.JK - Puradelta Lestari',
    'TAXI.JK': 'TAXI.JK - Express Transindo',
}


def _format_rupiah(value, decimals=0):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return '-'
    try:
        value = float(value)
    except Exception:
        return str(value)

    formatted = f"{value:,.{decimals}f}"
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    if decimals == 0:
        formatted = formatted.split(',')[0]
    return f"Rp {formatted}"


@st.cache_data(show_spinner=False)
def _load_dataset():
    return backend.load_historical_dataset().copy()


@st.cache_resource(show_spinner=False)
def _warm_models():
    if getattr(backend, 'loaded_models', None):
        if backend.loaded_models:
            return True
    try:
        backend.preload_models()
    except Exception:
        return False
    return True


_warm_models()


st.markdown(
    """
    <div class="header">
        <div class="container">
            <div class="header-content">
                <div>
                    <h1><i class="fas fa-chart-line"></i> Stock Price Prediction - CNN-LSTM</h1>
                    <p class="subtitle">Transportation Stock Analysis & Prediction System</p>
                </div>
                <div class="header-badge"><i class="fas fa-shield-alt"></i> Professional Trading Tool</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.form('prediction_form'):
    st.markdown(
        """
        <div class="card-header">
            <h2><i class="fas fa-cog"></i> Model Configuration</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    row1 = st.columns(3)
    with row1[0]:
        st.markdown('<label class="form-label"><i class="fas fa-building"></i> Stock Code</label>', unsafe_allow_html=True)
        ticker = st.selectbox(
            label='Stock Code',
            options=list(TICKER_LABELS.keys()),
            format_func=lambda v: TICKER_LABELS.get(v, v),
            label_visibility='collapsed',
        )
    with row1[1]:
        st.markdown('<label class="form-label"><i class="fas fa-brain"></i> Model Type</label>', unsafe_allow_html=True)
        model_type = st.selectbox(
            label='Model Type',
            options=['cnn_lstm', 'lstm'],
            format_func=lambda v: 'CNN-LSTM (Hybrid)' if v == 'cnn_lstm' else 'LSTM (Pure)',
            label_visibility='collapsed',
        )
    with row1[2]:
        st.markdown('<label class="form-label"><i class="fas fa-calendar"></i> Data Period</label>', unsafe_allow_html=True)
        data_period = st.selectbox(
            label='Data Period',
            options=[3, 6, 12, 24, 36],
            index=2,
            format_func=lambda v: f"{v} Months",
            label_visibility='collapsed',
        )

    row2 = st.columns(3)
    with row2[0]:
        st.markdown('<label class="form-label"><i class="fas fa-bolt"></i> Activation</label>', unsafe_allow_html=True)
        activation = st.selectbox(
            label='Activation',
            options=['auto', 'linear', 'relu', 'sigmoid', 'tanh'],
            index=0,
            format_func=lambda v: 'Auto (Best)' if v == 'auto' else v.capitalize(),
            label_visibility='collapsed',
        )
    with row2[1]:
        st.markdown('<label class="form-label"><i class="fas fa-cog"></i> Optimizer</label>', unsafe_allow_html=True)
        optimizer = st.selectbox(
            label='Optimizer',
            options=['auto', 'adam', 'nadam', 'adamax', 'adagrad'],
            index=0,
            format_func=lambda v: 'Auto (Best)' if v == 'auto' else v.capitalize(),
            label_visibility='collapsed',
        )
    with row2[2]:
        st.markdown('<label class="form-label"><i class="fas fa-calendar-check"></i> Prediction</label>', unsafe_allow_html=True)
        prediction_days = st.selectbox(
            label='Prediction Days',
            options=[1, 5, 10, 30],
            index=1,
            format_func=lambda v: f"{v} Day" if v == 1 else f"{v} Days",
            label_visibility='collapsed',
        )

    submitted = st.form_submit_button('⏯️ Run Prediction')


@st.cache_data(show_spinner=False)
def _ticker_history(ticker_value):
    try:
        logger.info(f"Fetching history for ticker: {ticker_value}")
        history = backend.get_ticker_history(ticker_value).copy()
        logger.info(f"History fetched successfully for {ticker_value}: {len(history)} records")
        return history
    except Exception as e:
        logger.error(f"Error fetching ticker history for {ticker_value}: {str(e)}")
        logger.error(traceback.format_exc())
        return pd.DataFrame()


def _slice_history_by_months(df, months):
    try:
        logger.info(f"Slicing history by {months} months")
        if df.empty:
            logger.warning("DataFrame is empty, returning as is")
            return df
        last_date = df['Date'].max()
        cutoff = last_date - pd.DateOffset(months=int(months))
        sliced = df[df['Date'] >= cutoff].copy()
        if sliced.empty:
            logger.warning(f"Sliced DataFrame is empty for {months} months, returning original")
            return df
        logger.info(f"Slicing successful: {len(sliced)} records")
        return sliced
    except Exception as e:
        logger.error(f"Error slicing history by months: {str(e)}")
        logger.error(traceback.format_exc())
        return df



def _compute_historical_stats(prices):
    if len(prices) <= 1:
        return 0.0
    returns = np.diff(prices) / np.maximum(prices[:-1], 1e-8)
    return float(np.std(returns) * np.sqrt(252) * 100)



def _build_stats_html(stats, change_class, change_icon, volatility_class, volatility_label):
    return f"""
    <div class="stats-grid">
        <div class="stat-card primary">
            <div class="stat-label">Current Price</div>
            <div class="stat-value">{_format_rupiah(stats['last_historical_price'])}</div>
            <div class="stat-info">{stats['data_points']} Data Points</div>
        </div>
        <div class="stat-card {change_class}">
            <div class="stat-label">Final Prediction</div>
            <div class="stat-value">{_format_rupiah(stats['predicted_price'])}</div>
            <div class="stat-change {change_class}">
                {change_icon} {_format_rupiah(abs(stats['change']))} ({stats['change_percent']:.2f}%)
            </div>
        </div>
        <div class="stat-card info">
            <div class="stat-label">Prediction Range</div>
            <div class="stat-value" style="font-size: 1.1rem;">
                {_format_rupiah(stats['min_prediction'])} - {_format_rupiah(stats['max_prediction'])}
            </div>
            <div class="stat-info">Avg: {_format_rupiah(stats['avg_prediction'])}</div>
        </div>
        <div class="stat-card {volatility_class}">
            <div class="stat-label">Volatility</div>
            <div class="stat-value">{stats['volatility']:.2f}%</div>
            <div class="stat-info">{volatility_label} Risk</div>
        </div>
    </div>
    """



def _metric_class(value, thresholds):
    if value is None:
        return 'poor', 'Needs Improvement'
    for threshold, cls, label in thresholds:
        if value <= threshold:
            return cls, label
    return thresholds[-1][1], thresholds[-1][2]



def _build_metrics_html(metrics):
    r2 = metrics.get('r2')
    rmse = metrics.get('rmse')
    mape = metrics.get('mape')
    mse = metrics.get('mse')

    r2_cls = 'excellent'
    r2_label = 'Excellent'
    if r2 is not None:
        if r2 < 0.7:
            r2_cls, r2_label = 'poor', 'Needs Improvement'
        elif r2 < 0.8:
            r2_cls, r2_label = 'fair', 'Fair'
        elif r2 < 0.9:
            r2_cls, r2_label = 'good', 'Good'

    rmse_cls = 'excellent'
    rmse_label = 'Excellent'
    if rmse is not None:
        if rmse > 0.1:
            rmse_cls, rmse_label = 'poor', 'Needs Improvement'
        elif rmse > 0.05:
            rmse_cls, rmse_label = 'fair', 'Fair'
        elif rmse > 0.03:
            rmse_cls, rmse_label = 'good', 'Good'

    mape_cls = 'excellent'
    mape_label = 'Excellent'
    if mape is not None:
        if mape > 10:
            mape_cls, mape_label = 'poor', 'Needs Improvement'
        elif mape > 7:
            mape_cls, mape_label = 'fair', 'Fair'
        elif mape > 5:
            mape_cls, mape_label = 'good', 'Good'

    r2_value = '-' if r2 is None else f"{r2 * 100:.2f}%"
    rmse_value = '-' if rmse is None else f"{rmse:.4f}"
    mape_value = '-' if mape is None else f"{mape:.2f}%"
    mse_value = '-' if mse is None else f"{mse:.6f}"

    return f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">R&sup2; Score</div>
            <div class="metric-value {r2_cls}">{r2_value}</div>
            <div class="metric-desc">{r2_label}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">RMSE</div>
            <div class="metric-value {rmse_cls}">{rmse_value}</div>
            <div class="metric-desc">{rmse_label}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MAPE</div>
            <div class="metric-value {mape_cls}">{mape_value}</div>
            <div class="metric-desc">{mape_label}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">MSE</div>
            <div class="metric-value">{mse_value}</div>
            <div class="metric-desc">Mean Squared Error</div>
        </div>
    </div>
    """



def _build_table_html(pred_dates, pred_prices, last_price):
    rows = []
    for idx, date in enumerate(pred_dates):
        prev_price = last_price if idx == 0 else pred_prices[idx - 1]
        current_price = pred_prices[idx]
        day_change = current_price - prev_price
        day_change_percent = (day_change / prev_price) * 100 if prev_price != 0 else 0.0
        change_class = 'positive' if day_change >= 0 else 'negative'
        arrow = '^' if day_change >= 0 else 'v'

        rows.append(
            f"<tr>"
            f"<td>{date}</td>"
            f"<td>{_format_rupiah(current_price)}</td>"
            f"<td class='stat-change {change_class}'>{arrow} {_format_rupiah(abs(day_change))}</td>"
            f"<td class='stat-change {change_class}'>{day_change_percent:.2f}%</td>"
            f"</tr>"
        )

    rows_html = ''.join(rows)
    return f"""
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Predicted Price</th>
                    <th>Change</th>
                    <th>% Change</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """



def _build_plot(result, ticker_label):
    try:
        logger.info(f"Building plot for ticker: {ticker_label}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=result['historical']['dates'],
            y=result['historical']['prices'],
            mode='lines',
            name='Actual Price',
            line=dict(color='#2563eb', width=2.5),
        ))
        fig.add_trace(go.Scatter(
            x=result['historical']['dates'],
            y=result['historical']['ma7'],
            mode='lines',
            name='MA 7',
            line=dict(color='#059669', width=1.5, dash='dot'),
            opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=result['historical']['dates'],
            y=result['historical']['ma30'],
            mode='lines',
            name='MA 30',
            line=dict(color='#d97706', width=1.5, dash='dot'),
            opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=result['predictions']['dates'],
            y=result['predictions']['prices'],
            mode='lines+markers',
            name='Prediction',
            line=dict(color='#dc2626', width=3, dash='dash'),
            marker=dict(size=9, color='#dc2626', line=dict(color='#ffffff', width=2)),
        ))

        fig.update_layout(
            title=dict(
                text=f"Price Analysis - {ticker_label}",
                font=dict(size=18, family='Inter', color='#1e293b'),
            ),
            xaxis=dict(title='Date', showgrid=True, gridcolor='#e2e8f0'),
            yaxis=dict(title='Price (IDR)', showgrid=True, gridcolor='#e2e8f0'),
            hovermode='x unified',
            plot_bgcolor='#f8fafc',
            paper_bgcolor='#ffffff',
            height=500,
            margin=dict(l=60, r=40, t=60, b=60),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#e2e8f0',
                borderwidth=1,
            ),
        )
        logger.info(f"Plot built successfully for {ticker_label}")
        return fig
    except Exception as e:
        logger.error(f"Error building plot: {str(e)}")
        logger.error(traceback.format_exc())
        raise



if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None


if submitted:
    try:
        with st.spinner('Processing prediction...'):
            logger.info(f"Form submitted - Ticker: {ticker}, Model: {model_type}, Prediction days: {prediction_days}")
            
            try:
                model = backend.get_or_load_model(ticker, model_type)
                logger.info(f"Model loading attempt for {ticker} ({model_type})")
            except Exception as e:
                logger.error(f"Error loading model for {ticker} ({model_type}): {str(e)}")
                logger.error(traceback.format_exc())
                model = None
            
            if model is None:
                logger.warning(f"Model is None for {ticker} ({model_type}), using mock prediction")
                try:
                    result = backend.generate_mock_prediction(ticker, prediction_days)
                    result['model_type'] = model_type
                    error_text = backend.model_errors.get((ticker, model_type), 'unknown error')
                    result['message'] = (
                        'Using mock prediction because model failed to load: '
                        f'{error_text}'
                    )
                    logger.info(f"Mock prediction generated for {ticker}")
                except Exception as e:
                    logger.error(f"Error generating mock prediction: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"❌ Error generating prediction: {str(e)}")
                    result = None
            else:
                logger.info(f"Model loaded successfully, generating prediction for {ticker}")
                try:
                    result = backend.generate_prediction(ticker, model, model_type, prediction_days)
                    logger.info(f"Prediction generated successfully for {ticker}")
                except Exception as e:
                    logger.error(f"Error generating prediction: {str(e)}")
                    logger.error(traceback.format_exc())
                    st.error(f"❌ Error generating prediction: {str(e)}")
                    result = None
            
            if result:
                st.session_state['last_result'] = {
                    'result': result,
                    'ticker': ticker,
                    'model_type': model_type,
                    'data_period': data_period,
                    'activation': activation,
                    'optimizer': optimizer,
                }
                logger.info(f"Result saved to session state for {ticker}")
            else:
                logger.error("Result is None, prediction failed")
                st.error("❌ Failed to generate prediction. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error in form submission: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"❌ Unexpected error occurred: {str(e)}")
        st.info("💡 Please check the logs/debug information or try again with different parameters.")


state = st.session_state.get('last_result')
if state and state.get('result'):
    try:
        result = state['result']
        ticker_value = state['ticker']
        model_value = state['model_type']
        data_period_value = state['data_period']
        model_label = 'CNN-LSTM' if model_value == 'cnn_lstm' else 'LSTM'

        logger.info(f"Processing results for {ticker_value} with {model_label} model")

        if result.get('model_status') != 'loaded':
            st.markdown(
                f"<div class='alert alert-error'><i class='fas fa-exclamation-circle'></i> {result.get('message', 'Model belum siap, menggunakan prediksi mock.')}</div>",
                unsafe_allow_html=True,
            )
            logger.warning(f"Model status is not 'loaded' for {ticker_value}")
        else:
            st.markdown(
                f"<div class='alert alert-success'><i class='fas fa-check-circle'></i> Prediction for {ticker_value} completed successfully using {model_label} model!</div>",
                unsafe_allow_html=True,
            )
            logger.info(f"Model status OK for {ticker_value}")

        # ====== Fetch Historical Data ======
        logger.info(f"Fetching historical data for {ticker_value}")
        history_df = _ticker_history(ticker_value)
        logger.info(f"Historical data fetched: {len(history_df)} records")
        
        logger.info(f"Slicing history by {data_period_value} months")
        history_df = _slice_history_by_months(history_df, data_period_value)
        logger.info(f"History sliced: {len(history_df)} records")
        
        if history_df.empty:
            logger.error("Historical data is empty after slicing")
            st.error("❌ Dataset error: No data available for selected period")
            st.stop()

        # ====== Process Price Data ======
        logger.info("Processing price data")
        historical_prices = history_df['Close'].astype(float).tolist()
        historical_dates = history_df['Date'].dt.strftime('%Y-%m-%d').tolist()
        logger.info(f"Processed: {len(historical_prices)} prices")

        ma7 = [
            float(np.mean(historical_prices[i - 6:i + 1])) if i >= 6 else None
            for i in range(len(historical_prices))
        ]
        ma30 = [
            float(np.mean(historical_prices[i - 29:i + 1])) if i >= 29 else None
            for i in range(len(historical_prices))
        ]
        logger.info("Moving averages calculated")

        # ====== Calculate Statistics ======
        logger.info("Calculating prediction statistics")
        predictions = result['predictions']['prices']
        last_historical_price = float(historical_prices[-1]) if historical_prices else 0.0
        predicted_final = float(predictions[-1]) if predictions else 0.0
        change = predicted_final - last_historical_price
        change_percent = (change / last_historical_price) * 100 if last_historical_price != 0 else 0.0

        volatility = _compute_historical_stats(historical_prices)

        display_stats = {
            'last_historical_price': last_historical_price,
            'predicted_price': predicted_final,
            'change': change,
            'change_percent': change_percent,
            'min_prediction': float(min(predictions)) if predictions else 0.0,
            'max_prediction': float(max(predictions)) if predictions else 0.0,
            'avg_prediction': float(np.mean(predictions)) if predictions else 0.0,
            'volatility': volatility,
            'data_points': len(historical_prices),
        }
        logger.info(f"Statistics calculated: volatility={volatility:.2f}%")

        change_class = 'positive' if change >= 0 else 'negative'
        change_icon = '^' if change >= 0 else 'v'

        if volatility > 40:
            volatility_class = 'danger'
            volatility_label = 'Very High'
        elif volatility > 30:
            volatility_class = 'warning'
            volatility_label = 'High'
        elif volatility > 20:
            volatility_class = 'warning'
            volatility_label = 'Moderate'
        else:
            volatility_class = 'info'
            volatility_label = 'Low'

        # ====== Render UI ======
        logger.info(f"Rendering UI components for {ticker_value}")
        st.markdown(
            """
            <div class="card">
                <div class="card-header">
                    <h2><i class="fas fa-chart-pie"></i> Prediction Summary</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            _build_stats_html(display_stats, change_class, change_icon, volatility_class, volatility_label),
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">
                <div class="card-header">
                    <h2><i class="fas fa-tasks"></i> Model Evaluation</h2>
                </div>
                <div style="margin-top: 1.5rem;">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(_build_metrics_html(result['metrics']), unsafe_allow_html=True)
        st.markdown(
            """
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        display_result = {
            'historical': {
                'dates': historical_dates,
                'prices': historical_prices,
                'ma7': ma7,
                'ma30': ma30,
            },
            'predictions': result['predictions'],
        }

        logger.info("Building chart")
        fig = _build_plot(display_result, TICKER_LABELS.get(ticker_value, ticker_value))
        
        st.markdown(
            """
            <div class="card">
                <div class="card-header">
                    <h2><i class="fas fa-chart-area"></i> Price Chart</h2>
                </div>
                <div style="margin-top: 1.5rem;">
            """,
            unsafe_allow_html=True,
        )
        
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        })
        
        st.markdown(
            """
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">
                <div class="card-header">
                    <h2><i class="fas fa-table"></i> Daily Prediction Details</h2>
                </div>
                <div style="margin-top: 1.5rem;">
            """,
            unsafe_allow_html=True,
        )

        logger.info("Generating prediction table")
        st.markdown(
            _build_table_html(result['predictions']['dates'], result['predictions']['prices'], last_historical_price),
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            </div>
        </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<p class='section-caption'>Activation: {activation} | Optimizer: {optimizer} | Data period: {data_period_value} months</p>",
            unsafe_allow_html=True,
        )

        logger.info("Preparing CSV download")
        pred_table = pd.DataFrame({
            'Date': result['predictions']['dates'],
            'Prediction': result['predictions']['prices'],
        })
        csv_bytes = pred_table.to_csv(index=False).encode('utf-8')
        st.download_button(
            'Download CSV Prediksi',
            data=csv_bytes,
            file_name=f'prediksi_{ticker_value}_{model_value}.csv',
            mime='text/csv',
        )
        logger.info(f"Successfully rendered all components for {ticker_value}")
    except Exception as e:
        logger.error(f"Error processing results: {str(e)}")
        logger.error(traceback.format_exc())
        st.error(f"❌ Error processing results: {str(e)}")
        st.info("💡 Please try running the prediction again.")
else:
    logger.info("No prediction result yet, showing info message")
    st.markdown(
        """
        <div class="alert alert-success">
            <i class="fas fa-info-circle"></i> Pilih konfigurasi model lalu klik Run Prediction untuk melihat hasil.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Stock Prediction System - CNN-LSTM</p>
            <p>Professional Trading & Analysis Tool | For Educational & Research Purposes</p>
        </div>
    </footer>
    """,
    unsafe_allow_html=True,
)
