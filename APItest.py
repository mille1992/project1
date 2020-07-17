import requests
import os

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GOODREADSKEY", "isbns": "9781632168146"})
print(res.json())
