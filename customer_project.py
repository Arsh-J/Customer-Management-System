import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["CustomerDB"]
collection = db["Customers"]

# Streamlit UI setup
st.title("Customer Management System")

# Navigation menu
menu = ["Add Customer", "View Customers", "Update Customer", "Delete Customer"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Customer
if choice == "Add Customer":
    st.header("Add Customer")
    with st.form("add_form"):
        name = st.text_input("Enter customer name")
        age = st.number_input("Enter customer age", min_value=0, step=1)
        email = st.text_input("Enter customer email")
        phone = st.text_input("Enter customer phone number")
        submitted = st.form_submit_button("Add Customer")

    if submitted:
        customer = {
            "name": name,
            "age": age,
            "email": email,
            "phone": phone
        }
        collection.insert_one(customer)
        st.success("Customer added successfully!")

# View Customers
elif choice == "View Customers":
    st.header("View Customers")
    customers = list(collection.find())
    
    if customers:
        # Create a list of dictionaries with customer data
        customer_data = [{
            "Index": idx + 1,  # Add an index column starting from 1
            "ID": str(customer["_id"]),
            "Name": customer["name"],
            "Age": customer["age"],
            "Email": customer["email"],
            "Phone": customer["phone"]
        } for idx, customer in enumerate(customers)]
        
        # Display the data as a table
        st.dataframe(customer_data)
    else:
        st.warning("No customers found.")

# Update Customer
elif choice == "Update Customer":
    st.header("Update Customer")
    customer_id = st.text_input("Enter the ID of the customer to update")
    field = st.selectbox("Select the field to update", ["name", "age", "email", "phone"])
    new_value = st.text_input("Enter the new value")

    if st.button("Update Customer"):
        try:
            if field == "age":
                new_value = int(new_value)
            result = collection.update_one({"_id": ObjectId(customer_id)}, {"$set": {field: new_value}})
            if result.modified_count > 0:
                st.success("Customer updated successfully!")
            else:
                st.error("No matching customer found.")
        except Exception as e:
            st.error(f"Error: {e}")

# Delete Customer
elif choice == "Delete Customer":
    st.header("Delete Customer")
    customer_id = st.text_input("Enter the ID of the customer to delete")

    if st.button("Delete Customer"):
        try:
            object_id = ObjectId(customer_id)
            result = collection.delete_one({"_id": object_id})
            if result.deleted_count > 0:
                st.success("Customer deleted successfully!")
            else:
                st.error("No matching customer found.")
        except Exception as e:
            st.error(f"Invalid ID format: {e}")
