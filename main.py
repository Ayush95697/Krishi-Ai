import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load datasets
@st.cache_data
def load_data():
    market_price_df = pd.DataFrame({
        'Crop': ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Barley', 'Pulses', 'Groundnut'],
        'Market_price_per_quintal': [2200, 2500, 2000, 2800, 5400, 1900, 5000, 5200]
    })
    
    crop_yield_df = pd.DataFrame({
        'Crop': ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Barley', 'Pulses', 'Groundnut'],
        'Yield_per_acre_quintal': [22, 20, 18, 40, 10, 19, 13, 15]
    })
    
    crop_cost_df = pd.DataFrame({
        'Crop': ['Wheat', 'Rice', 'Maize', 'Sugarcane', 'Cotton', 'Barley', 'Pulses', 'Groundnut'],
        'Cost_per_acre': [12000, 15000, 10000, 18000, 14000, 11000, 9000, 13000]
    })
    
    return market_price_df, crop_yield_df, crop_cost_df

# Set page configuration
st.set_page_config(
    page_title="Krishi AI - Crop Recommendation System",
    page_icon="🌱",
    layout="wide"
)

# Title and description
st.title("Krishi AI - Smart Crop Recommendation System")
st.markdown("""
This intelligent application helps farmers determine the most suitable crop to cultivate
based on soil composition, environmental factors, and economic considerations.
""")

# Load the model
@st.cache_resource
def load_model():
    try:
        # For demo purposes, we'll create a simple model that returns a crop based on conditions
        # Replace this with loading your actual model
        class DummyModel:
            def predict(self, features):
                # This is a placeholder - replace with your actual model
                n, p, k, temperature, humidity, ph, rainfall = features[0]
                
                if temperature > 30 and humidity > 70 and rainfall > 75:
                    return ["Rice"]
                elif 20 <= temperature <= 30 and 50 <= humidity <= 70:
                    return ["Wheat"]
                elif temperature > 25 and rainfall < 40:
                    return ["Cotton"]
                elif ph < 6:
                    return ["Groundnut"]
                elif k > 100:
                    return ["Sugarcane"]
                elif n > 100:
                    return ["Maize"]
                elif p > 100:
                    return ["Pulses"]
                else:
                    return ["Barley"]
                    
        return DummyModel()
        
        # Uncomment this to use your actual model:
        # model = pickle.load(open('crop_recommendation_model.pkl', 'rb'))
        # return model
    except Exception as e:
        st.error(f"Model loading error: {e}")
        return None

# Load datasets
market_price_df, crop_yield_df, crop_cost_df = load_data()

# Define regions and their typical conditions (customize based on your needs)
regions = {
    "North India": {"temp_range": (15, 35), "humidity_range": (40, 70), "rainfall_range": (20, 60), "ph_range": (6.5, 7.5)},
    "South India": {"temp_range": (20, 40), "humidity_range": (60, 90), "rainfall_range": (40, 90), "ph_range": (6.0, 7.0)},
    "East India": {"temp_range": (18, 38), "humidity_range": (70, 95), "rainfall_range": (50, 95), "ph_range": (5.5, 6.5)},
    "West India": {"temp_range": (22, 42), "humidity_range": (30, 60), "rainfall_range": (10, 40), "ph_range": (7.0, 8.0)},
    "Central India": {"temp_range": (20, 40), "humidity_range": (40, 80), "rainfall_range": (30, 70), "ph_range": (6.8, 7.8)},
}

# Create main columns
col1, col2 = st.columns([1, 1.2])

# Farmer information
with col1:
    st.subheader("Farmer Information")
    farmer_name = st.text_input("Farmer's Name", "")
    region = st.selectbox("Region", list(regions.keys()))
    acres = st.number_input("Total Acres of Land", min_value=0.1, value=5.0, step=0.1)
    
    # Set default values based on region
    if region:
        region_data = regions[region]
        default_temp = sum(region_data["temp_range"]) / 2
        default_humidity = sum(region_data["humidity_range"]) / 2
        default_rainfall = sum(region_data["rainfall_range"]) / 2
        default_ph = sum(region_data["ph_range"]) / 2
    else:
        default_temp, default_humidity, default_rainfall, default_ph = 25, 60, 50, 7.0

