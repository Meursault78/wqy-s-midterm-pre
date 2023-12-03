from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite 数据库连接字符串，将 "your_database.db" 替换为你想要的数据库文件名
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义 Movie 模型
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(255), nullable=False)
    box = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/添加', methods=['POST'])
def add_movie():
    # 从表单中获取电影信息
    movie_id = request.form['movie_id']
    movie_name = request.form['movie_name']
    box = request.form['box']
    release_date = request.form['release_date']
    country = request.form['country']
    type = request.form['type']
    year = request.form['year']

    # 创建新的电影对象
    new_movie = Movie(movie_id=movie_id, movie_name=movie_name, box=box, release_date=release_date, country=country, type=type, year=year)

    # 在应用程序上下文中将电影保存到数据库
    with app.app_context():
        db.session.add(new_movie)
        db.session.commit()

    # 重定向到首页
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
