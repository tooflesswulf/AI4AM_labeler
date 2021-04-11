import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Button
from absl import flags
import threading
import time

# matplotlib.use('TkAgg')
# TK_SILENCE_DEPRECATION=1

FLAGS = flags.FLAGS


class AsyncImageLoader:
    def __init__(self, im_iter, lookahead=3):
        self.im_iter = im_iter
        self.ready_queue = []
        self.im_queue = []
        self.lookahead = lookahead

        self.t = threading.Thread(target=self.consume)
        self.t.start()
        self.finished = False

    def consume(self):
        last_path = None
        for path, bbox in self.im_iter:
            if last_path is None or last_path != path:
                im = plt.imread(path)
                last_path = path

            # x, y, lx, ly = bbox
            x, y = bbox
            lx, ly = x + FLAGS.crop_size, y + FLAGS.crop_size
            self.ready_queue.append((path, bbox))
            self.im_queue.append(im[x:lx, y:ly])

            while len(self.ready_queue) >= self.lookahead:
                time.sleep(.2)
        self.finished = True

    def __next__(self):
        while not self.finished and len(self.ready_queue) == 0:
            time.sleep(.2)
        if self.finished and len(self.ready_queue) == 0:
            self.t.join()
            raise StopIteration

        ret = self.ready_queue[0], self.im_queue[0]
        del self.ready_queue[0]
        del self.im_queue[0]
        return ret


class GUI():
    def __init__(self, img_iter=None):
        self.locked = False

        fig = plt.figure(1, figsize=(6, 6))
        ax1 = plt.subplot(4, 3, (1, 9))  # image displayer
        ax2 = plt.subplot(4, 3, 10)  # button1
        ax3 = plt.subplot(4, 3, 11)  # button2
        ax4 = plt.subplot(4, 3, 12)  # button3
        # fig.canvas.mpl_connect('key_press_event', self._on_press)
        b1 = Button(ax2, label='Under-extrusion', color='grey', hovercolor='green')
        b1.on_clicked(self._button1)
        b2 = Button(ax3, label='Normal', color='grey', hovercolor='green')
        b2.on_clicked(self._button2)
        b3 = Button(ax4, label='Over-extrusion', color='grey', hovercolor='green')
        b3.on_clicked(self._button3)
        self.fig = fig
        self.axs = [ax1, ax2, ax3, ax4]
        self.img_iter = img_iter
        self.img_list = []
        self.labels = []

        self._next_im()
        plt.show()

    def display_im(self, im):
        self.axs[0].clear()
        self.axs[0].imshow(im)
        plt.draw()
        # plt.show()
        pass

    def get_next_im(self):
        try:
            drow, im = next(self.img_iter)
            self.img_list.append(drow)
            # print(len(self.img_list))
        except StopIteration:
            # print(len(self.img_list))
            self.done()
            return

        return im
        # self.axs[0].imshow(im[loc[0]:loc[0]+FLAGS.crop_size, loc[1]:loc[1]+FLAGS.crop_size, :])
        # return im[loc[0]:loc[0] + FLAGS.crop_size, loc[1]:loc[1] + FLAGS.crop_size, :]

    def _lock(self):
        if not self.locked:
            self.locked = True
            return False
        return True

    def _unlock(self):
        self.locked = False

    def _next_im(self):
        im = self.get_next_im()
        self.display_im(im)
        self._unlock()

    def _button1(self, event):
        if self._lock():
            return
        print('Under-extrusion')
        self.labels.append('Under-extrusion')
        self._next_im()

    def _button2(self, event):
        if self._lock():
            return
        # self._next_im()
        print('Normal')
        self.labels.append('Normal')
        self._next_im()

    def _button3(self, event):
        if self._lock():
            return
        # self._next_im()
        print('Over-extrusion')
        self.labels.append('Over-extrusion')
        self._next_im()

    def done(self):
        print('Writing labels to file...')
        if FLAGS.import_img_list: 
            fileName = './labels_%s.txt' % FLAGS.saved_img_labels[:-4]
        else: 
            fileName = './labels.txt'
        with open(fileName, 'w') as f:
            for i in range(len(self.img_list)):
                f.write('%s, (%d, %d), %s\n' % (
                    self.img_list[i][0], self.img_list[i][1][0], self.img_list[i][1][1], self.labels[i]))
        print('DONE!!')
        exit()
