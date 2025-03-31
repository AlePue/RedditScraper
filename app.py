from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["reddit_scraper"]
    return db

def fetch_data():
    db = get_db()
    collection = db['scary_posts']
    
    # Fetch data from MongoDB and ensure missing fields are handled
    posts = []
    for doc in collection.find():
        posts.append({
            'title': doc.get('title', 'No title'),   # Default to 'No title' if missing
            'upvotes': doc.get('upvotes', 0),         # Default to 0 if missing
            'polarity': doc.get('polarity', 0.0),     # Default to 0.0 if missing
            'url': doc.get('url', '#')                # Default URL
        })

    return posts

@app.route('/')
def index():
    posts = fetch_data()
    return render_template('index.html', posts=posts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
