from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown


app = Flask(__name__)
 
Markdown(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog2.db'
db = SQLAlchemy(app)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    author= db.Column(db.String(200), nullable=False)
    date= db.Column(db.String(200), nullable=False)
    image=db.Column(db.String(200), nullable=False)
    tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return '<post %r>' % self.body

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.name)
    
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


@app.route('/add_new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body=request.form['body']
        author=request.form['author']
        date=request.form['date']
        image=request.form['image']
        tags=request.form['tags']
        tags_list=tags.split(',')

        
        post = Post(title=title,body=body,author=author,date=date,image=image)
        post.tags=[Tag(name=tag_name) for tag_name in tags_list ]

        try:
            db.session.add(post)
        except:
            return 'there was an error'        
        db.session.commit()
        return redirect('/')
        
    
    return render_template('update.html')


@app.route('/')
def index():
    css_file = url_for('static', filename='css/styles.css', v='1.15238')
    posts = Post.query.order_by(Post.title).all()
    return render_template('index.html', posts=posts,css_file=css_file)


@app.route('/post/<int:id>')
def show_post(id):
    # Fetch the blog post information from the database or wherever you store it
    post = Post.query.filter_by(id=id)
    css_file = url_for('static', filename='css/styles.css', v='1.15238')
    # Render the template with the post dat
    return render_template('post.html',post=post,css_file=css_file)

@app.route('/tag/<tag_name>')
def showPostByTag(tag_name):
    if tag_name:
        posts = Post.query.join(Post.tags).filter(Tag.name == tag_name).all()
    else:
        posts = Post.query.all()

    css_file = url_for('static', filename='css/styles.css', v='1.15238')    
    return render_template('index.html',posts=posts,css_file=css_file)
                

@app.route('/aboutme')
def about_me():
    css_file = url_for('static', filename='css/styles.css', v='1.1523359')
    bio='''Siddharth Kinger is a passionate fitness enthusiast and successful businessman. He has dedicated his life to maintaining a healthy lifestyle while excelling in his business ventures. With a deep love for fitness, Siddharth believes in the power of physical activity to enhance both personal and professional life.

As a fitness enthusiast, Siddharth actively engages in various workout routines, including weightlifting, cardio exercises, and yoga. He emphasizes the importance of regular exercise, proper nutrition, and a balanced lifestyle to achieve optimal physical and mental well-being.

In addition to his commitment to fitness, Siddharth is also a seasoned businessman. With years of experience in the industry, he has achieved significant success in his entrepreneurial endeavors. His strong work ethic, strategic mindset, and ability to overcome challenges have contributed to his accomplishments in the business world.

Siddharth's passion for fitness and business motivates him to inspire and empower others. Through his expertise and practical knowledge, he shares valuable insights on achieving work-life balance, setting and achieving fitness goals, and unlocking personal and professional potential.

Combining his love for fitness and his business acumen, Siddharth aims to make a positive impact by encouraging individuals to prioritize their health while pursuing their entrepreneurial dreams. His dedication, discipline, and determination serve as an inspiration to those striving for success in both their personal and professional lives.'''
    return render_template('aboutme.html',bio=(bio),css_file=css_file)

if __name__ == "__main__":
    app.run(debug=True)
