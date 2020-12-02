
import latent_vec_decode, latent_vec_generate
p = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/test1.mid'
s,mu,v = latent_vec_generate.encode(midi_batch=[p])['test1.mid']
#print(s)
target_directory = 'C:/Users/Li/PycharmProjects/AI_proj/AI-proj/testback'
latent_vec_decode.decode_to_midi(target_directory, length = len(s), z_batch = [s])

