# Simple URL Shortener

This is a very simple URL shortener written with FastAPI and Vue.js.

## To Run

1. Clone this repo
1. From the root directory, install the app dependencies with `pip install -r requirements.txt`
1. From the root directory run `uvicorn src.main:app`
1. Visit `http://localhost:8000`
1. Shorten some URL's!

Right now the app stores into a `app.db` Sqlite3 file. I plan to switch this to PostgreSQL with environment options for connecting before deploying.
