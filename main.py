from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ---------------- Day 1 ----------------
@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}


books = [
    {"id": 1, "title": "Python Basics", "author": "John Doe", "genre": "Tech", "is_available": True},
    {"id": 2, "title": "History of India", "author": "R Sharma", "genre": "History", "is_available": True},
    {"id": 3, "title": "Science World", "author": "A Kumar", "genre": "Science", "is_available": True},
    {"id": 4, "title": "Fiction Tales", "author": "M Singh", "genre": "Fiction", "is_available": True},
    {"id": 5, "title": "Advanced Python", "author": "John Doe", "genre": "Tech", "is_available": True},
    {"id": 6, "title": "World War", "author": "S Khan", "genre": "History", "is_available": True},
]

@app.get("/books")
def get_books():
    available = len([b for b in books if b["is_available"]])
    return {"books": books, "total": len(books), "available_count": available}


@app.get("/books/summary")
def books_summary():
    total = len(books)
    available = len([b for b in books if b["is_available"]])
    borrowed = total - available

    genre_count = {}
    for b in books:
        genre_count[b["genre"]] = genre_count.get(b["genre"], 0) + 1

    return {"total": total, "available": available, "borrowed": borrowed, "genre_breakdown": genre_count}


borrow_records = []
record_counter = 1

@app.get("/borrow-records")
def get_records():
    return {"records": borrow_records, "total": len(borrow_records)}


# ---------------- Day 2 ----------------
class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    borrow_days: int = Field(..., gt=0, le=60)
    member_id: str = Field(..., min_length=4)
    member_type: str = "regular"


@app.post("/borrow")
def borrow_book(req: BorrowRequest):
    global record_counter

    book = find_book(req.book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    if not book["is_available"]:
        raise HTTPException(400, "Book already borrowed")

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": req.member_name,
        "book_id": req.book_id,
        "due": calculate_due_date(req.borrow_days, req.member_type)
    }

    borrow_records.append(record)
    record_counter += 1

    return record


# ---------------- Day 3 ----------------
def find_book(book_id):
    for b in books:
        if b["id"] == book_id:
            return b
    return None


def calculate_due_date(days, member_type):
    if member_type == "premium":
        days = min(days, 60)
    else:
        days = min(days, 30)
    return f"Return by: Day {15 + days}"


def filter_books_logic(genre, author, is_available):
    result = books
    if genre is not None:
        result = [b for b in result if b["genre"].lower() == genre.lower()]
    if author is not None:
        result = [b for b in result if b["author"].lower() == author.lower()]
    if is_available is not None:
        result = [b for b in result if b["is_available"] == is_available]
    return result


@app.get("/books/filter")
def filter_books(genre: Optional[str] = None,
                 author: Optional[str] = None,
                 is_available: Optional[bool] = None):
    result = filter_books_logic(genre, author, is_available)
    return {"books": result, "count": len(result)}


@app.get("/books/browse")
def browse(keyword: Optional[str] = None,
           sort_by: str = "title",
           order: str = "asc",
           page: int = 1,
           limit: int = 3):

    result = books

    if keyword:
        result = [
            b for b in result
            if keyword.lower() in b["title"].lower()
            or keyword.lower() in b["author"].lower()
        ]

    if sort_by not in ["title", "author", "genre"]:
        raise HTTPException(400, "Invalid sort_by")

    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Invalid order")

    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "data": result[start:end]
    }


# ---------------- Day 4 ----------------
class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = True


@app.post("/books", status_code=201)
def add_book(book: NewBook):
    for b in books:
        if b["title"].lower() == book.title.lower():
            raise HTTPException(400, "Duplicate title")

    new_id = max([b["id"] for b in books]) + 1
    new_book = {"id": new_id, **book.dict()}
    books.append(new_book)
    return new_book


@app.put("/books/{book_id}")
def update_book(book_id: int, genre: Optional[str] = None, is_available: Optional[bool] = None):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    if genre is not None:
        book["genre"] = genre
    if is_available is not None:
        book["is_available"] = is_available

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    books.remove(book)
    return {"message": f"{book['title']} deleted successfully"}


# ---------------- Day 5 ----------------
queue = []

@app.post("/queue/add")
def add_queue(member_name: str, book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    if book["is_available"]:
        return {"message": "Book is available, no need to queue"}

    queue.append({"member_name": member_name, "book_id": book_id})
    return {"message": "Added to queue"}


@app.get("/queue")
def get_queue():
    return queue


@app.post("/return/{book_id}")
def return_book(book_id: int):
    global record_counter

    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    book["is_available"] = True

    for q in queue:
        if q["book_id"] == book_id:
            queue.remove(q)
            book["is_available"] = False

            record = {
                "record_id": record_counter,
                "member_name": q["member_name"],
                "book_id": book_id,
                "due": calculate_due_date(7, "regular")
            }
            borrow_records.append(record)
            record_counter += 1

            return {"message": "returned and re-assigned", "record": record}

    return {"message": "returned and available"}


# ---------------- Day 6 ----------------
@app.get("/books/search")
def search_books(keyword: str):
    result = [
        b for b in books
        if keyword.lower() in b["title"].lower()
        or keyword.lower() in b["author"].lower()
    ]
    return {"results": result, "total_found": len(result)}


@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):
    if sort_by not in ["title", "author", "genre"]:
        raise HTTPException(400, "Invalid sort_by")
    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Invalid order")

    sorted_books = sorted(books, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"sorted": sorted_books}


@app.get("/books/page")
def paginate_books(page: int = 1, limit: int = 3):
    total = len(books)
    start = (page - 1) * limit
    end = start + limit
    return {"total": total, "page": page, "limit": limit, "data": books[start:end]}


@app.get("/borrow-records/search")
def search_records(member_name: str):
    result = [r for r in borrow_records if member_name.lower() in r["member_name"].lower()]
    return result


@app.get("/borrow-records/page")
def paginate_records(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return borrow_records[start:end]


# ---------------- LAST ----------------
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return b
    return {"error": "Book not found"}
