# -*- coding: utf-8 -*-

"""
使用 Python 生成字母验证码图片
generate captcha with python
"""

import string
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter

MAX_LEN_LETTER_OF_CAPTCHA = 4

class CaptchaGenerator(object):

    """
    initialize parameters
    """
    def __init__(self):
        self._letters = string.uppercase + string.digits
        self._img = None
        self._draw = None

    """
    generate random letters
    @param letter_len: the len of letters, maximum is 4
    @return a string that contains all the letters splitted by whitespace
    """
    def generate_random_letter(self, letter_len):
        letter_len = letter_len if letter_len and letter_len <= MAX_LEN_LETTER_OF_CAPTCHA else MAX_LEN_LETTER_OF_CAPTCHA
        return '  '.join(random.sample(self._letters, letter_len))

    """
    draw lines over the image
    @param width: the width of the image
    @param height: the height of the image
    @param line_number: how many lines will be draw over the image
    """
    def draw_lines(self, width, height, line_number):
        for _ in range(line_number):
            line_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            begin_point = (random.randint(0, width), random.randint(0, height))
            end_point = (random.randint(0, width), random.randint(0, height))
            self._draw.line([begin_point, end_point], fill=line_color)

    """
    draw points over the image
    @param width: the width of the image
    @param height: the height of the image
    """
    def draw_points(self, width, height):
        point_chance = random.randint(0, 100)
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > point_chance:
                    point_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    self._draw.point((w, h), fill=point_color)

    """
    draw text over the image
    @param text: the text that will be draw over the image
    @param font: the font of the text
    @param font_width: the width of the font
    @param font_height: the height of the font
    @param width: the width of the image
    @param height: the height of the image
    @param fore_color: the foreground color
    """
    def draw_text(self, letters, font, font_width, font_height, width, height, fore_color):
        self._draw.text(((width - font_width) / 3, (height - font_height) / 3), letters , font=font, fill=fore_color)

    """
    generate a captcha
    @param letters: the letters that will be draw over the image
    @param img_type: the image format, default is JPEG
    @param mode: the mode to use for the image
    @param back_color: the background color of the image
    @param fore_color: the foreground color
    @param font_size: the size of the font
    @param font_type: the type to use for the font
    @param letter_len: the length of letters
    @param line_number: how many lines will be draw over the image
    @param dst_img: the destination image
    @param draw_lines: True: draw lines over the image, False: otherwise
    @param draw_points: True: draw points over the image, False: otherwise
    """
    def generate_captcha(self, letters=None,
                                img_type="JPEG",
                                mode="RGB",
                                back_color=(255,255,255),
                                fore_color=(0,0,255),
                                font_size=25,
                                font_type="Vera.ttf",
                                letter_len=4,
                                line_number=50,
                                dst_img="captcha.jpg",
                                draw_lines=True,
                                draw_points=True):

        letters = letters if letters else self.generate_random_letter(letter_len)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(letters)
        width, height = int(font_width * 1.2), int(font_height * 1.2)
        self._img = Image.new(mode, (width, height), back_color)
        self._draw = ImageDraw.Draw(self._img)

        if draw_lines:
            self.draw_lines(width, height, line_number)

        if draw_points:
            self.draw_points(width, height)

        self.draw_text(letters, font, font_width, font_height, width, height, fore_color)

        self._img.save(dst_img, img_type)


if __name__ == "__main__":
    captcha_generator = CaptchaGenerator()
    captcha_generator.generate_captcha()


