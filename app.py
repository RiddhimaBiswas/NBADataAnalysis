import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="NBA Analytics Dashboard", page_icon="🏀", layout="wide")

# 2. Load Data (Cached)
@st.cache_data
def load_data():
    games = pd.read_csv('master_games.csv')
    players = pd.read_csv('master_player_stats.csv', low_memory=False)
    rankings = pd.read_csv('ranking.csv')
    
    # Fix 1: Merge Conference info
    conf_map = rankings[['TEAM_ID', 'CONFERENCE']].drop_duplicates()
    conf_map = conf_map[conf_map['CONFERENCE'].isin(['East', 'West'])]
    games = pd.merge(games, conf_map, left_on='HOME_TEAM_ID', right_on='TEAM_ID', how='left')
    
    # Fix 2: Calculate Total Points & Home Win
    games['TOTAL_POINTS'] = games['PTS_home'] + games['PTS_away']
    games['IS_HOME_WIN'] = (games['PTS_home'] > games['PTS_away']).astype(int)
    
    return games, players

try:
    df_games, df_players = load_data()
except FileNotFoundError:
    st.error("Error: CSV files not found. Please ensure master_games.csv exists.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("🏀 Dashboard Filters")
st.sidebar.info("Explore 20 years of NBA evolution.")
st.sidebar.markdown("---")
st.sidebar.markdown("**About this Dashboard**")
st.sidebar.markdown("""
- **Data Source:** NBA Official Records (2004-2022)
- **Tech Stack:** Python, Streamlit, Plotly
- **Developer:** Saurabh Kumar, Riddhima Biswas, Abhijit Dalai
""")

# Global Season Filter
all_seasons = sorted(df_games['SEASON'].unique())
selected_season_range = st.sidebar.slider("Select Season Range:", 
                                          min_value=int(df_games['SEASON'].min()), 
                                          max_value=int(df_games['SEASON'].max()), 
                                          value=(2010, 2022))

# Filter Data Global
df_filtered = df_games[(df_games['SEASON'] >= selected_season_range[0]) & 
                       (df_games['SEASON'] <= selected_season_range[1])]

# 4. Main Dashboard UI
st.title("🏀 NBA Evolution Analysis")
st.markdown("Analyzing how the game has changed: **Scoring, Home Advantage, Star Power, and Team Rankings.**")

# --- UPDATED TABS (Added Rankings Tab) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends", "🌍 Conference", "⚔️ Head-to-Head", "👤 Players", "🏆 Rankings"])

# --- TAB 1: TRENDS ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("The Scoring Explosion")
        scoring_trend = df_filtered.groupby('SEASON')['TOTAL_POINTS'].mean().reset_index()
        fig_score = px.line(scoring_trend, x='SEASON', y='TOTAL_POINTS', markers=True,
                            title='Avg Total Points per Game', template='plotly_dark')
        st.plotly_chart(fig_score, use_container_width=True)
    with col2:
        st.subheader("Home Court Advantage")
        home_adv = df_filtered.groupby('SEASON')['IS_HOME_WIN'].mean().reset_index()
        home_adv['WIN_PERCENTAGE'] = home_adv['IS_HOME_WIN'] * 100
        fig_home = px.line(home_adv, x='SEASON', y='WIN_PERCENTAGE', markers=True,
                           title='Home Win %', template='plotly_dark')
        fig_home.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Neutral")
        st.plotly_chart(fig_home, use_container_width=True)

# --- TAB 2: CONFERENCE ---
with tab2:
    st.subheader("East vs. West Dominance")
    home_wins = df_filtered[df_filtered['PTS_home'] > df_filtered['PTS_away']]
    conf_wins = home_wins.groupby(['SEASON', 'CONFERENCE']).size().reset_index(name='WINS')
    fig_conf = px.bar(conf_wins, x='SEASON', y='WINS', color='CONFERENCE',
                      color_discrete_map={'East': '#0051B4', 'West': '#C9082A'},
                      barmode='group', template='plotly_dark')
    st.plotly_chart(fig_conf, use_container_width=True)

    st.markdown("---")
    st.subheader("🔥 Dynasty Heatmap: Consistency over Time")
    
    # Heatmap Logic
    season_standings = df_filtered.groupby(['SEASON', 'HOME_TEAM_NAME'])['IS_HOME_WIN'].sum().reset_index()
    season_standings.rename(columns={'HOME_TEAM_NAME': 'TEAM', 'IS_HOME_WIN': 'HOME_WINS'}, inplace=True)
    heatmap_data = season_standings.pivot(index='TEAM', columns='SEASON', values='HOME_WINS')
    
    fig_heat = px.imshow(heatmap_data, 
                        labels=dict(x="Season", y="Team", color="Home Wins"),
                        x=heatmap_data.columns, y=heatmap_data.index,
                        color_continuous_scale='Magma',
                        title="Team Performance Intensity (Home Wins)")
    fig_heat.update_layout(template='plotly_dark', height=800)
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 3: HEAD-TO-HEAD ---
with tab3:
    st.subheader("⚔️ Team Comparison Radar")
    
    # Prepare Data
    home_stats = df_filtered[['HOME_TEAM_NAME', 'PTS_home', 'AST_home', 'REB_home', 'FG_PCT_home', 'FG3_PCT_home']].rename(
        columns={'HOME_TEAM_NAME':'TEAM', 'PTS_home':'PTS', 'AST_home':'AST', 'REB_home':'REB', 'FG_PCT_home':'FG%', 'FG3_PCT_home':'3P%'})
    away_stats = df_filtered[['AWAY_TEAM_NAME', 'PTS_away', 'AST_away', 'REB_away', 'FG_PCT_away', 'FG3_PCT_away']].rename(
        columns={'AWAY_TEAM_NAME':'TEAM', 'PTS_away':'PTS', 'AST_away':'AST', 'REB_away':'REB', 'FG_PCT_away':'FG%', 'FG3_PCT_away':'3P%'})
    
    team_stats_all = pd.concat([home_stats, away_stats])
    avg_stats = team_stats_all.groupby('TEAM').mean().reset_index()

    teams_list = sorted(avg_stats['TEAM'].unique())
    col_a, col_b = st.columns(2)
    with col_a:
        team1 = st.selectbox("Select Team A", teams_list, index=0)
    with col_b:
        team2 = st.selectbox("Select Team B", teams_list, index=1)

    t1_data = avg_stats[avg_stats['TEAM'] == team1].iloc[0]
    t2_data = avg_stats[avg_stats['TEAM'] == team2].iloc[0]

    categories = ['Points', 'Assists', 'Rebounds', 'FG %', '3P %']
    t1_vals = [t1_data['PTS'], t1_data['AST'], t1_data['REB'], t1_data['FG%']*100, t1_data['3P%']*100]
    t2_vals = [t2_data['PTS'], t2_data['AST'], t2_data['REB'], t2_data['FG%']*100, t2_data['3P%']*100]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=t1_vals, theta=categories, fill='toself', name=team1))
    fig_radar.add_trace(go.Scatterpolar(r=t2_vals, theta=categories, fill='toself', name=team2))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 120])), template='plotly_dark')
    
    st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 4: PLAYERS (UPGRADED) ---
