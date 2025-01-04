from scripts.googledrivedownloader import GoogleFileIdFinder
import os
from scripts.instagramupload import InstagramUpload

# IMPORTANT!!!!
# instabot is incredibly jank and needs the config json to be deleted everytime except the first time you login
if os.path.isfile('config/yourinstagramusername_uuid_and_cookie.json'):
    os.remove('config/yourinstagramusername_uuid_and_cookie.json')

INSTAGRAM_USERNAME = 'your instagram username'
INSTAGRAM_PASSWORD = 'your instagram password'


drive_files = GoogleFileIdFinder()
instabot = InstagramUpload(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


drive_files.search_file_id()
drive_files.download_file(drive_files.file_id)

# Since Instabot is so janky, it'll fail logging into your instagram twice. don't panic,
# it'll succeed on the third try.

instabot.upload_cat_photo()
