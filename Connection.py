import cx_Oracle

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
			return {"success": True}
		except cx_Oracle.DatabaseError as e:
			result = {
				"success": False,
				"message": str(e)
			}
			self.close()
			return result

	def query(self, command):
		self.connect()
		self.cursor.execute(command)
		result = self.cursor.fetchall()
		self.close()
		return result