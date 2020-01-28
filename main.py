from SQLbackbone import MySQLconnection
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import datetime
import re
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import pandas as pd


LARGE_FONT = ("Comicsansms", 18)
ACTUAL_DATE = date.today().strftime("%d-%m-%Y")

# Baseline
class BudgetTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Tk.wm_title(self, 'Buget Tracker')
        tk.Tk.iconbitmap(self, 'wallet.ico')
        tk.Tk.geometry(self, '800x700')
        ttk.Style(self)
        ttk.Style.theme_use(self, 'xpnative')

        container = tk.Frame(self)
        container.place(x=0, y=0, width=800, height=800)

        self.frames = {}
        for Page in (DashBoard, Spending, Income, Setting):
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
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"
        self.df_costs = Spending(parent, controller).df_costs
        self.df_incomes = Income(parent, controller).df_incomes
        label = tk.Label(self, text="DASHBOARD", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=400, y=10)
        # MENU ======================================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_setting_pci = tk.PhotoImage(file="img\\setting_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_setting = ttk.Button(self, image=btn_setting_pci, text="         SETTING", width=22, command=lambda: controller.show_frame(Setting), compound='left')
        btn_setting.image = btn_setting_pci

        btn_dashboard.place(x=20, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_setting.place(x=0, y=210, width=200, height=50)

 # DASH CUMULATIVE ========================================================
        self.tv_dash_history = ttk.Treeview(self, height=10, selectmode="browse", displaycolumns="#all")
        self.tv_dash_history['columns'] = ("DATE", "AMOUNT")
        self.tv_dash_history.heading("DATE", text="DATE")
        self.tv_dash_history.heading("AMOUNT", text="AMOUNT")
        self.tv_dash_history.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tv_dash_history.column("DATE", width=120, minwidth=120, stretch=tk.NO)
        self.tv_dash_history.column("AMOUNT", width=90, minwidth=90, stretch=tk.NO)
        self.tv_dash_history.tag_configure(self, background='red')
        self.tv_dash_history.place(x=250, y=70)
        self.treeScroll = ttk.Scrollbar(self, command=self.tv_dash_history.yview)
        self.treeScroll.place(x=465, y=70, height=227)
        self.tv_dash_history.configure(yscrollcommand=self.treeScroll.set)
        self.refresh_sqldata()
        self.plot()

    def refresh_sqldata(self):
        self.tv_dash_history.delete(*self.tv_dash_history.get_children())
        val = sql.joint_result(self.cost_sql_table, self.incomes_sql_table)
        for ind, row in self.plot().iterrows():
            self.tv_dash_history.insert("", ind, values=[row[0], round(row[1],2)])

    def plot(self):
        x = np.array([xx[1] for xx in sql.joint_result(self.cost_sql_table, self.incomes_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.joint_result(self.cost_sql_table, self.incomes_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[:7])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()

        fig = Figure(figsize=(5,3), dpi=100, facecolor='lightgrey', tight_layout=True)
        axs = fig.add_subplot(111)
        fig.subplots_adjust(hspace=1.75)
        axs.set_title("Cumulative trend")
        axs.plot(df, '--', label='trend')
        axs.plot(df, 'o')
        axs.plot(self.df_costs, '-', label='costs')
        axs.plot(self.df_incomes, '-', label='incomes')
        axs.legend()
        axs.grid(True)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=250, y= 315)
        canvas.draw()

        df_new= pd.Series.to_frame(df)
        df_new['Date'] = list(df_new.index)
        df_new = df_new[['Date', 'Total']].reset_index(drop=True)
        return df_new


class Spending(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.lbl_alert = tk.Label(self, text="", fg='red')
        self.lbl_alert.place(x=250, y= 135)
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"

        label = tk.Label(self, text="SPENDING", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=420, y=10)
        # LEFT PANEL ==============================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_setting_pci = tk.PhotoImage(file="img\\setting_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_setting = ttk.Button(self, image=btn_setting_pci, text="         SETTING", width=22, command=lambda: controller.show_frame(Setting), compound='left')
        btn_setting.image = btn_setting_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=20, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_setting.place(x=0, y=210, width=200, height=50)

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
        self.ent_field_category.config(values=sql.category(self.cost_sql_table))
        self.ent_field_amount = ttk.Entry(self)
        self.ent_field_date.place(x=250, y=90, width=120)
        self.ent_field_description.place(x=372, y=90, width=180)
        self.ent_field_category.place(x=554, y=90, width=120)
        self.ent_field_amount.place(x=676, y=90, width=80)

        # SUBMIT button =============================================================
        btn_submit_entry = ttk.Button(self, text="SUBMIT", command=self.submitt)
        btn_submit_entry.place(x=676, y=120)
        # SPENDING HISTORY ========================================================
        self.tv_spending_history = ttk.Treeview(self, height=10, selectmode="browse", displaycolumns="#all")
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
        self.treeScroll.place(x=758, y=170, height=227)
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
        # TOTAL ==========================================================
        self.total = ttk.Label(self, text="TOTAL: - "+str(round(abs(self.plot()),2))+" EUR", font=("Arial", 10, "bold"), foreground='red')
        self.total.place(x=620, y=400)
        self.plot()

    def plot(self):
        x = np.array([xx[1] for xx in sql.spending_history(self.cost_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.spending_history(self.cost_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[:7])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()
        self.df_costs = df
        fig = Figure(figsize=(5,2.5), dpi=100, facecolor='lightgrey', tight_layout=True)
        axs = fig.add_subplot(111)
        fig.subplots_adjust(hspace=1.75)
        axs.set_title("Cumulative trend")
        axs.plot(df, '-o')
        axs.grid(True)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=253, y= 435)
        canvas.draw()
        return df[-1]

    def delete_row(self):
        self.selected_row = self.tv_spending_history.selection()
        self.subject = self.tv_spending_history.item(self.selected_row)['values']
        sql.delete_row(self.cost_sql_table, self.self.subject)
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
            get_entry_field_amount = -float(self.ent_field_amount.get())
        else:
            self.lbl_alert['text'] = "Wrong format of Amount"
        get_entry_field_ddescription = self.ent_field_description.get()
        get_entry_field_category = self.ent_field_category.get().upper()
        if amount_format_valid and date_format_valid and get_entry_field_ddescription and get_entry_field_category:
            self.lbl_alert['text'] = " "
            self.adding_spending(self.cost_sql_table, get_entry_field_date, get_entry_field_ddescription, get_entry_field_category, get_entry_field_amount)
            self.ent_field_category.config(values=sql.category(self.cost_sql_table))

            self.ent_field_amount.delete(0, tk.END)
            self.ent_field_category.delete(0, tk.END)
            self.ent_field_description.delete(0, tk.END)
        self.ent_field_description.focus()
        self.plot()

        # ADD SQL DATA into FINANCE TABLE =============================
    def adding_spending(self, tbl, *args):
        #add check of list
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        sql.add_cost(tbl, args)
        self.refresh_sqldata()

        # READ SQL DATA into SPENDING HISTORY =============================
    def refresh_sqldata(self):
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        val = sql.spending_history(self.cost_sql_table)
        for idx, v in reversed(list(enumerate(val, start=1))):
            v_list = [x for x in v]
            v_list[1] = datetime.datetime.strftime(v_list[1],"%d-%m-%Y")
            if v_list[4] < 0:
                self.tv_spending_history.insert("", idx, values=v_list[1:])

class Income(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.lbl_alert = tk.Label(self, text="", fg='red')
        self.lbl_alert.place(x=250, y= 135)
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"

        label = tk.Label(self, text="INCOME PAGE", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=420, y=10)

        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_setting_pci = tk.PhotoImage(file="img\\setting_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_setting = ttk.Button(self, image=btn_setting_pci, text="         SETTING", width=22, command=lambda: controller.show_frame(Setting), compound='left')
        btn_setting.image = btn_setting_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=20, y=140, width=200, height=50)
        btn_setting.place(x=0, y=210, width=200, height=50)

        # ENTRY FIELD ============================================================
        lbl_inc_date = ttk.Label(self, text="Date")
        lbl_inc_category = ttk.Label(self, text="Category")
        lbl_inc_amount = ttk.Label(self, text="Amount")
        lbl_inc_description = ttk.Label(self, text="Description")
        lbl_inc_date.place(x=290, y=70)
        lbl_inc_description.place(x=435, y=70)
        lbl_inc_category.place(x=580, y=70)
        lbl_inc_amount.place(x=690, y=70)
        self.ent_field_date = ttk.Entry(self, justify="center")
        self.ent_field_description = ttk.Entry(self)
        self.ent_field_category = ttk.Combobox(self)
        self.ent_field_category.config(values=sql.category(self.incomes_sql_table))
        self.ent_field_amount = ttk.Entry(self)
        self.ent_field_date.place(x=250, y=90, width=120)
        self.ent_field_description.place(x=372, y=90, width=180)
        self.ent_field_category.place(x=554, y=90, width=120)
        self.ent_field_amount.place(x=676, y=90, width=80)

        # SUBMIT button =============================================================
        btn_submit_entry = ttk.Button(self, text="SUBMIT", command=self.submit_inc)
        btn_submit_entry.place(x=676, y=120)
        # SPENDING HISTORY ========================================================
        self.tv_incomes_history = ttk.Treeview(self, height=10, selectmode="browse", displaycolumns="#all")
        self.tv_incomes_history['columns'] = ("DATE", "DESCRIPTION", "CATEGORY", "AMOUNT")
        self.tv_incomes_history.heading("DATE", text="DATE")
        self.tv_incomes_history.heading("DESCRIPTION", text="DESCRIPTION")
        self.tv_incomes_history.heading("CATEGORY", text="CATEGORY")
        self.tv_incomes_history.heading("AMOUNT", text="AMOUNT")
        self.tv_incomes_history.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tv_incomes_history.column("DATE", width=120, minwidth=120, stretch=tk.NO)
        self.tv_incomes_history.column("DESCRIPTION", width=185, minwidth=185, stretch=tk.NO)
        self.tv_incomes_history.column("CATEGORY", width=110, minwidth=110, stretch=tk.NO)
        self.tv_incomes_history.column("AMOUNT", width=90, minwidth=90, stretch=tk.NO)
        self.tv_incomes_history.tag_configure(self, background='red')
        self.tv_incomes_history.place(x=250, y=170)
        self.treeScroll = ttk.Scrollbar(self, command=self.tv_incomes_history.yview)
        self.treeScroll.place(x=758, y=170, height=227)
        self.tv_incomes_history.configure(yscrollcommand=self.treeScroll.set)
        self.refresh_sqldata()
        # DEFAULT ACTUAL DATE =============================================
        self.ent_field_date.insert(0, ACTUAL_DATE)
        # Press ENTER to run submit =======================================
        self.ent_field_amount.bind('<Return>', lambda x: self.submit_inc())
        # Delete SELECTION
        self.tv_incomes_history.bind('<Delete>', lambda x: self.delete_row())
        # remark under spending history
        self.lbl_remark=ttk.Label(self, text='! Select row and press DELETE key to delete', foreground='blue')
        self.lbl_remark.place(x=250, y=520)
        # TOTAL ==========================================================
        self.total = ttk.Label(self, text="TOTAL: "+str(round(self.plot(),2))+" EUR", font=("Arial", 10, "bold"), foreground='red')
        self.total.place(x=620, y=400)

        self.plot()

    def plot(self):
        x = np.array([xx[1] for xx in sql.spending_history(self.incomes_sql_table)], dtype=str)
        y = np.array([b[4] for b in sql.spending_history(self.incomes_sql_table)], dtype=float)  # TODO: add cumulation
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[:7])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()
        self.df_incomes = df
        fig = Figure(figsize=(5,2.5), dpi=100, facecolor='lightgrey', tight_layout=True)
        axs = fig.add_subplot(111)
        fig.subplots_adjust(hspace=1.75)
        axs.set_title("Cumulative trend")
        axs.plot(df, '-o', color='red')
        axs.grid(True)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=253, y= 435)
        canvas.draw()
        return df[-1]

    def delete_row(self):
        self.selected_row = self.tv_incomes_history.selection()
        self.subject = self.tv_incomes_history.item(self.selected_row)['values']
        sql.delete_row(self.subject)
        self.refresh_sqldata()

    def submit_inc(self):
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
            self.adding_incomes(self.incomes_sql_table, get_entry_field_date, get_entry_field_ddescription, get_entry_field_category, get_entry_field_amount)
            self.ent_field_category.config(values=sql.category(self.incomes_sql_table))

            self.ent_field_amount.delete(0, tk.END)
            self.ent_field_category.delete(0, tk.END)
            self.ent_field_description.delete(0, tk.END)
        self.ent_field_description.focus()
        self.plot()

        # ADD SQL DATA into TABLE =============================
    def adding_incomes(self, tbl, *args):
        #add check of list
        self.tv_incomes_history.delete(*self.tv_incomes_history.get_children())
        sql.add_income(tbl, args)
        self.refresh_sqldata()

        # READ SQL DATA into SPENDING HISTORY =============================
    def refresh_sqldata(self):
        self.tv_incomes_history.delete(*self.tv_incomes_history.get_children())
        val = sql.spending_history(self.incomes_sql_table)
        for idx, v in reversed(list(enumerate(val, start=1))):
            v_list = [x for x in v]
            v_list[1] = datetime.datetime.strftime(v_list[1],"%d-%m-%Y")
            if v_list[4] > 0:
                self.tv_incomes_history.insert("", idx, values=v_list[1:])

class Setting(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")
        btn_setting_pci = tk.PhotoImage(file="img\\setting_button_sm.png")

        label = tk.Label(self, text="SETTING", font=("Helvetica", 24, "bold"), foreground="darkblue")
        label.place(x=420, y=10)

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_setting = ttk.Button(self, image=btn_setting_pci, text="         SETTING", width=22, command=lambda: controller.show_frame(Setting), compound='left')
        btn_setting.image = btn_setting_pci

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
        btn_setting.place(x=20, y=210, width=200, height=50)


if __name__ == '__main__':
    sql = MySQLconnection()
    app = BudgetTracker()
    app.mainloop()
    sql.mysql_disconnect()
