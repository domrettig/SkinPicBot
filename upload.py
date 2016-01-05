from imgurpython import ImgurClient
from settings import client_id, client_secret, imgur_access_token, imgur_refresh_token
from os import remove

def upload_images(album_title, paths):
	client = ImgurClient(client_id, client_secret)
	client.set_user_auth(imgur_access_token, imgur_refresh_token)
	fields = {
		'title':album_title
	}
	album = client.create_album(fields)

	for i,img in enumerate(paths):
		config = {
			'album':album['id'],
			'name':str(i),
			'title':str(i)
		}
		image = client.upload_from_path(img,config=config,anon=False)
		remove(img)

	return album