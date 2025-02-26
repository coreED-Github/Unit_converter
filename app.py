import streamlit as st



st.set_page_config(page_title="Smart Unit Converter", layout="wide")


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
        
        .sidebar .sidebar-content {
            background-color: #292b2c;
            color: white;
            padding: 20px;
            border-radius: 10px;
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
        
        .emoji {
            font-size: 22px;
            padding-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

#Sidebar
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
st.sidebar.title("⚡ Quick Navigation")
st.sidebar.markdown("""
- 🏠 *Home*
-  *About*
- 📞 *Contact*
""")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

#Title
st.markdown('<h1>🌍 Google-Style Unit Converter with AI Explanation</h1>', unsafe_allow_html=True)

#Units
unit_categories = {
    "Length": ["Meter", "Kilometer", "Mile", "Foot", "Inch"],
    "Area": ["Square Meter", "Square Kilometer", "Square Mile", "Acre", "Hectare"],
    "Data Transfer Rate": ["Bits per second", "Kilobits per second", "Megabits per second", "Gigabits per second"],
    "Digital Storage": ["Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"],
    "Energy": ["Joule", "Kilojoule", "Calorie", "Kilocalorie", "Watt-hour"],
    "Frequency": ["Hertz", "Kilohertz", "Megahertz", "Gigahertz"],
    "Fuel Economy": ["Kilometers per Liter", "Miles per Gallon"],
    "Mass": ["Gram", "Kilogram", "Pound", "Ounce"],
    "Plane Angle": ["Degree", "Radian"],
    "Pressure": ["Pascal", "Bar", "Atmosphere", "PSI"],
    "Speed": ["Meters per second", "Kilometers per hour", "Miles per hour", "Knots"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Time": ["Second", "Minute", "Hour", "Day"],
    "Volume": ["Milliliter", "Liter", "Cubic Meter", "Gallon"]
}

category = st.selectbox("Choose Category", list(unit_categories.keys()))
from_unit = st.selectbox("From", unit_categories[category])
to_unit = st.selectbox("To", unit_categories[category])
value = st.number_input("Enter Value", min_value=0.0, step=0.1)

#factors
def convert_units(category, from_unit, to_unit, value):
    conversion_factors = {
        "Length": {"Meter": 1, "Kilometer": 0.001, "Mile": 0.000621371, "Foot": 3.28084, "Inch": 39.3701},
        "Area": {"Square Meter": 1, "Square Kilometer": 0.000001, "Square Mile": 3.861e-7, "Acre": 0.000247105, "Hectare": 0.0001},
        "Data Transfer Rate": {"Bits per second": 1, "Kilobits per second": 0.001, "Megabits per second": 0.000001, "Gigabits per second": 0.000000001},
        "Digital Storage": {"Byte": 1, "Kilobyte": 0.001, "Megabyte": 0.000001, "Gigabyte": 0.000000001, "Terabyte": 0.000000000001},
        "Energy": {"Joule": 1, "Kilojoule": 0.001, "Calorie": 0.239006, "Kilocalorie": 0.000239006, "Watt-hour": 0.000277778},
        "Frequency": {"Hertz": 1, "Kilohertz": 0.001, "Megahertz": 0.000001, "Gigahertz": 0.000000001},
        "Fuel Economy": {"Kilometers per Liter": 1, "Miles per Gallon": 2.352},
        "Mass": {"Gram": 1, "Kilogram": 0.001, "Pound": 0.00220462, "Ounce": 0.035274},
        "Plane Angle": {"Degree": 1, "Radian": 0.0174533},
        "Pressure": {"Pascal": 1, "Bar": 1e-5, "Atmosphere": 9.8692e-6, "PSI": 0.000145038},
        "Speed": {"Meters per second": 1, "Kilometers per hour": 3.6, "Miles per hour": 2.23694, "Knots": 1.94384},
        "Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400},
        "Volume": {"Milliliter": 1, "Liter": 0.001, "Cubic Meter": 0.000001, "Gallon": 0.000264172}
    }
# formula
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
        return value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])

#Convert Button
if st.button("Convert"):
    result = convert_units(category, from_unit, to_unit, value)
    st.success(f"✅ Converted Value: {result} {to_unit}")

#Footer
st.markdown("""
---
📌 Created by Saira | 🔗 [GitHub Repo](#) | 🌍 Deployed on Streamlit
""", unsafe_allow_html=True)


