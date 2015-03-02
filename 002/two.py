import datetime
from collections import OrderedDict
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:admin@localhost/activation_code?charset=utf8")
Base = declarative_base(engine)

class ActivationCode(Base):
	__tablename__ = "activation_code"

	id = Column(Integer, primary_key=True)
	code = Column(String(20), nullable=False)
	created_date = Column(Date, default=datetime.datetime.utcnow())


class CodeToMySQL(object):

	"""
	initialize parameters
	"""
	def __init__(self):
		self._session = self.create_session()
		self._code_dict = OrderedDict()

	"""
	read activation/coupon code from the file created by 001, and set them into a dict or return them
	@param org_file: the file that contains activation/coupon code
	@param delimiter: default is a whitespace that separates id and code
	@param returned: True: return the dictionary that contains all the code, otherwise
	"""
	def read_code_from_file(self, org_file="code.txt", delimiter=" ", returned=False):
		with open(org_file, "r") as f:
			for line in f:
				data = line.strip().split(delimiter)  # remove \n and split each line by space
				self._code_dict[str(data[0])] = data[1] # data[0]: id, data[1]: code

		if returned:
			return self._code_dict

	"""
	create sqlalchemy session
	@return: sqlalchemy session instance
	"""
	def create_session(self):
		session_factory = sessionmaker(bind=engine)
		session = scoped_session(session_factory)
		return session()

	"""
	insert one activation/coupon code into mysql
	@param id: id value
	@param code: the activation/coupon code
	"""
	def add_code(self, id, code):
		activation_code = ActivationCode(id=id, code=code)
		self._session.add(activation_code)
		self._session.commit()

	"""
	insert all code into mysql
	"""
	def add_all_code(self):
		for id, code in self._code_dict.items():
			activation_code = ActivationCode(id=id, code=code)
			self._session.add(activation_code)
			self._session.commit()


if __name__ == "__main__":
	import os
	os.system("clear")
	
	code_text_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "001/code.txt")

	code_to_mysql = CodeToMySQL()
	code_to_mysql.read_code_from_file(code_text_path)
	code_to_mysql.add_all_code()