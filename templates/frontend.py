import streamlit as st
from PIL import Image
from io import BytesIO
import requests


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       Global
    ------------------------------------------------------- */

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* -------------------------------------------------------
       Header
    ------------------------------------------------------- */

    .hero {
        position: relative;
        height: 390px;
        border-radius: 24px;
        overflow: hidden;

        background:
            linear-gradient(
                90deg,
                rgba(4, 18, 38, 0.90),
                rgba(4, 18, 38, 0.45)
            ),
            url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1800&q=85");

        background-size: cover;
        background-position: center;

        display: flex;
        align-items: center;
        padding: 55px;
        margin-bottom: 30px;
    }

    .hero-content {
        color: white;
        max-width: 650px;
    }

    .hero-small {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #8ed8ff;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 18px;
    }

    .hero-description {
        font-size: 19px;
        line-height: 1.6;
        color: #e4edf7;
    }


    /* -------------------------------------------------------
       Search Box
       ------------------------------------------------------- */

    .search-container {
        background: white;
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.07);
        margin-bottom: 35px;
    }

    .search-title {
        font-size: 25px;
        font-weight: 700;
        color: #152238;
        margin-bottom: 5px;
    }

    .search-subtitle {
        color: #667085;
        margin-bottom: 20px;
    }


    /* -------------------------------------------------------
       Flight cards
       ------------------------------------------------------- */

    .flight-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 18px;
        border: 1px solid #e8ecf2;
        box-shadow: 0 6px 20px rgba(0,0,0,0.045);
    }

    .airline {
        font-size: 18px;
        font-weight: 700;
        color: #172033;
    }

    .flight-number {
        font-size: 13px;
        color: #8993a4;
        margin-top: 4px;
    }

    .airport-code {
        font-size: 30px;
        font-weight: 800;
        color: #16243a;
    }

    .airport-time {
        font-size: 15px;
        color: #697586;
    }

    .route-line {
        color: #3b82f6;
        font-size: 24px;
        text-align: center;
    }

    .duration {
        text-align: center;
        font-size: 13px;
        color: #667085;
    }

    .stops {
        text-align: center;
        font-size: 12px;
        color: #98a2b3;
    }

    .price {
        font-size: 26px;
        font-weight: 800;
        color: #0f766e;
        text-align: right;
    }

    .price-label {
        font-size: 12px;
        color: #98a2b3;
        text-align: right;
    }


    /* -------------------------------------------------------
       AI Advice
       ------------------------------------------------------- */

    .advice {
        background: linear-gradient(
            135deg,
            #eff6ff,
            #f0fdfa
        );

        border: 1px solid #dbeafe;
        border-radius: 20px;

        padding: 25px;

        margin-top: 25px;
        margin-bottom: 30px;
    }

    .advice-title {
        font-size: 19px;
        font-weight: 700;
        color: #164e63;
        margin-bottom: 8px;
    }

    .advice-text {
        color: #475467;
        line-height: 1.6;
    }


    /* -------------------------------------------------------
       Section headings
       ------------------------------------------------------- */

    .section-title {
        font-size: 28px;
        font-weight: 750;
        color: #152238;
        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* -------------------------------------------------------
       Footer
       ------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #98a2b3;
        margin-top: 50px;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-small">
                AI POWERED TRAVEL ASSISTANT
            </div>
            <div class="hero-title">
                Your journey starts here.
            </div>
            <div class="hero-description">
                Tell us where you want to go and let AI help you
                discover flights, compare options and plan your trip.
            </div>
        </div>
    </div>
    """,unsafe_allow_html=True,
)


# ============================================================
# SEARCH
# ============================================================

st.markdown("""
    <div class="search-container">
        <div class="search-title">
            ✈️ What can I help you plan?
        </div>
        <div class="search-subtitle">
            Ask naturally. For example:
            "Find me the best flights from Delhi to London next Friday."
        </div>
    </div>
    """, unsafe_allow_html=True
)


query = st.text_area(
    label="Trip query",
    placeholder=(
        "Example: Find me flights from Delhi to London "
        "next Friday. I prefer fewer stops and morning departures."
    ),
    height=100,
    label_visibility="collapsed",
)


# ============================================================
# SEARCH BUTTON
# ============================================================

search_clicked = st.button(
    "✈️  Search Flights",
    type="primary",
    use_container_width=True,
)


# ============================================================
# MOCK FLIGHT DATA
#
# Replace this section with your AI agent/tool.
# ============================================================

def get_flight_results(user_query: str):

    # --------------------------------------------------------
    # TODO:
    #
    # Replace this function with:
    #
    # result = your_agent.invoke(user_query)
    #
    # --------------------------------------------------------

    return [
        {
            "airline": "Air India",
            "flight_number": "AI 101",
            "origin": "DEL",
            "origin_time": "10:30",
            "destination": "LHR",
            "destination_time": "15:45",
            "duration": "9h 45m",
            "stops": "1 stop",
            "price": "₹45,200",
        },
        {
            "airline": "Emirates",
            "flight_number": "EK 513",
            "origin": "DEL",
            "origin_time": "04:15",
            "destination": "LHR",
            "destination_time": "13:20",
            "duration": "10h 35m",
            "stops": "1 stop",
            "price": "₹48,600",
        },
        {
            "airline": "British Airways",
            "flight_number": "BA 142",
            "origin": "DEL",
            "origin_time": "01:35",
            "destination": "LHR",
            "destination_time": "06:10",
            "duration": "10h 05m",
            "stops": "Direct",
            "price": "₹57,800",
        },
    ]


# ============================================================
# DISPLAY RESULTS
# ============================================================

if search_clicked:

    if not query.strip():

        st.warning(
            "Please enter a trip request first."
        )

    else:

        with st.spinner(
            "✈️ Searching flights and planning your trip..."
        ):

            flights = get_flight_results(query)

        st.markdown(
            '<div class="section-title">✨ Recommended Flights</div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # AI ADVICE
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="advice">

                <div class="advice-title">
                    🤖 AI Trip Advice
                </div>

                <div class="advice-text">
                    I found several flight options for your trip.
                    If your priority is minimizing travel time,
                    the direct option is worth considering.
                    If price is more important, the connecting
                    options may offer better value.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # FLIGHT CARDS
        # ----------------------------------------------------

        for flight in flights:

            st.markdown("""
                <div class="flight-card">

                    <div style="display:flex;justify-content:space-between; align-items:center">
                        <div>
                            <div class="airline">
                                {flight["airline"]}
                            </div>

                            <div class="flight-number">
                                {flight["flight_number"]}
                            </div>

                        </div>

                        <div>

                            <div class="price">
                                {flight["price"]}
                            </div>

                            <div class="price-label">
                                per traveller
                            </div>

                        </div>

                    </div>


                    <div style= "display:grid; grid-template-columns:1fr 1fr 1fr; "
                                "gap:20px; align-items:center; margin-top:25px;">

                        <div>

                            <div class="airport-code">
                                {flight["origin"]}
                            </div>

                            <div class="airport-time">
                                {flight["origin_time"]}
                            </div>

                        </div>


                        <div>

                            <div class="route-line">
                                # <p>───── ✈ ─────</p>
                            </div>

                            <div class="duration">
                                {flight["duration"]}
                            </div>

                            <div class="stops">
                                {flight["stops"]}
                            </div>

                        </div>


                        <div style="text-align:right">

                            <div class="airport-code">
                                {flight["destination"]}
                            </div>

                            <div class="airport-time">
                                {flight["destination_time"]}
                            </div>

                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            # Button outside HTML so Streamlit can handle it.
            if st.button(
                f"View {flight['flight_number']}",
                key=f"flight_{flight['flight_number']}",
            ):
                st.info(
                    f"You selected {flight['airline']} "
                    f"{flight['flight_number']}."
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ✈️ AI Trip Planner · Flight information powered by your
        configured flight data provider
    </div>
    """,
    unsafe_allow_html=True,
)