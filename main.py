from SQLbackbone import MySQLconnection
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import datetime
import re

LARGE_FONT = ("Comicsansms", 18)
ACTUAL_DATE = date.today().strftime("%d-%m-%Y")



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
        sql.connect(host="sql7.freesqldatabase.com", user="sql7320036", passwd="GeftKNBYht", db="sql7320036")
        sql.read_table("budget")

        label = tk.Label(self, text="DASHBOARD", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)
        # MENU ======================================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_plan_pci = tk.PhotoImage(file="img\\plan_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_plan = ttk.Button(self, image=btn_plan_pci, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        btn_plan.image = btn_plan_pci
        btn_dashboard.config()

        btn_dashboard.place(x=20, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_plan.place(x=0, y=210, width=200, height=50)

        # TABLE ======================================================================
        tv_dashboard = ttk.Treeview(self, height=6,selectmode="none", displaycolumns="#all")
        tv_dashboard['columns'] = ("incomes", "expenses", "balance", "total")
        tv_dashboard.heading("incomes", text="INCOMES")
        tv_dashboard.heading("expenses", text="EXPENSES")
        tv_dashboard.heading("balance", text="BALANCE")
        tv_dashboard.heading("total", text="TOTAL")

        tv_dashboard.column("#0", width=100, minwidth=100, stretch=tk.NO)
        tv_dashboard.column("incomes", width=85, minwidth=85, stretch=tk.NO)
        tv_dashboard.column("expenses", width=85, minwidth=85, stretch=tk.NO)
        tv_dashboard.column("balance", width=85, minwidth=85, stretch=tk.NO)
        tv_dashboard.column("total", width=85, minwidth=85, stretch=tk.NO)
        tv_dashboard.tag_configure(self, background='red')

        tv_dashboard.insert("", 0,text="January 2020")
        tv_dashboard.insert("", 1,text="February 2020")
        tv_dashboard.insert("", 2,text="March 2020")
        tv_dashboard.insert("", 3,text="April 2020")
        tv_dashboard.insert("", 4,text="February 2020")
        tv_dashboard.insert("", 5,text="March 2020")
        tv_dashboard.insert("", 6,text="April 2020")
        tv_dashboard.insert("", 7,text="February 2020")
        tv_dashboard.insert("", 8,text="March 2020")
        tv_dashboard.insert("", 9,text="April 2020")

        tv_dashboard.place(x=280, y=70)

class Spending(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.lbl_alert = tk.Label(self, text="", fg='red')
        self.lbl_alert.place(x=250, y= 135)

        # LEFT PANEL ==============================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_plan_pci = tk.PhotoImage(file="img\\plan_button_sm.png")

        header_lbl = tk.Label(self, text="SPENDINGS", font=("Helvetica", 24, "bold"), foreground="darkblue")
        header_lbl.place(x=400, y=10)

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_plan = ttk.Button(self, image=btn_plan_pci, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        btn_plan.image = btn_plan_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=20, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_plan.place(x=0, y=210, width=200, height=50)

        # ENTRY FIELD ============================================================
        lbl_sp_date = ttk.Label(self, text="Date")
        lbl_sp_category = ttk.Label(self, text="Category")
        lbl_sp_amount = ttk.Label(self, text="Amount")
        lbl_sp_description = ttk.Label(self, text="Description")
        lbl_sp_date.place(x=290, y=70)
        lbl_sp_description.place(x=435, y=70)
        lbl_sp_category.place(x=580, y=70)
        lbl_sp_amount.place(x=690, y=70)
        self.ent_field_date = ttk.Entry(self, justify="center")
        self.ent_field_description = ttk.Entry(self)
        self.ent_field_category = ttk.Combobox(self)
        self.ent_field_category.config(values=sql.category('budget'))
        self.ent_field_amount = ttk.Entry(self)
        self.ent_field_date.place(x=250, y=90, width=120)
        self.ent_field_description.place(x=372, y=90, width=180)
        self.ent_field_category.place(x=554, y=90, width=120)
        self.ent_field_amount.place(x=676, y=90, width=80)

        # SUBMIT button =============================================================
        btn_submit_entry = ttk.Button(self, text="SUBMIT", command=self.submitt)
        btn_submit_entry.place(x=676, y=120)
        # SPENDING HISTORY ========================================================
        self.tv_spending_history = ttk.Treeview(self, height=16, selectmode="browse", displaycolumns="#all")
        self.tv_spending_history['columns'] = ("DATE", "DESCRIPTION", "CATEGORY", "AMOUNT")
        self.tv_spending_history.heading("DATE", text="DATE")
        self.tv_spending_history.heading("DESCRIPTION", text="DESCRIPTION")
        self.tv_spending_history.heading("CATEGORY", text="CATEGORY")
        self.tv_spending_history.heading("AMOUNT", text="AMOUNT")
        self.tv_spending_history.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tv_spending_history.column("DATE", width=120, minwidth=120, stretch=tk.NO)
        self.tv_spending_history.column("DESCRIPTION", width=185, minwidth=185, stretch=tk.NO)
        self.tv_spending_history.column("CATEGORY", width=110, minwidth=110, stretch=tk.NO)
        self.tv_spending_history.column("AMOUNT", width=90, minwidth=90, stretch=tk.NO)
        self.tv_spending_history.tag_configure(self, background='red')
        self.tv_spending_history.place(x=250, y=170)
        self.treeScroll = ttk.Scrollbar(self, command=self.tv_spending_history.yview)
        self.treeScroll.place(x=758, y=170, height=345)
        self.tv_spending_history.configure(yscrollcommand=self.treeScroll.set)
        self.refresh_sqldata()
        # DEFAULT ACTUAL DATE =============================================
        self.ent_field_date.insert(0, ACTUAL_DATE)
        # Press ENTER to run submit =======================================
        self.ent_field_amount.bind('<Return>', lambda x: self.submitt())
        # Delete SELECTION
        self.tv_spending_history.bind('<Delete>', lambda x: self.delete_row())
        # remark under spending history
        self.lbl_remark=ttk.Label(self, text='! Select row and press DELETE key to delete', foreground='blue')
        self.lbl_remark.place(x=250, y=520)
        
    def delete_row(self):
        self.selected_row = self.tv_spending_history.selection()
        self.subject = self.tv_spending_history.item(self.selected_row)['values']
        sql.delete_row(self.subject)
        self.refresh_sqldata()

    def submitt(self):
        get_entry_field_date = self.ent_field_date.get()
        get_entry_field_amount = self.ent_field_amount.get()
        date_format_valid = re.match("^\s*(3[01]|[12][0-9]|0?[1-9])\-(1[012]|0?[1-9])\-((?:19|20)\d{2})\s*$", get_entry_field_date)
        amount_format_valid = re.match("^\d*\.?\d*$", get_entry_field_amount)
        if date_format_valid:
            dt = datetime.datetime.strptime(get_entry_field_date, '%d-%m-%Y').strftime('%Y,%m,%d')
            get_entry_field_date = dt
        else:
            self.lbl_alert['text'] = "Wrong format of Date"
        if amount_format_valid:
            get_entry_field_amount = float(self.ent_field_amount.get())
        else:
            self.lbl_alert['text'] = "Wrong format of Amount"
        get_entry_field_ddescription = self.ent_field_description.get()
        get_entry_field_category = self.ent_field_category.get().upper()
        if amount_format_valid and date_format_valid and get_entry_field_ddescription and get_entry_field_category:
            self.lbl_alert['text'] = " "
            self.adding_spending(get_entry_field_date, get_entry_field_ddescription, get_entry_field_category, get_entry_field_amount)
            self.ent_field_category.config(values=sql.category('budget'))

            self.ent_field_amount.delete(0, tk.END)
            self.ent_field_category.delete(0, tk.END)
            self.ent_field_description.delete(0, tk.END)
        self.ent_field_description.focus()

        # ADD SQL DATA into FINANCE TABLE =============================
    def adding_spending(self, *args):
        #add check of list
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        sql.add_spending("budget",args)
        self.refresh_sqldata()

        # READ SQL DATA into SPENDING HISTORY =============================
    def refresh_sqldata(self):
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        val = sql.spending_history()
        for idx, v in reversed(list(enumerate(val, start=1))):
            v_list = [x for x in v]
            v_list[1] = datetime.datetime.strftime(v_list[1],"%d-%m-%Y")
            self.tv_spending_history.insert("", idx, values=v_list[1:])


class Income(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label1 = tk.Label(self, text="INCOME PAGE", font=LARGE_FONT)
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_plan_pci = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="INCOMES", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_plan = ttk.Button(self, image=btn_plan_pci, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        btn_plan.image = btn_plan_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=20, y=140, width=200, height=50)
        btn_plan.place(x=0, y=210, width=200, height=50)

class Plan(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_plan_pci = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="PLAN", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=420, y=10)

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_plan = ttk.Button(self, image=btn_plan_pci, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        btn_plan.image = btn_plan_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_plan.place(x=20, y=210, width=200, height=50)

sql = MySQLconnection()
app = BudgetTracker()
app.mainloop()
sql.mysql_disconnect()
