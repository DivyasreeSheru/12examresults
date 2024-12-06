# FRONTEND WORKING CODE

import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

# Function to generate an image with the prediction report
def generate_image(values, result, name):
    img = Image.new('RGB', (600, 800), color=(255, 255, 255))  
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arialbd.ttf", 18)
        large_font = ImageFont.truetype("arialbd.ttf", 50)
    except:
        font = ImageFont.load_default()
        large_font = ImageFont.load_default()

    heart_color = (255, 182, 193)
    heart_points = [(300, 220), (350, 170), (400, 220), (400, 280), (300, 380), (200, 280), (200, 220)]
    d.polygon(heart_points, fill=heart_color)

    title_text = "Heart Disease Prediction Report"
    underline_text = "-" * 50
    title_bbox = d.textbbox((0, 0), title_text, font=font)
    underline_bbox = d.textbbox((0, 0), underline_text, font=font)
    title_x = (img.width - (title_bbox[2] - title_bbox[0])) // 2
    underline_x = (img.width - (underline_bbox[2] - underline_bbox[0])) // 2
    d.text((title_x, 100), title_text, font=font, fill=(0, 0, 0))
    d.text((underline_x, 130), underline_text, font=font, fill=(0, 0, 0))

    y_text = 160
    for key, value in values.items():
        d.text((10, y_text), f"{key}: {value}", font=font, fill=(0, 0, 0))
        y_text += 30
    d.text((10, y_text), f"Result: {result}", font=font, fill=(0, 0, 0))

    now = datetime.now()
    d.text((10, y_text + 40), f"Date: {now.strftime('%Y-%m-%d')}", font=font, fill=(0, 0, 0))
    d.text((10, y_text + 70), f"Time: {now.strftime('%H:%M:%S')}", font=font, fill=(0, 0, 0))
    d.text((10, y_text + 100), f"Report Generated by: {name}", font=font, fill=(0, 0, 0))

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return img_buffer

# Login function
def login(username, password):
    return username == "heartdisease" and password == "heart@123"

