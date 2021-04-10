# AI4AM_labeler

## Before you start (Very Important)
1. The first screen is blank, click on any button to begin. It will not be logged. 
2. The data to be labeled are split into 15 batches. **If you do not run the program to the end, no label will be saved!!** Each batch have 50 images, it should be little enough to finish in one sitting. 
3. Only label each image once! Do not click buttons multiple times or it might influence the result of other images! You can check terminal output to see if the click went through (it will show your choice). 
4. Move the cursor out of the button to change to the next image. (It only save and fetch the next image after the cursor is moved away from the button clicked). 
5. Put all data in '../3d print data' relative to main.py 


## Running the code 
python3 main.py --data_dir='../3d print data' --import_img_list=True --saved_img_labels=label_img_list[0-15].pkl --percent_labels=10 --crop_mode=random --crops_per_img=10
*remember to change the tag --saved_img_labels=label_img_list[0-15].pkl according to which batch you are labeling!*


