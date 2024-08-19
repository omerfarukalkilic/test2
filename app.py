from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Tarih ve saat

    def __repr__(self):
        return f"<Task {self.id}>"

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))  
       
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))
    

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.status = True
    db.session.commit()
    return redirect(url_for('index'))   
  
import os

if __name__ == '__main__':
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else '127.0.0.1'
    app.run(debug=True, host=host)
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000

