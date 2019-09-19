
class Config:
    # S3 Access Credentials
    S3_ACCESS_KEY = ""
    S3_ACCESS_SECRET_KEY = ""
    # Database Connection String
    DATABASE_CONNECTION_STRING = """
        host=''
        port='5432'
        dbname='appsstaging'
        user='viewpoint_user'
        password='viewpoint'
        """
    # S3 Bucket for the Web Application and Output Files
    VIEWER_BUCKET = ""
    # Terrain Data S3 Bucket
    # (Public bucket that thinkWhere host (temporarily) data available from Ordnance Survey)
    TERRAIN_DATA_BUCKET = "ac-foss4g-terrain-data"
