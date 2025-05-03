import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Example usage
if openai_api_key:
    print("API key loaded successfully!")
else:
    print("Failed to load API key.")

# Load data
suppliers = pd.read_csv("Data/bushnell_supplier_list.csv")
products = pd.read_csv("Data/bushnell_simmons_tasco_products.csv")
brands = pd.read_csv("Data/Brands.csv")

# Merge datasets to link suppliers, products, and brands
products_with_brands = products.merge(brands, on="brand_id", how="left")
suppliers_with_products = suppliers.merge(
    products_with_brands, left_on="product_family_supported", right_on="product Family", how="inner"
)

st.title("📦 Bushnell Supply Chain Dashboard")

# Tab for the dashboard
tab1 = st.tabs(["Supplier Map"])[0]

with tab1:
    st.sidebar.title("Supplier Map")
    country_counts = suppliers["supplier_country_code"].value_counts().reset_index()
    country_counts.columns = ["supplier_country_code", "count"]

    # Plot the map
    fig = px.choropleth(
        country_counts,
        locations="supplier_country_code",
        locationmode="ISO-3",
        color="count",
        title="Suppliers by Country",
        color_continuous_scale="Blues",
    )
    st.sidebar.plotly_chart(fig, use_container_width=True)

    # Main screen: Display products and brands
    st.title("Supplier Dashboard")
    selected_country = st.sidebar.selectbox(
        "Select a Country", suppliers["supplier_country_code"].unique()
    )

    if selected_country:
        # Filter data by selected country
        filtered_data = suppliers_with_products[
            suppliers_with_products["supplier_country_code"] == selected_country
        ]
        st.write(f"Products supplied by {selected_country}:")
        st.dataframe(filtered_data[["product_name", "product Family", "brand"]])

# Debugging: Inspect the merged DataFrame
st.write("Suppliers with Products DataFrame:")
st.write(suppliers_with_products.head())
