import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, MinMaxScaler

MODEL = "model.pkl"
SCALER = StandardScaler()
MINMAX = MinMaxScaler()

st.title("Loan Approval Prediction App")
st.write("This app predicts **Loan Approval** using **Machine Learning**")



def input_form():
    with st.form("loan_form"):
        st.markdown("### Personal Information")
        st.write("Let's start with some personal details")
        name = st.text_input("Name")
        dependants = st.slider("Number of dependants", min_value=0, max_value=15, value=0, step=1)
        employment = st.selectbox("Are you self employed?", ["Yes", "No"])
        income = st.number_input("Yearly Income", min_value=0, value=0, step=100)
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])

        st.markdown("---------")

        st.markdown("### Assets Information") 
        st.write("Now let's talk about your assets")
        residence = st.number_input("Total value of residential property", min_value=0, value=0, step=100)
        commercial = st.number_input("Total value of commercial property", min_value=0, value=0, step=100)
        luxery = st.number_input("Total value of luxery property", min_value=0, value=0, step=100)
        bank = st.number_input("Total value of Assets in the Bank", min_value=0, value=0, step=100)

        st.markdown("---------")
        st.markdown("### Loan Information")
        st.write("Now let's talk about the loan")
        loan_amount = st.number_input("How much are you looking for?", min_value=0, value=0, step=100)
        loan_term = st.number_input("In how many years do you want to pay it?", min_value=0, max_value=30, value=0, step=1)
        credit_score = st.number_input("Credit Score", min_value=0, max_value=1000, value=0, step=1)
        st.markdown("---------")

        submit = st.form_submit_button("Submit")

    if submit:
        if any([name == "", dependants == 0, employment == "", income == 0, education == "",
                residence == 0, commercial == 0, loan_amount == 0, loan_term == 0, credit_score == 0, bank == 0]):
            st.warning("Please fill all the fields")
            return None
        
        data = [dependants, education, employment, income, loan_amount, loan_term, credit_score, residence, commercial, luxery, bank]
        # numerical = [dependants, income, residence, commercial, loan_amount, loan_term, credit_score, luxery, bank]
        # min_max = [dependants, loan_term]
        # categorical = [employment, education]
        return data

#function for form data preprocessing
# def preprocess(data):
#     numerical, categorical, min_max = data
#     numerical_2d = np.array(numerical).reshape(1, -1)
#     numerical_scaled = SCALER.fit_transform(numerical_2d)
#     numerical_rounded = np.round(numerical_scaled[0], 2)
#     return numerical_rounded

def predict(data):
    data_mapping = {"Yes": 1, "No": 0, "Graduate": 1, "Not Graduate": 0}
    print(data)
    data[2] = data_mapping.get(data[2], data[2])
    data[1] = data_mapping.get(data[1], data[1])
    df = pd.DataFrame(np.array(data).reshape(1, -1), columns=['no_of_dependents', 'education', 'self_employed', 'income_annum',
       'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
       'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'])
    print(df)
    with open(MODEL, "rb") as f:

        model = pickle.load(f)
    prediction = model.predict(df)
    predictio_map = {1: "Approved", 0: "Rejected"}
    prediction = predictio_map.get(prediction[0], prediction[0])
    return prediction

def main():
    st.write("You are here to find out if you are eligible for a loan")
    st.write("Please fill the form below")
    data = input_form()
    if data is not None:
        st.write("Form submitted successfully!")
        st.write("Numerical Data:", data)
        st.write("Categorical Data:", data[1])
        st.write("prediction:", predict(data))

if __name__ == "__main__":
    main()
  