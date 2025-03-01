## DESIGN OF THE AI-POWERERD DATA CLEANER 
    ## 1. Frontend – Streamlit UI (User Interface)
            ## The frontend is built with Streamlit, allowing users to upload datasets, preview data, and download the cleaned version.
        ## Features:
                ## File Uploader: Users can upload CSV, Excel, JSON, Parquet, XML, SQL
                ## Data Preview: Displays the first ten rows of the raw data. 
                ## One-Click Cleaning: The system automatically handles missing values and duplicates.
        ## Data Insights: 
                ## Descriptive statistics for quick dataset understanding.
                ## Missing values heatmap for easy visualization of incomplete data.
        ## Download Button: Users can save the cleaned dataset.
        ## Modern UI Design:
                ## Soft gradient background for a calm and professional look.
                ## Stylish sidebar with quick navigation.
                ## Interactive tabs for smooth workflow navigation.
        ## User Flow:
                ## User uploads a dataset.
                ## App displays the first ten rows of raw data.
                ## User selects cleaning preferences (missing value strategy, duplicate removal).
                ## AI cleans the data (handling missing values & duplicates).
                ## App displays the first ten rows of cleaned data.
                ## User downloads the cleaned dataset.
        ## frontend Tech Stack:
                ## Frontend: Streamlit (for UI).
                ## Data Handling: Pandas (for reading and processing data).
                ## File Handling: Streamlit’s file_uploader() and download_button().

    ## 2. Backend – AI Data Cleaning Engine
            ## The backend consists of a data cleaning class (AICleaner) that processes the uploaded dataset automatically.
        ## Features:
        ## Automatic Missing Value Handling:
                ## Numeric Columns: Filled using the mean.
                ## Categorical Columns: Filled using the most frequent value.
            ## Duplicate Removal: Ensures no redundant data.
            ## Efficient Data Processing: Handles various dataset formats, including CSV, Excel, JSON, Parquet, XML, and SQL databases.
            ##  Data Insights & Visualization: Generates statistical summaries and heatmaps to help users understand missing values.
        ## AI-Powered Data Transformation (Future Roadmap):
            ## Fuzzy Matching for Standardization (e.g., correcting inconsistent labels).
            ## Auto-Detection of Anomalies & Outliers.
        ## Backend Tech Stack:
                ## Machine Learning: Scikit-learn (for imputation).
                ## Data Processing: Pandas.
                ## Data Standardization: FuzzyWuzzy (planned for future fuzzy matching improvements).
                ## File Handling: SQLite (for handling database uploads).

import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
from sklearn.impute import SimpleImputer

# 🌟 Streamlit Page Config
st.set_page_config(
    page_title="Struqtura AI Data Cleaner",
    page_icon="🧼",
    layout="wide",
)

