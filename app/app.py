from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host="db",
        database="biodata",
        user="user",
        password="password"
    )

@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM people ORDER BY id;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO people (name, age, email) VALUES (%s, %s, %s)",
                    (name, age, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM people WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']

        cur.execute("UPDATE people SET name=%s, age=%s, email=%s WHERE id=%s",
                    (name, age, email, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM people WHERE id=%s", (id,))
    person = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit.html', person=person)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)