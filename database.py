from app import mysql,session
from Blockchain import Block,Blockchain
class InvalidTransactionException(Exception): pass
class InsufficientFundsException(Exception): pass

class table:
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column
            cur = mysql.connection.cursor() #create the table
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.close()


    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" % self.table)
        data = cur.fetchall()
        return data

    def getone(self, search, value):
        data = {}
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" % (self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close()
        return data

    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" % (self.table, search, value))
        mysql.connection.commit()
        cur.close()

    def deleteall(self):
        self.drop()  # remove table and recreate
        self.__init__(self.table, *self.columnsList)

    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()

    def insert(self, *args):
        data = ""
        for arg in args:  # convert data into string mysql format
            data += "\"%s\"," % (arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" % (self.table, self.columns, data[:len(data) - 1]))
        mysql.connection.commit()
        cur.close()

def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

def isnewtable(name_table):
    cur = mysql.connection.cursor()

    try:
        result = cur.execute("SELECT * from %s" %name_table)
        cur.close()
    except:
        return True
    else:
        return False

def isnewuser(username):
    users = table("users", "name", "email", "username", "password")
    data = users.getall()
    print(data,"\n")
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True

def data_blockchain():
    blockchain = Blockchain()
    blockchain_table = table("blockchain", "number", "hash", "previous", "data","time", "nonce")
    for b in blockchain_table.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), b.get('time'),int(b.get('nonce'))))

    return blockchain
def update_blockchain(blockchain):
    blockchain_data = table("blockchain", "number", "hash", "previous", "data","time", "nonce")
    block=blockchain.chain[-1]
    blockchain_data.insert(str(block.number), block.hash(), block.previous_hash, block.data,block.time, block.nonce)

def check_chain():
    blockchain = Blockchain()
    database = ["hello", " here"]

    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(number=num, data=data))
    update_blockchain(blockchain)

def send_money(sender, recipient, amount):

    #verify that the amount is an integer or floating value
    try: amount = float(amount)
    except ValueError:
        raise InvalidTransactionException("Invalid Transaction.")

    if amount > get_balance(sender) and sender != "ROOT":
        raise InsufficientFundsException("Insufficient Funds.")

    elif sender == recipient or amount <= 0.00:
        raise InvalidTransactionException("Invalid Transaction.")

    elif isnewuser(recipient):
        raise InvalidTransactionException("User Does Not Exist.")
    blockchain = data_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s-->%s-->%s" %(sender, recipient, amount)
    blockchain.mine(Block(number, data=data))
    update_blockchain(blockchain)

#get the balance of a user
def get_balance(username):
    balance = 0.00
    blockchain = data_blockchain()

    #loop through the blockchain and update balance
    for block in blockchain.chain:
        data = block.data.split("-->")
        if username == data[0]:
            balance -= float(data[2])
        elif username == data[1]:
            balance += float(data[2])
    return balance

def get_transactions(username):

    blockchain = data_blockchain()
    transactions=[]
    for block in blockchain.chain:
        if(len(transactions)==15):
            break
        data = block.data.split("-->")
        timestamp=block.time
        data.append(timestamp)
        if username == data[0] or username == data[1]:
            transactions.append(data)
    Formatted_transactions=[]
    for data in transactions:
        check = data
        if check[0]==username:
            Formatted_transactions.append("You Paid %s %s Commoncoins on %s" %(check[1], check[2],check[3]))
        elif check[1]==username:
            Formatted_transactions.append("You Received %s Commoncoins from %s on %s" %(check[2], check[0],check[3]))
    if len(Formatted_transactions)==0:
        Formatted_transactions.append("Empty")

    return Formatted_transactions