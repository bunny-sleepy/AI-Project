import Downloader
import os

# start position and end position
start = 10070
end = 10100
batch_size = 5

for iter in range(start, end, batch_size):
    try:
        Downloader.download_batch(iter, iter + batch_size)
    except:
        err_log_file = open("DownloadErrorLog.txt", "a+")
        err_log = "Download failed: " + str(iter) + " , batch size " + str(batch_size)
        err_log_file.write(err_log + "\n")
        print(err_log)

print("All finished!")