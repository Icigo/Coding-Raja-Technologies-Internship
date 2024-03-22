from flask import Flask,render_template,request
import pickle
import numpy as np

app = Flask(__name__, template_folder='template')

pt = pickle.load(open('pt.pkl','rb'))
movies = pickle.load(open('movies.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

@app.route('/recommend')
def recommend_ui():
    return render_template('index.html')



@app.route('/recommend_movies', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = movies[movies['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['genres'].values))
        
        data.append(item)
    
    print(data)
    return render_template('index.html',recommend_movies=data)


if __name__ == '__main__':
    app.run(debug=True)
    

