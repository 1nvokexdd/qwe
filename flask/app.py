from flask import Flask, render_template, request, jsonify
import plotly
import plotly.express as px
import pandas as pd
import json
from utils.db_connector import DBConnector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = DBConnector()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Все треки
@app.route('/tracks')
def tracks():
    tracks = db.get_all_tracks()
    return render_template('tracks.html', tracks=tracks)

# Расписание репертуара
@app.route('/repertoire')
def repertoire():
    schedule = db.get_repertoire_schedule()
    return render_template('repertoire.html', schedule=schedule)

# Статистика
@app.route('/statistics')
def statistics():
    stats = db.get_statistics()
    return render_template('statistics.html', stats=stats)

# Анализ
@app.route('/analysis')
def analysis():
    # Get daily analysis data
    daily_data = db.get_daily_analysis()
    
    # Create DataFrame for Plotly
    df = pd.DataFrame(daily_data)
    
    # Create Plotly charts
    fig1 = px.line(
        df, 
        x='hour', 
        y='avg_bpm',
        title='Средний BPM по часам',
        labels={'hour': 'Час дня', 'avg_bpm': 'BPM'}
    )
    
    fig2 = px.bar(
        df,
        x='hour',
        y='tracks_count',
        title='Количество треков по часам',
        labels={'hour': 'Час дня', 'tracks_count': 'Количество треков'}
    )
    
    # Convert to JSON for rendering in template
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template(
        'analysis.html',
        graph1JSON=graph1JSON,
        graph2JSON=graph2JSON,
        daily_data=daily_data
    )

# Поиск треков
@app.route('/search')
def search():
    search_term = request.args.get('q', '')
    results = []
    if search_term:
        results = db.search_tracks(search_term)
    return render_template('search.html', results=results, search_term=search_term)

# Предстоящие события
@app.route('/upcoming')
def upcoming():
    schedule = db.get_upcoming_schedule(days=7)
    return render_template('upcoming.html', schedule=schedule)

# API endpoints
@app.route('/api/tracks')
def api_tracks():
    tracks = db.get_all_tracks()
    return jsonify(tracks)

@app.route('/api/stats/tracks_by_genre')
def api_tracks_by_genre():
    data = db.execute_query("""
        SELECT g.name as genre, COUNT(*) as count
        FROM repertoire_musictrack mt
        JOIN repertoire_genre g ON mt.genre_id = g.id
        GROUP BY g.name
        ORDER BY count DESC
    """)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=5001)
