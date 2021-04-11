import numpy as np
from absl import app
from absl import flags
import os
import pickle

FLAGS = flags.FLAGS


class Sampler:
    def __init__(self, paths, im_dims=(0, 0), crop_size=400, num_crop=1):
        self.h, self.w = im_dims
        self.crop_size = crop_size
        self.num_crop = num_crop

        self.paths = paths
        if FLAGS.import_img_list: 
            with open(FLAGS.saved_img_labels, 'rb') as f:
                self.saved_crops = pickle.load(f)

    def random_crop(self, n=1):
        locs = np.random.randint(
            low=0, high=[self.h - self.crop_size, self.w - self.crop_size],
            size=(n, 2)
        )

        return locs
        # return np.hstack([locs, locs + self.crop_size])

    def __iter__(self):
        if FLAGS.import_img_list: 
            for fname, c in self.saved_crops: 
                yield fname, c
        else: 
            for fname in self.paths:
                crops = self.random_crop(n=self.num_crop)
                for c in crops:
                    yield fname, c


def get_crop_map(height, width):
    height_count = np.ceil(float(height - FLAGS.crop_size) / FLAGS.crop_size)
    height_space = np.ceil(float(height - FLAGS.crop_size) / height_count)
    width_count = np.ceil(float(width - FLAGS.crop_size) / FLAGS.crop_size)
    width_space = np.ceil(float(width - FLAGS.crop_size) / width_count)


# return top left corner of random crops (N, 2), each loc is (y, x)
def random_crop(height, width):
    locs = np.random.randint(low=0, high=[height - FLAGS.crop_size, width - FLAGS.crop_size],
                             size=(FLAGS.crops_per_img, 2))
    return locs


# return two lists with file path and location of each sample and each sample to be labeled
def sample_img(height, width):
    if FLAGS.import_img_list:
        # with open('img_list.pkl', 'rb') as f:
        #   img_list = pickle.load(f)
        with open(FLAGS.saved_img_labels, 'rb') as f:
            label_img_list = pickle.load(f)
        return None, label_img_list
    img_list = []
    label_img_list = []
    p = FLAGS.percent_labels 
    for root, dirs, files in os.walk(FLAGS.data_dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            if root[-8:] == 'unsorted' or 'UNUSED' in root:
                # print(os.path.join(root, name))
                continue
            if name[-3:] != 'png' and name[-3:] != 'jpg' and name[-4:] != 'JPEG':
                continue
            im_path = os.path.join(root, name)
            locs = random_crop(height, width)
            mask = np.random.random(FLAGS.crops_per_img)
            img_list.extend(list(map(lambda l: (im_path, l), list(locs))))
            label_img_list.extend(list(map(lambda l: (im_path, l), list(locs[mask < p, :]))))

        for name in dirs:
            pass
    # print(len(img_list))
    # print(len(label_img_list))
    if FLAGS.save_crops:
        with open('img_list.pkl', 'wb') as f:
            pickle.dump(img_list, f)

        batch_size = 50
        for i in range((len(label_img_list) // batch_size) + 1):
            with open('label_img_list%d.pkl' % i, 'wb') as f:
                pickle.dump(label_img_list[i * batch_size:(i + 1) * batch_size], f)
    return img_list, label_img_list
