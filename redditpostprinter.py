CONFIG = {
    "client_id": "", # Set your client ID here
    "client_secret": "", # Set your client secret here
    "user_agent": "PrintBot9000 by Hackerspace NTNU", # Can be left as-is
    "subreddit": "okbuddyretard", # Choose a meme subreddit here
    "dry_run": True # Set to False if you want to print with your thermal printer instead of to console
}



import praw
import requests
from shlex import quote
from os import system


def print_text_line(line: str):
    command = f"echo {quote(line)} | lp"
    if CONFIG["dry_run"]:
        print(command)
    else:
        system(command)

def print_file(filename: str):
    command = f"lp -o fit-to-page {quote(filename)}"
    if CONFIG["dry_run"]:
        print(command)
    else:
        system(command)

def print_post(post: praw.reddit.Submission):
    filename = "meme.png" if post.url.endswith(".png") else "meme.jpg"
    r = requests.get(post.url, stream=True)
    if r.status_code != 200:
        print("Error getting image")
        return
    with open(filename, "wb") as f:
        for chunk in r:
            f.write(chunk)
    print_text_line(post.title)
    print_text_line(f"  by u/{post.author}")
    print_text_line(f"  on r/{CONFIG['subreddit']}\n")
    print_file(filename)


def main():
    subreddit = praw.Reddit(client_id=CONFIG["client_id"],
                            client_secret=CONFIG["client_secret"],
                            user_agent=CONFIG["user_agent"]
                            ).subreddit(CONFIG["subreddit"])
    posts = subreddit.hot(limit=20)
    for post in posts:
        if post.stickied:
            continue
        if post.url.endswith(".png") or post.url.endswith(".jpg"):
            print_post(post)
            return
    print("No valid posts found :(")


if __name__ == "__main__":
    main()
