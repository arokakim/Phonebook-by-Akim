from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app=Flask(__name__)
DATABASE='phonebook.db'

#initialize the database
def init_db():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL
                   )
                   ''')
    conn.commit()
    conn.close()

#get all contacts
def get_contacts():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts=cursor.fetchall()
    conn.close()
    return contacts

#get a single contact
def get_contact(id):
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    cursor=conn. cursor()
    cursor.execute("SELECT * FROM contacts WHERE id=?", (id,))
    contact=cursor.fetchone()
    conn.close()
    return contact

@app.route('/')
def index():
    contacts=get_contacts()
    return render_template('index.html', users=contacts)

@app.route('/add', methods=['POST'])
def add():
    name=request.form.get('name')
    phone=request.form.get('phone')
    email=request.form.get('email')

    if name and phone and email:
        conn=sqlite3.connect(DATABASE)
        cursor=conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute("DELETE FROM contacts")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    contact=get_contact(id)
    return render_template('edit.html', user=contact)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name=request.form.get('name')
    phone=request.form.get('phone')
    email=request.form.get('email')

    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", (name, phone, email, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__=='__main__':
    init_db()
    app.run(debug=True)