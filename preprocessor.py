from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import pandas as pd
import streamlit as st


# Load the data once outside the functions
DATA = "Data/new/loan-train.csv"
df = pd.read_csv(DATA)
# st.dataframe(df.head())

df['Dependents'].astype(str)

column_names_ = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
min_max_cols = ['Loan_Amount_Term']
Label_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents']

column_names =  df.columns[1:-1]
# st.write(column_names)
# Create an instance of StandardScaler
scaler = StandardScaler()
minax = MinMaxScaler()
label_encoders={}



   
num_scaler = scaler.fit(df[column_names_])
minmax_scaler = minax.fit(df[min_max_cols])
for i in Label_cols:
    encoders = LabelEncoder().fit(df[i])
    label_encoders[i] = encoders    

# st.write("label_encoders: ", label_encoders)