import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

# Initialize Database
db = DB()

# Sidebar Menu
st.sidebar.title('✈️ Flights Analytics')
user_option = st.sidebar.selectbox('📌 Menu', ['Select One', 'Check Flights', 'Analytics'])

# Check Flights Section
if user_option == 'Check Flights':
    st.title('🔍 Check Flights')

    col1, col2 = st.columns(2)

    # Fetch City Names
    city = db.fetch_city_names()

    if not city:
        st.warning('⚠️ No cities found in the database. Please check the database connection or data.')
        city = ['No cities available']  # Prevents empty list issues

    with col1:
        source = st.selectbox('🌍 Source', city)
    with col2:
        destination = st.selectbox('🌍 Destination', city)

    # Search Flights
    if st.button('Search'):
        if source == destination:
            st.error("⚠️ Source and Destination cannot be the same!")
        else:
            results = db.fetch_all_flights(source, destination)
            if results:
                st.dataframe(results)
            else:
                st.warning("❌ No flights found for the selected route.")

# Analytics Section
elif user_option == 'Analytics':
    st.title("📊 Flight Analytics")

    # Pie Chart: Airline Frequency
    airline, frequency = db.fetch_airline_frequency()
    if not airline or not frequency:
        st.warning("⚠️ No airline frequency data available.")
    else:
        fig = go.Figure(go.Pie(labels=airline, values=frequency, hoverinfo='label+percent', textinfo='value'))
        st.header('📊 Airline Frequency Distribution')
        st.plotly_chart(fig)

    # Bar Chart: Busiest Airports
    city, flight_count = db.busy_airport()
    if not city or not flight_count:
        st.warning("⚠️ No airport traffic data available.")
    else:
        fig = px.bar(x=city, y=flight_count, labels={'x': 'Airport', 'y': 'Flights Count'},
                     title='🏙️ Busiest Airports', text_auto=True)
        st.header('📈 Busiest Airports')
        st.plotly_chart(fig, use_container_width=True)


    # daily number of flights frequency
    date, daily_number_of_flights = db.daily_frequency()

    if not date or not daily_number_of_flights:
        st.warning("⚠️ No flights data available")
    else:
        fig = px.line(
            x=date, y=daily_number_of_flights,
            labels={'x': 'Date', 'y': 'Flights Count'},
            title='📅 Daily Number of Flights'
        )
        st.header('📈 Daily Number of Flights')
        st.plotly_chart(fig, use_container_width=True)


# Default Section (Project Information)
else:
    st.title('ℹ️ About This Project')
    st.write("""
    This project provides an interactive platform for analyzing flight data, 
    searching for available flights, and understanding airline trends. 
    The analytics section offers insights into the busiest airports and airline frequency.
    """)

