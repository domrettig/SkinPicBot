import praw
from prawoauth2 import PrawOAuth2Mini
from settings import user_agent, app_key, app_secret, access_token, refresh_token, scopes
from urllib import urlopen, urlretrieve
from bs4 import BeautifulSoup as bs
from upload import upload_images

reddit = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit, app_key=app_key,
							app_secret=app_secret,
							access_token=access_token,
							refresh_token=refresh_token,
							scopes=scopes)

# csgo = reddit.get_subreddit("globaloffensive")

post = reddit.get_submission(submission_id='3b3dmp')
response = urlopen(post.url)
soup = bs(response.read(), 'html.parser')
response.close()

preview_images = []
for i,image in enumerate(soup.find_all('a')):
	try:
		if "Show" in image['onclick']:
			s = image['onclick']
			first = s.index('\'') + 1
			second = s.index('\'',first)
			url = s[first:second]
			print url
			urlretrieve(url,'previewImg'+str(i)+'.jpeg')
	except KeyError:
		continue