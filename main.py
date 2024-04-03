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
from preprocessor import num_scaler, minmax_scaler, label_encoders, column_names, column_names_, min_max_cols, Label_cols

MODEL = "loan_classifier_rf.pkl"

# Load the model once outside the functions
with open(MODEL, "rb") as f:
    model = pickle.load(f)

def input_form():
    # col1, col2 = st.columns(2)

    with st.form("loan_form"):
        
        st.markdown("### Personal Information")
        st.write("Let's start with some personal details")
        name = st.text_input("Name")
        gender = st.selectbox("Select your Gender", ['Male', 'Female'])
        email = st.text_input("Email to receive your loan status")
        dependants = st.slider("Number of dependants", min_value=0, max_value=15, value=0, step=1)
        employment = st.selectbox("Are you self employed?", ["Yes", "No"])
        income = st.number_input("Yearly Income", min_value=0, value=0, step=100)
        co_income = st.number_input("Co-Applicant's Yearly Income (if no co-applicant, leave at 0)", min_value=0, value=0, step=100)
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        married = st.selectbox("Are you married?", ["Yes", "No"])
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])


        
        st.markdown("---------")
        st.markdown("### Loan Information")
        st.write("Now let's talk about the loan")
        loan_amount = st.number_input("How much are you looking for?", min_value=0, value=0, step=100)
        loan_term = st.select_slider("Loan Term (in Month)", options=[12, 36, 60, 84, 120, 180, 240, 300, 360, 480])
        credit_score = st.selectbox("Credit Score", ["Good","Poor"])
        st.markdown("---------")

        submit = st.form_submit_button("Submit")

    if submit:
        if any([name == "",email == "", employment == "", income == 0, education == "",
                 loan_amount == 0, loan_term == 0,]):
            st.warning("Please fill all the fields")
            return None
        if dependants >= 3:
            dependants = '3+'
        else:
            dependants = str(dependants)
       
       
        st.session_state['name'] = name
        st.session_state['email'] = email
        data = [gender, married, dependants, education, employment, income, co_income, loan_amount, loan_term, credit_score, property_area]
        
        return data
def preprocess(data):
    # Use the appropriate column names based on the model training data
    
    # data_mapping = {"Yes": 1, "No": 0, "Graduate": 0, "Not Graduate": 1}   
    # for i in [2, 1]:
    #     data[i] = data_mapping.get(data[i], data[i])


    df = pd.DataFrame(np.array(data).reshape(1, -1), columns=column_names)
    df['Dependents'] = df['Dependents'].astype(object)
    for i in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']:
        df[i] = df[i].astype(float)
        df[i] = df[i]/1000

    credit_score_mapping = {"Good": 1, "Poor": 0}
    df['Credit_History'] = credit_score_mapping.get(df['Credit_History'].values[0], df['Credit_History'].values[0])

    df[column_names_] = num_scaler.transform(df[column_names_])
    df[min_max_cols] = minmax_scaler.transform(df[min_max_cols])
    for i in Label_cols:
        df[i] = label_encoders[i].transform(df[i])


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
        # st.write(prediction)
        if prediction == 1:
            
            st.write(f"Dear {st.session_state['name']}:  Congratulations, your loan Application has been Aprroved")
            smtp_mail("Approved")
        else:
            st.write(f"Dear {st.session_state['name']}:  Sorry, your loan Application has been Rejected")
            smtp_mail("Rejected")
        

if __name__ == "__main__":
    main()

