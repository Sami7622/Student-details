from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Sami%409515@localhost/student"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Subject(db.Model):
    __tablename__ = 'mst_subject'
    subject_key = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100))

class Student(db.Model):
    __tablename__ = 'mst_student'
    student_key = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    subject_key = db.Column(db.Integer, db.ForeignKey('mst_subject.subject_key'))
    grade = db.Column(db.Integer)
    remarks = db.Column(db.String(10))

    subject = db.relationship('Subject', backref='students')

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    search_name = request.form.get('search_name', '')
    remark_filter = request.form.get('remark_filter', '')

    query = db.session.query(Student).join(Subject)

    if search_name:
        query = query.filter(Student.student_name.ilike(f'%{search_name}%'))
    if remark_filter:
        query = query.filter(Student.remarks == remark_filter)

    students = query.all()

    return render_template('view.html', students=students)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # app.run(debug=True)
