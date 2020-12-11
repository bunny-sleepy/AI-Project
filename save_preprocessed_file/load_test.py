import numpy as np
from save_preprocessed_file.load_prepared import load_prepared_dataset as load

def main():
    filepath = 'C:/Users/Li/Desktop/Latex file/AI_proj/AI-proj/testback/storetest'
    latent_list, wordvec_list = load(filepath)
    print(np.shape(latent_list))

if __name__ == "__main__":
    main()