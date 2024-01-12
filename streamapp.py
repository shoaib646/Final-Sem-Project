import streamlit as st
import datetime
import os
from TrafficData.TrafficFlowPredictor import *
import route_finding as router

class Window:
    def __init__(self):
        self.windowTitle = st.set_page_config(page_title="Maple's Window")
        self.title = st.markdown("## Optimal Path Finder")
        self.developers = st.markdown("#### Developed by: [Shoaib Ahmed](https://www.cruzai.tech)")
        self.model = st.selectbox("Model:", [option.value for option in TrafficFlowModelsEnum])
        self.src = st.text_input("Source:", "")
        self.dest = st.text_input("Destination:", "")
        self.date_string = st.text_input("Date | Time:", "")

        if st.button("Generate"):
            self.run()        
        if st.button("View on Map"):
            self.view_routes()

        self.pred = st.text_input("Predict route Traffic Flow:")
        if st.button("Predict"):
            self.predict_flow()

    def parse_date(self, date_string):
        try:
            date = datetime.datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            date = datetime.datetime.now()
        return date

    def run(self):
        st.text("Generating Routes...")
        src = self.src
        dest = self.dest
        if src == '' or dest == '':
            st.text("Please enter Route ID")
            return
        routes = router.runRouter(src, dest, self.parse_date(self.date_string), self.model)
        self.set_text_box(routes)

    def set_text_box(self, text):
        st.text(text)

    def view_routes(self):
        map_html = open("index.html", "r").read()
        st.components.v1.html(map_html, height=600)
        

    def predict_flow(self):
        st.text("Predicting...")
        point = str(self.pred)

        if point == '':
            st.text("Please enter Route ID")
            return

        predictor = TrafficFlowPredictor()
        date = self.parse_date(self.date_string)
        try:
            flow = predictor.predict_traffic_flow(point, date, 4, self.model)
        except:
            st.text("Invalid Route ID")
            return

        st.text(f"--Predicted Traffic Flow--\nRoute_ID:\t\t{point}\nTime:\t\t{date.strftime('%Y/%m/%d %I:%M:%S')}\nPrediction:\t\t{str(flow)}veh/hr")


if __name__ == "__main__":
    window = Window()
