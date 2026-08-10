import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Clinical Trial Landscape Analysis")
st.write("Exploring immunotherapy trial distributions across cancer types.")

# Load data
df = pd.read_csv("data.csv")

# Interactive filter sidebar
selected_condition = st.sidebar.selectbox("Select Condition Keyword", ["lung", "breast", "brain"])

# Filter DataFrame
filtered_df = df[df['Conditions'].str.contains(selected_condition, case=False, na=False)]

# Plot top 10 conditions
st.subheader(f"Top Conditions for: {selected_condition.capitalize()}")
fig, ax = plt.subplots()
filtered_df['Conditions'].value_counts().head(10).plot(kind='barh', ax=ax)
st.pyplot(fig)