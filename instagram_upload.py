import os
from instabot import Bot


class Instagram_Upload(Bot):
    def __init__(self, instagram_username, instagram_password):
        super(Instagram_Upload, self).__init__()
        self.INSTAGRAM_USERNAME = instagram_username
        self.INSTAGRAM_PASSWORD = instagram_password
        self.directory = 'instagram_uploads'


    def upload_cat_photo(self):
        self.login(
            username=self.INSTAGRAM_USERNAME,
            password=self.INSTAGRAM_PASSWORD
        )
        for filename in os.listdir(self.directory):
            f = os.path.join(self.directory, filename)
            if os.path.isfile(f):
                if filename.endswith('.jpg'):
                    self.upload_photo(f)
                    os.remove(f'instagram_uploads/{filename}.REMOVE_ME')
                    print('upload complete')
                else:
                    # bug: instabot seems to be broken (shocker) and cannot actually upload videos despite telling you that
                    # it's been uploaded
                    self.upload_video(f)
                    print('upload complete')



