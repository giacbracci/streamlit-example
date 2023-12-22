import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import math

st.title("FEF Academy Stock Price Fair Value Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
rev = col1.number_input("2023 Revenues (billion $)", min_value=0, value=228.96)
fcf = col1.number_input("2023 Free Cash Flow (billion $)", min_value=0, value=9.56)
div = col1.number_input("2023 Dividends (billion $)", min_value=0, value=5.87)
mkt = col1.number_input("2023 Market Capitalization (billion $)", min_value=0, value=68.4)
current_price = col1.number_input("Current Price", min_value=0, value=11.19)

rev_h5 = col2.number_input("Revenue growth in next 5 years (%)", min_value=0, value=3)
rev_h10 = col2.number_input("Revenue growth in 5 to 10 years (%)", min_value=0, value=3)
fcf_m = col2.number_input("FCF margin", min_value=0, value=4)
r = col2.number_input("Discount rate", min_value=0, value=10)
t_m = col2.number_input("Terminal multiple", min_value=0, value=9)

# Create a data-frame with the REV-FCF-Div schedule.
schedule = []
# remaining_balance = loan_amount
rev_start = rev

for i in range(1, 11):
    if i < 6:
        rev_f = rev_start * (1+(rev_h5/100))
        fcf_f = rev_f * (fcf_m/100)
        div_f = fcf_f * (1+(r/100))^(i-2) * (div/fcf)
        rev_start = rev_f
    elif i > 6 and i < 11:
        rev_f = rev_start * (1+(rev_h5/100))
        fcf_f = rev_f * (fcf_m/100)
        div_f = fcf_f * (1+(r/100))^(i-2) * (div/fcf)
        rev_start = rev_f
    else:
        rev_f = rev_start
        fcf_f = rev_f * t_m
    schedule.append(
        [
            i,
            rev_f,
            fcf_f,
            div_f,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Year", "Revenues", "Free Cash Flow", "Dividends"],
    index_col=0
)

intrinsic_value = df["Dividends"].sum()
price_target = (current_price * intrinsic_value) / mkt

st.success(str(price_target))


