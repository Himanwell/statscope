# 📊 Statscope

A beginner‑friendly **Streamlit web app** that helps you quickly understand CSV or Excel datasets through clear insights, visualizations, and an auto‑generated PDF report.

This project is designed for **non‑technical users**, students, and early data learners who want meaningful explanations without heavy statistics jargon.

---

## ✨ Features

### 📂 File Support

- Upload **CSV** files
- Upload **Excel** files (`.xlsx`, `.xls`)

### 🧠 Explain Like I’m New Mode

- Toggle simple, human‑friendly explanations
- Avoids technical language when enabled

### 🔍 Automatic Analysis

- Dataset overview (rows, columns, date range)
- Missing data detection
- Numeric column analysis (mean, range, outliers)
- Categorical column summaries
- Correlation detection between numeric columns

### 📊 Visualizations

- Distribution (histogram) charts
- Correlation heatmap
- Category bar charts

### 📄 PDF Report Export

- Includes:
  - Dataset name
  - Summary statistics
  - Plain‑English insights
  - Embedded charts (histograms)
- One‑click download

---

## 🖥️ Demo Preview

Once a file is uploaded, the app:

1. Previews the dataset
2. Explains what the numbers mean
3. Shows visual charts
4. Generates a downloadable PDF report

---

## 🗂️ Project Structure

statscope/
│
├── app.py # Main Streamlit app
├── analyzer.py # Data analysis + PDF generation
├── visualizer.py # Chart creation functions
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/statscope.git
cd simple-data-analyzer
2️⃣ Create a virtual environment (recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
▶️ Run the App
bash
Copy code
streamlit run app.py
The app will open automatically in your browser.

📦 Requirements
Your requirements.txt should include:

nginx
Copy code
streamlit
pandas
matplotlib
reportlab
openpyxl
🧪 Supported Data Types
Type	Supported
Numeric	✅
Categorical	✅
Dates	✅ (auto‑detected)
IDs	🚫 (ignored automatically)

🧠 How Insights Are Generated
Skips ID‑like columns automatically

Uses:

Mean, median, min, max

IQR‑based outlier detection

Correlations shown only if strong enough

Beginner explanations simplify statistics into plain language

🚀 Who This Is For
Students learning data analysis

Teachers and educators

Non‑technical stakeholders

Anyone who wants quick insights without coding

🔮 Future Improvements (Planned)
PDF heatmap inclusion

Custom PDF themes

Column selection controls

AI‑generated recommendations

Export to Word / PowerPoint



🙌 Author
Ogunkoya Emmanuel Oluwakemi
Built with ❤️ using Python & Streamlit

If you find this useful, feel free to ⭐ the repo and share it!
```

