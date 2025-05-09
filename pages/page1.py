from navigation import make_sidebar
import streamlit as st
from datetime import datetime, timedelta
import fb_utils2 as fb
import pandas as pd

# saat refresh website, maka akan kembali ke halaman login
def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("Anda belum login. Mengarahkan ke halaman login...")
        #st.experimental_rerun()
        st.session_state.logged_in = False
        st.session_state.clear()
        st.switch_page("login.py")

# Panggil fungsi ini di awal setiap halaman
check_login()


@st.dialog("Date Error")
def date_error():
    st.write(f"The 'From' date must be before the 'To' date.")

hide_navigation_style = """
    <style>
    [data-testid="stSidebarNav"] > ul:first-child {
        display: none;
    }
    </style>
"""
st.markdown(hide_navigation_style, unsafe_allow_html=True)

make_sidebar()

st.title("📈Sales Analytics")

if 'idToken' in st.session_state and 'email' in st.session_state:
    idToken = st.session_state['idToken']
    user = st.session_state['email']
            
    st.header("Total Sales per Day🚀💸", divider="green")
    col1, col2 = st.columns(2)

    with col1:
        from_date_sales = st.date_input("From:", datetime.today() - timedelta(days=7), key="from_date_sales")  # Use datetime.date object

    with col2:
        to_date_sales = st.date_input("To:", datetime.today(), key="to_date_sales")

    if from_date_sales > to_date_sales:
        date_error()
    else:
        date, total = fb.get_sales(user, from_date_sales, to_date_sales)
        sales_data = pd.DataFrame({"Sales": total}, index=date)
        st.area_chart(sales_data)

    st.header("Menu Rankings🥤🥗🍔🍗🍟🥓", divider="red")
    col1, col2 = st.columns(2)

    with col1:
        from_date_menu = st.date_input("From:", datetime.today() - timedelta(days=7), key="from_date_menu")  # Use datetime.date object

    with col2:
        to_date_menu = st.date_input("To:", datetime.today(), key="to_date_menu")

    if from_date_menu > to_date_menu:
        if from_date_sales > to_date_sales:
            pass
        else:
            date_error()
    else:
        menu, counts = fb.get_menuranks(user, from_date_menu, to_date_menu)
        menuranks_data = pd.DataFrame({"Menu": menu, "Counts": counts})
        #menuranks_data = pd.DataFrame({"Counts":counts}, index=menu)
        excluded_menus = ["kamen rider", "turunan", "sia", "kamen faiz", "kamen raider"]
        menuranks_data = menuranks_data[~menuranks_data["Menu"].isin(excluded_menus)]
        menuranks_data.set_index("Menu", inplace=True)
        st.bar_chart(menuranks_data)
else:
    st.error("Anda belum login. Silakan login terlebih dahulu.")
    st.stop()