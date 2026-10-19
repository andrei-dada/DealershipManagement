# Car Dealership Management System

> **Intermediate exam project — Python & AI course**
> _A small full-stack-style project: a REST API, a command-line app, and a real
> relational database, all wired together. Graded 10/10._
>
> Built with Flask + MySQL, running locally through Docker.

## Description

This is a management app for a car dealership. It keeps track of four things —
**employees, clients, cars, and sales** — and the relationships between them (who sold
which car to whom, and for how much).

You can use it in two ways: a **REST API** (Flask) if you want to talk to it with HTTP
requests, or a **CLI** with menus if you'd rather work straight from the terminal. Both
sit on top of the same MySQL database, which runs in Docker so you don't have to install
MySQL on your machine.

The point of the project was less about building something fancy and more about
understanding the full chain: how you model data in related tables, how CRUD actually maps
to SQL, how you expose it over an API, and how you package a database so the whole thing
runs anywhere with one command.

## Explore

1. [What it does](#what-it-does)
1. [Tech used](#tech-used)
1. [How it works](#how-it-works)
1. [Database schema](#database-schema)
1. [API endpoints](#api-endpoints)
1. [Notes & things I learned](#notes--things-i-learned)
1. [How to run it](#how-to-run-it)

## What it does

- Full **CRUD** for employees, clients and cars (create, read, update, delete).
- Records **sales** that link a car + an employee + a client, and automatically marks the
  car as **unavailable** once it's sold.
- Won't let you sell a car that doesn't exist or is already sold.
- **Reports**: sales in a given period, best salesperson, best-selling car, and total profit.
- Runs the database in **Docker** — one command and it's up, no manual MySQL install.
- Keeps the database password out of the code, in a `.env` file.

## Tech used

| Part | What I used |
| --- | --- |
| Database | MySQL 8 (in Docker) |
| API | Flask |
| CLI | plain Python |
| DB driver | mysql-connector-python |
| Config / secrets | python-dotenv (`.env`) |
| Containerization | Docker Compose |

## How it works

The flow from launcher to database:

```
launcher.py → pick API or CLI
   → docker compose up -d        (starts the MySQL container)
   → wait until MySQL is ready
   → API: Flask routes   |   CLI: menu loop
   → parameterized SQL → MySQL → JSON response / printed rows
```

Step by step:

1. You run `launcher.py` and choose the Flask API or the CLI.
2. Either one first calls `docker compose up -d`, which starts MySQL in a container. On the
   very first start, `schema.sql` runs automatically and creates all the tables.
3. The app waits in a small loop until the database accepts connections.
4. From there it's normal CRUD — every query uses **parameterized SQL** (`%s`
   placeholders), so values are escaped properly and it's safe against SQL injection.
5. The API returns JSON; the CLI prints rows to the terminal.

## Database schema

Four tables, with `sales` tying the other three together through foreign keys:

- **employees** — `employee_id`, `last_name`, `first_name`, `hire_date`
- **clients** — `client_id`, `last_name`, `first_name`, `email`, `phone`
- **cars** — `car_id`, `vin` (unique), `make`, `model`, `manufacture_year`, `price`, `available`
- **sales** — `sale_id`, `car_id` → cars, `employee_id` → employees, `client_id` → clients,
  `sale_date`, `sale_price`

The schema lives in `schema.sql` and is applied automatically the first time the container
starts, so the database is never in a "half-set-up" state.

## API endpoints

| Method | Route | What it does |
| --- | --- | --- |
| GET | `/employees` | List employees |
| POST | `/employees` | Add one or more employees |
| PUT | `/employees/<id>` | Update an employee |
| DELETE | `/employees/<id>` | Delete an employee |
| GET / POST | `/clients` | List / add clients |
| PUT / DELETE | `/clients/<id>` | Update / delete a client |
| GET / POST | `/cars` | List / add cars |
| GET / POST | `/sales` | List / record sales |
| DELETE | `/sales/<id>` | Delete a sale |

Example — add an employee:

```
curl -X POST http://127.0.0.1:5001/employees \
  -H "Content-Type: application/json" \
  -d '{"last_name": "Popescu", "first_name": "Ion"}'
```
*Or you may use thunder client available as a plugin in VSCode.*

## Notes & things I learned

This is the part I actually want to remember, so I'm writing it down.

- **Secrets don't belong in code.** First version had the DB password hardcoded in three
  files. Moving it to a `.env` (git-ignored) with a `.env.example` committed as a template
  was the single most useful cleanup — and a habit worth keeping for anything real.

- **Virtualenvs are not portable.** I copied the project folder and the copied `.venv` kept
  pointing back to the original location, so packages "installed" into the wrong place and
  the app couldn't find them. Lesson: never copy `.venv` — leave it behind and recreate it
  with `python -m venv` + `pip install -r requirements.txt`.

- **Use the venv's Python, not the global one.** A lot of my "module not found" errors came
  from running `/usr/local/bin/python3` (the system Python) instead of the activated venv's
  `python`. VS Code's Run button does the same thing unless you select the interpreter.

- **Docker Compose beat my shell scripts.** I started with separate `.sh`/`.bat` scripts to
  start MySQL, which behaved differently across OSes and clashed on container names. One
  `docker-compose.yml` replaced all of them and runs the same on Windows, Mac and Linux.

- **Parameterized queries from the start.** Every insert/update uses `%s` placeholders
  instead of string formatting — safe against SQL injection and just cleaner.

### What I'd improve next

- **Input validation on the API** — right now a missing field throws a 500 instead of a
  friendly 400.
- **Narrow the `except`** in the DB-wait loop (it's a bare `except:`), so real errors aren't
  swallowed.
- **Connection handling** — it opens a new DB connection per request, which is fine for a
  learning project but wouldn't scale.
- **`debug=True`** is fine locally, but I know it shouldn't be left on for anything public.

## How to run it

```
git clone https://github.com/andrei-dada/DealershipManagement.git
cd DealershipManagement

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create your .env from the template and set the password
cp .env.example .env
# then edit .env → MYSQL_PASSWORD=yourpassword

python launcher.py
```

The database starts automatically (via Docker), and the API runs at
**http://127.0.0.1:5001**.

> You need **Docker Desktop** installed and running. The MySQL data lives in a Docker volume