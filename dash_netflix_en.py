import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import dash_bootstrap_components as dbc


# Read and preprocess data
df = pd.read_csv(r"C:\Users\zixin kuai\Desktop\DIGS 20004\Netflix\netflix_titles3.csv")


df['date_added'] = df['date_added'].fillna('Unknown')  # 填充缺失值为'Unknown'
df['year_added'] = df['date_added'].apply(
    lambda x: x.split(',')[-1].strip() if ', ' in x else '2020'  # 确保有逗号分隔
)
df['year_added'] = pd.to_numeric(df['year_added'], errors='coerce').fillna(2020).astype(int)

df['country'] = df['country'].apply(lambda x: x.replace(' ,', ',').replace(', ', ',').split(',') if pd.notna(x) else [])
lst_col = 'country'
data2 = pd.DataFrame({
    col: np.repeat(df[col].values, df[lst_col].str.len())
    for col in df.columns.drop(lst_col)}
).assign(**{lst_col: np.concatenate(df[lst_col].values)})[df.columns.tolist()]

# Handle category field
df['categories'] = df['listed_in'].apply(lambda x: x.split(',')[0] if pd.notna(x) else 'Unknown').str.strip()

df1 = df

# Filter data for years 2000-2020
df = df[(df['release_year'] >= 2000) & (df['release_year'] <= 2020)]

# Separate TV shows and movies
table_tv = df[df['type'] == 'TV Show']
table_mv = df[df['type'] == 'Movie']

# Figure 1: Content count distribution (bar chart)
year_counts = df['release_year'].value_counts().sort_index()
# Figure 2: Release trends (movies vs TV shows)
df_tv_count = table_tv['release_year'].value_counts().sort_index()
df_mv_count = table_mv['release_year'].value_counts().sort_index()
# Use TV show years as base (movie data might have missing years)
df_trends = pd.DataFrame({
    'Year': df_tv_count.index,
    'TV Shows': df_tv_count.values,
    'Movies': df_mv_count.reindex(df_tv_count.index, fill_value=0).values
})
# Figure 3: Content type ratio (pie chart)
type_counts = df['type'].value_counts()
# Figure 4: Rating comparison (TV shows vs movies)
tv_rating = table_tv['rating'].value_counts()
mv_rating = table_mv['rating'].value_counts()
rating_data = pd.concat([tv_rating, mv_rating], axis=1, keys=['TV Show', 'Movie']).fillna(0).astype(int)
rating_data = rating_data.sort_index()
# Figure 5: Movie ratings distribution (movies only)
mv_rating_df = table_mv['rating'].value_counts().reset_index()
mv_rating_df.columns = ['Rating', 'Count']
# Figure 6: Movie rating trends
# Create pivot table: rows=rating, columns=release_year
t_mv = table_mv.groupby(['rating', 'release_year']).size().unstack(fill_value=0)
# Keep common ratings
ratings_mv = ['TV-MA', 'TV-14', 'R', 'TV-PG', 'PG-13', 'PG', 'TV-Y', 'TV-G']
t_mv = t_mv.reindex(columns=sorted(t_mv.columns)).reset_index().melt(id_vars='rating', var_name='Year', value_name='Count')
t_mv = t_mv[t_mv['rating'].isin(ratings_mv)]
t_mv['Year'] = t_mv['Year'].astype(int)
# Figure 7: TV show ratings distribution (TV only)
tv_rating_df = table_tv['rating'].value_counts().reset_index()
tv_rating_df.columns = ['Rating', 'Count']
# Figure 8: TV rating trends
t_tv = table_tv.groupby(['rating', 'release_year']).size().unstack(fill_value=0)
ratings_tv = ['TV-MA', 'TV-14', 'TV-PG', 'TV-Y7', 'TV-Y', 'TV-G']
t_tv = t_tv.reindex(columns=sorted(t_tv.columns)).reset_index().melt(id_vars='rating', var_name='Year', value_name='Count')
t_tv = t_tv[t_tv['rating'].isin(ratings_tv)]
t_tv['Year'] = t_tv['Year'].astype(int)
# Figure 9: Movie duration distribution
# Clean duration field (remove " min")
df_movie = table_mv[table_mv['duration'].notnull()].copy()
df_movie['duration_clean'] = df_movie['duration'].str.replace(' min', '').astype(int)
duration_data = df_movie['duration_clean']

