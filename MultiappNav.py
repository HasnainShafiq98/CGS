import streamlit as st

class MultiappNav:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func,
        })

    def run(self):
        # app = st.sidebar.radio(
        app = st.selectbox(
            'Select Colaborative or Content Based Filtering',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()



