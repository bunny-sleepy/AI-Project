import bert_try
import numpy as np
import word2latent as w2l
import latent_vec_decode as decode
import harmonize as har
import os

'''
input: word_vec
output: latent vector
'''
def generateMidi(word_string,
                 wordvec_to_mean_model,
                 wordvec_to_variance_model,
                 music_vae_model,
                 coconet_model = None,
                 harmonize = True,
                 target_directory = './midi_output/generate_output',
                 generate_temperature = 0.5,
                 harmonize_batch_size = 1,
                 harmonize_to_piano = True):
    word_vec = bert_try.encode_nlp(word_string)
    # model output
    mu = wordvec_to_mean_model.predict(np.array([word_vec[0]]))
    sigma = wordvec_to_variance_model.predict(np.array([word_vec[0]]))

    tmp_normal = np.random.normal(0, 1, 512)
    latent_vec = np.array(mu + sigma @ tmp_normal)
    base_path = os.path.join(target_directory, word_string.replace(' ', '_'))
    os.mkdir(base_path)
    output_files = decode.decode_to_midi(target_directory=base_path,
                                         trained_model=music_vae_model,
                                         length = len(latent_vec),
                                         z_batch = [latent_vec],
                                         temperature=generate_temperature,
                                         file_name = word_string.replace(' ', '_'))
    # harmonize output
    if harmonize and (not coconet_model is None):
        print('The harmonization process may take a while...')
        for output_file in output_files:
            har.harmonize(output_file,
                          base_path,
                          coconet_model = coconet_model,
                          file_name = word_string.replace(' ', '_'),
                          batch_size = harmonize_batch_size,
                          to_piano = harmonize_to_piano)
    elif coconet_model is None:
        print('You must ')

# TODO: write a tentative main function
def main():
    # NOTE: you should change this configuration YOURSELF
    music_vae_config_str = 'hierdec-mel_16bar'
    music_vae_checkpoint_dir = './../repository/musicvae_hierdec-mel_16bar'
    target_directory = './midi_output/total_output'
    generate_temperature = 0.5
    coconet_checkpoint_dir = 'D:/code/Github/repository/coconet_model'
    harmonize_batch_size = 1

    music_vae_model = decode.generate_model(config_str = music_vae_config_str,
                                            checkpoint_dir = music_vae_checkpoint_dir)
    coconet_model = har.generate_coconet_model(coconet_model_path = coconet_checkpoint_dir)
    # train model
    w2vmodel_mean = w2l.train_model_mean(checkpoint_path_mean = 'D:/code/Github/AI-Project/model', train = False)
    w2vmodel_variance = w2l.train_model_variance(checkpoint_path_variance = 'D:/code/Github/AI-Project/model', train = False)
    word_input = "Happy"
    generateMidi(word_input,
                 w2vmodel_mean,
                 w2vmodel_variance,
                 music_vae_model = music_vae_model,
                 coconet_model = coconet_model,
                 harmonize = True,
                 target_directory = target_directory,
                 generate_temperature = generate_temperature,
                 harmonize_batch_size = harmonize_batch_size)

if __name__ == '__main__':
    main()