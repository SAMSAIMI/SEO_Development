# -*- coding: utf-8 -*-
# This build is to create webpage via frameworks of streamlit
# initial release 2023 by sasamsa

# from archiva import ArchivaClient, ArchivaException
import pandas as pd
from pathlib import Path
import streamlit as st
import hydralit_components as hc
from streamlit_extras.colored_header import colored_header
from datetime import date, time

pd.set_option("display.expand_frame_repr", False)
st.set_page_config(
    layout="wide",
    page_title="Satellite Operations",
    page_icon="💹",
    initial_sidebar_state="collapsed",
)


class SatelliteEnginerringOperation:
    # class attributes axcess by
    base_dirs = Path(__file__).resolve().parent

    def __init__(self, *args, **kwargs):
        self.todayDate = date.today()
        seo = SatelliteEnginerringOperation
        self.prediction = pd.read_csv(seo.base_dirs / "configuration/eclipse_prediction_from_2009_2032_complete.csv")

    def loadingPage(self, satId, launch):
        predict = self.prediction
        C1, C2, C3, C4 = st.columns((2, 2, 2, 2), gap="large")

        with C2:
            # st.write("<br>", unsafe_allow_html=True)
            unique_event_types = predict["Event_type"].unique().tolist()
            unique_event_types.insert(0, "Event Type")
            eventType = st.selectbox(
                "**Event Type**",
                unique_event_types,
                label_visibility="hidden",
            )
        with C3:
            # st.write("<br>", unsafe_allow_html=True)
            opsdate = st.date_input(
                label="Choose Event Date",
                value=None,
                # value= today - timedelta(days=1),
                min_value=pd.to_datetime(launch),
                max_value=self.todayDate,
                on_change=None,
                label_visibility="hidden",
            )

            df = predict.copy()
            df["Event_Start_Time"] = pd.to_datetime(df["Event_Start_Time"])
            df["Date"] = df["Event_Start_Time"].dt.date
            df = df[(df["Date"] == opsdate) & (df["Event_type"] == eventType)]
            print(df)

        colored_header(
            label=f"**{satId} Eclipse Data**",
            description="",
            color_name="violet-80",
        )

        if eventType == "Event Type":
            st.stop()

        if df.empty:
            st.write("No event registered on this date")
            st.markdown(
                f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">"No event registered on this date"</p>',
                unsafe_allow_html=True,
            )
            st.stop()

    def mainpage(self):
        st.write("<br>", unsafe_allow_html=True)
        menu_data = [
            {
                "id": "geo_event",
                "icon": "🌗",
                "label": "Eclipse Page",
                "submenu": [
                    {
                        "id": "m3aeclips",
                        "label": "M3A",
                    },
                    {
                        "id": "m3beclips",
                        "label": "M3B",
                    },
                    {
                        "id": "m3declips",
                        "label": "M3D",
                    },
                ],
            },
            {"id": "cdm_page", "icon": "💥", "label": "CDM"},
            {
                "id": "trending",
                "icon": "📊",
                "label": "SO Trend",
                "submenu": [
                    {
                        "id": "m3atrend",
                        "label": "M3A",
                    },
                    {
                        "id": "m3btrend",
                        "label": "M3B",
                    },
                    {
                        "id": "m3dtrend",
                        "label": "M3D",
                    },
                ],
            },  # no tooltip message
            {
                "id": "reporting",
                "icon": "🖨️",
                "label": "SO Report",
                "submenu": [
                    {
                        "label": "M3A",
                    },
                    {
                        "label": "M3B",
                    },
                    {
                        "label": "M3D",
                    },
                ],
            },
        ]

        over_theme = {"txc_inactive": "#FFFFFF"}
        menu_id = hc.nav_bar(
            menu_definition=menu_data,
            override_theme=over_theme,
            home_name="Home",
            # login_name='Logout',
            hide_streamlit_markers=False,  # disable humberger menu and info icon
            sticky_nav=True,  # at the top or not
            sticky_mode="pinned",  # ['sticky', 'pinned']
        )

        if menu_id == "Home":
            st.write("Welcome to SEO Homepage testing hydralit-component ")
        if menu_id == "geo_event":
            st.write("Eclipse section")

        if menu_id == "m3aeclips":
            SAT_ID = "M3A"
            Launch = "2009-06-01"
            self.loadingPage(SAT_ID, Launch)

            st.write("M3A Eclipse Section")
            st.write("** 🚧 Site Under Construction 🚧")

        if menu_id == "m3beclips":
            SAT_ID = "M3B"
            Launch = "2014-09-14"
            self.loadingPage(SAT_ID, Launch)

            st.write("M3B Eclipse Section")
            st.write("** 🚧 Site Under Construction 🚧")

        if menu_id == "m3declips":
            SAT_ID = "M3D"
            Launch = "2022-06-22"
            self.loadingPage(SAT_ID, Launch)

            st.write("M3D Eclipse Section")
            st.write("** 🚧 Site Under Construction 🚧")


if __name__ == "__main__":
    seo = SatelliteEnginerringOperation()
    seo.mainpage()
