from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'helpdesk123'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/invalid_cred')
def invalid_cred():
    return render_template('invalid_cred.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == 'helpdesk123':
        session['logged_in'] = True
        return redirect('/dashboard')
    else:
        return redirect('/invalid_cred')


@app.route('/create_ticket', methods=['POST'])
def createticket():
    title = request.form.get('title')
    reported_by = request.form.get('reportedBy')
    description = request.form.get('description')
    priority = request.form.get('priority')
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (title, reported_by, description, priority, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (title, reported_by, description, priority, created_at))

    conn.commit()
    conn.close()

    return render_template(
        'ticket_received.html',
        title=title,
        reported_by=reported_by,
        priority=priority
    )

@app.route('/dashboard')
def dashboard():

    if not session.get('logged_in'):
        return redirect('/login')
    
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tickets
    WHERE status = 'Open' OR status = 'Working On It'
    ORDER BY created_at DESC
""")
    tickets = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Open'")
    open_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Working On It'")
    working_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Resolved'")
    resolved_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Cancelled'")
    cancelled_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        tickets=tickets,
        open_count=open_count,
        working_count=working_count,
        resolved_count=resolved_count,
        cancelled_count=cancelled_count
    )


@app.route('/update_status/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):

    if not session.get('logged_in'):
        return redirect('/login')

    status = request.form.get('status')

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    if status in ['Resolved', 'Cancelled']:
        resolved_by = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
            UPDATE tickets
            SET status = ?, resolved_by = ?
            WHERE id = ?
        """, (status, resolved_by, ticket_id))
    else:
        cursor.execute("""
            UPDATE tickets
            SET status = ?, resolved_by = NULL
            WHERE id = ?
        """, (status, ticket_id))

    conn.commit()
    conn.close()

    return redirect(f'/ticket/{ticket_id}')


@app.route('/ticket/<int:ticket_id>')
def ticket_detail(ticket_id):
    if not session.get('logged_in'):
        return redirect('/login')
    
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    conn.close()

    return render_template('ticket_detail.html', ticket=ticket)

@app.route('/assign_ticket/<int:ticket_id>', methods=['POST'])
def assign_ticket(ticket_id):

    if not session.get('logged_in'):
        return redirect('/login')

    assignee = request.form.get('assignee')

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET assignee = ?, status = 'Working On It'
        WHERE id = ?
    """, (assignee, ticket_id))

    conn.commit()
    conn.close()

    return redirect(f'/ticket/{ticket_id}')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/update_notes/<int:ticket_id>', methods=['POST'])
def update_notes(ticket_id):
    if not session.get('logged_in'):
        return redirect('/login')

    internal_notes = request.form.get('internal_notes')

    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET internal_notes = ?
        WHERE id = ?
    """, (internal_notes, ticket_id))

    conn.commit()
    conn.close()

    return redirect(f'/ticket/{ticket_id}')

@app.route('/closed_tickets')
def closed_tickets():
    if not session.get('logged_in'):
        return redirect('/login')
    
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tickets
        WHERE status IN ('Resolved', 'Cancelled')
        ORDER BY created_at DESC
    """)
    tickets = cursor.fetchall()

    conn.close()

    return render_template('closed_tickets.html', tickets=tickets)

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True, port=8080)