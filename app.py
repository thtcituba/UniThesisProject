from flask import Flask, render_template, request, redirect, url_for
from db import get_conn

app = Flask(__name__)


# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return redirect(url_for("search"))


# -----------------------------
# MASTERS PAGE (Parent Tables)
# -----------------------------
@app.get("/masters")
def masters():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT A_ID, A_NAME FROM dbo.AUTHOR ORDER BY A_NAME")
    authors = cur.fetchall()

    cur.execute("SELECT UNI_ID, UNI_NAME FROM dbo.UNIVERSITY ORDER BY UNI_NAME")
    universities = cur.fetchall()

    cur.execute("SELECT S_ID, S_NAME FROM dbo.SUPERVISOR ORDER BY S_NAME")
    supervisors = cur.fetchall()

    cur.execute("SELECT INS_ID, INS_NAME FROM dbo.INSTITUTE ORDER BY INS_NAME")
    institutes = cur.fetchall()

    conn.close()
    return render_template(
        "masters.html",
        authors=authors,
        universities=universities,
        supervisors=supervisors,
        institutes=institutes
    )


# -----------------------------
# THESIS SUBMIT (GET)
# -----------------------------
@app.get("/submit")
def submit_page():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT A_ID, A_NAME FROM dbo.AUTHOR ORDER BY A_NAME")
    authors = cur.fetchall()

    cur.execute("SELECT UNI_ID, UNI_NAME FROM dbo.UNIVERSITY ORDER BY UNI_NAME")
    universities = cur.fetchall()

    cur.execute("SELECT S_ID, S_NAME FROM dbo.SUPERVISOR ORDER BY S_NAME")
    supervisors = cur.fetchall()

    cur.execute("SELECT INS_ID, INS_NAME FROM dbo.INSTITUTE ORDER BY INS_NAME")
    institutes = cur.fetchall()

    conn.close()
    return render_template(
        "submit.html",
        authors=authors,
        universities=universities,
        supervisors=supervisors,
        institutes=institutes
    )


# -----------------------------
# THESIS SUBMIT (POST)
# -----------------------------
@app.post("/submit")
def submit_thesis():
    data = request.form
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dbo.THESIS
        (T_TITLE, T_TOPIC, T_ABSTRACT, T_KEYWORD,
         T_YEAR, T_TYPE, T_INSTITUTE, T_PAGE,
         T_LANGUAGE, T_SUBDATE, A_ID, UNI_ID, S_ID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["T_TITLE"],
        data["T_TOPIC"],
        data.get("T_ABSTRACT"),
        data.get("T_KEYWORD"),
        data["T_YEAR"],
        data["T_TYPE"],
        data["T_INSTITUTE"],
        data["T_PAGE"],
        data["T_LANGUAGE"],
        data["T_SUBDATE"],
        data["A_ID"],
        data["UNI_ID"],
        data["S_ID"]
    ))

    conn.commit()
    conn.close()
    return redirect(url_for("search"))


