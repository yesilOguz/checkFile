import sqlite3
import random
import string

class databases:
    connMd5 = None
    cursorMd5 = None

    connAuthTokens = None
    cursorAuthTokens = None

    connUser = None
    cursorUser = None
    
    def __init__(self):
        self.connMd5 = sqlite3.connect('md5Database.db')
        self.cursorMd5 = self.connMd5.cursor()

        self.connAuthTokens = sqlite3.connect("userTokens.db")
        self.cursorAuthTokens = self.connAuthTokens.cursor()

        self.connUser = sqlite3.connect("user.db")
        self.cursorUser = self.connUser.cursor()

        self.cursorAuthTokens.execute('''
            CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY,
            userId INTEGER NOT NULL,
            token TEXT NOT NULL
            )
        ''')

        self.cursorUser.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username INTEGER NOT NULL,
            password TEXT NOT NULL
            )
        ''')

        self.connAuthTokens.commit()
        self.connUser.commit()

    def checkUser(self, username, password):
        self.cursorUser.execute("SELECT * FROM users WHERE username = '"
                                + username + "' AND password = '" + password + "'")

        fetchedUser = self.cursorUser.fetchone()

        if(fetchedUser == None):
            return False

        return fetchedUser
    
    def checkToken(self, token):
        self.cursorAuthTokens.execute("SELECT COUNT(*) FROM tokens WHERE token = '" + token + "'")

        countToken = self.cursorAuthTokens.fetchone()[0]
        
        if(countToken > 0):
            return True

        return False

    def createUser(self, username, password):
        self.cursorUser.execute("SELECT COUNT(*) FROM users WHERE username='" + username + "'")
        usernameCount = self.cursorUser.fetchone()[0]

        if(usernameCount > 0):
            return False
        
        self.cursorUser.execute("SELECT COUNT(*) FROM users")

        userCount = self.cursorUser.fetchone()[0]

        data_to_insert = (userCount+1, username, password)        
        self.cursorUser.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", data_to_insert)

        self.connUser.commit()
        
        return True

    def createToken(self, userId):
        characters = string.ascii_letters + string.digits

        def generate_token():
            token = ''
            for _ in range(16):
                token += random.choice(characters)
            return token

        token = generate_token()

        while self.checkToken(token):
            token = generate_token()

        self.cursorAuthTokens.execute("SELECT COUNT(*) FROM tokens")

        tokenCount = self.cursorAuthTokens.fetchone()[0]

        data_to_insert = (tokenCount+1, userId, token)        
        self.cursorAuthTokens.execute("INSERT INTO tokens (id, userId, token) VALUES (?, ?, ?)", data_to_insert)

        self.connAuthTokens.commit()
        
        return token

    def getToken(self, username, password):
        fetchedUser = self.checkUser(username, password)

        if not fetchedUser:
            return False

        userId = fetchedUser[0]
        
        self.cursorAuthTokens.execute("SELECT * FROM tokens WHERE userId = '" + str(userId) + "'")

        fetchedAuthToken = self.cursorAuthTokens.fetchone()

        if(fetchedAuthToken == None): 
            return self.createToken(userId)

        token = fetchedAuthToken[2]

        return token

    def checkMd5(self, token, md5):
        if not self.checkToken(token):
            return token

        self.cursorMd5.execute("SELECT COUNT(*) FROM md5 WHERE key = '" + md5 + "'")
        countKey = self.cursorMd5.fetchone()[0]

        if(countKey > 0):
            return True
        else:
            return False
    
