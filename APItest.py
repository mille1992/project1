import requests
import os

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADSKEY"), "isbns": "8129115301"})
print(res)
a = res.json()
b = a["books"][0]["isbn"]
print(res.json())
print(b)

