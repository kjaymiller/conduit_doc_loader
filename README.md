# CONDUIT Document Prep
This project is used to create a new folder and planning document for
[Conduit](https://relay.fm/conduit).

## Google Cloud Project Setup
In order to use this, you will need to create an new OAuth 2.0 setup. 
You will need to create your own project. This project runs in test. Please follow the [cloud API instructions for setting up a new project and enabling OAuth2.0](TODO: Link)

The following scopes are used for this project: 

- https://www.googleapis.com/auth/drive'
- https://www.googleapis.com/auth/documents']

# TODO - Reduce access to drives and docs to as limited as possible.

You'll need to ensure that the `credentials.json` file you are provided has those object
enabled. 

## Getting Started
- [Create Google Cloud Project and Setup Auth](#Google Cloud Project Setup) 
- install requirements
`pip install -r requirements.txt`
- create a new folder and planning doc
`python create_new_docs.py`


## Creating New Docs
Use `create_new_docs.py` to create a new 


