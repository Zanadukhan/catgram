from googledrivedownloader import GoogleFileIdFinder
import os
from instagram_upload import Instagram_Upload

# instabot is incredibly jank and needs the config json to be deleted everytime except the first time you login
if os.path.isfile('config/aten_sun_cat_uuid_and_cookie.json'):
    os.remove("config/aten_sun_cat_uuid_and_cookie.json")

INSTAGRAM_USERNAME = 'aten_sun_cat'
INSTAGRAM_PASSWORD = '@#av9R27RfmMRf'

user_input = input(f'Is this your first time using this program?'
                   f' enter "y" if so, otherwise, press enter to continue: ').lower()


drive_files = GoogleFileIdFinder()
instabot = Instagram_Upload(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


if user_input == 'y':
    drive_files.create_folder()

else:
    drive_files.search_file_id()
    drive_files.download_file(drive_files.file_id)

    # Since Instabot is so janky, it'll fail logging into your instagram twice. don't panic,
    # it'll succeed on the third try.

    instabot.upload_cat_photo()

