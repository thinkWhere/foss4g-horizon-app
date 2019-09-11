# horizon-app
Horizon image creation from OS Terrain 50 DEM Open Data

- Uses a processed form of Ordnance Survey Terrain 50 DEM open data
- Creates a PNG image of a horizon by scanning heights over 50km from a designated start point
- Creates a JSON file of Munro and Corbett peaks with bearing, elevation and distance

### Developing on Windows
Ensure you use windows installer to install all Python dependencies on Windows, as follows:

* Create an empty venv
    * ```python -m venv .\venv```
* Activate your virtual environment
    * ```.\venv\scripts\activate```
* Run the windows installer
    * ```.\devops\install\install.bat```

## First Run Config
You are going to need to set the AWS config prior to building the container in file `./app/config.py`

You will need to setup an IAM user that has read/write permissions for the Viewer Bucket.

```.env
S3_ACCESS_KEY = ""
S3_ACCESS_SECRET_KEY = ""
DATABASE_CONNECTION_STRING = ""
VIEWER_BUCKET = ""
TERRAIN_DATA_BUCKET = ""
```