"""
Creates the Shownotes.md
Docs and references:
  - [Create and populate folders  |  Google Drive API  |  Google Developers](https://developers.google.com/drive/api/v3/folder)
  Query from [Google Drive API in Python | List Files and Folders in a Google Drive Folder - YouTube](https://www.youtube.com/watch?v=kFR-O8BHIH4)
"""
from auth import docs, files
import typer
import os
from typing import Optional

folder_mime_type = "application/vnd.google-apps.folder"
parent_folder = os.environ.get('PARENT_FOLDER_ID')


def get_ep_number(title):
    """gets the number from the end of the Episode"""
    return int(title.lstrip("Episode"))


def get_last_episode_number() -> list[int]:
    """Returns the next file in the Podcast folder"""

    # query building params
    qmime_type = f"mimeType = '{folder_mime_type}'"
    qparents = f"parents = '{parent_folder}'"
    qfolder = f"name contains 'Episode'"
    qtrash = "trashed = false"
    q = "and".join((qmime_type, qparents, qfolder, qtrash))
    
    # create search request
    response = files.files().list(q=q).execute()

    # generate list of remaining files
    episodes = [get_ep_number(folder["name"]) for folder in response.get("files")]
    return max(episodes)


def create_folder(
        count: Optional[int] = typer.Option(1, '-c', help="Number of Folders"),
        replacements: Optional[list[str]] = typer.Option(None, '-r', help="substitution in key:value format"),
) -> None:
    """Create Folders with a Planning Doc inside. Use '-r' to replace values inside"""

    # get next episode number
    last_episode = get_last_episode_number()

    for entry in range(count):
        episode_number = last_episode + entry + 1

        # metadata for folder 
        file_metadata = {
            'name': f'Episode {episode_number}',
            "mimeType": folder_mime_type,
            "parents": [parent_folder],
        }

        # create folder
        file = files.files().create(
                body=file_metadata,
                fields='id, name'
        ).execute()

        # copy planning doc into created folder
        planning_doc = create_doc(name=f"Conduit {episode_number} Planning Doc", parent=file['id'])

        # process substitutions
        requests = [replace_text(f"episode_number:{episode_number}")]

        for request in replacements:
            requests.append(replace_text(request))
            print(f"replacing {request}")

        if requests:
            docs.documents().batchUpdate(
                    documentId=planning_doc,
                    body={'requests': requests},
            ).execute()

        print(f"{file['name']}: {file['id']}")


def create_doc(name:str, parent:str) -> str:
    """Create two documents using the templates"""
    shownotes_id = os.environ.get('COPY_DOC_ID')
    shownotes_body = {
        "name": name,
        "parents": [parent],
    }
    drive_response = files.files().copy(
        fileId=shownotes_id, body=shownotes_body).execute()
    planning_doc_id = drive_response.get('id')
    print(f"{planning_doc_id=}")
    return planning_doc_id 


def replace_text(replacement_pattern: str) -> dict[str, str]:
    """Wrapper for the replace text functionality for batchUpdates"""
    template_var, replacement_text = replacement_pattern.split(":", maxsplit=1)
    template_var = "{{" +  template_var + "}}"
    return {
            'replaceAllText': {
                'containsText': {
                    'text': template_var,
                    'matchCase': 'true',
                },
            'replaceText': replacement_text,
                }}


if __name__ == "__main__":
    typer.run(create_folder)
