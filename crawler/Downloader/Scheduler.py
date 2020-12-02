import Downloader
import os

"""
    TODO: you should change the range here (recommend 2000 each time) 
    Currently Finished: 10000-14999, 20000-21999
"""
# start position and end position
start = 20000
end = 22000
batch_size = 200

for iter in range(start, end, batch_size):
    try:
        Downloader.download_batch(iter, iter + batch_size)
    except:
        err_log_file = open("DownloadErrorLog.txt", "a+")
        err_log = "Download failed: " + str(iter) + " , batch size " + str(batch_size)
        err_log_file.write(err_log + "\n")
        print(err_log)

print("All finished!")