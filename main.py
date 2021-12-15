from mysql.connector import connect, Error


try:
    with connect(
        host="localhost",
        user='root',
        password='D2p96oMJ8Yrc1HDhSZDe',
        database="polyclinic",
    ) as connection:
        print(connection)
except Error as e:
    print(e)
