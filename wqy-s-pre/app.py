from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy import desc

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wqy_ruc_movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义 Movie 模型
class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(255), nullable=False)
    box = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    actor_name = db.Column(db.String(255), nullable=True)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    # 从表单中获取电影信息
    movie_id = request.form['movie_id']
    movie_name = request.form['movie_name']
    box = request.form['box']
    release_date_str = request.form['release_date']
    release_date = datetime.strptime(release_date_str, '%Y-%m-%d')
    country = request.form['country']
    type = request.form['type']
    year = request.form['year']
    actor_name = request.form['actor_name']

    new_movie = Movie(movie_id=movie_id, movie_name=movie_name, box=box, release_date=release_date,
        country=country, type=type, year=year,actor_name=actor_name)

    # 在应用程序上下文中将电影保存到数据库
    with app.app_context():
            db.session.add(new_movie)
            db.session.commit()

    # 重定向到首页
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search_movie():
    search_query = request.args.get('search_query', '')

    search_results = Movie.query.filter(or_(
        Movie.movie_id == search_query,
        Movie.movie_name.ilike(f"%{search_query}%"),
        Movie.actor_name.ilike(f"%{search_query}%"),
    )).all()

    all_movies = Movie.query.all()
    search_results_with_rank = add_ranking(all_movies, search_results)
    return render_template('index.html', movies=all_movies, search_results_with_rank=search_results_with_rank)


# 定义排行函数
def add_ranking(all_movies, search_results):
    sorted_movies = sorted(all_movies, key=lambda x: x.box, reverse=True)

    for i, movie in enumerate(sorted_movies, start=1):
        movie.rank = i

    matched_results = [movie for movie in sorted_movies if movie.movie_id in [result.movie_id for result in search_results]]

    return matched_results

if __name__ == '__main__':
    app.run(debug=True)
