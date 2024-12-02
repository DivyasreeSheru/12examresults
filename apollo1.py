import streamlit as st
import requests

# Main app function
def main():
    st.title("Heart Disease Prediction")

    st.subheader("Upload Patient Data")

    # User input for patient details
    name = st.text_input("Patient Name", placeholder="Enter patient's full name")
    age = st.number_input("Age", min_value=1, max_value=100)
    sex = st.selectbox("Sex", ["Male", "Female"])
    cp = st.number_input("Chest Pain Type (cp)", min_value=0, max_value=5)
    trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=94, max_value=200)
    chol = st.number_input("Serum Cholesterol (chol)", min_value=126, max_value=417)
    fbs = st.number_input("Fasting Blood Sugar (fbs)", min_value=0, max_value=1)
    restecg = st.number_input("Resting ECG (restecg)", min_value=0, max_value=2)
    thalach = st.number_input("Max Heart Rate (thalach)", min_value=71, max_value=202)
    exang = st.number_input("Exercise Induced Angina (exang)", min_value=0, max_value=1)
    oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=6.0)
    slope = st.number_input("Slope of Peak Exercise (slope)", min_value=0, max_value=2)
    ca = st.number_input("Major Vessels (ca)", min_value=0, max_value=4)
    thal = st.number_input("Thalassemia (thal)", min_value=1, max_value=3)

    if st.button("Submit"):
        # Prepare data for the API call
        patient_data = {
            "age": age,
            "sex": 1 if sex == "Male" else 0,  # Convert to binary
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal
        }

        # Send data to the backend API
        response = requests.post('http://localhost:5000/predict', json=patient_data)

        if response.status_code == 200:
            predictions = response.json()
            st.success("Predictions received!")
            st.write(f"**Extra Trees Prediction**: {'Sick' if predictions['Extra Trees Prediction'] == 1 else 'Not Sick'}")
        else:
            st.error("❌ Error in prediction request.")

if __name__ == "__main__":
    main()
