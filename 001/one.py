# -*- coding: utf-8 -*-

"""
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）
To create 200 activation code/ coupon code with python
"""
import string
import random
from collections import OrderedDict


class ActivationCode(object):
    """
    initialize parameters
    :param length: the length of the activation code
    :param flag_code: is the flag code mixed in activation code
    """

    def __init__(self, length=10, flag_code="L"):
        self._length = length
        self._flag_code = flag_code
        self._letters_and_numbers = string.ascii_letters + string.digits
        self._code_dict = OrderedDict()  # To make sure the code is ordered as created in the dict

    """
    get flag code
    :return the flag code
    """

    @property
    def flag_code(self):
        return self._flag_code

    """
    set flag code
    :param flag_code: the flag code
    """

    @flag_code.setter
    def flag_code(self, flag_code):
        self._flag_code = flag_code

    """
    create activation code
    :param id: the id of activation code retrieved from database
    :param length: the length of activation code, default 10
    :param flag_code: the flag code
    :return: one activation code
    """

    def create_code(self, id, length=None, flag_code=None):
        self._flag_code = flag_code if flag_code else self._flag_code
        self._length = length if length else self._length
        prefix = hex(int(id))[2:] + self._flag_code
        suffix_length = self._length - len(prefix)
        new_code = prefix + ''.join([random.choice(self._letters_and_numbers) for i in range(suffix_length)])
        self._code_dict[str(id)] = new_code
        return new_code

    """
    get the id from activation code
    :param code: the activation code
    :return: the real id
    """

    def get_id(self, code):
        try:
            hex_id = code.split(self._flag_code)[0]
            real_id = int(hex_id, 16)
        except ValueError:
            raise ValueError("Wrong activation code, please try again!")
        return real_id

    """
    write all the activation code to file
    @param dest_file: the file name
    """

    def write_code_to_txt(self, dest_file="code.txt"):
        with open(dest_file, "w") as f:
            f.write("\n".join([key + " " + value for key, value in self._code_dict.items()]))


if __name__ == '__main__':
    activation_code = ActivationCode()
    for i in range(10, 3010, 15):
        code = activation_code.create_code(i)
        id = activation_code.get_id(code)
        print "{id}=>{code}".format(id=id, code=code)
    activation_code.write_code_to_txt()