# Main app function
def main():
    st.title("Heart Disease Prediction")

    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://img.freepik.com/premium-photo/blur-short-white-hospital-walkway-background_7180-2422.jpg');
            background-size: cover;
            background-attachment: fixed;
            color: black;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for navigation
    option = st.sidebar.selectbox("Select a page:", ["Home", "Heart Disease Prediction", "About", "Logout"])

    if option == "Logout":
        st.session_state.logged_in = False
        st.experimental_set_query_params(page="Home")
        st.success("Logged out successfully.")
        return

    if option == "Home":
        st.image("https://cdn.pixabay.com/photo/2023/09/05/08/02/earth-8234588_1280.jpg", caption="Heart Health Matters")
        
        st.write(""" 
        ### Overview 
        This app uses machine learning models to predict the risk of heart disease based on several health metrics. It allows you to upload patient data, generate predictions, and provides a detailed report.

        ### Features:
        - Predicts heart disease based on various health metrics.
        - Supports multiple machine learning models for better accuracy.
        - Allows CSV data upload for bulk predictions.
        - Generates a customized report with results.

        ### Understanding Heart Disease Risk 
        Heart disease refers to several types of heart conditions, with coronary artery disease being the most common. Factors like high blood pressure, high cholesterol, smoking, and obesity significantly increase the risk of heart disease. Family history, age, and gender also play a role.

        **Risk Factors:**
        - High blood pressure and cholesterol
        - Smoking
        - Lack of physical activity
        - Poor diet and excessive alcohol
        - Obesity
        - Diabetes

        ### Protecting Your Heart:
        1. **Exercise Regularly**: Aim for at least 30 minutes of moderate exercise most days of the week.
        2. **Eat a Healthy Diet**: Include more fruits, vegetables, whole grains, and healthy fats like omega-3 fatty acids.
        3. **Quit Smoking**: Smoking is one of the leading causes of heart disease. Quitting helps improve heart health rapidly.
        4. **Manage Stress**: Chronic stress can raise blood pressure. Practice relaxation techniques like meditation or yoga.
        5. **Regular Health Check-ups**: Get regular screenings for blood pressure, cholesterol, and diabetes.
        6. **Maintain a Healthy Weight**: Reducing obesity reduces the risk of heart disease significantly.
        """)
    
        st.info("Login with **username**: `heartdisease` and **password**: `heart@123` to start using the app.")

    elif option == "Heart Disease Prediction":
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            st.subheader("Login to Continue")
            username = st.text_input("Username", placeholder="Enter Username")
            password = st.text_input("Password", type="password", placeholder="Enter Password")

            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.success("Logged in successfully!")
                else:
                    st.error("❌ Invalid credentials")
        else:
            st.subheader("CSV file")
            
            # "Back to Home" button
            if st.button("Back"):
                st.experimental_set_query_params(page="Home")
                return

            if "uploaded_file" not in st.session_state:
                uploaded_file = st.file_uploader("CSV file", type=["csv"])

                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.session_state.df = df  # Store the data in session state
                        st.session_state.uploaded_file = uploaded_file
                    except Exception as e:
                        st.error(f"Error reading the file: {e}")
                        return
                else:
                    st.warning("Please upload a CSV file to continue.")
                    return

            df = st.session_state.df  # Use the data from session state

            st.subheader("Enter Patient Details")
            name = st.text_input("Patient Name", placeholder="Enter patient's full name") 
            age = st.number_input("Age", min_value=1, max_value=100)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp = st.number_input("Chest Pain Type (cp)", min_value=0.0, max_value=5.0)
            trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=94.0, max_value=200.0)
            chol = st.number_input("Serum Cholesterol (chol)", min_value=126.0, max_value=417.0)
            fbs = st.number_input("Fasting Blood Sugar (fbs)", min_value=0.0, max_value=3.0)
            restecg = st.number_input("Resting ECG (restecg)", min_value=0.0, max_value=2.0)
            thalach = st.number_input("Max Heart Rate (thalach)", min_value=71.0, max_value=192.0)
            exang = st.number_input("Exercise Induced Angina (exang)", min_value=0.0, max_value=1.0)
            oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=5.6)
            slope = st.number_input("Slope of Peak Exercise (slope)", min_value=0.0, max_value=2.0)
            ca = st.number_input("Major Vessels (ca)", min_value=0.0, max_value=4.0)
            thal = st.number_input("Thalassemia (thal)", min_value=1.0, max_value=3.0)

            if not name.strip():
                st.error("❌ Please enter the patient's name.")
                return

            filtered_data = df[(df['age'] == age) & 
                               (df['sex'] == (1 if sex == "Male" else 0)) & 
                               (df['cp'] == cp)]
            if not filtered_data.empty:
                extra_trees_pred = filtered_data['Extra Trees Pred Target'].values[0]

                if st.button("Submit"):
                    result = "❤️ Heart disease predicted, Please consult a Cardiologist" if extra_trees_pred >= 0.5 else "💪 Person is healthy "
                    st.success(result)

                    values = {
                        "Name": name, 
                        "Age": age,
                        "Sex": sex,
                        "Chest Pain Type (cp)": cp,
                        "Resting Blood Pressure (trestbps)": trestbps,
                        "Serum Cholesterol (chol)": chol,
                        "Fasting Blood Sugar (fbs)": fbs,
                        "Resting ECG (restecg)": restecg,
                        "Max Heart Rate (thalach)": thalach,
                        "Exercise Induced Angina (exang)": exang,
                        "ST Depression (oldpeak)": oldpeak,
                        "Slope of Peak Exercise (slope)": slope,
                        "Major Vessels (ca)": ca,
                        "Thalassemia (thal)": thal
                    }
                    report_image = generate_image(values, result, "ML")
                    st.image(report_image, caption='Heart Disease Prediction Report', use_column_width=True)

                    # Add a download button for the report
                    st.download_button(
                        label="Download Report",
                        data=report_image,
                        file_name='heart_disease_prediction_report.png',
                        mime='image/png'
                    )
            else:
                st.error("❌ No matching data found for the entered values.")

    elif option == "About":
        st.header("About the App")
        st.write(""" 
        This Heart Disease Prediction app uses machine learning models to predict the possibility of heart disease based on various health metrics.
        - Log in with username - heartdisease and Password - heart@123
        - Upload the patient's data once.
        - The app uses Extra Trees Classifier to generate predictions.
        - Get the patient's report.
        """)
  
# Run the main function
if __name__ == "__main__":
    main()
