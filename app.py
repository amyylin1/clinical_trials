import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# --- App Title & Header ---
st.title("Clinical Trial Landscape Analysis")
st.write("Exploring immunotherapy trial distributions across cancer types and trial characteristics.")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# --- 2. Interactive Sidebar Filters ---
st.sidebar.header("Filter Options")

# Filter 1: Condition Keyword (Mandatory/Primary)
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

# Filter 2: Sex / Gender
gender_options = ["All"] + list(df['Sex'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Sex", gender_options)

# Filter 3: Trial Phase (New)
phase_options = ["All"] + list(df['Phases'].dropna().unique())
selected_phase = st.sidebar.selectbox("Select Phase", phase_options)

# Filter 4: Study Status (New)
status_options = ["All"] + list(df['Study Status'].dropna().unique())
selected_status = st.sidebar.selectbox("Select Study Status", status_options)

# Filter 5: Funder Type (New)
funder_options = ["All"] + list(df['Funder Type'].dropna().unique())
selected_funder = st.sidebar.selectbox("Select Funder Type", funder_options)

# Filter 6: Study Type (New)
study_type_options = ["All"] + list(df['Study Type'].dropna().unique())
selected_study_type = st.sidebar.selectbox("Select Study Type", study_type_options)


# --- 3. Apply Multi-Column Filtering Logic ---
# Start with condition keyword match
filtered_df = df[df['Conditions'].str.contains(selected_condition, case=False, na=False)]

# Apply optional categorical filters dynamically
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]

if selected_phase != "All":
    filtered_df = filtered_df[filtered_df['Phases'] == selected_phase]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df['Study Status'] == selected_status]

if selected_funder != "All":
    filtered_df = filtered_df[filtered_df['Funder Type'] == selected_funder]

if selected_study_type != "All":
    filtered_df = filtered_df[filtered_df['Study Type'] == selected_study_type]


# --- 4. Display Results & Analytics ---
st.subheader(f"Top Conditions for Keyword: {selected_condition}")

# Summary Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Matching Trials", len(filtered_df))
col2.metric("Active Filters Applied", sum([
    selected_gender != "All",
    selected_phase != "All",
    selected_status != "All",
    selected_funder != "All",
    selected_study_type != "All"
]))
col3.metric("Total Dataset Trials", len(df))

st.markdown("---")

if filtered_df.empty:
    st.warning("No trials match the combination of filters selected.")
else:
    # Compute Top 10 Conditions based on exact string counts
    counts = filtered_df['Conditions'].value_counts().head(10)

    # Wrap label text to preserve complete names across multiple lines
    wrapped_labels = [textwrap.fill(label, width=28) for label in counts.index]

    # Generate Matplotlib Horizontal Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(wrapped_labels, counts.values, color='#008cff')
    ax.invert_yaxis()  # Place top count at the top of the chart
    ax.set_xlabel("Number of Trials", fontsize=11)
    ax.set_ylabel("Condition", fontsize=11)

    # Annotate exact count values next to bars
    for index, value in enumerate(counts.values):
        ax.text(value + (max(counts.values) * 0.01), index, str(value), va='center', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

    # Display Filtered Data Table
    with st.expander("View Filtered Data Table"):
        st.dataframe(filtered_df[[
            'NCT Number',
            'Study Title',
            'Conditions',
            'Phases',
            'Study Status',
            'Sex',
            'Funder Type',
            'Study Type',
            'Locations'
        ]])