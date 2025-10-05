# 📚 Books App Backend

Books App is a **full-stack virtual bookstore** where users can browse books, purchase them, and manage their personal collection.  
This repository contains the **backend** built with **FastAPI**.

---

## 🚀 Features

- 🛍️ Browse Books with title, author, description, and rating
- ➕ Add to Cart
- 💳 Checkout / Purchase
- 📚 View purchased books in a dashboard
- 🔑 JWT Authentication for secure login
- 🗄️ PostgreSQL Database storing users, books, orders, and featured books
- 🌐 API endpoints for frontend consumption

---

## 🧰 Tech Stack

- **Python**
- **FastAPI** – High-performance API framework
- **Uvicorn** – ASGI server
- **PostgreSQL** – Database for users, books, orders
- **JWT** – Secure authentication
- **Environment Variables** – Store secrets and DB connection info

---

## 📁 Project Structure


```
books-app-backend/
├─ src/                     # Python source code
│  ├─ main.py
│  ├─ models.py
│  ├─ database.py
│  ├─ routers/
│  └─ scripts/
├─ requirements.txt          # Python dependencies
├─ .env
└─ README.md
```


---

## ⚙️ Environment Variables

Create a .env file:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```


## 🔧 How To Run Locally

```bash
# Clone the repository
git clone https://github.com/haimgubara/books-app-backend
cd books-app-backend/

# Create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

cd src

# Run the FastAPI server
uvicorn main:app --reload
```