# -----------------------------
# SEARCH (GET)
# -----------------------------
@app.get("/search")
def search():
    q = request.args.get("q")
    year_from = request.args.get("year_from")
    year_to = request.args.get("year_to")
    lang = request.args.get("lang")
    a_id = request.args.get("a_id")
    uni_id = request.args.get("uni_id")
    s_id = request.args.get("s_id")
    type_ = request.args.get("type")

    sql = """
        SELECT
            t.T_NO,
            t.T_TITLE,
            t.T_YEAR,
            u.UNI_NAME,
            a.A_NAME,
            s.S_NAME,
            t.T_LANGUAGE
        FROM dbo.THESIS t
        JOIN dbo.AUTHOR a ON t.A_ID = a.A_ID
        JOIN dbo.UNIVERSITY u ON t.UNI_ID = u.UNI_ID
        JOIN dbo.SUPERVISOR s ON t.S_ID = s.S_ID
        WHERE 1=1
    """
    params = []

    if q:
        sql += """ AND (
            t.T_TITLE LIKE ? OR
            t.T_TOPIC LIKE ? OR
            t.T_KEYWORD LIKE ? OR
            t.T_ABSTRACT LIKE ?
        )"""
        like_q = f"%{q}%"
        params.extend([like_q, like_q, like_q, like_q])

    if year_from:
        sql += " AND t.T_YEAR >= ?"
        params.append(year_from)

    if year_to:
        sql += " AND t.T_YEAR <= ?"
        params.append(year_to)

    if lang:
        sql += " AND t.T_LANGUAGE = ?"
        params.append(lang)

    if a_id:
        sql += " AND t.A_ID = ?"
        params.append(a_id)

    if uni_id:
        sql += " AND t.UNI_ID = ?"
        params.append(uni_id)

    if s_id:
        sql += " AND t.S_ID = ?"
        params.append(s_id)

    if type_:
        sql += " AND t.T_TYPE = ?"
        params.append(type_)

    sql += " ORDER BY t.T_YEAR DESC, t.T_TITLE ASC"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params)
    theses = cur.fetchall()

    filters = {
        "q": q,
        "year_from": year_from,
        "year_to": year_to,
        "lang": lang,
        "a_id": int(a_id) if a_id else None,
        "uni_id": int(uni_id) if uni_id else None,
        "s_id": int(s_id) if s_id else None,
        "type": type_
    }

    cur.execute("SELECT A_ID, A_NAME FROM dbo.AUTHOR ORDER BY A_NAME")
    authors = cur.fetchall()

    cur.execute("SELECT UNI_ID, UNI_NAME FROM dbo.UNIVERSITY ORDER BY UNI_NAME")
    universities = cur.fetchall()

    cur.execute("SELECT S_ID, S_NAME FROM dbo.SUPERVISOR ORDER BY S_NAME")
    supervisors = cur.fetchall()

    conn.close()

    return render_template(
        "search.html",
        theses=theses,
        filters=filters,
        authors=authors,
        universities=universities,
        supervisors=supervisors
    )


# -----------------------------
# THESIS DETAIL
# -----------------------------
@app.get("/thesis/<int:t_no>")
def thesis_detail(t_no):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.T_TITLE, t.T_TOPIC, t.T_ABSTRACT, t.T_KEYWORD,
            t.T_YEAR, t.T_TYPE, t.T_INSTITUTE, t.T_PAGE,
            t.T_LANGUAGE, t.T_SUBDATE,
            a.A_NAME, u.UNI_NAME, s.S_NAME
        FROM dbo.THESIS t
        JOIN dbo.AUTHOR a ON t.A_ID = a.A_ID
        JOIN dbo.UNIVERSITY u ON t.UNI_ID = u.UNI_ID
        JOIN dbo.SUPERVISOR s ON t.S_ID = s.S_ID
        WHERE t.T_NO = ?
    """, (t_no,))

    thesis = cur.fetchone()
    conn.close()

    if not thesis:
        return "Thesis not found", 404

    return render_template("thesis_detail.html", thesis=thesis, t_no=t_no)


# -----------------------------
# THESIS DELETE
# -----------------------------
@app.get("/thesis/<int:t_no>/delete")
def thesis_delete(t_no):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dbo.THESIS WHERE T_NO = ?", (t_no,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for("search"))


# -----------------------------
# THESIS EDIT (GET)
# -----------------------------
@app.get("/thesis/<int:t_no>/edit")
def thesis_edit_page(t_no):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            T_NO, T_TITLE, T_TOPIC, T_ABSTRACT, T_KEYWORD,
            T_YEAR, T_TYPE, T_INSTITUTE, T_PAGE,
            T_LANGUAGE, T_SUBDATE, A_ID, UNI_ID, S_ID
        FROM dbo.THESIS
        WHERE T_NO = ?
    """, (t_no,))
    thesis = cur.fetchone()

    if not thesis:
        conn.close()
        return "Thesis not found", 404

    cur.execute("SELECT A_ID, A_NAME FROM dbo.AUTHOR ORDER BY A_NAME")
    authors = cur.fetchall()
    cur.execute("SELECT UNI_ID, UNI_NAME FROM dbo.UNIVERSITY ORDER BY UNI_NAME")
    universities = cur.fetchall()
    cur.execute("SELECT S_ID, S_NAME FROM dbo.SUPERVISOR ORDER BY S_NAME")
    supervisors = cur.fetchall()

    conn.close()

    return render_template(
        "thesis_edit.html",
        thesis=thesis,
        authors=authors,
        universities=universities,
        supervisors=supervisors
    )


