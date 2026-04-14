"""
Convert Keras models from .keras format to .h5 format for compatibility
"""
import os
import sys
import json
import zipfile
import tempfile
import shutil
from pathlib import Path

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
H5_MODELS_DIR = os.path.join(BASE_DIR, 'models_h5')

# Create output directory
os.makedirs(os.path.join(H5_MODELS_DIR, 'lstm'), exist_ok=True)
os.makedirs(os.path.join(H5_MODELS_DIR, 'cnn_lstm'), exist_ok=True)

TICKERS = ['BIRD.JK', 'BPTR.JK', 'GIAA.JK', 'LRNA.JK', 'PURA.JK', 'TAXI.JK']
MODEL_TYPES = ['lstm', 'cnn_lstm']

def fix_keras_config(model_path):
    """Fix batch_shape compatibility issue in keras model"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract keras file
            with zipfile.ZipFile(model_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Fix config.json
            config_path = os.path.join(temp_dir, 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                def fix_config_recursive(obj):
                    if isinstance(obj, dict):
                        if 'batch_shape' in obj:
                            batch_shape = obj.pop('batch_shape')
                            if batch_shape and len(batch_shape) > 1:
                                obj['input_shape'] = batch_shape[1:]
                        obj.pop('optional', None)
                        for v in obj.values():
                            fix_config_recursive(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            fix_config_recursive(item)
                
                fix_config_recursive(config)
                
                with open(config_path, 'w') as f:
                    json.dump(config, f)
            
            # Recreate keras file
            fixed_keras = os.path.join(temp_dir, 'fixed_model.keras')
            shutil.make_archive(fixed_keras.replace('.keras', ''), 'zip', temp_dir)
            
            with open(fixed_keras + '.zip', 'rb') as f:
                return f.read()
    except Exception as e:
        print(f"  ⚠ Fix attempt failed: {e}")
        return None

def load_model_safe(model_path):
    """Load model with compatibility fixes"""
    try:
        # Try direct load
        return load_model(model_path, compile=False)
    except Exception as e:
        if "batch_shape" in str(e) or "optional" in str(e):
            print(f"  Applying compatibility fix...")
            fixed_content = fix_keras_config(model_path)
            if fixed_content:
                with tempfile.NamedTemporaryFile(suffix='.keras', delete=False) as tmp:
                    tmp.write(fixed_content)
                    tmp_path = tmp.name
                try:
                    model = load_model(tmp_path, compile=False)
                    os.unlink(tmp_path)
                    return model
                except Exception as inner_e:
                    os.unlink(tmp_path)
                    raise inner_e
        raise e

print("\n" + "="*70)
print("🔄 STARTING MODEL CONVERSION (.keras → .h5)")
print("="*70 + "\n")

total = len(TICKERS) * len(MODEL_TYPES)
converted = 0
failed = 0

for model_type in MODEL_TYPES:
    print(f"\n📦 Converting {model_type.upper()} models:")
    print("-" * 70)
    
    for ticker in TICKERS:
        keras_path = os.path.join(MODELS_DIR, model_type, f'{ticker}_{model_type}.keras')
        h5_path = os.path.join(H5_MODELS_DIR, model_type, f'{ticker}_{model_type}.h5')
        
        if not os.path.exists(keras_path):
            print(f"  ✗ {ticker:10} - File not found")
            failed += 1
            continue
        
        try:
            print(f"  ⏳ {ticker:10} - Loading keras model...", end='', flush=True)
            model = load_model_safe(keras_path)
            print(" ✓ Loaded", end='', flush=True)
            
            print(" - Saving to H5...", end='', flush=True)
            model.save(h5_path)
            print(" ✓")
            converted += 1
            
            # Verify
            file_size_kb = os.path.getsize(h5_path) / 1024
            print(f"            → Saved: {file_size_kb:.1f} KB")
            
        except Exception as e:
            print(f" ✗ Error: {str(e)[:50]}")
            failed += 1

print("\n" + "="*70)
print("✅ CONVERSION SUMMARY")
print("="*70)
print(f"✓ Successfully converted: {converted}/{total}")
print(f"✗ Failed: {failed}/{total}")
print(f"📁 Output directory: {H5_MODELS_DIR}")
print("="*70 + "\n")

if failed == 0:
    print("🎉 All models converted successfully!")
    print("\nNext steps:")
    print("  1. Update app.py to use H5 models")
    print("  2. Replace old .keras files with new .h5 files")
    print("  3. Restart the Flask server")
else:
    print(f"⚠ {failed} models failed to convert. Check the errors above.")
    sys.exit(1)
