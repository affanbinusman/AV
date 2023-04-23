import os
import random
import shutil

imgList = os.listdir('images')


#shuffling images
random.shuffle(imgList)

split = 0.2

# train_path = 'custom_dataset2/train'
# val_path = 'custom_dataset2/val'
train_path_img = 'custom_dataset20230419_sweep/train/images'
train_path_lbl = 'custom_dataset20230419_sweep/train/labels'
val_path_img = 'custom_dataset20230419_sweep/val/images'
val_path_lbl = 'custom_dataset20230419_sweep/val/labels'

if os.path.isdir(train_path_img) == False:
    os.makedirs(train_path_img)
if os.path.isdir(train_path_lbl) == False:
    os.makedirs(train_path_lbl)
if os.path.isdir(val_path_img) == False:
    os.makedirs(val_path_img)
if os.path.isdir(val_path_lbl) == False:
    os.makedirs(val_path_lbl)

imgLen = len(imgList)
print("Images in total: ", imgLen)

train_images = imgList[: int(imgLen - (imgLen*split))]
val_images = imgList[int(imgLen - (imgLen*split)):]
print("Training images: ", len(train_images))
print("Validation images: ", len(val_images))

for imgName in train_images:
    og_path = os.path.join('images', imgName)
    target_path = os.path.join(train_path_img, imgName)

    shutil.copyfile(og_path, target_path)

    # og_txt_path = os.path.join('bbox_txt', imgName.replace('.jpg', '.txt'))
    if ".jpeg" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.jpeg', '.txt'))
    elif ".JPG" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.JPG', '.txt'))
    elif ".jpg" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.jpg', '.txt'))
    # target_txt_path = os.path.join(train_path, imgName.replace('.jpg', '.txt'))
    if ".jpeg" in imgName:
        target_txt_path = os.path.join(train_path_lbl, imgName.replace('.jpeg', '.txt'))
    elif ".JPG" in imgName:
        target_txt_path = os.path.join(train_path_lbl, imgName.replace('.JPG', '.txt'))
    elif ".jpg" in imgName:
        target_txt_path = os.path.join(train_path_lbl, imgName.replace('.jpg', '.txt'))

    shutil.copyfile(og_txt_path, target_txt_path)

for imgName in val_images:
    og_path = os.path.join('images', imgName)
    target_path = os.path.join(val_path_img, imgName)

    shutil.copyfile(og_path, target_path)

    # og_txt_path = os.path.join('bbox_txt', imgName.replace('.jpg', '.txt'))
    # target_txt_path = os.path.join(val_path, imgName.replace('.jpg', '.txt'))
    if ".jpeg" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.jpeg', '.txt'))
    elif ".JPG" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.JPG', '.txt'))
    elif ".jpg" in imgName:
        og_txt_path = os.path.join('labels', imgName.replace('.jpg', '.txt'))
    if ".jpeg" in imgName:
        target_txt_path = os.path.join(val_path_lbl, imgName.replace('.jpeg', '.txt'))
    elif ".JPG" in imgName:
        target_txt_path = os.path.join(val_path_lbl, imgName.replace('.JPG', '.txt'))
    elif ".jpg" in imgName:
        target_txt_path = os.path.join(val_path_lbl, imgName.replace('.jpg', '.txt'))
    

    shutil.copyfile(og_txt_path, target_txt_path)


print("Done! ")