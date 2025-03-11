from sqlalchemy import create_engine
import pymysql

# ✅ Correct Credentials
username = "root"
password = "b122600Vaibhav@"  # Replace with your MySQL password
host = "127.0.0.1"
port = 3306  # Use the correct port
database = "indigo"

try:
    # ✅ Use 'pymysql' instead of 'mysqlconnector'
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

    # ✅ Test connection
    with engine.connect() as conn:
        print("✅ Connected to MySQL!")

    # ✅ Upload DataFrame to MySQL
    df.to_sql(name="flights", con=engine, if_exists="replace", index=False)
    print("✅ Data uploaded successfully!")

except Exception as e:
    print("❌ Connection failed:", e)
