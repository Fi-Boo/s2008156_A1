from flask import Flask, redirect, render_template, request, session, url_for

#dummy data generation. This will be replaced with G-datastore stuff once I flesh out the rest of my code.

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


app = Flask(__name__)
app.secret_key = "helloworld"

#this routes the pages as per tutorial 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        
        #take the user input id and password from the html form and store it for validation
        login_id = request.form.get("loginid")
        login_pw = request.form.get("loginpw")
        
        #use of for loop to go through the userList to validate user input values
        for user in userList:
            
            if login_id == user.getID() and login_pw == user.getPassword():
                
                session["user"] = user.getUsername()
                #if valid user inputs load up forumMain page otherwise just display error msg
                return render_template("forumMain.html", name = user.getUsername())
                
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
        
        for user in userList:
            
            if regoId == user.getID():
                 
                return render_template("registration.html", error_id = "The ID already exists")
            
            elif regoUname == user.getUsername():
                
                return render_template("registration.html", error_username = "The username already exists")
            
            else:
                
                #add code to add new user!
                
                return redirect(url_for('index'))
            
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
    

  
    
