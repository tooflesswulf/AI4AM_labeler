from absl import app
from absl import flags
import sampling
import gui
import os
import random

FLAGS = flags.FLAGS

flags.DEFINE_string('data_dir', None, 'Path to the folder containing images.')
flags.DEFINE_boolean('import_img_list', False, 'import pre-generated img_list')
flags.DEFINE_string('saved_img_labels', None, 'file with images to be labeled')
flags.DEFINE_float('percent_labels', 1, 'Percentage of data to be labeled.', lower_bound=0, upper_bound=1)
flags.DEFINE_enum('crop_mode', 'fixed', ['fixed', 'random'], 'Fixed cropping or random cropping.')
flags.DEFINE_integer('crop_size', 400, 'Size to crop.', lower_bound=0)
flags.DEFINE_integer('crops_per_img', 10, 'Random crops per image', lower_bound=1)
flags.DEFINE_boolean('save_crops', False, 'Save sampled crops')
flags.DEFINE_boolean('key_input', False, '<CURRENTLY DEPRECIATED>Use 1, 2, 3 key as input (under, normal, over)')


def image_walk(path):
    for root, dirs, files in os.walk(path):
        if 'UNUSED' in root:
            continue
        for name in files:
            if name[-3:] in ['png', 'jpg']:
                yield os.path.join(root, name)


def main(argv):
    if FLAGS.data_dir is None:
        print('No data_dir specified. See --help')
        return 0

    img_paths = list(image_walk(FLAGS.data_dir))
    random.shuffle(img_paths)

    samp = sampling.Sampler(img_paths,
                            im_dims=(720, 1280),
                            crop_size=FLAGS.crop_size,
                            num_crop=FLAGS.crops_per_img,
                            )

    loader = gui.AsyncImageLoader(samp)

    # img_list, label_img_list = sampling.sample_img(720, 1280)
    # print(len(img_list))

    # newboi = list(samp)
    # print(len(newboi))

    gui_handler = gui.GUI(loader)


if __name__ == '__main__':
    app.run(main)