colors = ['#221f1f', '#b20710', '#4682B4', '#FFD700', '#32CD32', '#8A2BE2', '#FF4500']
df3 = df.explode('country')
unique_countries = df3['country'].dropna().unique()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Navbar with Home on the left and Data Source on the right
navbar = dbc.Navbar(
    dbc.Container([
        # Left-aligned "Home" link
        dbc.NavbarBrand("Home", href="#", style={'fontSize': '20px', 'fontStyle': 'italic'}),

        # Right-aligned "Data Source" link
        dbc.Nav(
            dbc.NavItem(dbc.NavLink("Data Source", href="https://www.kaggle.com/datasets/shivamb/netflix-shows", style={'fontSize': '18px'})),
            className="ms-auto",  # Aligns "Data Source" to the right
        ),
    ]),
    color="light",  # Light background color
    style={'backgroundColor': '#f8f9fa'},  # Custom light gray background
    className="mb-4",  # Adds bottom margin
)

app.layout = html.Div([
    navbar,  # Include navbar at the top
    html.H1(
        "Analysis Of Netflix Movies And TV Shows ",
        style={
            'textAlign': 'center',
            'fontSize': '32px',
            'fontWeight': 'bold',
            'fontStyle': 'italic', 
            'fontFamily': 'Georgia, serif', 
            'marginBottom': '5px'
        }
    ),
    html.H3(
        "(2000-2020)",
        style={
            'textAlign': 'center',
            'fontSize': '24px',
            'fontStyle': 'italic', 
            'color': '#555', 
            'fontFamily': 'Georgia, serif'
        }
    ),
    html.H3(
        "Observe The Distribution Of The Number Of Movies And TV Series",
        style={
            'textAlign': 'center',
            'fontSize': '20px', 
            'fontWeight': 'bold', 
            'fontFamily': 'Georgia, serif',
            'marginTop': '30px' 
        }
    ),
    html.Div(
        html.P(
            "Since 2000, the data has shown significant changes, so the analysis focuses on the period from 2000 to 2020.",
            style={'fontSize': '16px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    html.Div([
        dcc.Graph(id='graph1'),

        html.Label("Select Year Range:", style={'fontSize': 18, 'color': '#212121'}),
        dcc.RangeSlider(
            id='year-slider',
            min=2000,
            max=2020,
            step=1,
            marks={i: str(i) for i in range(2000, 2021, 5)},
            value=[2000, 2020]
        )
    ], style={'width': '80%', 'margin': 'auto', 'padding': '20px 0'}),

    html.H3(
        "Observe The Trend In The Number Of Movies And TV Series Releases", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The chart highlights a significant rise in content production after 2010, with movies peaking in 2018-2019 before declining, while TV shows continue to grow steadily. This suggests a shift in the entertainment industry, where serialized content is becoming more dominant in the streaming era.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph2'),
    
        html.H3(
        "Compare The Number Of Movies And TV Series", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "While movies currently dominate the content landscape, TV shows hold a strong and growing share, reflecting a shift in audience preferences and industry strategies. The trend suggests a potential increase in TV show production in the future, especially driven by streaming platforms.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph3'),

        html.H3(
        "Observe The Number Of Movies And TV Series By Rating", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The majority of TV shows and movies are aimed at teen and adult audiences, with TV-MA and TV-14 being the most frequent ratings. While there is some children’s content, it is much less common compared to mature-rated productions. The dominance of R-rated and PG-13 movies further highlights a preference for content that appeals to older viewers.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph4'),

        html.H3(
        "Observe The Number Of Movies In Each Rating Category Over The Past 20 Years", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The majority of movies are targeted at mature and teenage audiences, with TV-MA and TV-14 dominating. Family-friendly and children's movies make up a small portion, while NC-17 and Unrated movies are rare. This reflects a market preference for adult-oriented content, particularly as streaming platforms focus on engaging older audiences.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph5'),

        html.H3(
        "Observe The Release Trends Of Movies By Rating", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The movie industry saw significant growth in mature-rated content (TV-MA, TV-14, R) from 2015 to 2019, reflecting the shift towards adult-oriented films. However, production declined in 2020, possibly due to industry challenges. Family-friendly and children's movies remained relatively stable over time, indicating a continued but smaller demand for these genres.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph6'),

        html.H3(
        "Observe The Number Of TV Series By Rating Over The Past 20 Years", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The majority of TV shows are aimed at mature (TV-MA) and teenage (TV-14) audiences, reflecting the growing demand for more adult-themed and dramatic content. Meanwhile, family and children's programming remains a smaller segment, suggesting that platforms may prioritize content for older demographics.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph7'),

        html.H3(
        "Observe The Release Trends Of Movies By Rating", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The majority of new TV shows are geared towards mature audiences (TV-MA) and teenagers (TV-14), showing a clear shift towards darker, more adult-oriented storytelling. While family-friendly content has grown, it remains a smaller segment, suggesting that streaming platforms prioritize more mature and teen-focused programming.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph8'),

        html.H3(
        "Observe The Distribution Of Movie Duration Data", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The majority of movies fall within the 90-100 minute range, supporting the idea that feature films are optimized for audience engagement within this timeframe. While short films and extremely long movies exist, they are much less frequent. The right skew in the distribution suggests that some films push beyond the conventional runtime, but they remain outliers.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph9'),

        html.H3(
        "Observe The Trend In TV Series Releases. ", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The chart suggests a strong upward trend in content diversity, with International content leading the growth. Other categories, such as Kids, Crime, and TV, have also expanded, indicating an increased demand for varied content over the years",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph10'),

        html.H3(
        "Observing The Release Trends Of Different Movie Genres", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "From 2015 to 2019, there was a significant increase in the release of all genres, particularly Dramas and Documentaries. However, after 2019, there was a slight decline, possibly due to industry shifts or changing audience preferences.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    dcc.Graph(id='graph11'),

        html.H3(
        "Global Growth Of Streaming Content Over Time", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The rise of streaming services has driven a massive increase in content production, particularly after 2015. The United States dominates, but international content has seen steady growth. The peak in 2020 followed by a decline suggests possible industry adjustments in response to market saturation or external factors.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    html.Br(),
    dcc.Dropdown(
        id='country-selector',
        options=[{'label': country, 'value': country} for country in unique_countries],
        value=['United States', 'India'],  # 默认选择
        multi=True,
        style={'fontSize': '18px', 'width': '100%'}
    ),
    dcc.Graph(id='graph13'),

        html.H3(
        "Global Movies And TV Production Trends By Country", style={'textAlign': 'center','fontSize': '20px','fontWeight': 'bold','fontFamily': 'Georgia, serif','marginTop': '30px'    }
    ),
    html.Div(
        html.P(
            "The chart highlights a strong dominance of the United States and India in film and TV production, with Europe and Canada contributing significantly. The surge in production after 2015 reflects the impact of streaming platforms, which have driven global content expansion. However, some regions still have limited contributions, emphasizing ongoing disparities in global media production.",
            style={'fontSize': '14px', 'color': '#212121', 'textAlign': 'center'}
        ),
        style={'width': '50%', 'margin': 'auto'} 
    ),
    html.Br(),
    dcc.Graph(id='graph12'),

], style={'maxWidth': '1200px', 'margin': 'auto'})

# Callbacks: All charts filter data based on year range

# Figure 1: Content count distribution
@app.callback(
    Output('graph1', 'figure'),
    Input('year-slider', 'value')
)
def update_graph1(year_range):
    data = df1['release_year'].value_counts().reset_index()
    data.columns = ['Year', 'Count']
    data = data.sort_values(by='Year')
    fig = px.bar(
        data, x='Year', y='Count',
        title="Bar Chart of Netflix Films and TV Shows' Release Years",
        labels={'x': 'Year', 'y': 'Count'}
    )
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        )
    )
    return fig

# Figure 2: Release trends
@app.callback(
    Output('graph2', 'figure'),
    Input('year-slider', 'value')
)
def update_graph2(year_range):
    yr_min, yr_max = year_range
    mask_tv = (table_tv['release_year'] >= yr_min) & (table_tv['release_year'] <= yr_max)
    mask_mv = (table_mv['release_year'] >= yr_min) & (table_mv['release_year'] <= yr_max)
    tv_data = table_tv[mask_tv]['release_year'].value_counts().sort_index()
    mv_data = table_mv[mask_mv]['release_year'].value_counts().sort_index()
    common_years = sorted(set(tv_data.index) | set(mv_data.index))
    trend_df = pd.DataFrame({
        'Realease Year': common_years,
        'TV Shows': [tv_data.get(y, 0) for y in common_years],
        'Movies': [mv_data.get(y, 0) for y in common_years]
    })
    fig = px.line(trend_df, x='Realease Year', y=['TV Shows', 'Movies'],
                  markers=True,
                  title="Trends in the number of TV Show & Movies")
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Release Year",
        yaxis_title="Number of TV Show & Movie"
    )
    return fig


# Figure 3: Content type ratio
@app.callback(
    Output('graph3', 'figure'),
    Input('year-slider', 'value')
)
def update_graph3(year_range):
    yr_min, yr_max = year_range
    mask = (df['release_year'] >= yr_min) & (df['release_year'] <= yr_max)
    data = df[mask]['type'].value_counts()
    fig = px.pie(values=data.values, names=data.index,
                 title="TV Show & Movie Proportion")
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ))
    return fig

# Figure 4: Rating comparison
@app.callback(
    Output('graph4', 'figure'),
    Input('year-slider', 'value')
)
def update_graph4(year_range):
    yr_min, yr_max = year_range
    mask = (df['release_year'] >= yr_min) & (df['release_year'] <= yr_max)
    
    tv_data = df[mask & (df['type'] == 'TV Show')]['rating'].value_counts()
    mv_data = df[mask & (df['type'] == 'Movie')]['rating'].value_counts()
    
    # Ensure that data is not empty, if empty, use default data
    if tv_data.empty:
        tv_data = pd.Series([0], index=['No Data'])
    if mv_data.empty:
        mv_data = pd.Series([0], index=['No Data'])
    
    data = pd.concat([tv_data, mv_data], axis=1, keys=['TV Show', 'Movie']).fillna(0).astype(int)
    data = data.sort_index().reset_index().rename(columns={'index': 'Rating'})
    
    fig = px.bar(data, x='rating', y=['TV Show', 'Movie'],
                 barmode='group', title="Ratings of TV Show & Movies",
                 labels={'value': 'Count', 'Rating': 'Rating'})
    
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Ratings",
        yaxis_title="Number of TV Show & Movie"
    )
    return fig


# Figure 5: Rating of Movie
@app.callback(
    Output('graph5', 'figure'),
    Input('year-slider', 'value')
)
def update_graph5(year_range):
    yr_min, yr_max = year_range
    # Apply a mask to filter data based on the selected year range
    mask = (table_mv['release_year'] >= yr_min) & (table_mv['release_year'] <= yr_max)
    data = table_mv[mask]['rating'].value_counts().reset_index()
    print(data.columns)
    data.columns = ['Rating', 'Count']
    data = data.dropna(subset=['Rating', 'Count'])
    # Print the first few rows of the data to verify it looks correct
    print(data.head())
    fig = px.bar(data, x='Rating', y='Count', title="Ratings of Movies")
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Ratings",
        yaxis_title="Number of Movies"
    )
    return fig


# Figure 6: Trends in the number of Movie
@app.callback(
    Output('graph6', 'figure'),
    Input('year-slider', 'value')
)
def update_graph6(year_range):
    yr_min, yr_max = year_range
    temp = table_mv[(table_mv['release_year'] >= yr_min) & (table_mv['release_year'] <= yr_max)]
    t = temp.groupby(['rating', 'release_year']).size().unstack(fill_value=0)
    ratings_mv = ['TV-MA', 'TV-14', 'R', 'TV-PG', 'PG-13', 'PG', 'TV-Y', 'TV-G']
    t = t.loc[t.index.intersection(ratings_mv)]
    t = t.reset_index().melt(id_vars='rating', var_name='Year', value_name='Count')
    t['Year'] = t['Year'].astype(int)
    fig = px.line(t, x='Year', y='Count', color='rating', title="Trends in the number of Movie")
    
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Release Year",
        yaxis_title="Number of TV Movie")
    return fig


# Figure 7: Number of TV Show
@app.callback(
    Output('graph7', 'figure'),
    Input('year-slider', 'value')
)
def update_graph7(year_range):
    yr_min, yr_max = year_range
    mask = (table_tv['release_year'] >= yr_min) & (table_tv['release_year'] <= yr_max)
    data = table_tv[mask]['rating'].value_counts().reset_index()
    data.columns = ['Rating', 'Count']
    fig = px.bar(data, x='Rating', y='Count', title="Number of TV Show", color='Rating', 
                 color_discrete_sequence=['#B0C4DE', '#98FB98', '#AFEEEE', '#FFDAB9', '#D3D3D3', '#F5F5F5', '#E0FFFF'])

    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Ratings",
        yaxis_title="Number of TV Show")
    return fig



