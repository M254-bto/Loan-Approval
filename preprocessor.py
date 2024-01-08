from sklearn.preprocessing import StandardScaler
import pandas as pd


# Load the data once outside the functions
DATA = "Data/loan_approval_dataset.csv"
df = pd.read_csv(DATA)

column_names_ = ['no_of_dependents', 'income_annum',
                     'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
                     'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']

df.rename(columns=lambda x: x.strip(), inplace=True)
column_names =  df.columns[1:-1]

# Create an instance of StandardScaler
scaler = StandardScaler()
   
num_scaler = scaler.fit(df[column_names_])

