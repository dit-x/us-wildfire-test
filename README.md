# Introduction
To complete the task, the app was deployed using streamlit, and the step to replicate the deployment is stated below.

# Project Setup
`Note` for optimization reasons, the application is deployed using only the data required to conduct the analysis and generate reports on a web page. To use the original data from Kaggle, follow the [Dev branch](https://github.com/dit-x/us-wildfire-test/tree/dev) readme


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
When all is set up, see the running application on a local browser using:
``` shell
http://localhost:8502/
```

### `Locally`
Run the application locally by using Makefile. Few things to consider 
``` text
# Modify and change the setup section of the Makefile accordingly as shown below

setup:
    # Create python virtualenv & source it
    # python3 -m venv .venv
    # source .venv/bin/activate
```

# Usage
### `Cause prediction`
To predict the fire cause using the web app, the app takes in the fire size, date, and location (lat and long). Once all the parameters are provided, generate the result using the `Predict Result` button.
### `Report`
Here are the things to know
- use the checkbox to filter and compare
- use the slider to increase or decrease the number of records fetched



# Output
If the project is running, the web page should show similar output in the picture below.

<img src="sample_image.png" alt="Alt text" title="Optional title">