import sqlite3

# create a db named SolutionTipsVideos if it doesn't exist
# only two records: videoid should be unique and also id should be unique
def database():
    conn = sqlite3.connect("SolutionTipsVideos.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Videos (id INTEGER PRIMARY KEY, videoId TEXT UNIQUE)")
    conn.commit()
    # if created, print message and return connection
    print("[+] Starting Up")
    return conn

# close connection
def closeDB(conn):
    conn.close()
    print("[+] Shutting Down")

# add video to the database and make sure videoId is unique
def addVideo(conn, videoId):
    c = conn.cursor()
    c.execute("INSERT INTO Videos VALUES (NULL, ?)", (videoId,))
    conn.commit()
    print("[+] Video Saved")
    print("[+] Total Videos Saved " + str(numVideos(conn)))

# delete video from database as per videoId
def deleteVideo(conn, videoId):
    c = conn.cursor()
    c.execute("DELETE FROM Videos WHERE videoId = ?", (videoId,))
    conn.commit()
    print("[+] Video Deleted")

# get all videos from the database and print them
def getVideos(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Videos")
    videos = c.fetchall()
    return videos

# print all videos
def printVideos(conn):
    videos = getVideos(conn)
    for video in videos:
        print(video)

# number of videos in the database
def numVideos(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Videos")
    videos = c.fetchall()
    return len(videos)

# get all videos from the database make a dictionary of id and videoId
def getVideoIds(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM Videos")
    videos = c.fetchall()
    videoIds = {}
    for video in videos:
        videoIds[video[0]] = video[1]
    return videoIds

# menu
def addVideoMenu(conn):
    num = 0
    while True:
        videoUrl = input("[+] Enter Video URL: ")
        videoId = videoUrl.split("=")[1]
        addVideo(conn, videoId)
        # num = int(input("[+] Enter -9 to exit: "))

# main handler
def main():
    conn = database()
    addVideoMenu(conn)
    closeDB(conn)

# starting up
main()

# list of videos
# conn = database()
# # printVideos(conn)
# # delete video
# # deleteVideo(conn, "2vDhspVsCJE&t")
# getVideoIds(conn)