# -----------------------------
# THESIS EDIT (POST)
# -----------------------------
@app.post("/thesis/<int:t_no>/edit")
def thesis_edit_save(t_no):
    data = request.form

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE dbo.THESIS
        SET
            T_TITLE=?,
            T_TOPIC=?,
            T_ABSTRACT=?,
            T_KEYWORD=?,
            T_YEAR=?,
            T_TYPE=?,
            T_INSTITUTE=?,
            T_PAGE=?,
            T_LANGUAGE=?,
            T_SUBDATE=?,
            A_ID=?,
            UNI_ID=?,
            S_ID=?
        WHERE T_NO=?
    """, (
        data["T_TITLE"],
        data["T_TOPIC"],
        data.get("T_ABSTRACT"),
        data.get("T_KEYWORD"),
        data["T_YEAR"],
        data["T_TYPE"],
        data["T_INSTITUTE"],
        data["T_PAGE"],
        data["T_LANGUAGE"],
        data["T_SUBDATE"],
        data["A_ID"],
        data["UNI_ID"],
        data["S_ID"],
        t_no
    ))

    conn.commit()
    conn.close()
    return redirect(url_for("thesis_detail", t_no=t_no))


# -----------------------------
# MASTERS CRUD
# -----------------------------
@app.post("/masters/author/add")
def add_author():
    name = request.form.get("A_NAME", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.AUTHOR (A_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.post("/masters/author/update/<int:a_id>")
def update_author(a_id):
    name = request.form.get("name", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("UPDATE dbo.AUTHOR SET A_NAME=? WHERE A_ID=?", (name, a_id))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.get("/masters/author/delete/<int:a_id>")
def delete_author(a_id):
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dbo.AUTHOR WHERE A_ID=?", (a_id,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for("masters"))


@app.post("/masters/university/add")
def add_university():
    name = request.form.get("UNI_NAME", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.UNIVERSITY (UNI_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.post("/masters/university/update/<int:uni_id>")
def update_university(uni_id):
    name = request.form.get("name", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("UPDATE dbo.UNIVERSITY SET UNI_NAME=? WHERE UNI_ID=?", (name, uni_id))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.get("/masters/university/delete/<int:uni_id>")
def delete_university(uni_id):
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dbo.UNIVERSITY WHERE UNI_ID=?", (uni_id,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for("masters"))


@app.post("/masters/supervisor/add")
def add_supervisor():
    name = request.form.get("S_NAME", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.SUPERVISOR (S_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.post("/masters/supervisor/update/<int:s_id>")
def update_supervisor(s_id):
    name = request.form.get("name", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("UPDATE dbo.SUPERVISOR SET S_NAME=? WHERE S_ID=?", (name, s_id))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.get("/masters/supervisor/delete/<int:s_id>")
def delete_supervisor(s_id):
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dbo.SUPERVISOR WHERE S_ID=?", (s_id,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for("masters"))


@app.post("/masters/institute/add")
def add_institute():
    name = request.form.get("INS_NAME", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.INSTITUTE (INS_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.post("/masters/institute/update/<int:ins_id>")
def update_institute(ins_id):
    name = request.form.get("name", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("UPDATE dbo.INSTITUTE SET INS_NAME=? WHERE INS_ID=?", (name, ins_id))
        conn.commit(); conn.close()
    return redirect(url_for("masters"))

@app.get("/masters/institute/delete/<int:ins_id>")
def delete_institute(ins_id):
    conn = get_conn(); cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dbo.INSTITUTE WHERE INS_ID=?", (ins_id,))
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for("masters"))


# -----------------------------
# QUICK ADD FROM SUBMIT PAGE
# -----------------------------
@app.post("/submit/add-author")
def submit_add_author():
    name = request.form.get("new_author", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.AUTHOR (A_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("submit_page"))

@app.post("/submit/add-university")
def submit_add_university():
    name = request.form.get("new_university", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.UNIVERSITY (UNI_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("submit_page"))

@app.post("/submit/add-supervisor")
def submit_add_supervisor():
    name = request.form.get("new_supervisor", "").strip()
    if name:
        conn = get_conn(); cur = conn.cursor()
        cur.execute("INSERT INTO dbo.SUPERVISOR (S_NAME) VALUES (?)", (name,))
        conn.commit(); conn.close()
    return redirect(url_for("submit_page"))


if __name__ == "__main__":
    app.run(debug=True)
