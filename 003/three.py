# -*- coding: utf-8 -*-

"""
将 0001 题生成的 200 个激活码（或者优惠券）保存到 Redis 非关系型数据库中
Insert all the activation/coupon code created by 001 into Redis
"""
import redis

redis = redis.StrictRedis(host="localhost", port=6379)

def write_code_to_redis(org_file="code.txt"):
	with open(org_file, "r") as f:
			for line in f:
				data = line.strip().split(" ") # remove \n and split each line by space
				id, code = data[0], data[1]
				redis.set(str(id), code)

if __name__ == "__main__":
	write_code_to_redis("../001/code.txt")


