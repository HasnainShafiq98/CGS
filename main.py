import streamlit as st
from MultiappNav import MultiappNav
from Apps import ContentBaseFilter, Colabfiltering
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)')


def add_usersdata(username, password):
    c.execute('INSERT INTO users(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    data = c.fetchall()
    return data

def check_user(username):
    c.execute('select username from users where username =?', (username,))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    return data

def logSi():
        """
        Simple login app
        :return:
        """
        st.title("Cinematic Guidance System")
        menu = ["Home", "Login", "SignUp"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            st.subheader("Home")
        elif choice == "Login":
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("Password", type='password')
            if st.sidebar.checkbox("Login"):
                create_usertable()
                result = login_user(username, password)
                if result:
                    st.success("Logged in as {} ".format(username))
                    Colabfiltering.getuserId(username)
                    app = MultiappNav()
                    app.add_app("Colabarative Filtering",Colabfiltering.app)
                    app.add_app("Content Based Filtering",ContentBaseFilter.app)
                    app.run()
                else:
                    st.warning("Incorrect username/password")
        elif choice == "SignUp":
            st.subheader("Create a new account")
            new_user = st.text_input("User Name")
            new_password = st.text_input("Password", type='password')
            if st.button("Signup"):
                person = []
                person = check_user(new_user)
                if(len(person)!=0):
                    st.warning("username already exists please choose another username")
                    print(check_user(new_user))
                elif(len(person)== 0):
                    create_usertable()
                    add_usersdata(new_user, new_password)
                    st.success("You have successfully created an account")
                    st.info("Go to Menu to Login")


if __name__ == '__main__':
    logSi()