with tab4:
    st.subheader("👤 Player Insights")
    
    # 1. Scatter Plot (General)
    curr_season = st.selectbox("Select Season for Overview:", all_seasons, index=len(all_seasons)-1)
    season_stats = df_players[df_players['SEASON'] == curr_season]
    
    # Aggregating for Scatter
    top_players = season_stats.groupby('PLAYER_NAME')[['PTS', 'REB', 'AST']].mean().reset_index()
    top_players = top_players[top_players['PTS'] > 10]
    
    fig_player = px.scatter(top_players, x='PTS', y='REB', size='PTS', color='AST',
                            hover_name='PLAYER_NAME', title=f'Offensive Leaders ({curr_season})',
                            template='plotly_dark', color_continuous_scale='Viridis')
    st.plotly_chart(fig_player, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Player Career Search (New Interactivity!)
    st.subheader("🔎 Search Player Career Trajectory")
    
    # Get list of unique players
    player_list = sorted(df_players['PLAYER_NAME'].unique())
    # Default selection (e.g., LeBron)
    default_ix = player_list.index("LeBron James") if "LeBron James" in player_list else 0
    
    selected_player = st.selectbox("Type to Search Player:", player_list, index=default_ix)
    
    # Filter data for this player
    player_career = df_players[df_players['PLAYER_NAME'] == selected_player]
    
    # Group by Season to see evolution
    career_stats = player_career.groupby('SEASON')[['PTS', 'REB', 'AST']].mean().reset_index()
    
    fig_career = px.line(career_stats, x='SEASON', y=['PTS', 'REB', 'AST'], 
                         markers=True, title=f"Career Trajectory: {selected_player}",
                         template='plotly_dark')
    st.plotly_chart(fig_career, use_container_width=True)

# --- TAB 5: RANKINGS (NEW FEATURE) ---
with tab5:
    st.subheader("🏆 Team Rankings & Win-Loss Patterns")
    
    rank_season = st.selectbox("Select Season for Rankings:", all_seasons, index=len(all_seasons)-1, key='rank_select')
    
    # Calculate Wins/Losses for that season
    # Get Home Wins
    season_games = df_games[df_games['SEASON'] == rank_season]
    
    # Home Wins
    home_wins = season_games[season_games['PTS_home'] > season_games['PTS_away']].groupby('HOME_TEAM_NAME').size()
    # Away Wins
    away_wins = season_games[season_games['PTS_away'] > season_games['PTS_home']].groupby('AWAY_TEAM_NAME').size()
    
    # Combine
    total_wins = home_wins.add(away_wins, fill_value=0).sort_values(ascending=False).reset_index()
    total_wins.columns = ['Team', 'Wins']
    
    # Calculate Losses (Total Games - Wins)
    # Count games played (Home + Away)
    games_played_home = season_games.groupby('HOME_TEAM_NAME').size()
    games_played_away = season_games.groupby('AWAY_TEAM_NAME').size()
    total_games = games_played_home.add(games_played_away, fill_value=0).reset_index()
    total_games.columns = ['Team', 'Games Played']
    
    # Merge
    standings = pd.merge(total_wins, total_games, on='Team')
    standings['Losses'] = standings['Games Played'] - standings['Wins']
    standings['Win %'] = (standings['Wins'] / standings['Games Played'] * 100).round(1)
    
    # Display Leaderboard
    col_rank1, col_rank2 = st.columns([1, 2])
    
    with col_rank1:
        st.caption(f"Regular Season Standings ({rank_season})")
        st.dataframe(standings[['Team', 'Wins', 'Losses', 'Win %']].style.highlight_max(axis=0, color='darkgreen'), height=600)
        
    with col_rank2:
        st.caption("Win % Distribution")
        fig_standings = px.bar(standings, x='Wins', y='Team', orientation='h', 
                               color='Win %', title=f"Leaderboard: {rank_season}",
                               template='plotly_dark', color_continuous_scale='Blues')
        fig_standings.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_standings, use_container_width=True)