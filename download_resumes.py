from __future__ import print_function

import os.path
from venv import create
import io 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from docx2pdf import convert

'''
This python script downloads all resumes from Google Drive, converts everything
to PDFs, and saves them locally.
If you are having issues with Google Authentication, please watch this video (you
can probably start at the 7:00): 
    https://www.youtube.com/watch?v=10ANOSssdCw&ab_channel=JonathanMeier
'''

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive']

class Resume:
    def __init__(self, resume_name, file_id):
        self.resume_name = resume_name
        self.file_id     = file_id

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow  = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_resume_files(creds):
    resumes     = []
    folder_id   = "1po3bU62ThSSbYcUYKQd7jjcx87hIjO4xyqQj7pQokUr-8QOH5M-FbrASiyV6z-3okH0zbNR2"
    num_resumes = 100

    try:
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(
            pageSize=num_resumes, 
            q="parents in '{0}'".format(folder_id),
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        for item in items:
            resume = Resume(item["name"], item["id"])
            resumes.append(resume)

    except HttpError as error:
        print(f'An error occurred: {error}')

    return resumes

def download_resume(creds, resume):
    directory_name = "resumes"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    service    = build('drive', 'v3', credentials=creds)
    request    = service.files().get_media(fileId=resume.file_id)
    file       = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    try:
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

        path = "resumes/" + resume.resume_name
        with open("resumes/" + resume.resume_name, "wb") as f:
            f.write(file.getbuffer())

        return path

    except:
        print("error with: " + resume.resume_name)
        return ""
        
if __name__ == '__main__':
    creds   = get_credentials()
    resumes = get_resume_files(creds)

    for resume in resumes:
        path = download_resume(creds, resume)
