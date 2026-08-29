import streamlit as st
import pandas as pd
import textwrap
import matplotlib.pyplot as plt

st.title("Clinical Trial Landscape Analysis")
st.write("Exploring immunotherapy trial distributions across cancer types.")

# Load data
df = pd.read_csv("data.csv")

# --- Interactive Filter Sidebar ---
selected_condition = st.sidebar.selectbox(
    "Select Condition Keyword",
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
    ]
)

# Get unique gender/sex options from your DataFrame dynamically
gender_options = list(df['Sex'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

# --- Apply Combined Filters ---
# 1. Condition filter
condition_mask = df['Conditions'].str.contains(selected_condition, case=False, na=False)

# 2. Gender filter (apply if anything other than "All" is selected)
if selected_gender != "All":
    gender_mask = df['Sex'] == selected_gender
    filtered_df = df[condition_mask & gender_mask]
else:
    filtered_df = df[condition_mask]

# --- Display Results ---
st.subheader(f"Top Conditions for: {selected_gender} | Keyword: {selected_condition}")

if filtered_df.empty:
    st.warning("No trials match the selected filters.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))

    counts = filtered_df['Conditions'].value_counts().head(10)

    # wrap long labels across multiple lines
    wrapped_labels = [textwrap.fill(label, width=25) for label in counts.index]

    # Plot horizontal bar chart
    counts.plot(kind='barh', ax=ax, color='#008cff')

    ax.invert_yaxis()  # Keep highest count at top
    ax.set_xlabel("Number of Trials")
    ax.set_ylabel("Condition")

    #ax.set_yticklabels([
    #f"{label.get_text()[:30]}..." if len(label.get_text()) > 30 else label.get_text()
    #for label in ax.get_yticklabels()])

    plt.tight_layout()

    st.pyplot(fig)