# Soil and environmental inputs
with col2:
    st.subheader("Soil and Environmental Parameters")
    
    # Create two columns within col2
    subcol1, subcol2 = st.columns(2)
    
    with subcol1:
        st.markdown("**Soil Composition**")
        n = st.slider("Nitrogen (N)", 0, 150, 50, help="Amount of Nitrogen in soil (mg/kg)")
        p = st.slider("Phosphorus (P)", 0, 150, 50, help="Amount of Phosphorus in soil (mg/kg)")
        k = st.slider("Potassium (K)", 0, 150, 50, help="Amount of Potassium in soil (mg/kg)")
        ph = st.slider("pH value", 0.0, 14.0, default_ph, 0.1, help="pH level (0-14)")
    
    with subcol2:
        st.markdown("**Environmental Factors**")
        temperature = st.slider("Temperature (°C)", 0.0, 50.0, default_temp, 0.1, 
                              help="Temperature in degrees Celsius")
        humidity = st.slider("Humidity (%)", 0.0, 100.0, default_humidity, 0.1, 
                           help="Relative humidity in percentage")
        rainfall = st.slider("Rainfall (mm)", 1.0, 100.0, default_rainfall, 0.1, 
                           help="Annual rainfall in millimeters")

# Load model
model = load_model()

# Recommend button
if st.button("Recommend Suitable Crop", type="primary"):
    if model is not None and farmer_name.strip() != "":
        # Make prediction
        try:
            features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
            prediction = model.predict(features)
            recommended_crop = prediction[0]
            
            # Get crop details
            crop_yield = crop_yield_df[crop_yield_df['Crop'] == recommended_crop]['Yield_per_acre_quintal'].values[0]
            cost_per_acre = crop_cost_df[crop_cost_df['Crop'] == recommended_crop]['Cost_per_acre'].values[0]
            market_price = market_price_df[market_price_df['Crop'] == recommended_crop]['Market_price_per_quintal'].values[0]
            
            # Calculate economics
            total_production_cost = cost_per_acre * acres
            labor_cost = total_production_cost * 0.2  # 20% additional labor cost
            total_cost = total_production_cost + labor_cost
            
            total_yield = crop_yield * acres
            total_revenue = total_yield * market_price
            profit = total_revenue - total_cost
            roi_percentage = (profit / total_cost) * 100
            
            # Display results
            st.markdown("---")
            st.subheader(f"Results for {farmer_name}")
            
            # Display recommendation
            st.success(f"### Recommended Crop: {recommended_crop.upper()}")
            
            # Economic analysis in three columns
            ec1, ec2, ec3 = st.columns(3)
            
            with ec1:
                st.info("### Cost Analysis")
                st.write(f"Base Cost: ₹{total_production_cost:,.2f}")
                st.write(f"Labor Cost (20%): ₹{labor_cost:,.2f}")
                st.write(f"**Total Investment: ₹{total_cost:,.2f}**")
            
            with ec2:
                st.info("### Revenue Analysis")
                st.write(f"Expected Yield: {total_yield:,.2f} quintals")
                st.write(f"Market Price: ₹{market_price:,.2f}/quintal")
                st.write(f"**Total Revenue: ₹{total_revenue:,.2f}**")
            
            with ec3:
                st.info("### Profit Analysis")
                st.write(f"**Net Profit: ₹{profit:,.2f}**")
                st.write(f"ROI: {roi_percentage:.2f}%")
                if profit > 0:
                    st.success("✅ Profitable Venture")
                else:
                    st.error("⚠️ Not Profitable")
            
            # Create a visualization
            st.subheader("Financial Breakdown")
            
            # Create financial data for visualization
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Cost breakdown
            cost_labels = ['Base Cost', 'Labor Cost']
            cost_values = [total_production_cost, labor_cost]
            ax1.pie(cost_values, labels=cost_labels, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Cost Breakdown')
            
            # Revenue vs Cost vs Profit
            categories = ['Investment', 'Revenue', 'Profit']
            values = [total_cost, total_revenue, profit]
            colors = ['#ff9999','#66b3ff','#99ff99']
            ax2.bar(categories, values, color=colors)
            ax2.set_title('Financial Overview')
            ax2.set_ylabel('Amount (₹)')
            
            # Add value labels on bars
            for i, v in enumerate(values):
                ax2.text(i, v/2, f'₹{v:,.0f}', ha='center', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Crop information
            st.subheader(f"About {recommended_crop}")
            
            # Sample crop information - you would expand this with actual data
            crop_info = {
                "Wheat": {
                    "description": "Wheat is one of the world's most common cereal grains and a staple food for many.",
                    "growing_period": "Rabi season (winter)",
                    "water_req": "45-65 mm",
                    "diseases": "Rust, smut, and powdery mildew"
                },
                "Rice": {
                    "description": "Rice is a staple food for over half the world's population, especially in Asia.",
                    "growing_period": "Kharif season (monsoon)",
                    "water_req": "80-100 mm",
                    "diseases": "Rice blast, bacterial leaf blight"
                },
                "Maize": {
                    "description": "Maize (corn) is a versatile crop used for food, feed, and industrial purposes.",
                    "growing_period": "Year-round (different varieties)",
                    "water_req": "50-80 mm",
                    "diseases": "Leaf blight, stalk rot"
                },
                "Sugarcane": {
                    "description": "Sugarcane is a tropical grass that is a major source of sugar.",
                    "growing_period": "12-18 months",
                    "water_req": "75-100 mm",
                    "diseases": "Red rot, smut"
                },
                "Cotton": {
                    "description": "Cotton is a soft, fluffy staple fiber that grows in a boll around the seeds of cotton plants.",
                    "growing_period": "Kharif season (monsoon)",
                    "water_req": "50-70 mm",
                    "diseases": "Bollworm, bacterial blight"
                },
                "Barley": {
                    "description": "Barley is a cereal grain used in bread, beverages, and animal fodder.",
                    "growing_period": "Rabi season (winter)",
                    "water_req": "45-60 mm",
                    "diseases": "Powdery mildew, leaf rust"
                },
                "Pulses": {
                    "description": "Pulses are leguminous crops that are harvested for their dry seeds.",
                    "growing_period": "Varies by type",
                    "water_req": "35-50 mm",
                    "diseases": "Wilt, mosaic virus"
                },
                "Groundnut": {
                    "description": "Groundnut (peanut) is a legume crop grown mainly for its edible seeds.",
                    "growing_period": "100-150 days",
                    "water_req": "50-70 mm",
                    "diseases": "Leaf spot, rust"
                }
            }
            
            if recommended_crop in crop_info:
                info = crop_info[recommended_crop]
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Growing Period:** {info['growing_period']}")
                st.write(f"**Water Requirement:** {info['water_req']}")
                st.write(f"**Common Diseases:** {info['diseases']}")
            
            # Suggestions section
            st.subheader("Recommendations")
            st.write(f"Based on your {acres} acres in {region}, {recommended_crop} is the most suitable crop.")
            
            if profit > 0:
                st.write(f"✅ This crop should yield a good profit of approximately ₹{profit:,.2f}.")
            else:
                st.write(f"⚠️ This crop may not be profitable under current conditions. Consider alternatives or consult an agricultural expert.")
                
            st.write("**Tips for successful cultivation:**")
            st.write("1. Ensure proper soil testing before planting")
            st.write("2. Follow recommended irrigation practices")
            st.write("3. Monitor for pests and diseases regularly")
            st.write("4. Consider crop insurance to mitigate risks")
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
    else:
        if farmer_name.strip() == "":
            st.warning("Please enter farmer's name")
        else:
            st.warning("Please ensure the model is loaded correctly before making predictions.")

# Add information at the bottom
st.markdown("---")
st.markdown("""
### How to use this tool:
1. Enter your personal information and land details
2. Select your region to get default environmental parameters
3. Adjust the soil and environment parameters if you have specific measurements
4. Click the "Recommend Suitable Crop" button
5. Review the economic analysis and recommendations

For more accurate results, consider getting your soil professionally tested.
""")

# Sidebar with additional information
with st.sidebar:
    st.header("About Krishi AI")
    st.write("Krishi AI is an intelligent crop recommendation system designed to help farmers make data-driven decisions about crop selection.")
    
    st.subheader("Note")
    st.write("This tool provides recommendations based on available data and is meant for guidance only. Results may vary based on actual conditions.")
    
    st.subheader("Supported Crops")
    st.write(", ".join(market_price_df['Crop'].tolist()))
    
    st.subheader("Contact")
    st.write("For assistance, please contact support ayushmishra7548@gmail.com")