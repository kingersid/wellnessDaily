from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown


app = Flask(__name__)
 
Markdown(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog1.db'
db = SQLAlchemy(app)




class PostL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    author= db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<post %r>' % self.body


@app.route('/add_new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body=request.form['body']
        author=request.form['author']

        new_post = PostL(title=title,body=body,author=author)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'
    
    return render_template('update.html')



@app.route('/')
def index():
    posts = PostL.query.order_by(PostL.title).all()
    return render_template('index.html', posts=posts)

@app.route('/aboutme')
def about_me():
    bio='''Siddharth Kinger is a passionate fitness enthusiast and successful businessman. He has dedicated his life to maintaining a healthy lifestyle while excelling in his business ventures. With a deep love for fitness, Siddharth believes in the power of physical activity to enhance both personal and professional life.

As a fitness enthusiast, Siddharth actively engages in various workout routines, including weightlifting, cardio exercises, and yoga. He emphasizes the importance of regular exercise, proper nutrition, and a balanced lifestyle to achieve optimal physical and mental well-being.

In addition to his commitment to fitness, Siddharth is also a seasoned businessman. With years of experience in the industry, he has achieved significant success in his entrepreneurial endeavors. His strong work ethic, strategic mindset, and ability to overcome challenges have contributed to his accomplishments in the business world.

Siddharth's passion for fitness and business motivates him to inspire and empower others. Through his expertise and practical knowledge, he shares valuable insights on achieving work-life balance, setting and achieving fitness goals, and unlocking personal and professional potential.

Combining his love for fitness and his business acumen, Siddharth aims to make a positive impact by encouraging individuals to prioritize their health while pursuing their entrepreneurial dreams. His dedication, discipline, and determination serve as an inspiration to those striving for success in both their personal and professional lives.'''
    return render_template('aboutme.html',bio=(bio))

if __name__ == "__main__":
    app.run(debug=True)
