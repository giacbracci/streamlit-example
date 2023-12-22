import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import math

st.title("FEF Academy Stock Price Fair Value Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
rev = col1.number_input("2023 Revenues (bn $)", min_value=0, step=0.01)
fcf = col1.number_input("2023 Free Cash Flow (billion $)", min_value=0)
div = col1.number_input("2023 Dividends (billion $)", min_value=0)
mkt = col1.number_input("2023 Market Capitalization (billion $)", min_value=0)
current_price = col1.number_input("Current Price", min_value=0)

rev_h5 = col2.number_input("Revenue growth in next 5 years (%)", min_value=0)
rev_h10 = col2.number_input("Revenue growth in 5 to 10 years (%)", min_value=0)
fcf_m = col2.number_input("FCF margin", min_value=0)
r = col2.number_input("Discount rate", min_value=0)
t_m = col2.number_input("Terminal multiple", min_value=0)

# Create a data-frame with the REV-FCF-Div schedule.
schedule = []
# remaining_balance = loan_amount
rev_start = rev
div_fcf = div/fcf

for i in range(1, 11):
    if i <= 5:
        rev_f = rev_start * (1 + (rev_h5 / 100))
    else:
        rev_f = rev_start * (1 + (rev_h10 / 100))
        
    if i<11:
        fcf_f = rev_f * (fcf_m/100)
    else:
        fcf_f = rev_f * t_m

    div_s = fcf_f * ((1+(r/100))**(1-i-1))
    div_f = div_s * div_fcf
    rev_start = rev_f
    schedule.append(
        [
            i,
            rev_f,
            fcf_f,
            div_f,
        ]
    )

df = pd.DataFrame(schedule, columns=["Year", "Revenues", "Free Cash Flow", "Dividends"])

intrinsic_value = df["Dividends"].sum()
price_target = (current_price * intrinsic_value) / mkt

st.bar_chart(df)
st.success(str(intrinsic_value))
st.success(str(price_target))


