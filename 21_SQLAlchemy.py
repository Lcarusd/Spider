# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Address(Base):
	"""电子邮件表"""
	__tablename__ = 'addresses'

	id = Column(Integer, primary_key=True)
	email_address = Column(String(30), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", back_populates="addresses")

	def __repr__(self):
		return "<Address(email_address='{}')>".format(self.email_address)


# class User(Base):
# 	 """用户表"""
# 	__tablename__ = 'users'
	
#     id = Column(Integer, primary_key=True)
#     name = Column(String(10))
#     fullname = Column(String(20))
#     password = Column(String(20))
#     addresses = relationship("Address", order_by=Address.id, back_populates="user")
    
#     def __repr__(self):
#         return "<User(name='{}', fullname='{}', password='{}')>".format(
#             self.name, self.fullname, self.password)

from sqlalchemy import create_engine
# 下面是MySQLdb/MySQL-Python默认写法
# engine = create_engine('mysql://root:mysql@127.0.0.1:3306/test', echo=True)
# 这里我使用的是PyMySQL
# echo=True是开启调试，这样当我们执行文件的时候会提示相应的文字
engine = create_engine('mysql+pymysql://root:mysql@127.0.0.1:3306/test', echo=True)

