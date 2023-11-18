# Description
This is a simple example of asynchronous REST service, which is working with DB Postgres.

# Stack 
FastAPI, Postgres, asyncpg, SQLAlchemy

# Task
We have 2 entities: Note and Board. Service functionality:
- Add, Edit, Delete Note - by id
- Get Node data by id
- Add, Delete Board - by id
- Edit Board: add note to board, delete note from board 
- DB should be created by service, if not exists.

# Run with docker
- Rename .env.example to .env, specify DB connection
- docker build . -t notes_web
- docker run -p 8080:80 notes_web
- go to http://localhost:8080/docs, if you haven't changed ports