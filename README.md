# CONDUIT Document Prep
This project is used to create a new folder and planning document for
[Conduit](https://relay.fm/conduit).

## Requirements
- python (developed with python3.10 but should be compatible with 3.8+)
- [Google Cloud Account](https://cloud.google.com)

**[HINT]:** This project was developed with [direnv](https://direnv.net) and [asdf](https://asdf-vm.com). You can use the provided .envrc to ensure your directory is using the same environment as the development.

## Google Cloud Project Setup
### In Google Drive

You will need a Parent folder. This is where all new folders will be created. 

You'll also
need a template file. This can be anywhere in Google Drive.


### In Google Cloud Console
In order to use this, you will need to create an new OAuth 2.0 setup. 
You will need to create your own project. This project runs in test. Please follow the [cloud API instructions for setting up a new project and enabling OAuth2.0](TODO: Link)

The following scopes are used for this project: 

- https://www.googleapis.com/auth/drive'
- https://www.googleapis.com/auth/documents'

<!-- (TODO - Reduce access to drives and docs to as limited as possible.) --> 

You'll need to ensure that the `credentials.json` file you are provided has those object
enabled. 

## Getting Started
- [Create Google Cloud Project and Setup Auth](#google-cloud-project-setup) 
- install requirements
`pip install -r requirements.txt`
- create a new folder and planning doc
`python create_new_docs.py`

## Running Scripts from the Terminal
The python scripts that are executable use a command line tool called
[Typer](https://typer.tiangolo.com). You can interface with the scripts you need to call with
`python <SCRIPT_FILENAME> [OPTIONS] ARGUMENTS`

Use the `--help` option for more information.

## Creating New Docs
Use `create_new_docs.py` to create a new folder with the planning doc.

### BEFORE YOU RUN
<!-- TODO: Switch to Secrets --> 
Add the id of the parent folder to the `PARENT_FOLDER_ID` environment variable
and the id of the template document to `COPY_DOC_ID` environment variable.

To run enter `python create_new_docs.py [OPTIONS]`
Here are the options available:
`-c/--count`: Number of new Episode files to create.
`-r/--replacement`: create a list of replacements, to update your template.
