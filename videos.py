import dbconnect as db

# get video id from video
def videoId(videoUrl):
    try:
        videoId = videoUrl.split("=")[1]
    except:
        videoId = videoUrl.split("shorts/")[1]

    return videoId

# create a table vidoes inside db if it doesn't exist with id and videoid
def addVideoId(conn, videoId):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, videoId TEXT)")
    conn.commit()
    
    # now insert the video and save it
    c.execute("INSERT INTO videos VALUES (NULL, ?)", (videoId,))
    conn.commit()
    print("[+] Video Saved")
    print("[+] Total Videos Saved " + str(db.numVideos(conn)))

# get all video ids from videos table
def getVideoIds(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM videos")
    videoIds = c.fetchall()
    return videoIds

# get number of videos in the database
def numVideos(conn):
    return (len(getVideoIds(conn)))

