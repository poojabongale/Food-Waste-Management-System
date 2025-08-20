import streamlit as st
import joblib
import pandas as pd
import queries
from queries import (
    providers_and_receivers_by_city,
    top_provider_type,
    provider_contacts_by_city,
    top_receivers,
    food_available,
    highest_food_listings,
    food_types,
    food_claims,
    highest_successful_food_claims,
    pending_completed_cancelled_Foodclaims,
    food_quantity_per_receiver,
    meal_type,
    food_donated
)

# Page Config
st.set_page_config(page_title="Food Waste Management Dashboard", layout="wide")
st.title("🍽️ Food Waste Management Dashboard")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Select Query",
    [
        "1. Providers & Receivers by City",
        "2. Top Provider Type",
        "3. Provider Contacts by City",
        "4. Top Receivers",
        "5. Total Food Quantity Available",
        "6. City with Highest Food Listings",
        "7. Most Commonly Available Food Types",
        "8. Food Claims per Item",
        "9. Provider with Most Successful Claims",
        "10. Claims Status Percentage",
        "11. Average Quantity Claimed per Receiver",
        "12. Most Claimed Meal Type",
        "13. Total Quantity Donated by Each Provider"
    ]
)

# Query Execution
if menu == "1. Providers & Receivers by City":
    st.subheader("Providers & Receivers by City")
    st.dataframe(providers_and_receivers_by_city())

elif menu == "2. Top Provider Type":
    st.subheader("Top Provider Type")
    st.dataframe(top_provider_type())

elif menu == "3. Provider Contacts by City":
    city = st.text_input("Enter City Name:")
    if st.button("Search"):
        df = queries.provider_contacts_by_city(city)
        if df.empty:
            st.warning("No providers found for that city.")
        else:
            st.dataframe(df)

elif menu == "4. Top Receivers":
    st.subheader("Top Receivers")
    st.dataframe(top_receivers())

elif menu == "5. Total Food Quantity Available":
    st.subheader("Total Food Quantity Available")
    st.dataframe(food_available())

elif menu == "6. City with Highest Food Listings":
    st.subheader("City with Highest Food Listings")
    st.dataframe(highest_food_listings())

elif menu == "7. Most Commonly Available Food Types":
    st.subheader("Most Commonly Available Food Types")
    st.dataframe(food_types())

elif menu == "8. Food Claims per Item":
    st.subheader("Food Claims per Item")
    st.dataframe(food_claims())

elif menu == "9. Provider with Most Successful Claims":
    st.subheader("Provider with Most Successful Claims")
    st.dataframe(highest_successful_food_claims())

elif menu == "10. Claims Status Percentage":
    st.subheader("Claims Status Percentage")
    st.dataframe(pending_completed_cancelled_Foodclaims())

elif menu == "11. Average Quantity Claimed per Receiver":
    st.subheader("Average Quantity Claimed per Receiver")
    st.dataframe(food_quantity_per_receiver())

elif menu == "12. Most Claimed Meal Type":
    st.subheader("Most Claimed Meal Type")
    st.dataframe(meal_type())

elif menu == "13. Total Quantity Donated by Each Provider":
    st.subheader("Total Quantity Donated by Each Provider")
    st.dataframe(food_donated())

st.subheader("🔹 Provider CRUD Operations")

crud_action = st.selectbox(
    "Choose Action",
    ["Create", "Read", "Update", "Delete"]
)

if crud_action == "Create":
    provider_id = st.text_input("Provider ID")
    name = st.text_input("Provider Name")
    provider_type = st.text_input("Type (Restaurant, Grocery, etc.)")
    address = st.text_area("Address")
    city = st.text_input("City")
    contact = st.text_input("Contact")

    if st.button("Add Provider"):
        msg = queries.add_provider(provider_id,name, provider_type, address, city, contact)
        st.success(msg)

elif crud_action == "Read":
    if st.button("Show All Providers"):
        df = queries.get_all_providers()

        if df is None or len(df) == 0:
            st.warning("No provider records found.")
        else:
            st.dataframe(df)

elif crud_action == "Update":
    st.write("### Update Provider")
    df = queries.get_all_providers()
    st.dataframe(df)

    provider_id = st.number_input("Enter Provider ID to Update", min_value=1)
    name = st.text_input("New Provider Name")
    provider_type = st.text_input("New Type")
    address = st.text_area("New Address")
    city = st.text_input("New City")
    contact = st.text_input("New Contact")

    if st.button("Update Provider"):
        msg = queries.update_provider(provider_id, name, provider_type, address, city, contact)
        st.success(msg)

elif crud_action == "Delete":
    st.write("### Delete Provider")
    df = queries.get_all_providers()
    st.dataframe(df)

    provider_id = st.number_input("Enter Provider ID to Delete", min_value=1)
    if st.button("Delete Provider"):
        msg = queries.delete_provider(provider_id)
        st.success(msg)

# Load model & encoder
meal_model = joblib.load("meal_model.pkl")
encoder_meal = joblib.load("encoder_meal.pkl")

st.subheader("🥢🍜 Meal Type prediction 🥢🍜")
st.write("Enter provider details to predict the **Meal Type**")

# Input fields
provider_type = st.text_input("Provider Type (e.g., Restaurant, Cafe)")
food_name = st.text_input("Food Name (e.g., Rice, Pasta)")
location = st.text_input("Location (e.g., East Sheena, Downtown)")

if st.button("Predict"):
    if provider_type and food_name and location:
        # Create DataFrame for input
        input_df = pd.DataFrame([[provider_type, food_name, location]],
                                columns=["Provider_Type", "Food_Name", "Location"])

        # Encode input
        input_encoded = encoder_meal.transform(input_df)

        # Predict
        prediction = meal_model.predict(input_encoded)[0]

        st.success(f"✅ Predicted Meal Type: **{prediction}**")
    else:
        st.warning("⚠️ Please fill in all fields before predicting.")

