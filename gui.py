import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from absl import app
from absl import flags
import sampling

FLAGS = flags.FLAGS

class GUI(): 
    def __init__(self, img_list=None): 
        fig = plt.figure(1, figsize=(6, 6))
        ax1 = plt.subplot(4, 3, (1, 9)) # image displayer
        ax2 = plt.subplot(4, 3, 10) # button1
        ax3 = plt.subplot(4, 3, 11) # button2
        ax4 = plt.subplot(4, 3, 12) # button3
        fig.canvas.mpl_connect('key_press_event', self._on_press)
        b1 = Button(ax2, label='Under-extrusion', color='grey', hovercolor='green')
        b1.on_clicked(self._button1)
        b2 = Button(ax3, label='Normal', color='grey', hovercolor='green')
        b2.on_clicked(self._button2)
        b3 = Button(ax4, label='Over-extrusion', color='grey', hovercolor='green')
        b3.on_clicked(self._button3)
        self.fig = fig
        self.axs = [ax1, ax2, ax3, ax4]
        self.img_list = img_list
        self.img_iter = iter(img_list)
        self.labels = []
        plt.show()
        return 

    def display_im(self, im): 
        self.axs[0].imshow(im)
        # plt.show()
        pass

    def get_next_im(self):
        try: 
            im_path, loc = next(self.img_iter)
        except StopIteration: 
            self.done()
        im = plt.imread(im_path)
        # self.axs[0].imshow(im[loc[0]:loc[0]+FLAGS.crop_size, loc[1]:loc[1]+FLAGS.crop_size, :])
        return im[loc[0]:loc[0]+FLAGS.crop_size, loc[1]:loc[1]+FLAGS.crop_size, :]

    def _on_press(self, event): 
        if FLAGS.key_input: 
            if event.key == '1': 
                self._button1(event)
            elif event.key == '2': 
                self._button2(event)
            elif event.key == '3': 
                self._button3(event)
            else: 
                pass
    def _button1(self, event): 
        print('Under-extrusion')
        self.labels.append('Under-extrusion')
        im = self.get_next_im()
        self.display_im(im)
    def _button2(self, event): 
        print('Normal')
        self.labels.append('Normal')
        im = self.get_next_im()
        self.display_im(im)
    def _button3(self, event): 
        print('Over-extrusion')
        self.labels.append('Over-extrusion')
        im = self.get_next_im()
        self.display_im(im)
    def done(self): 
        print('Writing labels to file...')
        with open('./labels_%s.txt' %FLAGS.saved_img_labels[:-4], 'w') as f: 
            for i in range(len(self.img_list)): 
                f.write('%s, (%d, %d), %s\n' % (self.img_list[i][0], self.img_list[i][1][0], self.img_list[i][1][1], self.labels[i+1]))
        print('DONE!!')
        exit()

