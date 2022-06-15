class Database:
    def __init__(self):
        self.contents = {'users': []}  # dict

    def add_usr(self,usr ):
        self.contents['users'].append(usr)

    def get_usr(self,username):
        for user in self.contents['users']:
            if user['name'] == username:
                return user
        return None

def new_user(username, password):
    if username and password:
        return {'name': username, 'password': password}
    else:
        return None

