# 🎮 Game Ranking Web App

A full-stack web application to catalog, manage, and rank your favorite games by platform.

Built as the final project for the **MAC0350 — Software Development Introduction** course at USP.

---

## ✨ Features

- Add games with name, description, platform, and score
- View and filter your game list sorted by **score**, **name**, or **platform**
- Add and manage platforms independently
- Edit or delete any game or platform
- Reactive UI with no page reloads (powered by HTMX)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · FastAPI |
| Frontend | HTML · CSS · HTMX |
| Database | SQLite · SQLModel |
| Templating | Jinja2 |

---

## 📁 Project Structure

```
Project/
├── main.py          # API routes and application logic
├── database.py      # Database setup and connection
├── models.py        # Data models
├── templates/       # Jinja2 HTML templates
│   ├── index.html
│   ├── lista.html
│   ├── options.html
│   ├── plataformas.html
│   └── options_plataforma.html
└── static/
    └── styles.css
```

---

## 🚀 How to Run

**Requirements:** Python 3.10+

**1. Clone the repository**
```bash
git clone https://github.com/caio-groff/mac0350_labjeff.git
cd mac0350_labjeff
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
cd Project
fastapi dev main.py
```

**5. Open in your browser**
```
http://localhost:8000
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
