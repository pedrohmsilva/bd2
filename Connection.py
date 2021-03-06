import cx_Oracle
from flask import jsonify
import sys
import auth

class Connection:

	username = auth.username
	password = auth.password
	host = auth.host
	port = auth.port

	connection = None
	cursor = None

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
			columns = [i[0] for i in self.cursor.description]
			result = {
				"success": True,
				"data": data,
				"columns": columns
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