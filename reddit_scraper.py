import praw  
from textblob import TextBlob
from datetime import datetime
from pymongo import MongoClient

# Reddit API Credentials
reddit = praw.Reddit(
    client_id="BC1-xYnKUVweE50MkN7dSQ",
    client_secret="XfUPoVXfFua_gebAuD07t6hyNDQN9w",
    user_agent="python:RedditScraper:v1.0 (by /u/Substantial-Catch-97)"
)

# MongoDB connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["reddit_scraper"]
    return db


# Function to get top posts from subreddit
def get_top_posts(subreddit_name, limit=5):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = []
    
    for post in subreddit.top(limit=limit):
        polarity = TextBlob(post.selftext).sentiment.polarity

        post_data = {
            'title': post.title,
            'content': post.selftext,
            'upvotes': post.ups,
            'url': post.url,
            'polarity': polarity,
            'timestamp': datetime.now().isoformat()
        }
        top_posts.append(post_data)
    
    return top_posts


def export_to_mongo(posts, db):
    collection = db['scary_posts']
    collection.insert_many(posts)
    print(f"✅ Saved {len(posts)} posts to MongoDB")


# Main function to run the scraper
def main():
    db = get_db()

    # Fetch and filter posts
    top_posts = get_top_posts('scarystories', limit=5)
    
    export_to_mongo(top_posts, db)

# Run the script
if __name__ == "__main__":
    main()
