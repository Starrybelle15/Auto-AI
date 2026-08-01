import praw

# Configure Reddit API
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="LuxuryBagReviewIntelligence"
)

def collect_reviews(query, limit=25):
    """
    Search Reddit for discussions about a luxury bag.
    Returns a list of review-like text.
    """

    reviews = []

    for submission in reddit.subreddit("all").search(query, limit=limit):

        reviews.append(submission.title)

        submission.comments.replace_more(limit=0)

        for comment in submission.comments[:10]:

            if len(comment.body) > 30:

                reviews.append(comment.body)

    return reviews
