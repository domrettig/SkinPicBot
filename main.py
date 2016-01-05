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
def get_images(post):
	# post = reddit.get_submission(submission_id='3b3dmp')
	response = urlopen(post.url)
	soup = bs(response.read(), 'html.parser')
	response.close()

	paths = []
	for i,image in enumerate(soup.find_all('a')):
		try:
			if 'Show' in image['onclick']:
				s = image['onclick']
				first = s.index('\'') + 1
				second = s.index('\'',first)
				url = s[first:second]
				urlretrieve(url,'previewimg'+str(i)+'.jpeg')
				paths.append('previewimg'+str(i)+'.jpeg')
		except KeyError:
			continue

	gun_name = soup.find('div', {'class':'workshopItemTitle'}).text
	author = '/u/' + post.author.name
	title = gun_name + ' by ' + author
	album = upload_images(title,paths)
	link = 'http://imgur.com/a/' + album['id']
	return link

def make_comment(post, link):
	comment = ("I uploaded the skins to Imgur for easier mobile viewing."
				"\n\nAlbum: [imgur](" + link + ")"
				"\n\n_____"
				"\n\n[[Code]](https://github.com/domrettig/SkinPicBot) | "
				"[[PM]](https://www.reddit.com/message/compose/?to=SkinPicBot)")
	c = post.add_comment(comment)
	return c