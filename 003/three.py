# -*- coding: utf-8 -*-

"""
将 0001 题生成的 200 个激活码（或者优惠券）保存到 Redis 非关系型数据库中
Insert all the activation/coupon code created by 001 into Redis
"""
import redis
import json
from collections import OrderedDict


class CodeToRedis(object):

	"""
	initialize parameters
	@param host: redis host
	@param port: port number
	@param db: db name default is db0
	"""
	def __init__(self, host="localhost", port=6379, db=0):
		self._redis = redis.StrictRedis(host=host, port=port, db=db)
		self._code_dict = OrderedDict()

	"""
	read activation/coupon code from the file created by 001, and set them into a dict
	@param org_file: the file that contains activation/coupon code
	@param delimiter: default is a whitespace that separates id and code
	"""
	def read_code_from_file(self, org_file="code.txt", delimiter=" "):
		with open(org_file, "r") as f:
			for line in f:
				data = line.strip().split(delimiter)  # remove \n and split each line by space
				self._code_dict[str(data[0])] = data[1] # data[0]: id, data[1]: code

	"""
	write activation/coupon code into redis with key(id),value(code) each by each
	"""
	def write_code_to_redis(self):
		for key, value in self._code_dict.items():
			self._redis.set(key, value)

	"""
	write activation/coupon code into redis with json format(converted into string)
	@param key_name: the key that mapping to dumped json data
	"""
	def write_code_with_json(self, key_name="activation_code"):
		if self._code_dict:
			self._redis.set(key_name, json.dumps(self._code_dict))

	"""
	get the stored json data(activation code) from redis
	@param key_name: the key that mapping to dumped json data
	@return: activation code in json format
	"""
	def get_code_with_json(self, key_name="activation_code"):
		need_json_load_values = self._redis.get(key_name)
		if need_json_load_values is None:
			return None
		return json.loads(need_json_load_values, object_pairs_hook=OrderedDict) # object_pairs_hook is to ensure the order


if __name__ == "__main__":
	import os
	os.system("clear")
	
	code_text_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "001/code.txt")
	code_to_redis = CodeToRedis()
	code_to_redis.read_code_from_file(code_text_path)
	code_to_redis.write_code_with_json()
	for key,value in code_to_redis.get_code_with_json().items():
		print "{key}=>{value}".format(key=key, value=value)


