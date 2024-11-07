from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

# Load pre-processed data and similarity matrix from the pickle file
model_path = 'model.pkl'
with open(model_path, 'rb') as file:
    new_df = pickle.load(file)
    similarity = pickle.load(file)

app = Flask(__name__)

# Recommendation function
def recommend(music):
    if music not in new_df['title'].values:
        return ["Song not found in the database."]
    music_index = new_df[new_df['title'] == music].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_songs = [new_df.iloc[i[0]].title for i in music_list]
    return recommended_songs

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_songs():
    # Get song title from form
    song_title = request.form['song_title']
    recommendations = recommend(song_title)
    
    # Display recommendations on the web page
    return render_template('index.html', recommendations=recommendations, song_title=song_title)

if __name__ == "__main__":
    app.run(debug=True)
