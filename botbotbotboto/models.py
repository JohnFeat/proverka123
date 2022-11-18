from peewee import *

db = SqliteDatabase('data.db')
 
 
class User(Model):
	class Meta:
		database = db
		db_table = "Users"
	vk_id = IntegerField()
	vigs = IntegerField()
	pred = IntegerField()
	nickname = IntegerField()
	adminstatus = IntegerField()
	org = IntegerField()
	warns = IntegerField()
	discord = IntegerField()
	forumnik = IntegerField()
	data = IntegerField()
	lgoti = IntegerField()
	lvladmin = IntegerField()



 

class Chat(Model):
	class Meta:
		database = db
		db_table = "ChatIDs"
	chatiki = IntegerField()
	

if __name__ == '__main__':
	db.create_tables([User])
	db.create_tables([Chat])