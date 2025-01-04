from __future__ import print_function

from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import shutil

import os.path

from PIL import Image

from datetime import datetime

now = datetime.now()
current_date = now.strftime('%m/%d/%Y')


class GoogleFileIdFinder:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        if os.path.exists('google_auth/token.json'):
            self.creds = Credentials.from_authorized_user_file('google_auth/token.json', scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'google_auth/credentials.json', scopes)
                self.creds = self.flow.run_local_server(port=0)
            with open('google_auth/token.json', 'w') as token:
                token.write(self.creds.to_json())
        # stores folder_id of desired google drive folder that you want to download contents from for later use
        self.file_id = ''
        self.service = build('drive', 'v3', credentials=self.creds)

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
                    q="mimeType = 'application/vnd.google-apps.folder' and name = 'cat pics' and trashed = false",
                    spaces='drive',
                    fields='nextPageToken, ''files(id, name)',
                    pageToken=page_token).execute()
                # the google drive is checked for any folder titled, 'cat pics'. If not found, a new folder
                # with that title is created
                if response.get('files', []):
                    for file in response.get('files', []):
                        self.file_id += file.get('id')
                else:
                    print('Error: Folder was not found \n'
                          'A new folder called "cat pics" has been created. Populate the folder with pictures'
                          ' rerun the program')
                    self.create_folder()
                    quit()

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
                pageSize=10,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print("Error: No pictures were found in the folder\n"
                      "try again once you've populated the folder with pictures")
                quit()
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
                    print(item['name'])
                    shutil.copy(item['name'], 'instagram_uploads')
                    os.remove(item['name'])
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


        except HttpError as error:
            print(F'An error occurred: {error}')
            return None

    @staticmethod
    def rotate_jpg(jpg):
        # problem:
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
