import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Clinical Trial Analysis")
st.write("Exploring immunotherapy trial of Keytruda across cancer types.")

# Load data
df = pd.read_csv("data.csv")

# Interactive filter sidebar
selected_condition = st.sidebar.selectbox("Select Condition Keyword",
[
    'Melanoma',
    'Non-small Cell Lung Cancer',
    'Carcinoma, Non-Small-Cell Lung',
    'Breast Cancer',
    'Neoplasms',
    'Head and Neck Squamous Cell Carcinoma',
    'Renal Cell Carcinoma',
    'Hepatocellular Carcinoma',
    'Advanced Solid Tumors'
])

# Filter DataFrame
filtered_df = df[df['Conditions'].str.contains(selected_condition, case=False, na=False)]

# Plot top 10 conditions
st.subheader(f"Top Conditions for: {selected_condition}")

fig, ax = plt.subplots(figsize=(10, 5))
counts = filtered_df['Conditions'].value_counts().head(10)

# Plot horizontal bar chart
counts.plot(kind='barh', ax=ax, color='#008cff')
ax.invert_yaxis()  # Highest count at the top
ax.set_xlabel("Number of Trials")
ax.set_ylabel("Condition")
plt.tight_layout()

st.pyplot(fig)