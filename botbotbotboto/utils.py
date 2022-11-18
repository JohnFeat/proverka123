from models import User, Chat

chat_ids = []
def get_user_by_id(user_id):
	try:
		return User().get(vk_id=user_id)
	except:
		User(
			vk_id=user_id,
			warns=0,
			nickname = 'none',
			adminstatus = 'none',
			org = 'none',
			pred = 0,
			vigs = 0,
			forumnik = 'N\A',
			discord = 'N\A',
			data = 'N\A',
			lgoti = 0,
			lvladmin = 0,
			).save()
		return User().get(vk_id=user_id)
  
def get_chat_by_id(chat_id):
	try:
		chatiki = chat_id
		for i in range(max(id)):
			
			chat_ids.append(chatiki)

		return Chat().get(chatiki=chat_id)
	except: 
		Chat(
			chatiki=chat_id,
			chat_ids = [],
			).save()	 
		return Chat().get(chatiki=chat_id)

