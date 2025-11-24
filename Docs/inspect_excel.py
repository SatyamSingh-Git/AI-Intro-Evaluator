import pandas as pd

try:
    df = pd.read_excel('Case study for interns.xlsx')
    print("Columns:", df.columns.tolist())
    
    print("\n--- Searching for instructions in the Excel file ---")
    for col in df.columns:
        for idx, val in df[col].items():
            if isinstance(val, str) and len(val) > 20:
                print(f"\n[Row {idx}, Col {col}]:")
                print(val)
                
except Exception as e:
    print(f"Error: {e}")

