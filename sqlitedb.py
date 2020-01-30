import sqlite3
from tabulate import tabulate


class SqlDb:
    def __init__(self):
        self.connection = False
        self.table = False

    def connect(self, dbfile):
        self.host=dbfile
        try:
            self.db_connection = sqlite3.connect(dbfile)
            self.connection = True
        except Exception as e:
            print("Can't connect to the database:", e)

        if self.connection:
            self.my_cursor = self.db_connection.cursor()
            print("\nConnected to SQL server!\n.")

    def __str__(self):
        if self.connection:
            return self.host
        return "No connection to sql database."

    def disconnect(self):
        self.db_connection.close()
        print("Connection to db closed.")

    def list_sqltbl(self, tbl):
        if self.connection:
            sql = f"SELECT * FROM {tbl}"
            self.my_cursor.execute(sql)
            rows = list(self.my_cursor.fetchall())
            return rows

    def add_cost(self, table_name, args):
        if self.connection:
            sql = f"INSERT INTO {table_name} (DATE, DESCRIPTION, CATEGORY, SPENDINGS) VALUES {args};"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def add_income(self, table_name, args):
        if self.connection:
            sql = f"INSERT INTO {table_name} (DATE, DESCRIPTION, CATEGORY, INCOMES) VALUES {args};"
            #sql = f"INSERT INTO {table_name} (DATE, DESCRIPTION, CATEGORY, INCOMES) VALUES ('{arg[0]}', '{arg[1]}', '{arg[2]}', {arg[3]});"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def category(self, table_name):
        if self.connection:
            sql=f"SELECT DISTINCT CATEGORY FROM {table_name} ORDER BY CATEGORY ASC;"
            self.my_cursor.execute(sql)
        return tuple(x[0] for x in self.my_cursor.fetchall())

    def delete_row_spending(self, tbl, arg):
        if self.connection:
            sql = f"DELETE FROM {tbl} WHERE DATE='{arg[0]}' AND DESCRIPTION='{str(arg[1])}' AND CATEGORY='{str(arg[2])}' AND SPENDINGS='{arg[3]}';"
            print(sql)
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def delete_row_income(self, tbl, arg):
        if self.connection:
            sql = f"DELETE FROM {tbl} WHERE DATE='{arg[0]}' AND DESCRIPTION='{str(arg[1])}' AND CATEGORY='{str(arg[2])}' AND INCOMES='{arg[3]}';"
            self.my_cursor.execute(sql)
            self.db_connection.commit()

    def joint_result(self, tbl1, tbl2):
        if self.connection:
            sql1 = f"SELECT * FROM {tbl1}"
            sql2 = f"SELECT * FROM {tbl2}"
            res1 = self.my_cursor.execute(sql1)

            r1 =list(self.my_cursor.fetchall())
            res2 = self.my_cursor.execute(sql2)
            r2 = list(self.my_cursor.fetchall())
            r = r1+r2
        return r

    # def drop_table(self, table_name):
    #     if self.connection:
    #         self.my_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # def create_table(self, table_name, columns):
    #     self.table_name = table_name
    #     sql = f"CREATE TABLE {table_name} ({columns})"
    #     self.my_cursor.execute(sql)
    #     self.db_connection.commit()
    #     self.table = True

    # def insert_values(self, table_name, *args ):
    #     if table_name and self.connection:
    #         sql = f"INSERT INTO {table_name} VALUES {args};"
    #         self.my_cursor.execute(sql)
    #         self.db_connection.commit()
    #         print(f"{args} added")
    #     else:
    #         print(f"    {args} failed to add")

    # def read_table(self, table_name):
    #     if self.connection:
    #         sql_command = f"SELECT * FROM {table_name}"
    #         self.my_cursor.execute(f"SELECT * FROM {table_name}")
    #         rows = self.my_cursor.fetchall()

    # def action(self, todo):
    #     if self.connection:
    #         self.my_cursor.execute(todo)
    #         self.db_connection.commit()
    #         print(self.my_cursor.fetchall())
    #         print(tabulate(self.my_cursor.fetchall()))


#if __name__ == "__main__":
    # sql = SqlDb()
    # sql.connect('data.db')
    # sql.create_table("tbl_spendings", "ID INT PRIMARY KEY, DATE DATE NOT NULL, DESCRIPTION TEXT NOT NULL, CATEGORY TEXT NOT NULL, SPENDINGS TEXT NOT NULL")
    # sql.create_table("tbl_incomes", "ID INT PRIMARY KEY, DATE DATE NOT NULL, DESCRIPTION TEXT NOT NULL, CATEGORY TEXT NOT NULL, INCOMES TEXT NOT NULL")
    # sql.insert_values("tbl_spendings", '30','27-01-2020', 'Tankovanie','Auto' ,'-10.00')
    # sql.insert_values("tbl_incomes", '1', '27-01-2020', 'Mzda','Auto' ,'10.00')
    # sql.action('SELECT * FROM tbl_incomes;')
    # sql.disconnect()