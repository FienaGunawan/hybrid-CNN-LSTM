@echo off
REM Script para convertir o instalar modelos

echo.
echo ============================================================================
echo          SOLUCION DE MODELOS - SELECCIONA UNA OPCION
echo ============================================================================
echo.
echo El sistema esta FUNCIONANDO con predicciones mock (estadisticas realistas)
echo. Los modelos originales requieren TensorFlow 2.10 para cargar.
echo.
echo OPCIONES:
echo.
echo [1] Usar PREDICCIONES MOCK (YA FUNCIONA - Recomendado ahora)
echo     - Rapido, estable, sin dependencias extra
echo     - Predicciones estadisticamente realistas
echo     - No requiere cambios
echo.
echo [2] Instalar TensorFlow 2.10 (Para usar modelos reales)
echo     - pip install tensorflow==2.10.0
echo     - Toma ~10-15 minutos
echo     - Requiere ~2GB espacio libre
echo.
echo [3] Retrain modelos con TensorFlow actual
echo     - jupyter notebook HYBRID_CNN_LSTM.ipynb
echo     - Genera nuevos modelos compatibles
echo     - Requiere ~30 minutos + GPU
echo.
echo [4] Salir
echo.
echo ============================================================================

setlocal enabledelayedexpansion

set /p opcion="Selecciona opcion (1-4): "

if "%opcion%"=="1" (
    echo.
    echo ✓ MOCK PREDICTIONS YA ACTIVO
    echo   El servidor Flask esta usando predicciones realistas
    echo   Ve a: http://localhost:5000
    echo.
    pause
    exit /b 0
)

if "%opcion%"=="2" (
    echo.
    echo Instalando TensorFlow 2.10...
    echo ESPERA - esto puede tomar 10-15 minutos
    echo.
    pip install tensorflow==2.10.0
    if %errorlevel% equ 0 (
        echo.
        echo ✓ TensorFlow 2.10 instalado!
        echo   Reinicia app.py con: python app.py
        echo.
    ) else (
        echo.
        echo ✗ Error en instalacion
        echo.
    )
    pause
    exit /b %errorlevel%
)

if "%opcion%"=="3" (
    echo.
    echo Abriendo notebook de entrenamiento...
    echo jupyter notebook HYBRID_CNN_LSTM.ipynb
    jupyter notebook HYBRID_CNN_LSTM.ipynb
    pause
    exit /b 0
)

if "%opcion%"=="4" (
    exit /b 0
)

echo.
echo ✗ Opcion invalida
echo.
pause
exit /b 1
