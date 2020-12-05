import os
import latent_vec_decode, latent_vec_generate
path = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/midids'

list_name=[]
list_midi=[]
list_vector=[]
list_midiname=[]
for file in os.listdir(path):  
        file_path = path + '/' + file 
        if os.path.splitext(file_path)[1]=='.mid':  
            list_name.append(file_path)
            list_midi.append(file_path)
            list_midiname.append(file)
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#print(list_midiname)
encoded_list = latent_vec_generate.encode(midi_batch=list_midi)
for m in list_midiname:
    z,u,v = encoded_list[m]
    list_vector.append(z)

print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

path1 = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/testback/latentback'
path2 = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/testback/nameback'
with open(path1, 'w+') as file_object:
    file_object.write(str(list_vector))
with open(path2, 'w+') as file_object:
    file_object.write(str(list_midiname))

#print(s)
#target_directory = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/testback'
#latent_vec_decode.decode_to_midi(target_directory, length = len(s), z_batch = [s])

