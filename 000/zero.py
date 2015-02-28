# -*- coding: utf-8 -*-

"""
将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。

To add red color text to the right-top of a image
"""

import os, sys
from PIL import Image, ImageDraw, ImageFont

class DrawText(object):

	def __init__(self, path=None, font_size=100):
		self._path = path
		self._font_size = font_size
		self._img = None
		self._font = None
		self._current_path = os.path.dirname(os.path.abspath(__file__))

	def open(self, path):
		if os.path.exists(path):
			self._path = path
			self._img = Image.open(self._path)
			width, height = self._img.size
			self._font_size = width / 4
		return self

	def load_font(self, font_file=None, font_size=None):
		if font_size:
			self._font_size = font_size

		self._font = ImageFont.truetype(font_file, self._font_size)
		return self

	def draw_img(self, text="4", size=(0,0), full_opacity=False):
		fill = (255,255,255) if full_opacity else (255,0,0)
		text = "99+" if int(text) > 99 else text if text.isdigit() else "4"
		draw = ImageDraw.Draw(self._img)
		draw.text(size, text, fill, font=self._font)
		return self

	def save(self, des_path=None, file_name="out", file_type="jpg"):
		des_path = des_path if des_path and os.path.exists(des_path) else self._current_path 
		self._img.save(des_path+"/"+file_name+"."+file_type)


if __name__ == '__main__':
	argvs = sys.argv
	try:
		dt = DrawText()
		dt.open("avatar.jpg")
		dt.load_font("Vera.ttf", 50)
		width, height = dt._img.size
		print width
		dt.draw_img(size=(width-100,0), text="100")
		dt.save(file_name=argvs[1])
	except Exception as e:
		print e


		