# Figure 8: TV rating trends
@app.callback(
    Output('graph8', 'figure'),
    Input('year-slider', 'value')
)
def update_graph8(year_range):
    yr_min, yr_max = year_range
    temp = table_tv[(table_tv['release_year'] >= yr_min) & (table_tv['release_year'] <= yr_max)]
    t = temp.groupby(['rating', 'release_year']).size().unstack(fill_value=0)
    ratings_tv = ['TV-MA', 'TV-14', 'TV-PG', 'TV-Y7', 'TV-Y', 'TV-G']
    t = t.loc[t.index.intersection(ratings_tv)]
    t = t.reset_index().melt(id_vars='rating', var_name='Year', value_name='Count')
    t['Year'] = t['Year'].astype(int)
    fig = px.line(t, x='Year', y='Count', color='rating',
                  title="Trends in the number of TV Show", 
                  color_discrete_sequence=['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2', '#FF4500'])
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Ratings",
        yaxis_title="Number of TV Show")
    return fig


# Figure 9: Movie duration distribution
@app.callback(
    Output('graph9', 'figure'),
    Input('year-slider', 'value')
)
def update_graph9(year_range):
    yr_min, yr_max = year_range
    temp = table_mv[(table_mv['release_year'] >= yr_min) & (table_mv['release_year'] <= yr_max)]
    temp = temp[temp['duration'].notnull()].copy()
    temp['duration_clean'] = temp['duration'].str.replace(' min', '').astype(int)
    fig = ff.create_distplot([temp['duration_clean']], group_labels=['Duration'], show_hist=True, show_rug=False,
                             colors=['#D32F2F'])
    fig.update_layout(title="Movie Duration Distribution", xaxis_title="Minutes", yaxis_title="Density")
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Duration",
        yaxis_title="Density")
    return fig

