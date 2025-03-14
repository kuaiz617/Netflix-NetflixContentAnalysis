# 🎬 Netflix Data Analysis Visualization
![Netflix Content Trends](images/Netflix.png)

## 📊 Project Introduction
As someone who loves movies and TV shows, I have always been fascinated by the evolution of streaming platforms and how they have changed the way people consume entertainment. This project was an exciting opportunity to explore Netflix’s content library through data analysis and visualization.

Netflix is a leading OTT (Over-the-Top) streaming platform, offering a vast collection of TV shows, movies, and documentaries to millions of subscribers worldwide. It provides a vast collection of TV shows, movies, anime, and documentaries, making it a dominant force in the streaming industry. With the rise of affordable smartphones and high-speed internet, streaming services have become more accessible than ever, eliminating the need for traditional cable TV. The competition between platforms such as Netflix, Amazon Prime, and Disney+ has intensified, leading to an ever-growing demand for data-driven insights to enhance content strategy.

Given this dynamic landscape, understanding Netflix’s content growth and distribution is crucial. This report explores Netflix’s content trends from 2000 to 2020, examining how the platform has expanded its library over time. The insights gained from this study could help in understanding broader streaming industry trends, including content production strategies, genre preferences, and changes in audience engagement. The project includes **interactive visualizations** using **Plotly Dash**, enabling dynamic exploration of the dataset.

## 📂 Data Description
| Feature   | Description |
|--------------|------------|
| **show_id**  | Unique ID for every Movie/TV Show |
| **type**  | Type of Content: Movie/TV Show |
| **title** | Name of the Movie/TV Show |
| **director** | Name of the Director of the Movie/TV Show |
| **cast** | Actors involved in the Movie/TV Show |
| **country** | Name of the Countries where the Movie/TV Show is produced |
| **date_added** | The Date in which the Movie/TV Show was added on Netflix |
| **release_year** | Original Release Year of the Movie/TV Show |
| **rating** | Rating of the Movie/TV Show |
| **duration** | Total Duration of the Movie (in Minutes) or TV Show (in Seasons) |
| **listed_in** | Genre of the Movie/TV Show |
| **description** | Summary of the Movie/TV Show |

## 📊 Implemented Visualizations

### 1️⃣ Yearly Release Trends
- **Visualization Type:** Line Chart
- **Description:** Tracks the number of TV shows and movies released per year.
- **Interactivity:** Hover tooltips for details.

### 2️⃣ Geographic Distribution of Netflix Content
- **Visualization Type:** Choropleth Map
- **Description:** Shows how Netflix content is distributed worldwide.
- **Interactivity:** Animated by year, hover functionality for country-specific insights.

### 3️⃣ TV Show & Movie Proportion
- **Visualization Type:** Pie Chart
- **Description:** Displays the proportion of TV Shows vs. Movies available on Netflix.
- **Interactivity:** Hover to see percentage details.

### 4️⃣ Content Added Over Time by Country
- **Visualization Type:** Stacked Area Chart
- **Description:** Compares the number of TV shows and movies added over time for different countries.
- **Interactivity:** Dropdown filter to select specific countries, hover tooltips for specific year insights.


## 🚀 Interactive Dashboard
- **Built with Plotly Dash** for seamless data exploration and interactivity.
- **Features**:
  - **Dynamic Data Filtering**:
    - Dropdown selectors allow filtering by content type (Movies/TV Shows) and rating.
    - Country selection enables trend visualization for specific regions.
  - **Multiple Interactive Visualizations**:
    - **Choropleth Map**: Displays Netflix content distribution across different countries over time.
    - **Time-Series Analysis**: Interactive trend charts track the number of TV shows and movies released per year.
    - **Pie Charts**: Visual representation of content proportions based on type and rating.
  - **Animated Visualizations**:
    - Yearly updates in the choropleth map provide insights into content distribution growth.
    - Hover tooltips display detailed data points for enhanced analysis.

📌 **Explore Netflix Trends with Interactive Controls!**

## 🛠 Data Preparation & Cleaning
### 📂 Dataset: `Cleaned_Netflix_Titles_Data.csv`
The dataset underwent preprocessing to ensure consistency, handle missing values, and optimize it for visualization.

### 🔍 Cleaning Process
- **Standardization**:
  - Trimmed spaces and converted column names to lowercase for consistency.
  - Extracted `year_added` from `date_added` for trend analysis.

- **Handling Missing Data**:
  - `release_year`: Filled missing values with `2020` for consistency.
  - `date_added`: Replaced missing entries with `"Unknown"`.
  - `country`: Entries with multiple countries were split into separate records.

- **Feature Selection & Transformation**:
  - Retained relevant fields like `type`, `release_year`, `rating`, `country`, and `categories`.
  - Parsed `listed_in` to select only the primary genre for better categorization.

### 📊 Sampling Methodology
- Focused on data from **2000 to 2020**, as trends became more significant post-2000.
- Ensured computational efficiency while maintaining meaningful insights.

This cleaning process allowed for **accurate trend analysis** and ensured that the dataset was well-structured for visualization. 🚀


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

### 📈 Key Insights
- **TV Shows vs. Movies**: TV show production surged post-2015, surpassing movies in recent years.
- **Rating Trends**: Mature content (`TV-MA`, `TV-14`) dominates Netflix’s catalog.
- **Global Expansion**: The **United States** leads in content production, followed by **India**.
- **Streaming Boom**: Content releases peaked between 2018-2019 before a decline in 2020.

### ⚠️ Limitations
- **Incomplete Data**: Some `date_added` and `release_year` values are missing, affecting timeline accuracy.
- **Single-Platform Focus**: The study is limited to **Netflix** and does not account for trends on competing platforms.
- **Simplified Genre Classification**: Only the **primary** genre was retained, potentially omitting nuanced classifications.

### 🚀 Future Improvements
- **Cross-Platform Comparison**: Expanding analysis to other streaming services (Disney+, Hulu, etc.).
- **Audience Reception Analysis**: Integrating IMDb/TMDb ratings to assess content popularity.
- **Real-Time Updates**: Utilizing APIs like **TMDb** for live data tracking.
- **Predictive Analytics**: Building a recommendation system based on content trends and user engagement.
- **Sentiment Analysis**: Examining audience reviews to uncover deeper viewing preferences.

## 🎬 Conclusion
This project explored **Netflix’s content trends (2000-2020)**, revealing key patterns in **content strategy, production shifts, and rating distributions**. While the study provides meaningful insights, incorporating **external data sources, sentiment analysis, and machine learning models** could further enhance the findings.

As streaming platforms continue to evolve, **data-driven insights** play a crucial role in shaping content strategies. Future research could **broaden scope, incorporate audience feedback, and utilize predictive modeling** to gain a more **comprehensive understanding** of the streaming industry.

## 📢 Contribution
- Feel free to **fork** this repository and open **pull requests**!
- Report issues via [GitHub Issues](https://github.com/yourusername/netflix-dashboard/issues).

## 📜 License
This project is licensed under the **MIT License**.


