
from flask import Flask, redirect, render_template, request, session, url_for
from google.cloud import datastore
from google.cloud.datastore import query
from google.cloud.datastore.query import PropertyFilter

datastore_client = datastore.Client()

#went with an object for the users. This will probably be obselete once i hook up datastore
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
    def getID(self):
        return self.id

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def setPassword(self, password):
        self.password = password 
    
    def setUsername(self, username):
        self.username = username


def validateLogin(id,password):
    query = datastore_client.query(kind="user")
    query.add_filter(filter = PropertyFilter("id", "=", id))
    query.add_filter(filter = PropertyFilter("password", "=", password))
    
    return list(query.fetch())

def setUser(id,password):
    query = datastore_client.query(kind="user")
    query.add_filter(filter = PropertyFilter("id", "=", id))
    query.add_filter(filter = PropertyFilter("password", "=", password))
    
    for entity in query.fetch():
        
        user = User(entity["id"],entity["user_name"],entity["password"])
        
        return user
    

def checkId(id):
    query = datastore_client.query(kind="user")
    query.add_filter(filter = PropertyFilter("id", "=", id))

    return list(query.fetch())

def checkUname(username):
    query = datastore_client.query(kind="user")
    query.add_filter(filter = PropertyFilter("user_name", "=", username))

    return list(query.fetch())


        
'''
#dummy List of users This is based off the requirements for part 1.
userList = []

def populateList():
    
    value = 0

    numbers = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4]

    #playing with a while loop to make adding users easier
    while value < 10:
        id = "s2008156" + str(value)
        username = "phibui" + str(value)
        password = str(numbers[0+value]) + str(numbers[1+value]) + str(numbers[2+value]) + str(numbers[3+value]) + str(numbers[4+value]) + str(numbers[5+value]) 
        userList.append (User(id, username, password))
        value += 1
        
#function call to create the list. Python works from top down like html.     
populateList() 
'''

app = Flask(__name__)
app.secret_key = "helloworld"

#this routes the pages as per tutorial 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        
        #take the user input id and password from the html form and store it for validation
        login_id = request.form.get("loginid")
        login_pw = request.form.get("loginpw")
        
        results = validateLogin(login_id, login_pw)
        
        if len(results) > 0:
            
            user = setUser(login_id,login_pw)
            session["user"] = user.getUsername()
            
            return render_template("forumMain.html", name = session["user"])
        else:
            
            return render_template("index.html", error_message = "incorrect id or password")
    else:         
        return render_template("index.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        
        regoId = request.form.get("regId")
        regoUname = request.form.get("regUsername")
        regoPword = request.form.get("regPword")

        if (len(checkId(regoId)) > 0):
            
            return render_template("registration.html", error_id = "The ID already exists")
        
        elif (len(checkUname(regoUname)) > 0):
                
            return render_template("registration.html", error_username = "The username already exists")
            
        else:
        
            return redirect(url_for('index'))
        
        '''
        for user in userList:
            
            if regoId == user.getID():
                 
                return render_template("registration.html", error_id = "The ID already exists")
            
            elif regoUname == user.getUsername():
                
                return render_template("registration.html", error_username = "The username already exists")
            
            else:
                
                #add code to add new user!
                
                return redirect(url_for('index'))
        '''
    else:
        return render_template("registration.html")
     

@app.route("/userAdmin", methods=['GET', 'POST'])
def userAdmin():
    
    if "user" in session:
        
        if request.method == 'POST':
            
            oldPword = request.form.get("oldPword")
            newPword = request.form.get("newPword")
            
            for user in userList:
                
                if session["user"] == user.getUsername() and oldPword == user.getPassword():
                    
                    print("pass")
                    return redirect(url_for('index'))
                
                else:
                    
                    return render_template("userAdmin.html", name = session["user"], error_oldPword = "incorrect password")
        
        else:
        
            return render_template("userAdmin.html", name = session["user"])
    
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    

  
    
