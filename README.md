# 🎬 Netflix Data Analysis Visualization

## 📊 Project Overview
This project explores Netflix data from **2000 to 2020**, analyzing trends in content release, distribution by country, and rating distributions. The project includes **interactive visualizations** using **Plotly Dash**, enabling dynamic exploration of the dataset.

## 📊 Implemented Visualizations

### 1️⃣ Yearly Release Trends
- **Visualization Type**: Line Chart
- **Description**: Tracks the number of TV shows and movies released per year.
- **Interactivity**: Hover tooltips for details.

### 2️⃣ Geographic Distribution of Netflix Content
- **Visualization Type**: Choropleth Map
- **Description**: Shows how Netflix content is distributed worldwide.
- **Interactivity**: Animated by year, hover functionality for country-specific insights.

### 3️⃣ Content Ratings Distribution
- **Visualization Type**: Bar Chart
- **Description**: Displays the number of titles across different ratings (G, PG, TV-MA, etc.).

## 🚀 Interactive Dashboard
- **Built with Plotly Dash** for seamless exploration.
- **User Inputs**:
  - Dropdowns for filtering by content type (Movies/TV Shows) and rating.
  - Animated choropleth map for content distribution over the years.

## 📈 Data Preparation & Cleaning
### Dataset: `Cleaned_Netflix_Titles_Data.csv`
- **Columns Standardized**: Trimmed spaces, converted to lowercase.
- **Missing Values**:
  - `release_year` filled with `NULL` → Replaced with `2020`.
  - `country` entries split into multiple records.
- **Data Transformation**:
  - `date_added` parsed to extract `year_added`.
  - Grouped data by `release_year` and `rating` for structured analysis.

## 📝 How to Run the Project
### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/netflix-dashboard.git
cd netflix-dashboard
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Dash Application
```bash
python app.py
```
- Open **http://127.0.0.1:8050/** in your browser.

## 🔍 Key Insights & Limitations
- **TV Shows vs. Movies**: TV Shows increased significantly post-2015.
- **Rating Distribution**: `TV-MA` is the most common rating.
- **Geographic Trends**: USA dominates Netflix content production.
- **Limitations**:
  - Dataset may not include **all** Netflix releases.
  - Some `country` and `release_year` values are incomplete.

## 📢 Contribution
- Feel free to **fork** this repository and open **pull requests**!
- Report issues via [GitHub Issues](https://github.com/yourusername/netflix-dashboard/issues).

## 📜 License
This project is licensed under the **MIT License**.


