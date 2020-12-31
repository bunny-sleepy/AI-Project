import os
import latent_vec_decode as lvd
import latent_vec_generate as lvg

def wwh_test():
    model_path = 'D:/code/Github/repository/musicvae_hierdec-mel_16bar'
    trained_model = lvg.generate_model(checkpoint_dir = model_path)
    test1_path = 'D:/code/Github/AI-Project/midi_input/TakeMeToYourHeart.mid'
    midi_batch = []
    midi_batch.append(test1_path)
    dict1 = lvg.encode(trained_model = trained_model, midi_batch = midi_batch)
    i = 0
    target_dir = 'D:/code/Github/AI-Project/midi_output/test_output'
    z_batch = []
    for key in dict1:
        z, _, _ = dict1[key]
        z_batch.append(z)
    lvd.decode_to_midi(trained_model = trained_model, target_directory = target_dir, z_batch = z_batch, file_name = '1')

def lzz_test():
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
    encoded_list = lvg.encode(midi_batch=list_midi)
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

if __name__ == "__main__":
    wwh_test()