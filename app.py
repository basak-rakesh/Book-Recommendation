from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import os


current_directory = os.path.abspath(os.getcwd())
file_path_file = os.path.join(current_directory, 'popular.pkl')
popular_df = pd.read_pickle(file_path_file)

table = pd.read_pickle(os.path.join(current_directory, 'table.pkl'))
books = pd.read_pickle(os.path.join(current_directory, 'books.pkl'))
similarity_score = pd.read_pickle(os.path.join(current_directory, 'similarity_score.pkl'))
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)