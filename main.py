import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from preprocessor import num_scaler

MODEL = "model2.pkl"

# Load the model once outside the functions
with open(MODEL, "rb") as f:
    model = pickle.load(f)

def input_form():
    with st.form("loan_form"):
        st.markdown("### Personal Information")
        st.write("Let's start with some personal details")
        name = st.text_input("Name")
        email = st.text_input("Email to receive your loan status")
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
        if any([name == "",email == "", dependants == 0, employment == "", income == 0, education == "",
                residence == 0, commercial == 0, loan_amount == 0, loan_term == 0, credit_score == 0, bank == 0]):
            st.warning("Please fill all the fields")
            return None
        st.session_state['name'] = name
        st.session_state['email'] = email
        data = [dependants, education, employment, income, loan_amount, loan_term, credit_score, residence, commercial, luxery, bank]
        
        return data
def preprocess(data):
    # Use the appropriate column names based on the model training data
    column_names = ['no_of_dependents', 'education', 'self_employed', 'income_annum',
                     'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
                     'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']
    
    column_names_ = ['no_of_dependents', 'income_annum',
                     'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
                     'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']
    
    data_mapping = {"Yes": 1, "No": 0, "Graduate": 0, "Not Graduate": 1}   
    for i in [2, 1]:
        data[i] = data_mapping.get(data[i], data[i])


    df = pd.DataFrame(np.array(data).reshape(1, -1), columns=column_names)
    df[column_names_] = num_scaler.transform(df[column_names_])

    return df

def predict(data):
    scaler_data = preprocess(data)
    
    # Use the model to make predictions
    prediction = model.predict(scaler_data)
        
    return prediction

def smtp_mail(prediction):
    
    email_sender = 'ngechamike26@gmail.com'
    email_receiver = st.session_state['email']
    subject = 'Loan Application Status'
    body = 'Dear '+st.session_state['name']+',\n\nYour loan application has been ' + prediction + '.\n\nRegards,\n\nLoan Application Team'
    password = 'vvct jwfp kjlq mdvq' 


    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Error sending email : {e}")



def main():
    st.write("You are here to find out if you are eligible for a loan")
    st.write("Please fill the form below")
    data = input_form()
    # st.write(data)
    if data is not None:
        st.success("Form submitted successfully!")
        # st.write("Input Data:", data)
        prediction = predict(data)
        if prediction == 0:
            
            st.write(f"Dear {st.session_state['name']}:  Congratulations, your loan Application has been Aprroved")
            smtp_mail("Approved")
        else:
            st.write(f"Dear {st.session_state['name']}:  Sorry, your loan Application has been Rejected")
            smtp_mail("Rejected")
        

if __name__ == "__main__":
    main()