# 🎨 Custom Styling for Background and Sidebar
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #e6eff7, #f4f9fc);
        padding: 20px;
    }
    .stSidebar {
        background-color: #2c3e50 !important;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .stHeader {
        color: #34495e;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
    }
    .stLeftAlign {
        text-align: left;
        color: #34495e;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 📌 Sidebar Navigation
st.sidebar.markdown('<h1 class="stSidebar">🔍 Navigation</h1>', unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["🏠 Home", "🧼 Data Cleaner", "📖 About Us", "📩 Contact Us"])

# 📍 Page Navigation Logic
if page == "🏠 Home":
    st.markdown('<h1 class="stTitle">Welcome to Struqtura</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Your Ultimate AI-Powered Data Cleaning Solution</h2>', unsafe_allow_html=True)
    st.markdown("""
    - 🧼 **Automatically clean messy datasets**
    - 📊 **Generate insightful visualizations**
    - ⚡ **Boost productivity with AI-driven data transformations**
    - 🏆 **Enterprise-ready & scalable**
    """)

elif page == "🧼 Data Cleaner":
    st.markdown('<h1 class="stTitle">🧼 AI Data Cleaner</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="stHeader">Upload your dataset, and let AI clean it automatically!</h2>', unsafe_allow_html=True)

    # 📂 File Upload
    uploaded_file = st.file_uploader(
        "Upload CSV, Excel, JSON, Parquet, XML, SQL files",
        type=["csv", "xlsx", "json", "parquet", "xml", "db"]
    )

    # 📌 File Handling Logic
    def load_file(uploaded_file):
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            return pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".json"):
            return pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith(".parquet"):
            return pd.read_parquet(uploaded_file)
        elif uploaded_file.name.endswith(".xml"):
            return pd.read_xml(uploaded_file)
        elif uploaded_file.name.endswith(".db"):
            conn = sqlite3.connect(uploaded_file)
            df = pd.read_sql_query("SELECT * FROM main_table", conn)
            conn.close()
            return df
        else:
            st.error("❌ Unsupported file format")
            return None

    if uploaded_file:
        df = load_file(uploaded_file)

        if df is not None:
            st.sidebar.success("✅ File uploaded successfully!")

            # 🔹 Cleaning Options
            missing_strategy = st.sidebar.selectbox("🛠 Missing Value Handling", ["mean", "median", "most_frequent"])
            remove_duplicates = st.sidebar.checkbox("🗑 Remove Duplicates?", True)

            # 📊 Tabs for Better Organization
            tab1, tab2, tab3, tab4 = st.tabs(["📜 Raw Data", "🧼 Cleaning Process", "📊 Insights", "📥 Download"])

            with tab1:
                st.markdown("### 🔍 Raw Data Preview")
                st.dataframe(df.head(10))

                st.markdown("### 📌 Dataset Overview")
                st.write(df.describe())

            with tab2:
                with st.spinner("🚀 AI is cleaning your data... Please wait."):
                    class AICleaner:
                        def __init__(self, df):
                            self.df = df

                        def clean_data(self, missing_strategy="mean", remove_duplicates=True):
                            self.handle_missing_values(strategy=missing_strategy)
                            if remove_duplicates:
                                self.remove_duplicates()
                            return self.df

                        def handle_missing_values(self, strategy="mean"):
                            numeric_cols = self.df.select_dtypes(include=['number']).columns
                            categorical_cols = self.df.select_dtypes(include=['object']).columns

                            imputer_num = SimpleImputer(strategy=strategy)
                            imputer_cat = SimpleImputer(strategy='most_frequent')

                            if not numeric_cols.empty:
                                self.df[numeric_cols] = imputer_num.fit_transform(self.df[numeric_cols])

                            if not categorical_cols.empty:
                                self.df[categorical_cols] = imputer_cat.fit_transform(self.df[categorical_cols])

                        def remove_duplicates(self):
                            self.df.drop_duplicates(inplace=True)

                    cleaner = AICleaner(df)
                    cleaned_df = cleaner.clean_data(missing_strategy=missing_strategy, remove_duplicates=remove_duplicates)
                st.success("✅ Data cleaned successfully!")

                st.markdown("### ✅ Cleaned Data Preview")
                st.dataframe(cleaned_df.head(10))

            with tab3:
                st.markdown("### 📈 Data Insights")
                st.markdown("#### 🔍 Missing Values Heatmap")
                fig = px.imshow(df.isnull(), color_continuous_scale="viridis", title="Missing Values Heatmap")
                st.plotly_chart(fig, use_container_width=True)

            with tab4:
                cleaned_csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.sidebar.download_button("⬇️ Download Cleaned Data", cleaned_csv, "cleaned_data.csv", "text/csv", key="download")

elif page == "📖 About Us":
    st.markdown('<h1 class="stTitle">📖 About Struqtura</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stLeftAlign">
    At **Struqtura**, we specialize in transforming chaotic, unstructured data into clean, reliable, and actionable insights. 
    Organizations often struggle with inconsistent formats, missing values, and duplicated entries.  
    Our intelligent platform automates data cleaning, structuring, and integration—eliminating manual intervention.
    </div>
    """, unsafe_allow_html=True)

elif page == "📩 Contact Us":
    st.markdown('<h1 class="stTitle">📩 Contact Struqtura</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stLeftAlign">
    📧 **Email:** support@struqtura.com  
    🌍 **Website:** [www.struqtura.com](#)
    </div>
    """, unsafe_allow_html=True)
