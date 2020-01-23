from SQLbackbone import MySQLconnection
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date

LARGE_FONT = ("Comicsansms", 18)
ACTUAL_DATE = date.today().strftime("%Y-%m-%d")


# Baseline
class BudgetTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Tk.wm_title(self, 'Buget Tracker')
        tk.Tk.iconbitmap(self, 'wallet.ico')
        tk.Tk.geometry(self, '800x800')
        ttk.Style(self)

        ttk.Style.theme_use(self, 'xpnative')

        container = tk.Frame(self)
        container.place(x=0, y=0, width=800, height=800)
        # container.configure(bg='red')
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (DashBoard, Spending, Income, Plan):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.place(x=10, y=10, width=780, height=780)
            # frame.configure(bg='grey')
        self.show_frame(DashBoard)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class DashBoard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #sql = MySQLconnection()
        sql.connect(host="sql7.freesqldatabase.com", user="sql7320036", passwd="GeftKNBYht", db="sql7320036")
        sql.read_table("FINANCE")

        label = tk.Label(self, text="DASHBOARD", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)
        # MENU ======================================================================
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")

        button_dashboard = ttk.Button(self, image=dashboard_butt_photo, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        button_dashboard.image=dashboard_butt_photo
        button_spending = ttk.Button(self, image=spending_butt_photo, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        button_spending.image = spending_butt_photo
        button_income = ttk.Button(self, image=income_butt_photo, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        button_income.image = income_butt_photo
        button_plan = ttk.Button(self, image=plan_butt_photo, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        button_plan.image = plan_butt_photo
        button_dashboard.config()

        button_dashboard.place(x=20, y=0, width=200, height=50)
        button_spending.place(x=0, y=70, width=200, height=50)
        button_income.place(x=0, y=140, width=200, height=50)
        button_plan.place(x=0, y=210, width=200, height=50)
        # DASHBOARD ======================================================================
        # col_label_incomes = ttk.Label(self, text='INCOMES', font=('Comicsans',10,"bold"))
        # col_label_expenses = ttk.Label(self, text='EXPENSES', font=('Comicsans',10,"bold"))
        # col_label_balance = ttk.Label(self, text='BALANCE', font=('Comicsans',10,"bold"))
        # col_label_total = ttk.Label(self, text='TOTAL', font=('Comicsans',10,"bold"))
        # col_label_incomes.place(x=350, y=20)
        # col_label_expenses.place(x=450, y=20)
        # col_label_balance.place(x=550, y=20)
        # col_label_total.place(x=650, y=20)

        # TABLE ======================================================================
        table_dashboard = ttk.Treeview(self, height=6,selectmode="none", displaycolumns="#all")
        table_dashboard['columns'] = ("incomes", "expenses", "balance", "total")
        table_dashboard.heading("incomes", text="INCOMES")
        table_dashboard.heading("expenses", text="EXPENSES")
        table_dashboard.heading("balance", text="BALANCE")
        table_dashboard.heading("total", text="TOTAL")

        table_dashboard.column("#0", width=100, minwidth=100, stretch=tk.NO)
        table_dashboard.column("incomes", width=85, minwidth=85, stretch=tk.NO)
        table_dashboard.column("expenses", width=85, minwidth=85, stretch=tk.NO)
        table_dashboard.column("balance", width=85, minwidth=85, stretch=tk.NO)
        table_dashboard.column("total", width=85, minwidth=85, stretch=tk.NO)
        table_dashboard.tag_configure(self, background='red')

        table_dashboard.insert("", 0,text="January 2020")
        table_dashboard.insert("", 1,text="February 2020")
        table_dashboard.insert("", 2,text="March 2020")
        table_dashboard.insert("", 3,text="April 2020")
        table_dashboard.insert("", 4,text="February 2020")
        table_dashboard.insert("", 5,text="March 2020")
        table_dashboard.insert("", 6,text="April 2020")
        table_dashboard.insert("", 7,text="February 2020")
        table_dashboard.insert("", 8,text="March 2020")
        table_dashboard.insert("", 9,text="April 2020")

        table_dashboard.place(x=280, y=70)

        # date_row1 = ttk.Label(self, text="January 2020", font=('Comicsans',10,"bold"), justify='right',background='red', width=14)
        # date_row2 = ttk.Label(self, text="February 2020", font=('Comicsans',10,"bold"), justify='right',background='red', width=14)
        # date_row3 = ttk.Label(self, text="March 2020", font=('Comicsans',10,"bold"), justify='right',background='red', width=14)
        # date_row1.place(x=245, y=75)
        # date_row2.place(x=245, y=95)
        # date_row3.place(x=245, y=140)

class Spending(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="SPENDINGS", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)

        button_dashboard = ttk.Button(self, image=dashboard_butt_photo, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        button_dashboard.image=dashboard_butt_photo
        button_spending = ttk.Button(self, image=spending_butt_photo, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        button_spending.image = spending_butt_photo
        button_income = ttk.Button(self, image=income_butt_photo, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        button_income.image = income_butt_photo
        button_plan = ttk.Button(self, image=plan_butt_photo, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        button_plan.image = plan_butt_photo

        button_dashboard.place(x=0, y=0, width=200, height=50)
        button_spending.place(x=20, y=70, width=200, height=50)
        button_income.place(x=0, y=140, width=200, height=50)
        button_plan.place(x=0, y=210, width=200, height=50)

        spending_label_date = ttk.Label(self, text="Date")
        spending_label_category = ttk.Label(self, text="Category")
        spending_label_amount = ttk.Label(self, text="Amount")
        spending_label_description = ttk.Label(self, text="Description")
        spending_label_date.place(x=290, y=70)
        spending_label_description.place(x=435, y=70)
        spending_label_category.place(x=580, y=70)
        spending_label_amount.place(x=690, y=70)

        self.entry_field_date = ttk.Combobox(self)
        self.entry_field_description = ttk.Entry(self)
        self.entry_field_category = ttk.Combobox(self)
        self.entry_field_amount = ttk.Entry(self)

        self.entry_field_date.place(x=250, y=90, width=120)
        self.entry_field_description.place(x=372, y=90, width=180)
        self.entry_field_category.place(x=554, y=90, width=120)
        self.entry_field_amount.place(x=676, y=90, width=80)

        button_submit_entry = ttk.Button(self, text="SUBMIT", command=self.submitt)
        button_submit_entry.place(x=676, y=120)
        # HISTORY ========================================================
        self.table_spending_history = ttk.Treeview(self, height=16,selectmode="none", displaycolumns="#all")
        self.table_spending_history['columns'] = ("DATE", "DESCRIPTION", "CATEGORY", "AMOUNT")
        self.table_spending_history.heading("DATE", text="DATE")
        self.table_spending_history.heading("DESCRIPTION", text="DESCRIPTION")
        self.table_spending_history.heading("CATEGORY", text="CATEGORY")
        self.table_spending_history.heading("AMOUNT", text="AMOUNT")
        self.table_spending_history.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.table_spending_history.column("DATE", width=120, minwidth=120, stretch=tk.NO)
        self.table_spending_history.column("DESCRIPTION", width=185, minwidth=185, stretch=tk.NO)
        self.table_spending_history.column("CATEGORY", width=110, minwidth=110, stretch=tk.NO)
        self.table_spending_history.column("AMOUNT", width=90, minwidth=90, stretch=tk.NO)
        self.table_spending_history.tag_configure(self, background='red')
        self.table_spending_history.place(x=250, y=170)
        self.refresh_sqldata()

        # ENTRY ==========================================================
        self.entry_field_date.insert(0, ACTUAL_DATE)
    def submitt(self):
        #self.entry_field_date.insert(0, ACTUAL_DATE)
        #self.entry_field_description.delete(0, tk.END)
        #self.entry_field_description.insert(0, "")
        #self.entry_field_category.delete(0, tk.END)
        #self.entry_field_category.insert(0, "")
        #self.entry_field_amount.delete(0, tk.END)
        #self.entry_field_amount.insert(0, "0")

        get_entry_field_date = self.entry_field_date.get()
        get_entry_field_ddescription = self.entry_field_description.get()
        get_entry_field_category = self.entry_field_category.get()
        get_entry_field_amount = float(self.entry_field_amount.get())

        self.adding_spending(get_entry_field_date, get_entry_field_ddescription, get_entry_field_category, get_entry_field_amount)


        # ADD SQL DATA into FINANCE TABLE =============================
    def adding_spending(self, *args):
        #add check of list
        self.table_spending_history.delete(*self.table_spending_history.get_children())

        sql.add_spending(args)

        self.refresh_sqldata()

        # READ SQL DATA into SPENDING HISTORY =============================
    def refresh_sqldata(self):
        #self.table_spending_history.delete()
        val = sql.spending_history()
        for idx, v in reversed(list(enumerate(val, start=1))):
            self.table_spending_history.insert("", idx, values=v[1:])
        #table_spending_history.insert("", 0, values=["2020-01-01", "hello", "auto", 50.0])

class Income(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label1 = tk.Label(self, text="INCOME PAGE", font=LARGE_FONT)
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="INCOMES", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)

        button_dashboard = ttk.Button(self, image=dashboard_butt_photo, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        button_dashboard.image=dashboard_butt_photo
        button_spending = ttk.Button(self, image=spending_butt_photo, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        button_spending.image = spending_butt_photo
        button_income = ttk.Button(self, image=income_butt_photo, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        button_income.image = income_butt_photo
        button_plan = ttk.Button(self, image=plan_butt_photo, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        button_plan.image = plan_butt_photo

        button_dashboard.place(x=0, y=0, width=200, height=50)
        button_spending.place(x=0, y=70, width=200, height=50)
        button_income.place(x=20, y=140, width=200, height=50)
        button_plan.place(x=0, y=210, width=200, height=50)

class Plan(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="PLAN", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=420, y=10)

        button_dashboard = ttk.Button(self, image=dashboard_butt_photo, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        button_dashboard.image=dashboard_butt_photo
        button_spending = ttk.Button(self, image=spending_butt_photo, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        button_spending.image = spending_butt_photo
        button_income = ttk.Button(self, image=income_butt_photo, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        button_income.image = income_butt_photo
        button_plan = ttk.Button(self, image=plan_butt_photo, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        button_plan.image = plan_butt_photo

        button_dashboard.place(x=0, y=0, width=200, height=50)
        button_spending.place(x=0, y=70, width=200, height=50)
        button_income.place(x=0, y=140, width=200, height=50)
        button_plan.place(x=20, y=210, width=200, height=50)

sql = MySQLconnection()
app = BudgetTracker()
app.mainloop()
sql.mysql_disconnect()
