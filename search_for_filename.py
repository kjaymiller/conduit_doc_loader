"""QUICK """
from auth import files

page_token = None
while True:
    response = files.files().list().execute()
    for file in response.get('files', []):
        # Process change
        if name:=file.get("name") == "<Search for File>":
            print(f'Found file: {file.get("name")} {file.get("id")}')
            break