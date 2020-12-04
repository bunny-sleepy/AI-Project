import os
import re

dataset_path = "I:\\FinalProj\\AI-Project\\preprocessing\\TitlePreprocessor\\dataset"

char_set = {'朘','朅','#','œ', '抯', '’','Ç', 'á','朏', ']', '&', 'ü',
 '=', 'Φ','骃', '＆', '[','é', '朙', 'î','閛', 'Ø', 'à', 'ン','ス', '鉶', '閡', 
 'è','+','ï','№','朠', '鵪', '驪', 'í', 'û','朣', 'ダ', '抦'}

id_set = {'(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)'}

pattern= "[A-Z]"

# Delete useless files
def FileFilter():
    for filename in os.listdir(dataset_path):
        has_deleted = False
        for char in char_set:
            if char in filename and not has_deleted:
                os.remove(dataset_path + "\\" + filename)
                has_deleted = True
        for char in id_set:
            if char in filename and not has_deleted:
                os.remove(dataset_path + "\\" + filename)
                has_deleted = True       

# Rename files
def Rename():
    global pattern
    for filename in os.listdir(dataset_path):
        # split
        # new_filename = re.sub(pattern,lambda x:" "+x.group(0), filename)
        new_filename = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", filename)
        try:
            os.rename(dataset_path + "\\" + filename, dataset_path + "\\" + new_filename)
        except:
            os.remove(dataset_path + "\\" + filename)

Rename()