# Figure 10: Trend Chart of TV Show Genres' Release Year Analysis
@app.callback(
    Output('graph10', 'figure'),
    Input('year-slider', 'value')
)
def update_graph10(year_range):
    yr_min, yr_max = year_range
    temp = table_tv[(table_tv['release_year'] >= yr_min) & (table_tv['release_year'] <= yr_max)]
    m = temp.groupby(['categories', 'release_year']).size().unstack(fill_value=0)
    top_categories = m.sum(axis=1).sort_values(ascending=False).head(5).index.tolist()
    m = m.loc[top_categories].reset_index().melt(id_vars='categories', var_name='Year', value_name='Count')
    m['Year'] = m['Year'].astype(int)
    fig = px.line(m, x='Year', y='Count', color='categories',
                  title="Trend Chart of TV Show Genres' Release Year Analysis",
                  color_discrete_sequence=['#D32F2F', '#FF6B6B', '#FF9999', '#8B0000', '#FFD700'])
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Release Year",
        yaxis_title="Number of categories")
    return fig

# Figure 11: Trend Chart of Movie Genres' Release Year Analysis
@app.callback(
    Output('graph11', 'figure'),
    Input('year-slider', 'value')
)
def update_graph11(year_range):
    yr_min, yr_max = year_range
    temp = table_mv[(table_mv['release_year'] >= yr_min) & (table_mv['release_year'] <= yr_max)]
    v = temp.groupby(['categories', 'release_year']).size().unstack(fill_value=0)
    top_categories = v.sum(axis=1).sort_values(ascending=False).head(5).index.tolist()
    v = v.loc[top_categories].reset_index().melt(id_vars='categories', var_name='Year', value_name='Count')
    v['Year'] = v['Year'].astype(int)
    fig = px.line(v, x='Year', y='Count', color='categories',
                  title="Trend Chart of Movie Genres' Release Year Analysis",
                  color_discrete_sequence=['#D32F2F', '#FF6B6B', '#FF9999', '#8B0000', '#FFD700'])
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ),
        xaxis_title="Release Year",
        yaxis_title="Number of categories")
    return fig

