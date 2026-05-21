import mysql.connector
from mysql.connector import Error


def write_and_print(file, text=""):
    print(text)
    file.write(str(text) + "\n")


try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD_HERE",
        database="project2"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        with open("output.txt", "w") as file:

            write_and_print(file, "Connected to MySQL database: project2")
            write_and_print(file, "")

            write_and_print(file, "1. Output from Titles table:")
            cursor.execute("SELECT * FROM titles")
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "2. Creating customer table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customer (
                    custID INT NOT NULL,
                    custName VARCHAR(50),
                    zip VARCHAR(10),
                    city VARCHAR(30),
                    state VARCHAR(30),
                    PRIMARY KEY (custID)
                )
            """)
            connection.commit()
            write_and_print(file, "Customer table created.")
            write_and_print(file, "")

            write_and_print(file, "3. Inserting customers...")
            customer_data = [
                (1, 'ABRAHAM SILBERSCHATZ', '10001', 'New York', 'NY'),
                (2, 'HENRY KORTH', '19104', 'Philadelphia', 'PA'),
                (3, 'CALVIN HARRIS', '90001', 'Los Angeles', 'CA'),
                (4, 'MARTIN GARRIX', '33101', 'Miami', 'FL'),
                (5, 'JAMES GOODWILL', '60601', 'Chicago', 'IL')
            ]

            cursor.executemany("""
                INSERT IGNORE INTO customer 
                (custID, custName, zip, city, state)
                VALUES (%s, %s, %s, %s, %s)
            """, customer_data)
            connection.commit()

            cursor.execute("SELECT * FROM customer")
            customers = cursor.fetchall()
            for customer in customers:
                write_and_print(file, customer)
            write_and_print(file, "")

            write_and_print(file, "4. Publisher(s) who have published the fewest titles:")
            cursor.execute("""
                SELECT p.pname, COUNT(t.titleID) AS title_count
                FROM publishers p
                LEFT JOIN titles t ON p.pubID = t.pubID
                GROUP BY p.pubID, p.pname
                HAVING title_count = (
                    SELECT MIN(title_count)
                    FROM (
                        SELECT COUNT(t2.titleID) AS title_count
                        FROM publishers p2
                        LEFT JOIN titles t2 ON p2.pubID = t2.pubID
                        GROUP BY p2.pubID
                    ) AS counts
                )
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "5. Authors and number of titles written:")
            cursor.execute("""
                SELECT a.aName, COUNT(ta.titleID) AS number_of_titles
                FROM authors a
                JOIN titleauthors ta ON a.auID = ta.auID
                GROUP BY a.auID, a.aName
                ORDER BY number_of_titles DESC
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "6. Titles written by exactly one author:")
            cursor.execute("""
                SELECT t.title
                FROM titles t
                JOIN titleauthors ta ON t.titleID = ta.titleID
                GROUP BY t.titleID, t.title
                HAVING COUNT(ta.auID) = 1
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "7. Publishers with at least one Hard Cover book priced above $450:")
            cursor.execute("""
                SELECT DISTINCT p.pname
                FROM publishers p
                JOIN titles t ON p.pubID = t.pubID
                WHERE t.cover = 'HARD COVER'
                  AND t.price > 450
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "8. Authors who wrote VISUAL BASIC.NET but not JAVA LANGUAGE:")
            cursor.execute("""
                SELECT DISTINCT a.aName
                FROM authors a
                JOIN titleauthors ta ON a.auID = ta.auID
                JOIN titles t ON ta.titleID = t.titleID
                JOIN subjects s ON t.subID = s.subID
                WHERE s.sName = 'VISUAL BASIC.NET'
                  AND a.auID NOT IN (
                      SELECT DISTINCT a2.auID
                      FROM authors a2
                      JOIN titleauthors ta2 ON a2.auID = ta2.auID
                      JOIN titles t2 ON ta2.titleID = t2.titleID
                      JOIN subjects s2 ON t2.subID = s2.subID
                      WHERE s2.sName = 'JAVA LANGUAGE'
                  )
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "9. Authors whose email address is from Gmail:")
            cursor.execute("""
                SELECT aName, email
                FROM authors
                WHERE email LIKE '%@GMAIL.COM'
            """)
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)
            write_and_print(file, "")

            write_and_print(file, "10. Updating prices:")
            cursor.execute("""
                UPDATE titles
                SET price = CASE
                    WHEN pubDate < '2003-01-01' THEN price * 0.95
                    WHEN pubDate > '2004-12-31' THEN price * 1.15
                    ELSE price
                END
            """)
            connection.commit()

            write_and_print(file, "Prices updated.")
            write_and_print(file, "Updated Titles table:")

            cursor.execute("SELECT * FROM titles")
            rows = cursor.fetchall()
            for row in rows:
                write_and_print(file, row)

except Error as e:
    print("Error while connecting to MySQL:", e)

finally:
    if "connection" in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")