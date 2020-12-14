import coconet.coconet_sample as cs
import coconet.lib_util as lib_util
import os
import re
import tensorflow.compat.v1 as tf
import pretty_midi
import numpy as np

def generate_coconet_model(coconet_model_path):
    """Generate a coconet model based on the model path


    """
    tf.compat.v1.disable_eager_execution()
    coconet_model = cs.instantiate_model(coconet_model_path)
    return coconet_model

# TODO: change the instrument of the harmonized sample
def harmonize(file_path, output_dir, coconet_model, temperature = 0.8, batch_size = 2):
    """harmonize a midi file

    Args:
        file_path: the input path
        coconet_model: the loaded coconet model
        output_dir: the output path
        temperature: the generation temperature
        batch_size: how many samples to generate each time

    Return:
        None
    """
    strategy = "harmonize_midi_melody"
    generator = cs.Generator(coconet_model, strategy)
    midi_outs = generator.run_generation(midi_in = pretty_midi.PrettyMIDI(file_path),
                                         gen_batch_size = batch_size)

    # Creates a folder for storing the process of the sampling.
    label = "sample_%s_%s_%s_T%g_l%i_%.2fmin" % (lib_util.timestamp(),
                                                 strategy,
                                                 generator.hparams.architecture,
                                                 temperature,
                                                 batch_size,
                                                 generator.time_taken)
    basepath = os.path.join(output_dir, label)
    tf.logging.info("basepath: %s", basepath)
    tf.gfile.MakeDirs(basepath)

    # Saves the results as midi or returns as midi out.
    midi_path = os.path.join(basepath, "midi")
    tf.gfile.MakeDirs(midi_path)
    tf.logging.info("Made directory %s", midi_path)
    cs.save_midis(midi_outs, midi_path, label)

    result_npy_save_path = os.path.join(basepath, "generated_result.npy")
    tf.logging.info("Writing final result to %s", result_npy_save_path)
    with tf.gfile.Open(result_npy_save_path, "wb") as p:
        np.save(p, generator.pianorolls)

    # Stores all the (intermediate) steps.
    intermediate_steps_path = os.path.join(basepath, "intermediate_steps.npz")
    with lib_util.timing("writing_out_sample_npz"):
        tf.logging.info("Writing intermediate steps to %s", intermediate_steps_path)
        generator.logger.dump(intermediate_steps_path)

    # Save the prime as midi and npy if in harmonization mode.
    # First, checks the stored npz for the first (context) and last step.
    tf.logging.info("Reading to check %s", intermediate_steps_path)
    with tf.gfile.Open(intermediate_steps_path, "rb") as p:
        foo = np.load(p)
        for key in foo.keys():
            if re.match(r"0_root/.*?_strategy/.*?_context/0_pianorolls", key):
                context_rolls = foo[key]
                context_fpath = os.path.join(basepath, "context.npy")
                tf.logging.info("Writing context to %s", context_fpath)
                with lib_util.atomic_file(context_fpath) as context_p:
                    np.save(context_p, context_rolls)
                if "harm" in strategy:
                    # Only synthesize the one prime if in Midi-melody-prime mode.
                    primes = context_rolls
                    if "Melody" in strategy:
                        primes = [context_rolls[0]]
                    prime_midi_outs = cs.get_midi_from_pianorolls(primes, generator.decoder)
                    cs.save_midis(prime_midi_outs, midi_path, label + "_prime")
                break
    tf.logging.info("Done")

# example of usage
def main():
    coconet_model_path = "D:/code/Github/repository/coconet_model"
    coconet_model = generate_coconet_model(coconet_model_path)
    file_path = "D:/code/Github/AI-Project/midi_input/test.mid"
    output_path = "D:/code/Github/AI-Project/midi_output/harmonize_output"
    harmonize(file_path, output_path, coconet_model)

if __name__ == "__main__":
    main()