from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB = "memo.db"

# --- DB初期化 ---
def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE memo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
        """)
        conn.commit()
        conn.close()

# --- 一覧 ---
@app.route("/")
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title FROM memo")
    memos = c.fetchall()
    conn.close()
    return render_template("list.html", memos=memos)

# --- 新規作成 ---
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO memo (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("form.html", memo=None)

# --- 更新 ---
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == "POST":
        title = request.form["title"]
        c.execute("UPDATE memo SET title=? WHERE id=?", (title, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        c.execute("SELECT id, title FROM memo WHERE id=?", (id,))
        memo = c.fetchone()
        conn.close()
        return render_template("form.html", memo=memo)

# --- 削除 ---
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("DELETE FROM memo WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("delete.html", id=id)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
