import requests

graph_api_version = 'v2.9'
access_token = 'YOUR_FACEBOOK_ACCESS_TOKEN'

# LHL's Facebook user id
user_id = '125845680811480'

# the id of LHL's response post at https://www.facebook.com/leehsienloong/posts/1505690826160285
post_id = '1505690826160285'

# the graph API endpoint for comments on LHL's post
url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, post_id)

comments = []

r = requests.get(url, params={'access_token': access_token})
while True:
    data = r.json()

    # catch errors returned by the Graph API
    if 'error' in data:
        raise Exception(data['error']['message'])

    # append the text of each comment into the comments list
    for comment in data['data']:
        # remove line breaks in each comment
        text = comment['message'].replace('\n', ' ')
        comments.append(text)

    print('got {} comments'.format(len(data['data'])))

    # check if there are more comments
    if 'paging' in data and 'next' in data['paging']:
        r = requests.get(data['paging']['next'])
    else:
        break

# save the comments to a file
with open('comments.txt', 'w', encoding='utf-8') as f:
    for comment in comments:
        f.write(comment + '\n')



    from google.cloud import language, exceptions

# create a Google Cloud Natural Languague API Python client
client = language.Client()


# a function which takes a block of text and returns its sentiment and magnitude
def detect_sentiment(text):
    """Detects sentiment in the text."""

    # Instantiates a plain text document.
    document = client.document_from_text(text)

    sentiment = document.analyze_sentiment().sentiment

    return sentiment.score, sentiment.magnitude


# keep track of count of total comments and comments with each sentiment
count = 0
positive_count = 0
neutral_count = 0
negative_count = 0

# read our comments.txt file
with open('comments.txt', encoding='utf-8') as f:
    for line in f:
        # use a try-except block since we occasionally get language not supported errors
        try:
            score, mag = detect_sentiment(line)
        except exceptions.BadRequest:
            # skip the comment if we get an error
            continue

        # increment the total count
        count += 1

        # depending on whether the sentiment is positve, negative or neutral, increment the corresponding count
        if score > 0:
            positive_count += 1
        elif score < 0:
            negative_count += 1
        else:
            neutral_count += 1

        # calculate the proportion of comments with each sentiment
        positive_proportion = positive_count / count
        neutral_proportion = neutral_count / count
        negative_proportion = negative_count / count

        print(
            'Count: {}, Positive: {:.3f}, Neutral: {:.3f}, Negative: {:.3f}'.format(
                count, positive_proportion, neutral_proportion, negative_proportion))

        
    