import cx_Oracle
from flask import jsonify
import sys

class Connection:

	username = ""
	password = ""
	host = ""
	port = ""

	connection = None;
	cursor = None;

	def connect(self):
		self.connection = cx_Oracle.connect(self.username + "/" + self.password + "@//" + self.host + ":" + self.port, encoding='UTF-8')
		self.cursor = self.connection.cursor()

	def close(self):
		self.cursor.close()
		self.connection.close()

	def update(self, command):
		self.connect()
		try:
			self.cursor.execute(command)
			self.connection.commit()
			result = {"success": True}
			self.close()
			return result
		except cx_Oracle.DatabaseError as e:
			result = {
				"success": False,
				"message": str(e)
			}
			self.close()
			return result

	def query(self, command):
		self.connect()
		try:
			self.cursor.execute(command)
			data = self.cursor.fetchall()
			result = {
				"success": True,
				"data": data
			}
			self.close()
			return result
		except cx_Oracle.DatabaseError as e:
			result = {
				"success": False,
				"message": str(e)
			}
			self.close()
			return result