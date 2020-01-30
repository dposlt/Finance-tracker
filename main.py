from sqlitedb import SqlDb
import tkinter as tk
from tkinter import messagebox, ttk, font
from datetime import date
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rcParams
import numpy as np
import pandas as pd
import datetime
import re


rcParams['font.family'] = 'fantasy'
rcParams['font.variant'] = 'small-caps'

LARGE_FONT = ("Comicsansms", 18)
ACTUAL_DATE = date.today().strftime("%d-%m-%Y")

# Baseline
class BudgetTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tk.Tk.wm_title(self, 'Finance tracker')
        tk.Tk.iconbitmap(self, 'wallet.ico')
        tk.Tk.geometry(self, '820x740')
        ttk.Style(self)
        ttk.Style.theme_use(self, 'xpnative')

        container = tk.Frame(self)
        container.place(x=0, y=0, width=820, height=740)

        self.frames = {}
        for Page in (DashBoard, Expenses, Income):
            frame = Page(container, self)
            frame.configure(bg='gray86')
            self.frames[Page] = frame
            frame.place(x=10, y=10, width=800, height=720)

        self.show_frame(DashBoard)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if cont == DashBoard:
            frame.reload()

class DashBoard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.style = ttk.Style()
        self.target = 2000
        self.configure(relief='ridge', borderwidth=5, padx=10, pady=10)
        sql.connect('data.db')
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"
        self.df_costs = Expenses(parent, controller).df_costs
        self.df_incomes = Income(parent, controller).df_incomes
        label = ttk.Label(self, text="FINANCIAL OVERVIEW", font=("Comic Sans MS", 24, "bold"), background='gray86')
        label.place(x=300, y=0)
        label_sql = ttk.Label(self, text="Connected to: " + str(sql))
        label_sql.place(x=0, y=680)
