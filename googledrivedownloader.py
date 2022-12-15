from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client import client, tools, file
from googleapiclient.http import MediaIoBaseDownload
import shutil
from PIL import Image
from datetime import datetime

# TODO: 1. Moving downloaded files from google drive to seperate backup folder

now = datetime.now()
current_date = now.strftime('%m/%d/%Y')


class GoogleFileIdFinder:
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        self.store = file.Storage('google_auth/storage.json')
        self.creds = self.store.get()
        self.service = build('drive', 'v3', credentials=self.creds)
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets('google_auth/user_auth.json', SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
        # stores folder_id of desired google drive folder that you want to download contents from for later use
        self.file_id = ''

    def search_file_id(self):
        """
        This searches through your google drive for a valid folderid that will be stored in the folder_id attribute and
         used to download photos from.
        :return: folderid attribute
        """
        # searches for required folder_id in order to be able to download desired contents
        try:
            files = []
            page_token = None
            while True:
                response = self.service.files().list(
                    q="mimeType = 'application/vnd.google-apps.folder' and name contains 'cat'",
                    spaces='drive',
                    fields='nextPageToken, ''files(id, name)',
                    pageToken=page_token).execute()
                for file in response.get('files', []):
                    self.file_id += file.get('id')
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

        except HttpError as error:
            print(F'An error occurred: {error}')
            files = None

        return files

    def download_file(self, folder_id):
        """
        Using the folder_id attribute to locate the desired folder, the pictures are downloaded into the repository and
        moved into another folder called "instagram_uploads"
        """
        page_token = None
        while True:
            # Call the Drive v3 API
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=10, fields="nextPageToken, files(id, name)",
                pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    print(f'{item["name"], item["id"]}')

                    file_id = item['id']
                    request = self.service.files().get_media(fileId=file_id)

                    with open(item['name'], 'wb') as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print("Download %d%%." % int(status.progress() * 100))
                    shutil.copy(item['name'], 'instagram_uploads')
                    self.rotate_jpg(item['name'])
                    # Folder used is renamed to "backup{current_date}" and
                    # a new "cat pics" folder is created for future use
                    self.update_used_folder(self.file_id)
                    self.create_folder()

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    def create_folder(self):
        """
        Creates a new folder that can be searched by this program.

        """
        try:
            file_metadata = {
                'name': 'cat pics',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            self.service.files().create(body=file_metadata, fields='id').execute()
            print('A new folder has been created in google drive. '
                  'move your pictures into "cat pics" folder and rerun this program')


        except HttpError as error:
            print(F'An error occurred: {error}')
            return None

    @staticmethod
    def rotate_jpg(jpg):
        """
        rotates downloaded image from google drive so that it is oriented properly when posted on instagram
        :param jpg: picture that is to be rotated
        """
        if jpg.endswith('.jpg'):
            inst_image = Image.open(f"instagram_uploads/{jpg}")
            # google drive download
            inst_image = inst_image.rotate(-90)
            inst_image.save(f"instagram_uploads/{jpg}")

    def update_used_folder(self, folderid):
        """
        renames used folder as a backup
        :param folderid: id of folder that has been downloaded from
        """
        body = {'name': f'uploadbackup{current_date}'}
        self.service.files().update(fileId=folderid, body=body).execute()
