import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

st.set_page_config(page_title="Smart Unit Converter", layout="wide")

# add css
st.markdown("""
    <style>
        @keyframes gradientAnimation {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .main {
            background: linear-gradient(-45deg, #FFDEE9, #B5FFFC, #C2FFD8, #FFF6B7);
            background-size: 400% 400%;
            animation: gradientAnimation 10s ease infinite;
        }
        
        h1 {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ff6ec4, #7873f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 1.5s infinite alternate;
        }
        
        @keyframes glow {
            from {text-shadow: 0 0 10px #ff6ec4;}
            to {text-shadow: 0 0 20px #7873f5;}
        }


        .explanation-box {
            background-color: #f0f8ff;
            border-left: 6px solid #007bff;
            padding: 15px;
            border-radius: 5px;
            font-family: Arial, sans-serif;
            font-size: 16px;
            color: #333;
            line-height: 1.5;
        }

         .input-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-direction:row
        }
        .input-container div {
            width: 45%;
        }
        .stSelectbox, .stNumberInput {
            border: 2px solid rgb(215, 97, 197);
            border-radius: 8px;
            padding: 5px;
            font-size: 16px;
        }


        
        .stButton>button {
            background-color: #ff6ec4;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px 20px;
            transition: 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #7873f5;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1>UnitPro_Professional unit conversions with history & export</h1>', unsafe_allow_html=True)
st.markdown("<br><br>" , unsafe_allow_html=True)


import streamlit as st

unit_categories = {
    "Length": ["Meter", "Kilometer", "Mile", "Foot", "Inch", "Centimeter", "Millimeter", "Yard", "Nautical Mile"],
    "Mass": ["Gram", "Kilogram", "Pound", "Ounce", "Ton", "Milligram", "Microgram", "Stone"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Time": ["Second", "Minute", "Hour", "Day", "Week", "Month", "Year", "Millisecond", "Microsecond"],
    "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour", "Knots", "Feet per second"],
    "Area": ["Square meter", "Square kilometer", "Square mile", "Square foot", "Square inch", "Acre", "Hectare"],
    "Volume": ["Liter", "Milliliter", "Cubic meter", "Cubic centimeter", "Cubic inch", "Gallon (US)", "Quart (US)", "Pint (US)"],
    "Energy": ["Joule", "Kilojoule", "Calorie", "Kilocalorie", "Watt-hour", "Kilowatt-hour", "Electronvolt"],
    "Power": ["Watt", "Kilowatt", "Horsepower", "Megawatt"],
    "Pressure": ["Pascal", "Kilopascal", "Bar", "PSI", "Atmosphere"],
    "Data Storage": ["Bit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Petabyte"],
    "Fuel Economy": ["Kilometers per liter", "Liters per 100 kilometers", "Miles per gallon (US)", "Miles per gallon (UK)"],
}

# Inputs
category = st.selectbox("Choose Category", list(unit_categories.keys()))
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", unit_categories[category], key="from_unit")
with col2:
    to_unit = st.selectbox("To", unit_categories[category], key="to_unit")
st.markdown('</div>', unsafe_allow_html=True)
value = st.number_input("Enter Value", min_value=0.0, step=0.1)


def convert_units(category, from_unit, to_unit, value):
    conversion_factors = {
        "Length": {"Meter": 1, "Kilometer": 0.001, "Mile": 0.000621371, "Foot": 3.28084, "Inch": 39.3701, "Centimeter": 100, "Millimeter": 1000, "Yard": 1.09361, "Nautical Mile": 0.000539957},
        "Mass": {"Gram": 1, "Kilogram": 0.001, "Pound": 0.00220462, "Ounce": 0.035274, "Ton": 0.000001, "Milligram": 1000, "Microgram": 1000000, "Stone": 0.000157473},
        "Speed": {"Meters per second": 1, "Kilometers per hour": 3.6, "Miles per hour": 2.23694, "Knots": 1.94384, "Feet per second": 3.28084},
        "Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400, "Week": 1/604800, "Month": 1/2628000, "Year": 1/31536000, "Millisecond": 1000, "Microsecond": 1000000},
        "Area": {"Square meter": 1, "Square kilometer": 0.000001, "Square mile": 3.861e-7, "Square foot": 10.7639, "Square inch": 1550, "Acre": 0.000247105, "Hectare": 0.0001},
        "Volume": {"Liter": 1, "Milliliter": 1000, "Cubic meter": 0.001, "Cubic centimeter": 1000, "Cubic inch": 61.0237, "Gallon (US)": 0.264172, "Quart (US)": 1.05669, "Pint (US)": 2.11338},
        "Energy": {"Joule": 1, "Kilojoule": 0.001, "Calorie": 0.239006, "Kilocalorie": 0.000239006, "Watt-hour": 0.000277778, "Kilowatt-hour": 2.7778e-7, "Electronvolt": 6.242e+18},
        "Power": {"Watt": 1, "Kilowatt": 0.001, "Horsepower": 0.00134102, "Megawatt": 1e-6},
        "Pressure": {"Pascal": 1, "Kilopascal": 0.001, "Bar": 1e-5, "PSI": 0.000145038, "Atmosphere": 9.8692e-6},
        "Data Storage": {"Bit": 1, "Byte": 0.125, "Kilobyte": 0.000125, "Megabyte": 1.25e-7, "Gigabyte": 1.25e-10, "Terabyte": 1.25e-13, "Petabyte": 1.25e-16},
        "Fuel Economy": {"Kilometers per liter": 1, "Liters per 100 kilometers": 100, "Miles per gallon (US)": 2.35215, "Miles per gallon (UK)": 2.82481},
    }

    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return ((value - 32) * 5/9) + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return ((value - 273.15) * 9/5) + 32
        else:
            return None

    elif category in conversion_factors:
        if from_unit in conversion_factors[category] and to_unit in conversion_factors[category]:
            return value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])

    return None


# Storing Conversions
if "conversions" not in st.session_state:
    st.session_state.conversions = []

if st.button("Convert"):
    result = convert_units(category, from_unit, to_unit, value)

    if result is not None:
        conversion_record = {
            "Category": category,
            "From Unit": from_unit,
            "To Unit": to_unit,
            "Input Value": value,
            "Converted Value": round(result, 4),
        }
        st.session_state.conversions.append(conversion_record)
        st.success(f"✅ {value} {from_unit} is equal to {round(result, 4)} {to_unit}")
    else:
        st.error("❌ Conversion not possible. Please check your input units.")

# explaination
    st.markdown("<br><br>" , unsafe_allow_html=True)
    st.subheader("📘 How the Conversion Works:")

    explanation = f"""
    <div class="explanation-box">
       <p>The conversion of <b>{from_unit}</b> to <b>{to_unit}</b> follows this formula:</p>
       <ul>
          <li> <b>{value} {from_unit}</b> * (conversion factor) = <b>{round(result, 4)} {to_unit}</b> </li>
       </ul>
    <p>This method ensures accuracy using a predefined set of unit ratios.</p>
    </div>
    """

    st.markdown(explanation, unsafe_allow_html=True)
    
#Conversion History

if st.session_state.conversions:
    st.markdown("<br><br>" , unsafe_allow_html=True)
    st.subheader("📜 Conversion History")
    df = pd.DataFrame(st.session_state.conversions)
    st.dataframe(df)

# CSV Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="unit_conversions.csv",
        mime="text/csv",
    )

    # PDF Export Function
    def create_pdf(conversions):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Unit Conversion History", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        for conversion in conversions:
            pdf.cell(200, 10, f"{conversion['Input Value']} {conversion['From Unit']} -> {conversion['Converted Value']} {conversion['To Unit']}", ln=True)

        pdf_file_path = "unit_conversions.pdf"
        pdf.output(pdf_file_path)
        return pdf_file_path

    # Generate pdf
    if st.button("📄 Download as PDF"):
        pdf_path = create_pdf(st.session_state.conversions)
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        st.download_button(
            label="📥 Download PDF",
            data=pdf_data,
            file_name="unit_conversions.pdf",
            mime="application/pdf",
        )

# Footer
st.markdown("""
---
📌 Created by Saira | 🔗 [GitHub Repo](#) | 🌍 Streamlit
""", unsafe_allow_html=True)