# MENU ==================================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      EXPENSES", width=22, command=lambda: controller.show_frame(Expenses), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic
        btn_dashboard.place(x=20, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
# TARGET ================================================================
        self.lbl_target = ttk.Label(self, text='CURRENT GOAL [EUR]', background='gray86', font=("Comic Sans MS", 8))
        self.lbl_target.place(x=500, y=70)
        self.ent_target = ttk.Entry(self)
        self.ent_target.place(x=500, y=90)
        self.btn_target = ttk.Button(self, text='Change', command=self.unlock_target)
        self.ent_target.bind('<Return>', lambda x: self.unlock_target())
        self.btn_target.place(x=650, y=88)
# DASH CUMULATIVE =======================================================
        self.tv_dash_history = ttk.Treeview(self, height=10, selectmode="browse", displaycolumns="#all")
        self.tv_dash_history['columns'] = ("DATE", "BALANCE")
        self.tv_dash_history.heading("DATE", text="DATE")
        self.tv_dash_history.heading("BALANCE", text="BALANCE")
        self.tv_dash_history.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tv_dash_history.column("DATE", width=80, minwidth=80, stretch=tk.NO, anchor=tk.E)
        self.tv_dash_history.column("BALANCE", width=90, minwidth=90, stretch=tk.NO, anchor=tk.E)
        self.tv_dash_history.tag_configure(self, background='red')
        self.tv_dash_history.place(x=250, y=60)
        self.treeScroll = ttk.Scrollbar(self, command=self.tv_dash_history.yview)
        self.treeScroll.place(x=423, y=60, height=226)
        self.tv_dash_history.configure(yscrollcommand=self.treeScroll.set)
        self.refresh_sqldata()
        self.plot()
        self.saved_target()

    def saved_target(self):
        with open('target.gl', 'r') as f:
            targ = f.read()
            if int(targ):
                self.target_saved = int(targ)
                self.target = self.target_saved
                self.ent_target.delete(0, tk.END)
                self.ent_target.insert(0, self.target_saved)
                self.ent_target.configure(state='disabled')
        self.yesno = False
        self.refresh_sqldata()
        self.plot()

    def unlock_target(self):
        self.ent_target.configure(state='enabled')
        self.btn_target.configure(text='Save')
        self.target_new = int(self.ent_target.get())
        if self.target_new != self.target_saved:
            self.yesno = tk.messagebox.askyesno("Attention!", 'Please confirm the change!')
            if self.yesno:
                self.target = self.target_new
                self.ent_target.delete(0, tk.END)
                self.ent_target.insert(0, self.target)
                self.ent_target.configure(state='disabled')
                self.btn_target.configure(text='Change')
                self.reload()
                with open('target.gl', 'w') as f:
                    f.write(str(self.target))
                    self.target_saved = self.target
            else:
                self.target_saved = self.target
                self.ent_target.delete(0, tk.END)
                self.ent_target.insert(0, self.target_saved)
                self.ent_target.configure(state='disabled')
                self.btn_target.configure(text='Change')

    def refresh_sqldata(self):
        self.tv_dash_history.delete(*self.tv_dash_history.get_children())
        val = sql.joint_result(self.cost_sql_table, self.incomes_sql_table)
        for ind, row in self.plot().iterrows():
            if round(row[1],2) >= 0:
                self.tv_dash_history.insert("", ind, values=[row[0], round(row[1],2)], tags=('positive',))
            else:
                self.tv_dash_history.insert("", ind, values=[row[0], round(row[1],2)], tags=('negative',))
        self.tv_dash_history.tag_configure('positive', background='#DFDFDF', foreground='green')
        self.tv_dash_history.tag_configure('negative', background='red', foreground='red')

    def plot(self):
        x = np.array([xx[1] for xx in sql.joint_result(self.cost_sql_table, self.incomes_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.joint_result(self.cost_sql_table, self.incomes_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[-7:])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()

        fig = Figure(figsize=(10,5), dpi=75, facecolor='gainsboro', tight_layout=True)
        axs = fig.add_subplot(111)
        #fig.style.use(['dark_background', 'presentation'])
        fig.subplots_adjust(hspace=0.75)
        axs.set_title("Money statistics", fontsize=24)

        axs.plot(df, 'bo--', label='Total balance')
        axs.plot(self.df_costs, 'r-', label='Expenses')
        axs.plot(self.df_incomes, 'g-', label='Incomes')

        x_min = min([self.df_costs.index.min(), self.df_incomes.index.min()])
        x_max = max([self.df_costs.index.max(), self.df_incomes.index.max()])
        y_min = df.min()
        y_max = df.max()
        y_max = int(max(y_max, self.target)*1.1)
        axs.hlines(self.target, xmin=x_min, xmax=x_max, colors='k', linestyle='-', label='goal')
        axs.legend()
        axs.grid(True)
        axs.text(0.05,self.target*1.1, 'GOAL', fontsize=14)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')
        axs.set_xlabel('Months')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=10, y= 300)
        canvas.draw()

        df_new= pd.Series.to_frame(df)
        df_new['Date'] = list(df_new.index)
        df_new = df_new[['Date', 'Total']].iloc[::-1].reset_index(drop=True)
        return df_new

    def reload(self):
        self.df_costs = Expenses(self, self).df_costs
        self.df_incomes = Income(self, self).df_incomes
        self.plot()
        self.refresh_sqldata()

class Expenses(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(relief='ridge', borderwidth=5, padx=10, pady=10)
        self.lbl_alert = tk.Label(self, text="", fg='red', background='gray86')
        self.lbl_alert.place(x=250, y= 135)
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"

        label = tk.Label(self, text="EXPENSES", font=("Comic Sans MS", 24, "bold"), foreground="black", background='gray86')
        label.place(x=400, y=0)
        label_sql = ttk.Label(self, text="Connected to: "+str(sql))
        label_sql.place(x=0, y=680)
# MENU ==============================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      EXPENSES", width=22, command=lambda: controller.shoExpenses, compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=20, y=70, width=200, height=50)
        btn_income.place(x=0, y=140, width=200, height=50)
# ENTRY FIELD ============================================================
        lbl_sp_date = ttk.Label(self, text="Date", background='gray86')
        lbl_sp_category = ttk.Label(self, text="Category", background='gray86')
        lbl_sp_amount = ttk.Label(self, text="Amount", background='gray86')
        lbl_sp_description = ttk.Label(self, text="Description", background='gray86')
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
        btn_submit_entry.place(x=678, y=120)
# EXPENSES HISTORY ========================================================
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
# DELETE SELECTION
        self.tv_spending_history.bind('<Delete>', lambda x: self.delete_row())

        self.lbl_remark=ttk.Label(self, text='Select row and press <DELETE> key to delete', foreground='blue', background='gray86')
        self.lbl_remark.place(x=250, y=400)
# TOTAL ==========================================================
        self.total = ttk.Label(self, text="TOTAL: - "+str(round(abs(self.plot()),2))+" EUR", font=("Arial", 10, "bold"), foreground='red', background='gray86')
        self.total.place(x=620, y=400)
        self.reload()

    def plot_category(self):
        x = np.array([xx[3] for xx in sql.list_sqltbl(self.cost_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.list_sqltbl(self.cost_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Category': x, 'Total': y}, columns=['Category', 'Total'])
        df = df.groupby(['Category'])['Total'].sum()
        df= df.cumsum()

        fig = Figure(figsize=(2,2), dpi=125, facecolor='gainsboro', tight_layout=True)

        axs = fig.add_subplot(111)
        axs.pie(abs(df.values), labels=df.index, autopct='%1.1f%%',textprops={'fontsize': 6})
        axs.axis('equal')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=0, y= 435)
        canvas.draw()

    def plot(self):
        x = np.array([xx[1] for xx in sql.list_sqltbl(self.cost_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.list_sqltbl(self.cost_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[-7:])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()
        self.df_costs = df
        fig = Figure(figsize=(5,2.5), dpi=100, facecolor='gainsboro', tight_layout=True)
        axs = fig.add_subplot(111)
        fig.subplots_adjust(hspace=1.75)
        axs.set_title("Cumulative trend of expenses")
        axs.plot(df, '-o')
        axs.grid(True)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')
        axs.set_xlabel('Months')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=253, y= 435)
        canvas.draw()
        if len(df):
            return df[-1]
        return 0

    def reload(self):
        self.refresh_sqldata()
        self.plot()
        self.plot_category()

    def delete_row(self):
        self.selected_row = self.tv_spending_history.selection()
        self.subject = self.tv_spending_history.item(self.selected_row)['values']
        sql.delete_row_spending(self.cost_sql_table, self.subject)
        self.reload()

    def submitt(self):
        get_entry_field_date = self.ent_field_date.get()
        get_entry_field_amount = self.ent_field_amount.get()
        date_format_valid = re.match("^\s*(3[01]|[12][0-9]|0?[1-9])\-(1[012]|0?[1-9])\-((?:19|20)\d{2})\s*$", get_entry_field_date)
        amount_format_valid = re.match("^\d*\.?\d*$", get_entry_field_amount)
        if not date_format_valid:
            self.lbl_alert['text'] = "Wrong format of Date"
        if amount_format_valid:
            get_entry_field_amount = round(-float(self.ent_field_amount.get()),2)
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
        self.reload()

    def adding_spending(self, tbl, *args):
        #add check of list
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        sql.add_cost(tbl, args)
        self.reload()

    def refresh_sqldata(self):
        self.tv_spending_history.delete(*self.tv_spending_history.get_children())
        val = sql.list_sqltbl(self.cost_sql_table)
        for idx, v in reversed(list(enumerate(val, start=1))):
            v_list = [x for x in v]
            self.tv_spending_history.insert("", idx, values=v_list[1:])

class Income(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(relief='ridge', borderwidth=5, padx=10, pady=10)
        self.lbl_alert = tk.Label(self, text="", fg='red', background='gray86')
        self.lbl_alert.place(x=250, y= 135)
        self.cost_sql_table = "tbl_spendings"
        self.incomes_sql_table = "tbl_incomes"

        label = tk.Label(self, text="INCOMES", font=("Comic Sans MS", 24, "bold"), foreground="black", background='gray86')
        label.place(x=400, y=0)
        label_sql = ttk.Label(self, text="Connected to: "+str(sql))
        label_sql.place(x=0, y=680)
# MENU =================================================================
        btn_dashboard_pic = tk.PhotoImage(file="img\\dash_button_sm.png")
        btn_spending_pic = tk.PhotoImage(file="img\\spending_button_sm.png")
        btn_income_pic = tk.PhotoImage(file="img\\income_button_sm.png")

        btn_dashboard = ttk.Button(self, image=btn_dashboard_pic, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        btn_dashboard.image=btn_dashboard_pic
        btn_spending = ttk.Button(self, image=btn_spending_pic, text="      EXPENSES", width=22, command=lambda: controller.show_frame(Expenses), compound='left')
        btn_spending.image = btn_spending_pic
        btn_income = ttk.Button(self, image=btn_income_pic, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        btn_income.image = btn_income_pic

        btn_dashboard.place(x=0, y=0, width=200, height=50)
        btn_spending.place(x=0, y=70, width=200, height=50)
        btn_income.place(x=20, y=140, width=200, height=50)
# ENTRY FIELD ============================================================
        lbl_inc_date = ttk.Label(self, text="Date", background='gray86')
        lbl_inc_category = ttk.Label(self, text="Category", background='gray86')
        lbl_inc_amount = ttk.Label(self, text="Amount", background='gray86')
        lbl_inc_description = ttk.Label(self, text="Description", background='gray86')
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
        btn_submit_entry.place(x=678, y=120)
# EXPENSES HISTORY ========================================================
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
# remark under expenses history
        self.lbl_remark=ttk.Label(self, text='Select row and press <DELETE> key to delete', foreground='blue', background='gray86')
        self.lbl_remark.place(x=250, y=400)
# TOTAL ==========================================================
        self.total = ttk.Label(self, text="TOTAL: "+str(round(self.plot(),2))+" EUR", font=("Arial", 10, "bold"), foreground='red', background='gray86')
        self.total.place(x=620, y=400)
        self.reload()

    def plot(self):
        x = np.array([xx[1] for xx in sql.list_sqltbl(self.incomes_sql_table)], dtype=str)
        y = np.array([b[4] for b in sql.list_sqltbl(self.incomes_sql_table)], dtype=float)  # TODO: add cumulation
        df = pd.DataFrame(data={'Date': x, 'Total': y}, columns=['Date', 'Total'])
        df['Month'] = df['Date'].apply(lambda x: x[-7:])
        df = df.groupby(['Month'])['Total'].sum()
        df= df.cumsum()
        self.df_incomes = df
        fig = Figure(figsize=(5,2.5), dpi=100, facecolor='gainsboro', tight_layout=True)
        axs = fig.add_subplot(111)
        fig.subplots_adjust(hspace=1.75)
        axs.set_title("Cumulative trend of incomes")
        axs.plot(df, '-o', color='red')
        axs.grid(True)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
        axs.set_ylabel('EUR')
        axs.set_xlabel('Months')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=253, y= 435)
        canvas.draw()
        return df[-1]

    def plot_category(self):
        x = np.array([xx[3] for xx in sql.list_sqltbl(self.incomes_sql_table)], dtype=str) #dates
        y = np.array([b[4] for b in sql.list_sqltbl(self.incomes_sql_table)], dtype=float)  #EUR
        df = pd.DataFrame(data={'Category': x, 'Total': y}, columns=['Category', 'Total'])
        df = df.groupby(['Category'])['Total'].sum()
        df= df.cumsum()

        fig = Figure(figsize=(2,2), dpi=125, facecolor='gainsboro', tight_layout=True)
        axs = fig.add_subplot(111)
        axs.pie(abs(df.values), labels=df.index, autopct='%1.1f%%',textprops={'fontsize': 6})
        axs.axis('equal')
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(x=0, y= 435)
        canvas.draw()

    def reload(self):
        self.refresh_sqldata()
        self.plot()
        self.plot_category()

    def delete_row(self):
        self.selected_row = self.tv_incomes_history.selection()
        self.subject = self.tv_incomes_history.item(self.selected_row)['values']
        sql.delete_row_income(self.incomes_sql_table, self.subject)
        self.reload()

    def submit_inc(self):
        get_entry_field_date = self.ent_field_date.get()
        get_entry_field_amount = self.ent_field_amount.get()
        date_format_valid = re.match("^\s*(3[01]|[12][0-9]|0?[1-9])\-(1[012]|0?[1-9])\-((?:19|20)\d{2})\s*$", get_entry_field_date)
        amount_format_valid = re.match("^\d*\.?\d*$", get_entry_field_amount)
        if not date_format_valid:
            self.lbl_alert['text'] = "Wrong format of Date"
        if amount_format_valid:
            get_entry_field_amount = format(float(self.ent_field_amount.get()),'.2f')
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
        self.reload()

    def adding_incomes(self, tbl, *args):
        #add check of list
        self.tv_incomes_history.delete(*self.tv_incomes_history.get_children())
        sql.add_income(tbl, args)
        self.reload()

    def refresh_sqldata(self):
        self.tv_incomes_history.delete(*self.tv_incomes_history.get_children())
        val = sql.list_sqltbl(self.incomes_sql_table)
        for idx, v in reversed(list(enumerate(val, start=1))):
            v_list = [x for x in v]
            self.tv_incomes_history.insert("", idx, values=v_list[1:])


if __name__ == '__main__':
    sql = SqlDb()
    app = BudgetTracker()
    app.mainloop()
    sql.disconnect()
