import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

import app as backend


st.set_page_config(
    page_title='Stock Price Prediction',
    layout='wide',
)


def _format_number(value, suffix=''):
    if value is None:
        return '-'
    try:
        return f'{value:,.2f}{suffix}'
    except Exception:
        return f'{value}{suffix}'


@st.cache_data(show_spinner=False)
def _load_dataset():
    return backend.load_historical_dataset().copy()


def _build_chart_frame(result):
    hist = result['historical']
    pred = result['predictions']

    hist_df = pd.DataFrame({
        'Date': pd.to_datetime(hist['dates']),
        'Historical': hist['prices'],
        'MA 7': hist.get('ma7', []),
        'MA 30': hist.get('ma30', []),
    }).set_index('Date')

    pred_df = pd.DataFrame({
        'Date': pd.to_datetime(pred['dates']),
        'Prediction': pred['prices'],
    }).set_index('Date')

    return hist_df.join(pred_df, how='outer')


st.title('Stock Price Prediction')
st.write(
    'Dashboard ini menjalankan model CNN-LSTM dan LSTM untuk prediksi harga saham '
    'transportasi berdasarkan data historis.'
)


with st.sidebar:
    st.header('Konfigurasi')
    ticker = st.selectbox('Kode saham', backend.TICKERS)
    model_label = st.selectbox(
        'Tipe model',
        ['CNN-LSTM (Hybrid)', 'LSTM (Standalone)'],
    )
    model_type = 'cnn_lstm' if model_label.startswith('CNN') else 'lstm'
    prediction_days = st.slider('Jumlah hari prediksi', 1, 30, 5)
    run_prediction = st.button('Jalankan Prediksi', type='primary')


try:
    dataset = _load_dataset()
    last_date = pd.to_datetime(dataset['Date']).max()
    st.caption(
        f'Data terakhir: {last_date:%Y-%m-%d} | Total baris: {len(dataset):,}'
    )
except Exception as exc:
    st.error(f'Dataset gagal dimuat: {exc}')
    st.stop()


model_path = backend.get_model_path(ticker, model_type)
model_exists = os.path.exists(model_path)
model_status = 'Ada' if model_exists else 'Tidak ditemukan'
st.caption(f'Status model file: {model_status} ({os.path.basename(model_path)})')

model_error = backend.model_errors.get((ticker, model_type))
if model_error:
    st.warning(f'Catatan model: {model_error}')


if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None

if run_prediction:
    with st.spinner('Menjalankan prediksi...'):
        model = backend.get_or_load_model(ticker, model_type)
        if model is None:
            result = backend.generate_mock_prediction(ticker, prediction_days)
            result['model_type'] = model_type
            error_text = backend.model_errors.get((ticker, model_type), 'unknown error')
            result['message'] = (
                'Using mock prediction because model failed to load: '
                f'{error_text}'
            )
        else:
            result = backend.generate_prediction(ticker, model, model_type, prediction_days)

    st.session_state['last_result'] = result


result = st.session_state.get('last_result')
if result:
    if result.get('model_status') != 'loaded':
        st.warning(result.get('message', 'Model belum siap, menggunakan prediksi mock.'))

    stats = result['statistics']
    metrics = result['metrics']

    st.subheader('Ringkasan')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Harga terakhir', _format_number(stats['last_historical_price']))
    col2.metric('Prediksi akhir', _format_number(stats['predicted_price']))
    change_delta = f"{stats['change_percent']:.2f}%"
    col3.metric('Perubahan', _format_number(stats['change']), change_delta)
    col4.metric('Volatilitas', _format_number(stats['volatility'], '%'))

    st.subheader('Grafik Harga')
    chart_df = _build_chart_frame(result)
    st.line_chart(chart_df, height=420)

    st.subheader('Prediksi Harian')
    pred_table = pd.DataFrame({
        'Tanggal': result['predictions']['dates'],
        'Prediksi': result['predictions']['prices'],
    })
    st.dataframe(pred_table, hide_index=True, use_container_width=True)

    st.subheader('Evaluasi Model')
    metrics_table = pd.DataFrame({
        'Metric': ['RMSE', 'R2', 'MAPE', 'MSE'],
        'Value': [
            metrics.get('rmse'),
            metrics.get('r2'),
            metrics.get('mape'),
            metrics.get('mse'),
        ],
    })
    st.dataframe(metrics_table, hide_index=True, use_container_width=True)

    csv_bytes = pred_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        'Download CSV Prediksi',
        data=csv_bytes,
        file_name=f'prediksi_{ticker}_{model_type}.csv',
        mime='text/csv',
    )
