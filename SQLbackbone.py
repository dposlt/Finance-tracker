import MySQLdb


class MySQLconnection:
    def __init__(self):
        self.connection = False
        self.table = False

    def connect(self, host, user, passwd, db):
        try:
            self.db_connection = MySQLdb.connect(host, user, passwd, db)
            self.connection = True
        except Exception as e:
            print("Can't connect to the database:", e)

        if self.connection:
            self.my_cursor = self.db_connection.cursor()
            print("\nConnected to SQL server!\n.")

    def drop_table(self, table_name):
        if self.connection:
            self.my_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

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
        self.db_connection.commit()
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


    def spending_history(self, tbl):
        if self.connection:
            sql_command = f"SELECT * FROM {tbl}"
            self.my_cursor.execute(sql_command)
            rows = list(self.my_cursor.fetchall())
            return rows

    def add_cost(self, table_name, args):
        if self.connection:
            sql = f"INSERT INTO {table_name} (DATE, DESCRIPTION, CATEGORY, SPENDING) VALUES {args};"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def add_income(self, table_name, args):
        if self.connection:
            sql = f"INSERT INTO {table_name} (DATE, DESCRIPTION, CATEGORY, INCOMES) VALUES {args};"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def mysql_disconnect(self):
        self.db_connection.close()
        print("Connection to db closed.")

    def category(self, table_name):
        if self.connection:
            sql=f"SELECT DISTINCT CATEGORY FROM {table_name} ORDER BY CATEGORY ASC;"
            self.my_cursor.execute(sql)
        return tuple(x[0] for x in self.my_cursor.fetchall())

    def delete_row(self, tbl, arg):
        if self.connection:
            sql = f"DELETE FROM tbl WHERE DATE=STR_TO_DATE('{arg[0]}', '%d-%m-%Y') AND DESCRIPTION='{str(arg[1])}' AND CATEGORY='{str(arg[2])}' AND AMOUNT='{arg[3]}';"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def action(self, todo):
        if self.connection:
            self.my_cursor.execute(todo)
            self.db_connection.commit()
            print(self.my_cursor.fetchall())

if __name__ == "__main__":
    sqlconnection = MySQLconnection()
    connection = sqlconnection.connect(host="sql7.freesqldatabase.com", user="sql7320036", passwd="GeftKNBYht", db="sql7320036")
    if sqlconnection.connection:
        #sqlconnection.drop_table("budget")
        #sqlconnection.create_table("tbl_incomes", "ID INT PRIMARY KEY AUTO_INCREMENT, DATE DATE NOT NULL, DESCRIPTION VARCHAR(25) NOT NULL, CATEGORY VARCHAR(10) NOT NULL, INCOMES FLOAT DEFAULT 0.00")

        #sqlconnection.insert_values("budget", '1', '27-01-2020', 'Tankovanie','Auto' ,'10.00')
        #sqlconnection.insert_values("budget", '2', '26-01-2020','Tesco nakup','Potraviny' ,'4.50')

        # sqlconnection.read_table("FINANCE")
        #print(sqlconnection.spending_history())
        sqlconnection.action('SHOW COLUMNS FROM tbl_spendings;')
        #sqlconnection.action('DELETE FROM budget WHERE ID=6;')
        #print(sqlconnection.category())
        sqlconnection.mysql_disconnect()
