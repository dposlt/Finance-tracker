from SQLbackbone import MySQLconnection
import tkinter as tk
from tkinter import messagebox, ttk

LARGE_FONT = ("Comicsansms", 18)

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
        # MENU ======================================================================
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="DASHBOARD PAGE", font=LARGE_FONT)
        label.place(x=240,y=0)

        button_dashboard = ttk.Button(self, image=dashboard_butt_photo, text="DASHBOARD", width=15, command=lambda: controller.show_frame(DashBoard), compound='left')
        button_dashboard.image=dashboard_butt_photo
        button_spending = ttk.Button(self, image=spending_butt_photo, text="      SPENDINGS", width=22, command=lambda: controller.show_frame(Spending), compound='left')
        button_spending.image = spending_butt_photo
        button_income = ttk.Button(self, image=income_butt_photo, text="      INCOMES", width=22, command=lambda: controller.show_frame(Income), compound='left')
        button_income.image = income_butt_photo
        button_plan = ttk.Button(self, image=plan_butt_photo, text="         PLAN", width=22, command=lambda: controller.show_frame(Plan), compound='left')
        button_plan.image = plan_butt_photo
        button_dashboard.config()

        # button_dashboard.pack(side=tk.LEFT, padx=10, pady=10)
        # button_spending.pack(side=tk.LEFT, padx=10, pady=10)
        # button_income.pack(side=tk.LEFT, padx=10, pady=10)
        # button_plan.pack(side=tk.LEFT, padx=10, pady=10)
        button_dashboard.place(x=20, y=0, width=200, height=50)
        button_spending.place(x=0, y=70, width=200, height=50)
        button_income.place(x=0, y=140, width=200, height=50)
        button_plan.place(x=0, y=210, width=200, height=50)
        # DASHBOARD ======================================================================
        box = ttk.Combobox(self,  height=200, width=50, justify='center')
        box.place(x=250, y=50)

class Spending(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="SPENDING PAGE", font=LARGE_FONT)
        label.place(x=240, y=70)

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

class Income(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label1 = tk.Label(self, text="INCOME PAGE", font=LARGE_FONT)
        dashboard_butt_photo = tk.PhotoImage(file="img\\dash_button_sm.png")
        spending_butt_photo = tk.PhotoImage(file="img\\spending_button_sm.png")
        income_butt_photo = tk.PhotoImage(file="img\\income_button_sm.png")
        plan_butt_photo = tk.PhotoImage(file="img\\plan_button_sm.png")
        label = tk.Label(self, text="INCOME PAGE", font=LARGE_FONT)
        label.place(x=240, y=140)

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
        label = tk.Label(self, text="PLAN PAGE", font=LARGE_FONT)
        label.place(x=240, y=210)

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


app = BudgetTracker()
app.mainloop()
