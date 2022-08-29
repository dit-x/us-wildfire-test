# Introduction
This is a guide to replicate the project locally or using docker. It is important that there will be some manual steps ti carry out to download the data from Kaggle to your local environment or docker container. The ste will be indicated below.

# Project Setup
## Kaggle API Setup
This is the manual part of the set up to download the dataset directly for Kaggle use [Kaggle API](https://www.kaggle.com/docs/api). Here are the steps to follow: 
- Login to Kaggle.com
- Navigate to `Account` page
- In the API section, create New API Token.
- Move the downloaded file to `~/.kaggle` folder
DONE!!!

## Environment Setup
### `Using Docker`
To use docker, cd into the project folder and run 
``` shell
cp -r ~/.kaggle .
docker compose up --build 
```
or run in background with
``` shell
cp -r ~/.kaggle .
docker compose up --build -d
```
when all is set up, see the running application on local browser using:
``` shell
http://localhost:8502/
```

### `Locally`
Run the application locally by using Makefile. Few things to consider 
``` text
# Modify and change the setup section of the Mak accordly as shown below

setup:
	# Create python virtualenv & source it
	# python3 -m venv .venv
	# source .venv/bin/activate
```

