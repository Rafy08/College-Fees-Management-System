import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if needed
db = client['college']  # Create or connect to the 'college' database
fees_collection = db['fees']  # Create or connect to the 'fees' collection

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Add Fees", "View Fees"])

# Function to add student fee details
if menu == "Add Fees":
    st.title("Add Student Fees")
    
    # Input fields
    student_name = st.text_input("Enter Student Name")
    student_id = st.text_input("Enter Student ID")
    total_fees = st.number_input("Total Fees", min_value=0)
    amount_paid = st.number_input("Amount Paid", min_value=0)
    
    # Calculate pending fees
    pending_fees = total_fees - amount_paid

    if st.button("Submit"):
        if student_name and student_id and total_fees >= 0 and amount_paid >= 0:
            # Create a document with the fee data
            fee_data = {
                "student_name": student_name,
                "student_id": student_id,
                "total_fees": total_fees,
                "amount_paid": amount_paid,
                "pending_fees": pending_fees
            }

            # Insert the fee data into MongoDB
            fees_collection.insert_one(fee_data)
            st.success(f"Fee details added for {student_name}")
        else:
            st.error("Please fill all the fields correctly.")

# Function to view student fee details with search by student ID
elif menu == "View Fees":
    st.title("Search Student's Fee Details by Student ID")
    
    # Input field to search by student ID
    search_student_id = st.text_input("Enter Student ID to Search")

    if st.button("Search"):
        if search_student_id:
            # Retrieve the fee record from the MongoDB collection by student ID
            fee_record = fees_collection.find_one({"student_id": search_student_id})

            if fee_record:
                st.write(f"**Student Name**: {fee_record['student_name']}")
                st.write(f"**Student ID**: {fee_record['student_id']}")
                st.write(f"**Total Fees**: {fee_record['total_fees']}")
                st.write(f"**Amount Paid**: {fee_record['amount_paid']}")
                st.write(f"**Pending Fees**: {fee_record['pending_fees']}")
            else:
                st.warning(f"No records found for Student ID: {search_student_id}")
        else:
            st.error("Please enter a valid Student ID to search.")
