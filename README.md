# 📚 Teacher Reminder App

A web-based platform that helps teachers assign and manage reminders for students. Teachers can send assignment, revision, or task reminders to individual students, while students manage and update their own task lists independently.

> 🚀 **Live Demo**: [https://todo-list-app-yeui.onrender.com](https://todo-list-app-yeui.onrender.com)

---

## ✨ Features

### ✅ For All Users
- Secure registration and login
- View personal reminder list
- Edit, complete, or delete personal reminders
- JWT authentication via secure cookie

### 🧑‍🏫 For Teachers (Admin Role)
- View a list of all registered students
- View any student's reminder list
- Add/edit/delete reminders **for any student**
- Use a teacher-specific interface with expanded access

### 👩‍🎓 For Students
- Manage only their own reminders
- Cannot view or modify other users' data
- Simple interface for personal use

---

## 🛠️ Tech Stack

| Layer        | Tools/Frameworks                           |
|--------------|---------------------------------------------|
| Backend      | [FastAPI](https://fastapi.tiangolo.com/), Python 3 |
| Frontend     | HTML, Bootstrap, Vanilla JS, Jinja2         |
| Auth         | OAuth2 with Password Flow, JWT (cookie-based) |
| Database     | SQLAlchemy ORM + PostgreSQL (Render-hosted) |
| Deployment   | [Render.com](https://render.com/)           |

---


---

## 🔐 Roles and Permissions

| Role    | Can View | Can Edit | Notes |
|---------|----------|----------|-------|
| Student | Own reminders only | Own reminders only | No access to others' data |
| Teacher | All student lists | Add/edit/delete any student's reminders | Admin panel view only |

---

## 📸 Sample Use Cases

- **Teacher:** “Remind John to review for Thursday’s quiz.”
- **Student:** Sees reminder on login, marks complete after finishing.
- **Teacher:** Clicks into a student to track progress or modify items.

---

## 💡 Future Ideas

- Add due dates and filtering
- Send automated reminder emails
- Role-based dashboard UI
- Reminder completion analytics

---

## 👤 Author

**Lydia Gao**  
Computer Science @ University of Waterloo  
Backend-focused full-stack developer with project experience in AI, UI, and systems design.

---

## 📄 License

This project is licensed under the MIT License.


