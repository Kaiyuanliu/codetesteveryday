# -*- coding: utf-8 -*-

"""
copy and pasty 005, just need to modify the constants, the code is reuseable
"""
import os
from PIL import Image

IPHONE_IMAGE_WIDTH = 1334  # iPhone6 width
IPHONE_IMAGE_HEIGHT = 750  # iPhone6 height
IMAGES_TYPE = ['*.jpg', '*.jpeg', '*png', '*.tif', '*.tiff']  # image type allowed


class ResizeImage(object):

    def __init__(self, org_image=None):
        """
        initialize parameters
        @param org_image: orginal image path
        """
        self._org_image = org_image
        self._img = None

    def open(self, org_image):
        """
        open image using PIL
        @param org_image: orginal image path
        @return: self for chain purpose
        """
        if os.path.exists(org_image):
            self._org_image = org_image
            self._img = Image.open(self._org_image)
        return self

    def resize_image(self, dst_image=None,
                     dst_width=IPHONE_IMAGE_WIDTH,
                     dst_height=IPHONE_IMAGE_HEIGHT,
                     quality=75):
        """
        resize image
        @param dst_image: the destination image path
        @param dst_width: the destination image width default is iPhone6 screen width
        @param dst_height: the destination image height default is iPhone6 screen height
        @param quality: the destination image quality after resizing, default is 75
        @return: resized image
        """
        org_image_name,  org_image_type = os.path.splitext(self._org_image)
        org_width, org_height = self._img.size
        width_ratio = None
        height_ratio = None
        ratio = 1

        if (org_width and org_width > dst_width) or (org_height and org_height > dst_height):
            if org_width > dst_width:
                width_ratio = float(dst_width) / org_width

            if org_height > dst_height:
                height_ratio = float(dst_height) / org_height

            if None not in (width_ratio, height_ratio):
                ratio = width_ratio if width_ratio < height_ratio else height_ratio
            else:
                temp_ratio = [x for x in (width_ratio, height_ratio) if x is not None]
                ratio = temp_ratio[0] if temp_ratio else ratio

        if ratio != 1:
            extra_text = dst_image if dst_image else 'resized'
            dst_image = org_image_name+"_"+extra_text+org_image_type
            return self._img.resize(
                (int(org_width*ratio), int(org_height*ratio)),
                Image.ANTIALIAS).save(dst_image, quality=quality)
        self._img = None
        self._org_image = None

    def resize_all_images(self,
                          method="glob",
                          path=os.getcwd(),
                          dst_image="iPhone6_resized",
                          dst_width=IPHONE_IMAGE_WIDTH,
                          dst_height=IPHONE_IMAGE_HEIGHT):
        """
        invoke resizing function according to the method
        @param method: which method is used to resize images, default is glob
        @param path: the path of directory, default is the current directory
        @param dst_image: the destination image path
        @param dst_width: the destination image width default is iPhone6 screen width
        @param dst_height: the destination image height default is iPhone6 screen height
        @param
        """
        result = getattr(self, "_resize_all_images_by_"+method, None)
        if result is not None:
            result(path, dst_image, dst_width, dst_height)

    def _resize_all_images_by_glob(self, path, dst_image, dst_width, dst_height):
        """
        resize all the images from some directory by using glob method
        @param path: the path of directory, default is the current directory
        @param dst_image: the destination image path
        @param dst_width: the destination image width
        @param dst_height: the destination image height
        """
        import glob
        images_list = [image for image_type in IMAGES_TYPE
                       for image in glob.glob(os.path.abspath(os.path.join(path, image_type)))]
        for one_image in images_list:
            self.open(one_image).resize_image(dst_image=dst_image, dst_width=dst_width, dst_height=dst_height)

    def _resize_all_images_by_oswalk(self, path, dst_image, dst_width, dst_height):
        """
        resize all the images from some directory by using os.walk and fnmatch
        @param path: the path of directory, default is the current directory
        @param dst_image: the destination image path
        @param dst_width: the destination image width
        @param dst_height: the destination image height
        """
        import fnmatch
        images_list = [os.path.abspath(os.path.join(root, file_name).replace('\\', '/'))
                       for root, subdir, filenames in os.walk(path)
                       for image_type in IMAGES_TYPE
                       for file_name in fnmatch.filter(filenames, image_type)]

        for one_image in images_list:
            self.open(one_image).resize_image(dst_image=dst_image, dst_width=dst_width, dst_height=dst_height)


if __name__ == "__main__":
    iPhone6_plus_resolution = (1920, 1080)
    resize_image = ResizeImage()
    resize_image.resize_all_images()  # resize to iphone6

    # resize to iphon6 plus
    resize_image.resize_all_images(
                                   dst_image="iPhone6_plus_resized",
                                   dst_width=iPhone6_plus_resolution[0],
                                   dst_height=iPhone6_plus_resolution[1])
