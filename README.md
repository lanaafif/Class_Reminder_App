# FastAPI Project Setup Guide (Video P4 + SQLite Setup from P43)

This guide summarizes how to move a FastAPI project to a new location and configure it with a virtual environment and SQLite support.

---

## 📁 Folder Layout

```
D:\vscode\2A\fastapi\
├── fastapienv\            # Virtual environment
├── main.py / books.py     # API definition
├── requirements.txt       # Dependencies
└── .git / .vscode         # Optional
```

---

## ✅ 1. Setup FastAPI Environment (from Video P4)

1. Move the entire `fastapi` folder to `D:\vscode\2A\`
2. Recreate the virtual environment:

   ```bash
   cd D:\vscode\2A\fastapi
   python -m venv fastapienv
   .\fastapienv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   # Or install manually:
   pip install fastapi uvicorn
   ```
4. Configure VS Code interpreter:

   * Ctrl+Shift+P → Python: Select Interpreter → choose `fastapienv\Scripts\python.exe`

---

## 📃 2. SQLite Configuration (from Video P43)

To add SQLite support for data persistence:

1. Install dependencies:

   ```bash
   pip install sqlalchemy sqlite3
   ```

   > Note: `sqlite3` is built-in with Python 3.7+, no need to install separately in most cases.

2. Create `database.py`:

   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker, declarative_base

   DATABASE_URL = 'sqlite:///./todos.db'

   engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   ```

3. Import and bind `Base` in your main app to auto-create tables:

   ```python
   import models
   from database import engine

   models.Base.metadata.create_all(bind=engine)
   ```

4. Create models in `models.py`:

   ```python
   from database import Base
   from sqlalchemy import Column, Integer, String, Boolean

   class Todos(Base):
       __tablename__ = 'todos'
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String)
       description = Column(String)
       priority = Column(Integer)
       complete = Column(Boolean, default=False)
   ```

---

## 🔧 Run the API

```bash
uvicorn books:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

---

## Summary

| Step                | Status       |
| ------------------- | ------------ |
| Project moved to D: | ✅ Done       |
| Virtual env created | ✅ Done       |
| FastAPI installed   | ✅ Done       |
| SQLite configured   | ✅ Done (P43) |
| API live at /docs   | ✅ Working    |

You're ready to continue building!
