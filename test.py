 # move folder1 with its files to folder2

def move_folder(folder1, folder2):
    import os
    import shutil
    # check if folder1 exists
    if os.path.exists(folder1):
        # check if folder2 exists
        if os.path.exists(folder2):
            # move folder1 to folder2
            shutil.move(folder1, folder2)
        else:
            # create folder2
            os.mkdir(folder2)
            # move folder1 to folder2
            shutil.move(folder1, folder2)
    else:
        print("Folder1 does not exist")