
import praw  # Import the PRAW library
from textblob import TextBlob
import csv
import json
from datetime import datetime
from pymongo import MongoClient



# Reddit API Credentials
reddit = praw.Reddit(
    client_id="BC1-xYnKUVweE50MkN7dSQ",           # Replace with your Reddit client ID
    client_secret="XfUPoVXfFua_gebAuD07t6hyNDQN9w",   # Replace with your Reddit client secret
    user_agent="python:RedditScraper:v1.0 (by /u/Substantial-Catch-97)"  # Replace with your Reddit username
)

# MongoDB connection
def get_db():
    client = MongoClient("mongodb://localhost:27017/") # Use Atlas URI for cloud DB
    db = client["reddit_scraper"]
    return db


# Function to get top posts from subreddit
def get_top_posts(subreddit_name, limit=2):
    subreddit = reddit.subreddit(subreddit_name)  # Choose the subreddit you want to access
    top_posts = []
    
    for post in subreddit.top(limit=limit):
        post_data = {
            'title': post.title,
            'content': post.selftext,  # Content of the post
            'upvotes': post.ups,
            'url': post.url
        }
        top_posts.append(post_data)
    
    return top_posts

# sentiment analysis using TextBlob
def is_good_post(post):
    # Use sentiment analysis to filter posts
    analysis = TextBlob(post['content'])
    # if post['upvotes'] > 100 and analysis.sentiment.polarity > 0.2:
    if post['upvotes'] > 200:
        return True
    return False

def polarity_score(post):
    # Use sentiment analysis to filter posts
    analysis = TextBlob(post['content'])
    return analysis.sentiment.polarity
        
def export_to_mongo(posts, db):
    collection = db['scary_posts']

    #insert posts into the mongoDB
    result = collection.insert_many(posts)
    print(f"✅ Saved {len(posts)} posts to MongoDB")




# --------------------------------------------------------------------------------------------------------------
# Add timestamping to filenames
def get_timestamp():
    """ Generate timestamp string for filenames """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# exports to differen files 
def export_to_csv(posts, filename_prefix="scary_posts"):
    timestamp = get_timestamp()
    filename = f"{filename_prefix}_{timestamp}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Upvotes", "Content", "Polarity", "URL"])
        writer.writeheader()

        for post in posts:
            writer.writerow({
                "Title": post['title'],
                "Upvotes": post['upvotes'],
                "Content": post['content'],
                # "Polarity": post['polarity'],
                # "Score": post['score'],
                "URL": post['url']
            })
    
    print(f"✅ Saved {len(posts)} posts to {filename}")

# Export to JSON
def export_to_json(posts, filename_prefix="scary_posts"):
    """ Save posts to a JSON file """
    timestamp = get_timestamp()
    filename = f"{filename_prefix}_{timestamp}.json"
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(posts, file, indent=4)
    print(f"✅ Saved {len(posts)} posts to {filename}")













# Main function to run the scraper
def main():

    db = get_db()

    # Fetch the top posts from r/AskReddit
    top_posts = get_top_posts('scarystories', limit=5)
   
    # Filter good posts using the sentiment analysis
    filtered_posts = [post for post in top_posts if is_good_post(post)]
    
    export_to_mongo(top_posts, db)


    # Export to CSV and JSON
    # export_to_csv(top_posts, "scary_stories.csv")
    # export_to_json(top_posts, "scary_stories.json")


# Run the script
if __name__ == "__main__":
    main()

# Stuff that was in main that is no longer needed since im using mongoDB
# --------------------------------------------------------------------------------
#    # Analyze and filter scary posts
    # analyze_post = []
    # analyzed_posts = [analyze_post(post) for post in top_posts]

    # Filter for scary posts (negative or slightly positive polarity)
    # scary_posts = [post for post in analyzed_posts if -0.8 < post['polarity'] < 0.2]

    # # Sort by score (upvotes × polarity)
    # scary_posts.sort(key=lambda x: x['score'], reverse=True)
# 
# 
# 
#  ✅ Print all top posts before filtering
    # print("\n🔥 Top 5 Posts from r/AskReddit 🔥\n")
    # for post in top_posts:
    #     print(f"Title: {post['title']}")
    #     print(f"Upvotes: {post['upvotes']}")
    #     print(f"Content: {post['content']}")
    #     print(f"Link: {post['url']}")
    #     print(f"Polarity: {polarity_score(post)}")
    #     print("-" * 40)
    #     
# ✅ Print filtered quality posts
    # print("\n✅ Filtered Quality Posts:")
    # if filtered_posts:
    #     for post in filtered_posts:
    #         print(f"Title: {post['title']}")
    #         print(f"Upvotes: {post['upvotes']}")
    #         print(f"Link: {post['url']}")
    #         print("-" * 40)
    # else:
    #     print("No posts met the quality criteria. 🛑")
