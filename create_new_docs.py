"""
Creates the Shownotes.md
Docs and references:
  - [Create and populate folders  |  Google Drive API  |  Google Developers](https://developers.google.com/drive/api/v3/folder)
  Query from [Google Drive API in Python | List Files and Folders in a Google Drive Folder - YouTube](https://www.youtube.com/watch?v=kFR-O8BHIH4)
"""
import logging
import os
from typing import Optional

import typer

from auth import docs, files

folder_mime_type = "application/vnd.google-apps.folder"
parent_folder = os.environ.get("PARENT_FOLDER_ID")


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


def main(
    count: Optional[int] = typer.Option(1, "-c", help="Number of Folders"),
    replacements: Optional[list[str]] = typer.Option(
        None, "-r", help="substitution in key:value format"
    ),
) -> None:
    """Create Folders with a Planning Doc inside. Use '-r' to replace values inside"""

    # get next episode number
    last_episode = get_last_episode_number()

    for entry in range(count):
        episode_number = last_episode + entry + 1

        folder_id = create_folder(episode_number, "Episode")
        doc_types = [
                ("Planning", os.environ.get('PLANNING_DOC_ID')),
                ("Shownotes", os.environ.get('SHOWNOTES_DOC_ID')),
                ]

        for name, id in doc_types:
            # copy planning doc into created folder
            doc_name=f"{os.environ.get('PODCAST_NAME')} {episode_number} {name} Doc"
            doc_body = {
                "name": doc_name,
                "parents": [folder_id]
            }

            doc = create_doc(
                doc_id= id,
                doc_body=doc_body,
            )

            requests = [replace_text(f"episode_number:{episode_number}")]

            for request in replacements:
                requests.append(replace_text(request))

            for r in requests:
                logging.debug(f"replacing {r}")
            docs.documents().batchUpdate(
                documentId=doc,
                body={"requests": requests},
            ).execute()


def create_folder(episode_number: int, folder_name: str):
    """builds folder object and returns ID"""
    # metadata for folder
    file_metadata = {
        "name": f"{folder_name} {episode_number}",
        "mimeType": folder_mime_type,
        "parents": [parent_folder],
    }

    # create folder
    file = files.files().create(body=file_metadata, fields="id, name").execute()
    typer.echo(f"{file['name']}: {file['id']}")
    return file.get("id")


def create_doc(doc_id: str, doc_body: dict[str]) -> str:
    """Create two documents using the templates"""
    drive_response = (
        files.files().copy(fileId=doc_id, body=doc_body).execute()
    )
    drive_doc_id = drive_response.get("id")
    print(f"{doc_id=}")
    return drive_doc_id


def replace_text(replacement_pattern: str) -> dict[str, str]:
    """Wrapper for the replace text functionality for batchUpdates"""
    template_var, replacement_text = replacement_pattern.split(":", maxsplit=1)
    template_var = "{{" + template_var + "}}"
    return {
        "replaceAllText": {
            "containsText": {
                "text": template_var,
                "matchCase": "true",
            },
            "replaceText": replacement_text,
        }
    }


if __name__ == "__main__":
    typer.run(main)
