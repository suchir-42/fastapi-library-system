---

# 📚 Library Management API (FastAPI)

## 🚀 Overview

This project is a **backend Library Management API** developed using **FastAPI**. It provides functionalities to handle books, manage borrowing and returning operations, maintain waiting queues, and support advanced features like filtering, searching, sorting, and pagination.

---

## 🧠 Key Features

### 📖 Book Handling

* Retrieve all books along with their availability status
* Add new books *(prevents duplicate titles)*
* Modify book details *(such as genre or availability)*
* Remove books from the system
* Generate a summary including:

  * Total number of books
  * Available vs borrowed books
  * Count based on genres

---

### 🔄 Borrow & Return Module

* Borrow books with proper validation checks
* Automatic calculation of return deadlines
* Supports different user types:

  * Regular users
  * Premium users
* Return functionality includes:

  * Automatic reassignment if users are in queue
  * Updating book availability status

---

### ⏳ Waiting Queue System

* Allows users to join a queue when a book is unavailable
* View current waiting list
* Automatically assigns book to next user when returned

---

### 🔍 Advanced Capabilities

* Search functionality using **title** or **author name**
* Filtering options based on:

  * Genre
  * Author
  * Availability status
* Sorting options:

  * Title
  * Author
  * Genre
* Pagination support for:

  * Book listings
  * Borrow history
* Combined operations:

  * Filtering + Sorting + Pagination

---

## 🛠️ Technology Stack

* 🐍 Python 3
* ⚡ FastAPI Framework
* ✅ Pydantic (Data Validation)
* 🚀 Uvicorn (ASGI Server)

---

## ⚙️ Setup Instructions

### 1️⃣ Install Required Packages

```bash
pip install fastapi uvicorn
```

### 2️⃣ Start the Application

```bash
uvicorn main:app --reload
```

### 3️⃣ Access API Documentation

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 Available API Routes

### 🔹 General

* `GET /` → API welcome message
* `GET /books` → Retrieve all books
* `GET /books/summary` → View books statistics

---

### 🔹 Borrowing

* `POST /borrow` → Borrow a book
* `GET /borrow-records` → Retrieve borrowing history

---

### 🔹 Book Management

* `POST /books` → Create a new book
* `PUT /books/{book_id}` → Edit book details
* `DELETE /books/{book_id}` → Remove a book
* `GET /books/{book_id}` → Fetch specific book

---

### 🔹 Search & Filters

* `GET /books/filter` → Apply filters
* `GET /books/search` → Search books

---

### 🔹 Sorting & Pagination

* `GET /books/sort` → Sort results
* `GET /books/page` → Paginate results

---

### 🔹 Queue Operations

* `POST /queue/add` → Join waiting queue
* `GET /queue` → View queue details

---

### 🔹 Return Handling

* `POST /return/{book_id}` → Return borrowed book

---

### 🔹 Extended Features

* `GET /borrow-records/search` → Search borrow records
* `GET /borrow-records/page` → Paginated records
* `GET /books/browse` → Combined filter, sort, and pagination

---

## 📸 Screenshots

* Swagger UI (`/docs`) is used to test all endpoints
* Screenshots demonstrating all functionalities are included

---

## 🧪 Validation & Error Handling

* Data validation implemented using **Pydantic**
* Handles various error scenarios such as:

  * Invalid inputs
  * Non-existent books
  * Duplicate borrow attempts
  * Incorrect sorting parameters

---

## 🎯 Learning Highlights

* Building REST APIs with FastAPI
* Implementing validation using Pydantic
* Performing CRUD operations
* Designing queue-based systems
* Applying search, filter, and pagination techniques
* Understanding real-world backend design

---


## 📌 Summary

This project showcases a **fully functional library backend system** built with modern API practices. It is well-structured, scalable, and incorporates essential real-world features required for efficient library management.

---

## ⭐ Thank You!

---
