import streamlit as st
import pandas as pd
import numpy as np
import pickle



st.title("Loan Approval Prediction App")
st.write("This app predicts **Loan Approval** using **Machine Learning**")

MODEL = "model.pkl"

def input_form():
    with st.form("loan_form"):
        st.markdown("### Personal Information")
        st.write("Let's start with some personal details")
        name = st.text_input("Name")
        dependants = st.slider("Number of dependants", min_value=0, max_value=15, value=0, step=1)
        employment = st.selectbox("Employment", ["Unemployed", "Self Employed", "Employed"])
        income = st.number_input("Applicant Income", min_value=0, value=0, step=100)
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])

        st.markdown("---------")

        st.markdown("### Assets Information") 
        st.write("Now let's talk about your assets")
        residence = st.number_input("Total cost of residential property", min_value=0, value=0, step=100)
        commercial = st.number_input("Total cost of commercial property", min_value=0, value=0, step=100)

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
                residence == 0, commercial == 0, loan_amount == 0, loan_term == 0, credit_score == 0]):
            st.warning("Please fill all the fields")
            return None
        numerical = [dependants, income, residence, commercial, loan_amount, loan_term, credit_score]
        categorical = [employment, education]
        return numerical, categorical
    

def predict(data):
    with open(MODEL, "rb") as f:
        model = pickle.load(f)
    prediction = model.predict(data)
    return prediction

def main():
    st.write("You are here to find out if you are eligible for a loan")
    st.write("Please fill the form below")
    data = input_form()
    if data is not None:
        st.write("Form submitted successfully!")
        st.write("Numerical Data:", data[0])
        st.write("Categorical Data:", data[1])

if __name__ == "__main__":
    main()