@app.callback(
    Output('graph13', 'figure'),
    Input('country-selector', 'value')
)
def update_graph13(selected_countries):
    if not selected_countries:
        return px.area(title="Select countries to view trends")

    df['country'] = df['country'].apply(lambda x: x[0] if isinstance(x, list) and x else x)

    filtered_df = df[df['country'].isin(selected_countries)].dropna(subset=['year_added'])

    filtered_df['year_added'] = filtered_df['year_added'].astype(int)

    grouped_data = filtered_df.groupby(['year_added', 'country']).size().reset_index(name='Count')
    
    if grouped_data.empty:
        return px.area(title="No data available for the selected countries")
    
    fig = px.area(grouped_data, x='year_added', y='Count', color='country', line_group='country',
                  title="Content Added Over Time by Country",
                  color_discrete_sequence=px.colors.qualitative.Set1)
    
    fig.update_traces(mode='lines', line_shape='spline', fill='tozeroy')
    fig.update_layout(
        title_font=dict(family='Arial', size=24, color='black'),
        xaxis_title="Year",
        yaxis_title="Content Count",
        xaxis=dict(tickmode='linear', tick0=grouped_data['year_added'].min(), dtick=1),
        hovermode='x unified',
        plot_bgcolor='white'
    )
    
    return fig


# Figure 12:Geographical Analysis Map of Production Countries by Release Year
@app.callback(
    Output('graph12', 'figure'),
    Input('year-slider', 'value')
)
def update_graph12(year_range):
    yr_min, yr_max = year_range
    
    # 根据年份范围过滤数据
    filtered = data2[(data2['year_added'] >= yr_min) & (data2['year_added'] <= yr_max)]
    
    year_country2 = filtered.groupby('year_added')['country'].value_counts().reset_index(name='counts')
    fig = px.choropleth(
        year_country2,
        locations="country",
        color="counts",
        locationmode='country names',
        animation_frame='year_added',
        range_color=[0, 200],
        color_continuous_scale=px.colors.sequential.OrRd,
        title='Geographical Analysis Map of Production Countries by Release Year'
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    fig.update_layout(
        title_font=dict(
            family='Arial',
            size=24,
            color='black'
        ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)