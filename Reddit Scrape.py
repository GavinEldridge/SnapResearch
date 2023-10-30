import praw
import csv
import pandas as pd
import datetime
import time

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="u99uQvSVpEoCZrWT9rfuKg",
    client_secret="NtyEBocdENI0JpKBiLjTVH9-HlpeLg",
    user_agent="macOS:Scraping SNAP discussions (by /u/lf_wants_data)",
    username="lf_wants_data",
    password="#########"
)

subreddit = reddit.subreddit("povertyfinance")

# Create dictionaries to store post and comment data
posts_dict = {
    "Title": [],
    "Date": [],
    "Post Text": [],
    "ID": [],
    "Score": [],
    "Total Comments": [],
    "Post URL": []
}

comments_dict = {
    "Post ID": [],
    "Comment ID": [],
    "Score": [],
    "Comment Text": [],
    "Comment Date": []
}

# Fetch top posts
posts = subreddit.top(time_filter="year", limit=None)

for post in posts:
    # Title of each post
    posts_dict["Title"].append(post.title)
    # Date of each post
    posts_dict["Date"].append(datetime.datetime.utcfromtimestamp(post.created_utc))
    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)
    # Unique ID of each post
    posts_dict["ID"].append(post.id)
    # The score of a post
    posts_dict["Score"].append(post.score)
    # Total number of comments inside the post
    posts_dict["Total Comments"].append(post.num_comments)
    # URL of each post
    posts_dict["Post URL"].append(post.url)

    # collect comments
    comments = post.comments
    for comment in comments:
        if isinstance(comment, praw.models.MoreComments):
            continue  # Skip "MoreComments" objects
        if not comment.body or comment.body == '[deleted]':
            continue  # Skip empty or deleted comments
        comments_dict["Post ID"].append(post.id)
        comments_dict["Comment ID"].append(comment.id)
        comments_dict["Parent Score"].append(post.score)
        comments_dict["Score"].append(comment.score)
        comments_dict["Comment Text"].append(comment.body)
        comments_dict["Comment Date"].append(datetime.datetime.utcfromtimestamp(comment.created_utc))

    # Sleep for a while to avoid rate limiting
    time.sleep(2)

# Create DataFrames
top_posts = pd.DataFrame(posts_dict)
top_post_comm = pd.DataFrame(comments_dict)

# Save to CSV
top_posts.to_csv("povertyfinance_post.csv", index=True)
top_post_comm.to_csv("povertyfinance_comm.csv", index=True)

