import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

plt.rcParams['figure.dpi'] = 120

class SalesDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊 Sales Insights Dashboard")
        self.geometry("1000x650")
        self.configure(bg="#1e1e1e")
        self.data = None

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, background="#2e2e2e", foreground="white")
        self.style.map("TButton", background=[("active", "#3e3e3e")])

        # Title
        title_label = tk.Label(self, text="📈 Sales Insights by Kshitij Yagnik", font=("Segoe UI", 32, "bold"),
                               fg="lime", bg="#1e1e1e")
        title_label.pack(pady=20)

        # Button Frame
        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="📂 Load & Process Data", command=self.load_data).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="📊 Statistics", command=self.show_statistics).grid(row=0, column=1, padx=8)
        ttk.Button(btn_frame, text="📈 Charts", command=self.show_charts).grid(row=0, column=2, padx=8)
        ttk.Button(btn_frame, text="🔮 Forecast", command=self.generate_forecasts).grid(row=0, column=3, padx=8)

        # Output Display
        output_frame = tk.Frame(self, bg="#1e1e1e")
        output_frame.pack(fill="both", expand=True, pady=20, padx=20)

        self.output_text = ScrolledText(output_frame, height=15, bg="#1e1e1e", fg="white",
                                        font=("Consolas", 11), insertbackground='white', borderwidth=0)
        self.output_text.pack(fill="both", expand=True)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            self.data = pd.read_csv(file_path)
            self.data.columns = self.data.columns.str.strip()

            if 'Date' not in self.data.columns:
                raise ValueError("The 'Date' column is missing.")

            self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce')
            self.data["Month"] = self.data["Date"].dt.to_period("M").astype(str)
            self.data["Sales Amount"] = pd.to_numeric(self.data["Sales Amount"], errors='coerce')

            self.output_text.insert(tk.END, f"✅ Data loaded from: {file_path}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error loading data: {e}\n")

    def show_statistics(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please load the data first.")
            return
        try:
            stats = self.data["Sales Amount"].describe()
            self.output_text.insert(tk.END, "\n📊 Sales Amount Statistics:\n")
            self.output_text.insert(tk.END, str(stats) + "\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error computing statistics: {e}\n")

    def show_charts(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please load the data first.")
            return
        try:
            trend = self.data.groupby("Month")["Sales Amount"].sum()
            composition = self.data.groupby("Category")["Sales Amount"].sum()
            distribution = self.data["Sales Amount"].dropna()

            fig, axs = plt.subplots(1, 3, figsize=(16, 4))
            trend.plot(ax=axs[0], kind='line', title="Monthly Sales Trend", color='lime')
            composition.plot(ax=axs[1], kind='pie', title="Category Composition", autopct="%1.1f%%", startangle=90)
            axs[2].hist(distribution, bins=20, color='skyblue')
            axs[2].set_title("Sales Distribution")

            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error generating charts: {e}\n")

    def generate_forecasts(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please load the data first.")
            return
        try:
            self.output_text.insert(tk.END, "\n🔮 Forecasting Next Month's Sales...\n")
            df = self.data.dropna(subset=["Month", "Sales Amount"]).copy()
            df["Month_Num"] = pd.factorize(df["Month"])[0]
            X = df[["Month_Num"]]
            y = df["Sales Amount"]
            model = LinearRegression()
            model.fit(X, y)
            future = np.array([[X["Month_Num"].max() + 1]])
            pred = model.predict(future)[0]
            forecast_month = (pd.Period(df["Month"].max(), freq='M') + 1).strftime('%Y-%m')
            self.output_text.insert(tk.END, f"📈 Predicted Sales for {forecast_month}: ₹{pred:.2f}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Forecasting failed: {e}\n")

if __name__ == "__main__":
    app = SalesDashboard()
    app.mainloop()
