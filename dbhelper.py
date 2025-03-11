import mysql.connector

class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='b122600Vaibhav',
                port=3306,
                database='indigo',
                auth_plugin='mysql_native_password'  # ✅ Force correct authentication plugin
            )
            self.mycursor = self.conn.cursor()
            print('✅ Connection established')
        except mysql.connector.Error as e:
            print(f'❌ Connection error: {e}')
            self.conn = None
            self.mycursor = None

    def fetch_city_names(self):
        """Fetch distinct city names from the flights table."""
        if self.mycursor is None:
            print('⚠️ Cursor is not initialized. Check database connection.')
            return []

        print('🔍 Fetching city names...')
        try:
            self.mycursor.execute('''
                SELECT DISTINCT Source FROM flights_cleaned_flights
                UNION 
                SELECT DISTINCT Destination FROM flights_cleaned_flights
            ''')
            data = self.mycursor.fetchall()
            city_list = [city[0] for city in data if city[0] is not None]

            print(f' Fetched cities: {city_list}')
            return city_list
        except mysql.connector.Error as e:
            print(f' Query error: {e}')
            return []

    def fetch_all_flights(self,source,destination):
        self.mycursor.execute('''
        SELECT Airline,Source,Destination,Route,Dep_Time,Price FROM flights_cleaned_flights
        WHERE Source ='{}' and Destination='{}' 
        '''.format(source,destination))

        data=self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline=[]
        frequency=[]
        self.mycursor.execute('''
         Select Airline,count(*) from flights_cleaned_flights 
         group by Airline ''')
        data=self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])


        return airline,frequency

    def busy_airport(self):
        city=[]
        frequency=[]
        self.mycursor.execute('''select Source,count(*) from(
				select Source from flights_cleaned_flights
				union all
			    select Destination from flights_cleaned_flights) t
                group by t.Source 
                order by count(*) desc''')
        data=self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            frequency.append(item[1])
        return city,frequency

    def daily_frequency(self):
        date=[]
        frequency=[]
        self.mycursor.execute('''
        SELECT Date_of_Journey ,count(*) from flights_cleaned_flights
        group by Date_of_Journey
        
        
        ''')

        data=self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            frequency.append(item[1])
        return date ,frequency

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.mycursor.close()
            self.conn.close()
            print('🔌 Database connection closed.')

# Run the script to test the database connection
if __name__ == "__main__":
    db = DB()
    cities = db.fetch_city_names()
    print(f'🌍 Available Cities: {cities}')
    db.close_connection()
