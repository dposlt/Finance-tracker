# -*- coding: utf-8 -*-

import MySQLdb


class MySQLconnection:
    def __init__(self):
        self.connection = False
        self.table = False

    # Open database connection, list to CLI the available tables in the db
    def connect(self, host, user, passwd, db):
        try:
            self.db_connection = MySQLdb.connect(host, user, passwd, db)
            self.connection = True
        except Exception as e:
            print("Can't connect to the database:", e)

        if self.connection:
            self.my_cursor = self.db_connection.cursor()
            print("\nConnected to SQL server!\n.")
            # self.my_cursor.execute("SHOW TABLES")
            # self.tables = self.my_cursor.fetchall()[0]
            # print(f"Available tables in db: {self.tables}\n.")

    # Drop table
    def drop_table(self, table_name):
        if self.connection:
            self.my_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create table
    def create_table(self, table_name, columns):
        """Creating table in the SQL database.

        Args:
            columns: "Coloumn1 Type1 Key|Default, Coloumn1 Type1 Key|Default, ..."
        [
            "ID INT PRIMARY KEY", "DESCRIPTION CHAR(25) NOT NULL", "PRICE FLOAT DEFAULT 0.00"
        ]
        """
        self.table_name = table_name
        sql = f"CREATE TABLE {table_name} ({columns})"
        self.my_cursor.execute(sql)
        self.table = True

    def insert_values(self, table_name, *args ):
        r"""Insert values to the table.
            e.g.
            insert_values("TABLE name",
            "value1", "value2", "value3"...)"""

        if table_name in self.tables and self.connection:
            sql = f"INSERT INTO {table_name} VALUES {args};"
            self.my_cursor.execute(sql)
            self.db_connection.commit()
            print(f"{args} added")
        else:
            print(f"    {args} failed to add")

    def read_table(self, table_name):
        """Read the conent of the table to the CLI"""

        if self.connection:
            sql_command = f"SELECT * FROM {table_name}"
            self.my_cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.my_cursor.fetchall()
            print(f"{table_name} table content using: '{sql_command}'")

            for row in rows:
                print(row)

    def spending_history(self):
        if self.connection:
            sql_command = f"SELECT * FROM FINANCE"
            self.my_cursor.execute(sql_command)
            rows = list(self.my_cursor.fetchall())
            
            return rows

    def add_spending(self, args):
        if self.connection:
            sql = f"INSERT INTO FINANCE(DATE, DESCRIPTION, CATEGORY, AMOUNT) VALUES {args};"
            print(sql)
            self.my_cursor.execute(sql)
            self.db_connection.commit()
            print(f"Values {args} added.")

    def mysql_disconnect(self):
        self.db_connection.close()
        print("Connection to db closed.")

    # def actions(self):
    #     if self.connection:
    #         sql = f"CREATE TABLE {table_name} ({columns})"
    #         self.my_cursor.execute(sql)
if __name__ == "__main__":
    sqlconnection = MySQLconnection()
    connection = sqlconnection.connect(host="sql7.freesqldatabase.com", user="sql7320036", passwd="GeftKNBYht", db="sql7320036")
    if sqlconnection.connection:
        #sqlconnection.drop_table("TRACKER")
        #sqlconnection.create_table("FINANCE", "ID INT PRIMARY KEY, DATE DATE NOT NULL, DESCRIPTION VARCHAR(25) NOT NULL, CATEGORY VARCHAR(10) NOT NULL, AMOUNT FLOAT DEFAULT 0.00")


        #sqlconnection.insert_values("FINANCE", '1', '01-01-2020', 'Tankovanie','Auto' ,'10.00')
        #sqlconnection.insert_values("FINANCE", '2', '02-01-2020','Tesco nakup','Potraviny' ,'4.50')

        # sqlconnection.read_table("FINANCE")
        sqlconnection.spending_history()

        sqlconnection.mysql_disconnect()
