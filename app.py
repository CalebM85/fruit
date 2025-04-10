import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Clinic Loan Visualization", layout="wide")
st.title("Clinic Loan Amount and 45+ at Statement Percentage")

# Data for the clinics
clinics = [
    "Mount Laurel Animal Hospital",
    "MSPCA - Angell Animal Medical Center",
    "Veterinary Emergency & Referral Group",
    "Gulf Coast Veterinary Specialists (GCVS) - Houston",
    "Eclipse",
    "VEG Clifton",
    "Massachusetts Veterinary Referral Hospital (MVRH)",
    "Animal Emergency & Referral Center of MN (RED)",
    "Summit Veterinary Referral Center",
    "Animal Emergency and Specialty Hospital of Byron Center"
]

loan_amounts = [324074, 321719, 298475, 286118, 283366, 266840, 255268, 223783, 214595, 201339]
percentages = [3.3, 6.0, 0.0, 3.9, 0.0, 1.7, 0.6, 3.0, 3.8, 3.0]

# Create positions for each clinic along the x-axis
x = np.arange(len(clinics))
bar_width = 0.6

# Create the figure and axis objects
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot loan amounts as vertical bars
bars = ax1.bar(x, loan_amounts, bar_width, color='skyblue', label="Loan Amount ($)")
ax1.set_xlabel("Clinic", fontsize=12)
ax1.set_ylabel("Loan Amount ($)", fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticks(x)
ax1.set_xticklabels(clinics, rotation=45, ha='right')

# Create a second y-axis for the percentages
ax2 = ax1.twinx()
line, = ax2.plot(x, percentages, color='darkred', marker='o', linestyle='-', linewidth=2, markersize=8, label="45+ at Statement (%)")
ax2.set_ylabel("45+ at Statement (%)", fontsize=12, color='darkred')
ax2.tick_params(axis='y', labelcolor='darkred')

# Combine legends from both axes
lines_labels = [bars, line]
labels = [l.get_label() for l in lines_labels]
ax1.legend(lines_labels, labels, loc='upper right')

ax1.set_title("Clinic Loan Amount and 45+ at Statement Percentage", fontsize=16, pad=20)
fig.tight_layout()

# Display the figure in the Streamlit app
st.pyplot(fig)
