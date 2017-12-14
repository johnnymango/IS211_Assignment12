/*IS_211 Assignment13 SQL
* Johnny Rodriguez
*/

-- Deletes existing tables
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS Results;

-- Creates the Student table
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    lastname TEXT
    );

-- Creates the Quiz table
CREATE TABLE Quiz (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    qz_subject TEXT,
    questions INTEGER,
    quiz_date DATE
    );

-- Creates the Results table
CREATE TABLE Results (
    results_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER
   );

-- Inserts data rows into each table.
INSERT INTO Students (student_id, firstname, lastname) VALUES (1, 'John', 'Smith');
INSERT INTO Quiz (quiz_id, qz_subject, questions, quiz_date) VALUES (1, 'Python Basics', 5, '2015-05-05');
INSERT INTO Results (score, quiz_id, student_id) VALUES (85, 1, 1);