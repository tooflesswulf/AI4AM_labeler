from absl import app
from absl import flags
import sampling
import gui
import sys
import matplotlib.pyplot as plt

FLAGS = flags.FLAGS

flags.DEFINE_string('data_dir', './', 'Path to the folder containing images.')
flags.DEFINE_boolean('import_img_list', False, 'import pre-generated img_list')
flags.DEFINE_string('saved_img_labels', None, 'file with images to be labeled')
flags.DEFINE_integer('percent_labels', 100, 'Percentage of data to be labeled.', lower_bound=0, upper_bound=100)
flags.DEFINE_enum('crop_mode', 'fixed', ['fixed', 'random'], 'Fixed cropping or random cropping.')
flags.DEFINE_integer('crop_size', 400, 'Size to crop.', lower_bound=0)
flags.DEFINE_integer('crops_per_img', 10, 'Random crops per image', lower_bound=1)
flags.DEFINE_boolean('save_crops', False, 'Save sampled crops')
flags.DEFINE_boolean('key_input', False, '<CURRENTLY DEPRECIATED>Use 1, 2, 3 key as input (under, normal, over)')


FLAGS(sys.argv)

print('Press any button to start')
sampling.random_crop(720, 1280)

img_list, label_img_list = sampling.sample_img(720, 1280)

gui_handler = gui.GUI(label_img_list)
