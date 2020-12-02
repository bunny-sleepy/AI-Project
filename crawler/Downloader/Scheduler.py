import Downloader
import os
from threading import Thread
"""
    TODO: you should change the range here (recommend 2000 each time) 
    Currently Finished: 10000-14999, 20000-21999
"""
# start position and end position
start = 0
end = 27000
iter_size = 3000
batch_size = 300

iters = [(0, 3000),
        (3000, 6000),
        (6000, 9000),
        (9000, 12000),
        (12000, 15000),
        (15000, 18000),
        (18000, 21000),
        (21000, 24000),
        (24000,27000)]

def schedule(iter_start, iter_end):
    for iter in range(iter_start, iter_end, batch_size):

        try:
            Downloader.download_batch(iter,
                                      iter + batch_size,
                                      "DownloadErrorLog_%d_to_%d.txt" % (iter, iter + batch_size - 1))
        except:
            err_log_file = open("DownloadErrorLog_%d_to_%d.txt" % (iter, iter + batch_size - 1), "a+")
            err_log = "Download failed: " + str(iter)
            err_log_file.write(err_log + "\n")
            print(err_log)

ts = [Thread(target = schedule, args = (iter_start ,iter_end, )) for iter_start, iter_end in iters]
for t in ts:
    t.start()
for t in ts:
    t.join()

print("All finished!") 