#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Assignment Week 12 - School Application"""

#Import modules
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template, flash


#App configuration items
DATABASE = "hw12.db"
SECRET_KEY = "key"
USERNAME = "admin"
PASSWORD = "password"

app = Flask(__name__)
app.config.from_object(__name__)

#Function creates and establishes connection with DB.
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#Request Database Connection
@app.before_request
def before_request():
    g.db = connect_db()

#Close Databae Connection
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#Creates the login route
@app.route('/')
def index():
    return redirect('/login')

#Function to capture errors and create session.
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Username is Invalid.'
            return render_template('login.html', error=error)
        elif request.form['password'] != 'password':
            error = 'Password is Invalid.'
            return render_template('login.html', error=error)

        else:
            session['logged_in'] = True
            return redirect('/dashboard')

    else:
        return render_template('login.html', error=error)


#Function to create dashboard route and select students and quizzes.
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute('SELECT student_id, firstname, lastname from students')
        students = [dict(student_id=row[0], firstname=row[1], lastname=row[2])
                    for row in cur.fetchall()]

        cur = g.db.execute('SELECT quiz_id, qz_subject, questions, quiz_date from quiz')
        quizzes = [dict(quiz_id=row[0], qz_subject=row[1], questions=row[2], quiz_date=row[3])
                   for row in cur.fetchall()]

        return render_template("dashboard.html", students=students, quizzes=quizzes)


#Function to add students to the DB.
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template("add_student.html")

    elif request.method == 'POST':
        g.db.execute('INSERT into Students (firstname, lastname) values (?, ?)',
                     [request.form['StudentFirstName'], request.form['StudentLastName']])
        g.db.commit()

    return redirect(url_for('dashboard'))

#Function to add quizzes to the DB.
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('add_quiz.html')

    elif request.method == 'POST':
        g.db.execute('INSERT into Quiz (qz_subject, questions, quiz_date) '
                     'values (?, ?, ?)', [request.form['QuizSubject'], request.form['QuizQuestions'],request.form['QuizDate']])

        g.db.commit()
    return redirect(url_for('dashboard'))

#Function adds quiz scores
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('add_score.html')

    elif request.method == 'POST':
        g.db.execute("INSERT into Results (student_id, quiz_id, score) values "
                     "(?, ?, ?)", (request.form['StudentID'], request.form['QuizID'], request.form['Score']))

        g.db.commit()
    return redirect('dashboard')


#Function displays results for students with quiz scores
@app.route('/results', methods=['GET'])
def view_results():
    if session['logged_in'] is not True:
        return redirect('/login')
    else:
        cur = g.db.execute("""SELECT students.firstname, students.lastname, quiz.qz_subject, results.score
                            FROM students
                            JOIN Results ON students.student_id = results.student_id
                            JOIN Quiz ON results.quiz_id = quiz.quiz_id;"""
                           )
        students = [dict(firstname=row[0], lastname=row[1], qz_subject=row[2], score=row[3])
                    for row in cur.fetchall()]


        return render_template("results.html", students=students)


if __name__ == '__main__':
    app.run(debug=True)