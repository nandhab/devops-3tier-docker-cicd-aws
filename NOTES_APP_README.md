# 📝 Notes App (Dockerized 3-Tier Example)

This is a simple 3-tier notes app using:

- **Frontend**: Nginx serving static HTML/CSS/JS
- **Backend**: FastAPI (Python REST API)
- **Database**: PostgreSQL

---

## 🚀 Features

- Add, view, edit, and delete notes
- Notion-style UI with inline editing
- Fully containerized with Docker Compose

---

## ⚙️ Requirements

- Docker
- Docker Compose

---

## 🗺️ How to Run

1️⃣ Clone this repository.

2️⃣ Make sure Docker and Docker Compose are installed.

4️⃣ Build and start the app:

```
docker-compose up --build
```

5️⃣ Open your browser at:

```
http://localhost:8080
```

✅ You can now add, edit, and delete notes!

🧹 Cleanup
To stop and remove containers, networks, and volumes:

```
docker-compose down
```

📜 License
MIT — use freely for learning or projects.
