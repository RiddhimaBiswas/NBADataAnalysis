🚀 Live Dashboard

🌐 Link: https://nbadataanalysis.streamlit.app/

🎯 Objectives of the Dashboard

This analytics dashboard was created to satisfy the following requirements:

✔ Season-wise & game-wise scoring trends
✔ Team-wise comparisons & East vs West conference dynamics
✔ Player insights – top scorers, rebounds, assists
✔ Official win–loss rankings & standings table
✔ Interactive filters: season slider, team selector
✔ Deep dive – team performance trend over time

✨ Dashboard Features (What You Can Do)
Feature	Description
📈 League Trends	View 20-year NBA scoring trend & home-court win percentage
🌍 Conference Analysis	Bar chart + heatmap comparing East vs West dominance
⚔️ Head-to-Head	Radar chart comparing two teams across 5 performance metrics
👤 Player Stars	Top 10 players each season (PTS, REB, AST) + scatter plot
🏆 Season Rankings	Full win–loss standings table based on total season wins
📊 Team Trends	Select a team and see its historical trajectory (Win%, Avg Points)
🎛 Interactivity	Filters for year range, team, and season
🧠 Insights From the Data (Useful If Asked in Interview / Judging)

🟢 NBA average scoring increased significantly after 2015
🟢 Home-court advantage remains around 55% win rate
🟢 Western conference dominated majority of seasons, though East shows comeback in specific years
🟢 Scatter plots reveal elite scorers form a clustered power curve
🟢 Radar view clearly differentiates offensive-heavy vs defensive-rebounding teams
🟢 Heatmap visually reveals dynasties — teams consistently high in home wins

🏗 Tech Stack
Layer	Technologies
🧠 Programming	Python
🖥 Web Framework	Streamlit
📊 Visualization	Plotly Express, Plotly Graph Objects
📂 Data Handling	Pandas, Numpy
🗂 Dataset Format	CSV
📂 Dataset Description

Folder contains full NBA dataset:

data/
 ├─ master_games.csv             # game-level stats (pts, fg%, assists, rebounds...)
 ├─ master_player_stats.csv      # player-level features season-wise
 ├─ ranking.csv                  # conference ID mapping


Coverage: Seasons 2004 – 2022

🧭 Project Structure
NBADataAnalysis/
 ├─ app.py                  # ⭐ Main dashboard application (Streamlit)
 ├─ data/                   # CSV dataset folder
 │   ├─ master_games.csv
 │   ├─ master_player_stats.csv
 │   ├─ ranking.csv
 ├─ requirements.txt        # Libraries needed
 ├─ README.md               # Documentation (this file)
 └─ screenshots/            # Optional screenshots (add manually)

🛠 Installation & Running Guide (Local Machine)
1️⃣ Clone the Repository
git clone https://github.com/RiddhimaBiswas/NBADataAnalysis.git
cd NBADataAnalysis

2️⃣ Install Python Dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit App
streamlit run app.py


➡ Output will open in browser at:

http://localhost:8501

🌟 Deployment (Optional)

Deploy using Streamlit Cloud in 1 minute:

1️⃣ Go to https://share.streamlit.io

2️⃣ Click “New App”
3️⃣ Connect Github → Select this repo
4️⃣ Set file path → app.py
5️⃣ Click Deploy 🚀
