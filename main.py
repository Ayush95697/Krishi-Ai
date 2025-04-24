import streamlit as st
import joblib
import os
import matplotlib.pyplot as plt
import pandas as pd


import streamlit as st
st.cache_data.clear()
st.cache_resource.clear()
# Set page configuration
st.set_page_config(
    page_title="KrishiGuru - Smart Crop Advisor",
    page_icon="🌾",
    layout="wide"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    .main-header {color: #2E7D32; font-size: 36px; font-weight: 700; margin-bottom: 0px;}
    .sub-header {color: #388E3C; font-size: 20px; font-weight: 500; margin-top: 0px;}
    .metric-card {
        background-color: black;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .metric-value {font-size: 24px; font-weight: bold; color: #2E7D32;}
    .metric-label {font-size: 14px; color: #666;}
    .recommendation-box {
        padding: 20px;
        background-color: #FFFFE0;  /* Changed to light yellow background */
        border-left: 5px solid #FBC02D;  /* Changed to amber border */
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .recommendation-title {
        margin-top: 0;
        color: #F57F17;  /* Changed to amber text */
    }
</style>
""", unsafe_allow_html=True)
st.markdown("### 🧪 Soil Health Resource")
st.markdown(
    
    "[Click here to access the Soil Health Lab Portal (Govt. of India)](https://soilhealth.dac.gov.in/soil-lab)",
    unsafe_allow_html=True,
)



# Load model
@st.cache_resource
def load_model():
    model_path = "artifacts/model.joblib"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        st.error("❌ Model file not found.")
        return None

# Inline financial + crop data
crop_data = {
    'rice': (15000, 20, 2500, "Staple food crop grown in waterlogged conditions."),
    'maize': (12000, 18, 2000, "Versatile grain used as food and fodder."),
    'chickpea': (11000, 14, 4800, "Protein-rich legume suited for dry areas."),
    'kidneybeans': (13000, 16, 5000, "Used in curries, needs moderate rainfall."),
    'pigeonpeas': (12500, 15, 4900, "Drought-resistant pulse."),
    'mothbeans': (10500, 13, 4700, "Resilient pulse for dry, sandy soil."),
    'mungbean': (10000, 12, 4600, "Nitrogen-fixing legume."),
    'blackgram': (11500, 14, 4500, "Used in South Indian dishes."),
    'lentil': (10000, 12, 4400, "High-protein pulse for cooler climates."),
    'pomegranate': (14000, 11, 5200, "Fruit with high export demand."),
    'banana': (16000, 24, 3000, "Grows year-round in tropical zones."),
    'mango': (15500, 22, 4000, "King of fruits, needs hot summers."),
    'grapes': (17000, 18, 3500, "Dry climate fruit for juice/wine."),
    'watermelon': (13000, 20, 3800, "Hot weather fruit, needs lots of water."),
    'muskmelon': (14000, 21, 3900, "Juicy melon grown in summer."),
    'apple': (18000, 25, 5500, "Temperate fruit needing cold winters."),
    'orange': (16000, 23, 4200, "Semi-tropical citrus fruit."),
    'papaya': (15000, 22, 3100, "Fast-growing fruit crop."),
    'coconut': (17000, 26, 5200, "Coastal crop used for oil/water."),
    'cotton': (14500, 17, 2800, "Cash crop for textile industry."),
    'jute': (13500, 16, 2700, "Fiber crop for sacks and mats."),
    'coffee': (19000, 10, 6000, "Hill-grown beverage crop.")
}

model = load_model()

# Sidebar
with st.sidebar:
    st.header("About KrishiGuru")
    st.write("KrishiGuru is an intelligent crop recommendation system designed to help farmers make data-driven decisions about crop selection.")
    st.markdown("**Supported Crops:**")
    
    # Display crops in a more elegant way
    crop_list = sorted(list(crop_data.keys()))
    cols = st.columns(2)
    for i, crop in enumerate(crop_list):
        cols[i % 2].write(f"• {crop.capitalize()}")
    
    st.markdown("---")
    st.markdown("📧 For assistance, contact: [support@krishiguru.com](mailto:support@krishiguru.com)")

# Main content
st.markdown("<h1 class='main-header'>🌾 Krishi AI - Smart Crop Advisor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Enter your region, land size, and environmental factors to get crop & profit recommendation.</p>", unsafe_allow_html=True)

if model:
    # Input section layout
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        st.subheader("👨‍🌾 Farmer Information")
        name = st.text_input("Farmer's Name")
        region = st.selectbox("Region", ["North India", "South India", "East India", "West India"])
        acres = st.number_input("Total Acres of Land", min_value=1.0)

    with input_col2:
        st.subheader("🧪 Soil and Environmental Parameters")
        
        # More organized layout for parameters
        col2a, col2b = st.columns(2)
        
        with col2a:
            N = st.slider("Nitrogen (N)", 0, 150, 50)
            P = st.slider("Phosphorus (P)", 0, 150, 50)
            K = st.slider("Potassium (K)", 0, 150, 50)
            
        with col2b:
            temp = st.slider("Temperature (°C)", 0.0, 50.0, 25.0)
            humidity = st.slider("Humidity (%)", 0.0, 100.0, 55.0)
            ph = st.slider("pH value", 3.0, 10.0, 7.0)
            
        rainfall = st.slider("Rainfall (mm)", 0.0, 300.0, 100.0)

    # Prominent action button
    if st.button("🌿 Recommend Suitable Crop", use_container_width=True):
        features = [[N, P, K, temp, humidity, ph, rainfall]]
        crop = model.predict(features)[0]
        
        # Get crop data
        cost, yield_, price, desc = crop_data.get(crop, (0, 0, 0, "No description available."))

        # Financial calculations
        base_cost = cost * acres
        labor_cost = base_cost * 0.20
        fertilizer_cost = base_cost * 0.15
        irrigation_cost = base_cost * 0.10
        misc_cost = base_cost * 0.05
        total_cost = base_cost + labor_cost + fertilizer_cost + irrigation_cost + misc_cost
        
        total_yield = yield_ * acres
        revenue = total_yield * price
        profit = revenue - total_cost
        roi = (profit / total_cost) * 100
        
        # Success message with attractive styling (changed background color)
        st.markdown(f"""
        <div class="recommendation-box">
            <h2 class="recommendation-title">🌱 Recommended Crop: {crop.upper()}</h2>
            <p>{crop_data[crop][3]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Financial Metrics Dashboard
        st.subheader("💰 Financial Analysis")
        
        # Reorganized financial metrics
        metric_cols = st.columns(4)
        
        metric_cols[0].markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Investment</div>
            <div class="metric-value">₹{int(total_cost):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        metric_cols[1].markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Expected Revenue</div>
            <div class="metric-value">₹{int(revenue):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        metric_cols[2].markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Net Profit</div>
            <div class="metric-value">₹{int(profit):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
        metric_cols[3].markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ROI</div>
            <div class="metric-value">{roi:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Only show the most important charts
        st.subheader("📊 Financial Breakdown")
        
        # Create 2 columns for the most important charts only
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            # Cost breakdown pie chart
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            cost_labels = ['Base Cost', 'Labor', 'Fertilizers', 'Irrigation', 'Misc']
            cost_values = [base_cost, labor_cost, fertilizer_cost, irrigation_cost, misc_cost]
            
            ax1.pie(cost_values, autopct='%1.1f%%', 
                    colors=['#4CAF50', '#8BC34A', '#CDDC39', '#FFC107', '#FF9800'],
                    startangle=90, textprops={'fontsize': 10})
            ax1.axis('equal')
            plt.legend(cost_labels, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8)
            plt.title('Cost Distribution', fontsize=12)
            st.pyplot(fig1)
            
        with fig_col2:
            # Financial overview bar chart
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            labels = ['Investment', 'Revenue', 'Profit']
            values = [total_cost, revenue, profit]
            bars = ax2.bar(labels, values, color=['#FF5722', '#4CAF50', '#2196F3'])
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01 * max(values),
                       f'₹{int(height):,}', ha='center', va='bottom', fontsize=8)
            
            ax2.set_title('Financial Overview', fontsize=12)
            ax2.set_ylabel('Amount (₹)', fontsize=10)
            ax2.grid(axis='y', linestyle='--', alpha=0.7)
            ax2.set_ylim(bottom=0)
            st.pyplot(fig2)
        
        # Crop specific recommendations
        st.subheader("🌾 Crop Management Recommendations")
        
        # Simplified recommendations using columns instead of tabs for better visual clarity
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("""
            **🌱 Planting Guide**
            
            - **Best Season:** Choose the appropriate planting season based on your regional climate
            - **Seed Rate:** Follow recommended seed rate for optimal plant population
            - **Spacing:** Maintain proper spacing between plants and rows
            - **Soil Preparation:** Deep plowing recommended before sowing
            """)
            
            st.markdown("""
            **💧 Irrigation Schedule**
            
            - Critical stages requiring irrigation:
              - Initial growth phase
              - Flowering/fruiting period
              - Grain filling stage
            - Water according to soil moisture and weather conditions
            """)
        
        with rec_col2:
            st.markdown("""
            **🧪 Fertilization Plan**
            
            - **Base Application:** Apply NPK fertilizers before planting
            - **Top Dressing:** Additional nitrogen during vegetative growth
            - **Micronutrients:** Apply as needed based on soil test results
            """)
            
            st.markdown("""
            **🐛 Pest & Disease Management**
            
            - Regular monitoring for early detection
            - Use integrated pest management practices
            - Focus on prevention with good field sanitation
            - Apply treatments only when necessary
            """)
        
        # Yield information in a clean format
        st.subheader("📈 Yield Analysis")
        
        # Display yield info with better formatting
        yield_cols = st.columns(4)
        
        with yield_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Yield per Acre</div>
                <div class="metric-value">{yield_} quintals</div>
            </div>
            """, unsafe_allow_html=True)
            
        with yield_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Land</div>
                <div class="metric-value">{acres} acres</div>
            </div>
            """, unsafe_allow_html=True)
            
        with yield_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Expected Yield</div>
                <div class="metric-value">{int(total_yield)} quintals</div>
            </div>
            """, unsafe_allow_html=True)
            
        with yield_cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Market Price</div>
                <div class="metric-value">₹{price}/quintal</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 Please enter your parameters and click 'Recommend Suitable Crop' to see analysis")
