
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="💸 Expense Tracker", layout="wide")
st.title("💸 Personal Expense Tracker")
st.write("Upload your expenses CSV file and get instant visual insights!")

st.markdown("""
**Expected CSV format:**
```
Date,Category,Amount
2025-04-01,Groceries,150
2025-04-01,Transport,50
2025-04-02,Entertainment,120
```
""")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')

    st.subheader("📊 Expense Summary")
    total_spent = df['Amount'].sum()
    st.metric("Total Spent", f"₹{total_spent:,.2f}")

    st.subheader("📌 Spending by Category")
    category_summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots()
    ax1.pie(category_summary, labels=category_summary.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    st.subheader("📅 Monthly Spending Trend")
    monthly_summary = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_summary['Month'] = monthly_summary['Month'].astype(str)
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=monthly_summary, x='Month', y='Amount', marker='o', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.subheader("📋 Raw Data")
    st.dataframe(df)
else:
    st.info("Please upload a CSV file to begin.")
