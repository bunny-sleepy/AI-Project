CONFIG=cat-mel_2bar_small

python -m magenta.models.music_vae.preprocess_tfrecord \
--input_tfrecord=/path/to/tfrecords/train.tfrecord \
--output_tfrecord=/path/to/tfrecords/train-$CONFIG.tfrecord \
--output_shards=10 \
--config=$CONFIG \
--alsologtostderr