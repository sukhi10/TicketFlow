# TicketFlow 🎫

A full stack IT helpdesk ticketing system built with Python and Flask, inspired by Jira. Built to understand how ticket management systems work under the hood.

## Features

- **Ticket Submission** — Employees submit support tickets with title, description, and priority
- **Helpdesk Dashboard** — Protected admin dashboard showing all active tickets with live stats
- **Ticket Management** — Assign tickets, update status, and leave internal notes
- **Closed Ticket Archive** — Separate view for resolved and cancelled tickets
- **Real-time Search** — Filter tickets instantly without page reload
- **Data Visualization** — Live doughnut chart showing ticket breakdown by status
- **Session Authentication** — Login system protecting all admin routes
- **Confirmation Page** — Users see a summary after submitting a ticket

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Styling | Tailwind CSS |
| Charts | Chart.js |
| Containerization | Docker |

## Getting Started

### Option 1 — Run with Docker (recommended)

```bash
docker build -t ticketflow .
docker run -p 8080:8080 ticketflow
```

Then open http://localhost:8080

### Option 2 — Run locally

```bash
pip install flask
python database.py
python app.py
```

Then open http://localhost:8080

## Login Credentials

```
Username: admin
Password: helpdesk123
```

## Project Structure

```
ticket-dashboard/
├── app.py              # Flask routes and application logic
├── database.py         # SQLite database setup
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
└── templates/
    ├── index.html          # Public ticket submission form
    ├── login.html          # Helpdesk login page
    ├── dashboard.html      # Active tickets dashboard
    ├── ticket_detail.html  # Individual ticket view
    ├── closed_tickets.html # Resolved/cancelled archive
    └── ticket_received.html # Submission confirmation
```

## Screenshots

> Dashboard, ticket detail, and submission form

## Motivation

Built this after using Jira daily during my IT internship at Arrow Machine and Fabrication. I wanted to understand how a ticketing system actually works end to end — from form submission to database design to session authentication.

## Future Improvements

- Multi-user support with a proper users table
- Email notifications on ticket assignment
- File attachment support for screenshots
- SQLAlchemy ORM instead of raw SQL
- Deploy to Railway or Render for live access
