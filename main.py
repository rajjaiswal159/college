from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Allow your frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def fun():
    return {"hello": "world"}

@app.get("/api/books")
def get_books():
    df = pd.read_csv("top_30_books.csv")

    # Rename columns to match frontend keys
    df = df.rename(columns={
        "Title": "title",
        "Author": "author",
        "Publication Year": "year",
        "AvgRating": "average_rating",
        "Image-URL": "image_url"
    })

    return df.to_dict(orient="records")

@app.get("/api/books/search")
def search_books(query: str = Query(..., description="Book name to search")):
    df = pd.read_csv("Books.csv")
    df = df.rename(columns={
        "Title": "title",
        "Author": "author",
        "Publication Year": "year",
        "AvgRating": "average_rating",
        "Image-URL": "image_url"
    })

    # Case-insensitive search
    result = df[df['title'].str.contains(query, case=False, na=False)]
    if result.empty:
        return {"message": "No book found."}
    return result.to_dict(orient="records")
