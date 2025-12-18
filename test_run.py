import sys
print("Testing imports...")
try:
    import streamlit as st
    print("✓ Streamlit imported")
    
    from diabetes_prediction import DiabetesPredictor, download_dataset
    print("✓ diabetes_prediction imported")
    
    print("\nAll imports successful!")
    print("\nTo run the app, use:")
    print("python -m streamlit run app.py")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
















