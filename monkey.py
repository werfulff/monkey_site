from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MONKEYS.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    appearance = db.Column(db.Text, nullable=False)
    habitat = db.Column(db.Text, nullable=False) 
    lifestyle = db.Column(db.Text, nullable=False)
    food = db.Column(db.Text, nullable=False)

    monkeys = db.relationship(
    'Monkey', backref = 'article', lazy=True
)
 
class Monkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)

    article_id = db.Column(
    db.Integer, db.ForeignKey('article.id'), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
def index():
    articles = Article.query.all()
    return render_template("main.html", articles=articles)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        appearance = request.form['appearance']
        habitat = request.form['habitat']
        lifestyle = request.form['lifestyle']
        food = request.form['food']
        
        filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        article = Article(
            name=name,
            image=filename,
            appearance=appearance,
            habitat=habitat,
            lifestyle=lifestyle,
            food=food
        )
        
        db.session.add(article)    
        db.session.commit()         
        return redirect(url_for('index'))
    return render_template('create_article.html')

@app.route('/add_monkey', methods=['GET', 'POST'])
def add_monkey():
    if request.method == 'POST':
        article_id = request.form['article_id']
        name = request.form['name']
        description = request.form['description']

        filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        monkey = Monkey(
            name = name,
            description = description,
            image = filename,
            article_id = article_id
        )
        db.session.add(monkey)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_monkey.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    article = Article.query.get(id)
    if article.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], article.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Удаляем всех обезьян этой породы
    for monkey in article.monkeys:

        # Удаляем фото обезьяны
        if monkey.image:
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                monkey.image
            )
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(monkey)

    # Удаляем породу
    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/podopechnye')
def podopechnye():
    return render_template('podopechnye.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/pravila')
def pravila():
    return render_template('pravila.html')

@app.route('/bilet')
def bilet():
    return render_template('bilet.html')

@app.route('/monkey/<int:id>')
def monkey(id):
    article = Article.query.get(id)
    return render_template('monkey.html', article=article)

if __name__ == '__main__':
    app.run(debug=True)