
import datetime
from flask import Flask, redirect, render_template, request, session, url_for
from google.cloud import datastore, storage
#from google.cloud.datastore import query
from google.cloud.datastore.query import PropertyFilter


datastore_client = datastore.Client()
storage_client = storage.Client()

bucket_name = "s2008156-cca1"
bucket = storage_client.bucket(bucket_name)
bucketProfilePath = "https://storage.cloud.google.com/s2008156-cca1/profile"
bucketPostPath = "https://storage.cloud.google.com/s2008156-cca1/"
filepath = "D:/Bachelor of IT - OUA/9. Cloud Computing/A1/s2008156_A1/static/images/"

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
        
class Post:
    def __init__ (self, user, timestamp, subject, message):
        self.user = user
        self.timestamp = timestamp
        self.subject = subject
        self.message = message

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

def updatePassword(username, newPword):
    
    with datastore_client.transaction():
        
        query = datastore_client.query(kind="user")
        query.add_filter(filter = PropertyFilter("user_name", "=", username))
        
        for entity in query.fetch():
            
            user = datastore_client.get(entity.key)
            user["password"] = newPword
            datastore_client.put(user)      

def addUser(id, username, password):
    
    entity = datastore.Entity(key=datastore_client.key("user"))
    entity.update({"id": id, "user_name": username, "password": password})
    datastore_client.put(entity)

def getIDfromName(user):
    query = datastore_client.query(kind="user")
    query.add_filter(filter = PropertyFilter("user_name", "=", user))

    for entity in query.fetch():
        
        return entity["id"]


def addForumPost(subject, message, file):
    
    imageSrc = getProfileImgSrc(session['user'])
    
    if file == "NA":
        postImage = "NA"
    else:
        uploadImg("post", "NA", file)
        postImage = bucketPostPath + file.filename
        
    entity = datastore.Entity(key=datastore_client.key("post"), exclude_from_indexes=("subject", "message"))
    entity.update({"user": session["user"], "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")  ,"subject": subject, "message": message, "profileImg": imageSrc, "postImg": postImage} )
    datastore_client.put(entity)

def getPosts(number):
    query = datastore_client.query(kind="post")
    query.order = ["-timestamp"]
    
    times = query.fetch(limit=number)
    return times

def getPostsByUser(user):
    query = datastore_client.query(kind="post")
    query.add_filter(filter = PropertyFilter("user", "=", user))
    
    tempList = list(query.fetch())
    
    #https://note.nkmk.me/en/python-dict-list-sort/ 
    time = sorted(tempList, key = lambda x: x['timestamp'], reverse=True)
    
    return time

def uploadImg(type, regoId, file):
    
    if type == "profile":
        
        imageName = "profile" + regoId
     
    else:
        
        imageName = file.filename
    
    blob = bucket.blob(imageName)
    blob.upload_from_file(file)

def getProfileImgSrc(user):
    
    return bucketProfilePath + getIDfromName(user)

def editForumPost(postNumber, subject, message, postOldImg, postNewImg):
    
    postImage=""
    
    if postNewImg == "NA":
        
        postImage = "NA"
        
        if postOldImg[0:5] == "https":
        
            postImage = postOldImg
        
    else:

        uploadImg("post", "NA", postNewImg)
        postImage = bucketPostPath + postNewImg.filename
        print(postImage)
  
    postList = getPostsByUser(session['user'])  
    entity = postList[int(postNumber)-1]
    key = entity.key
    user = datastore_client.get(key)
    user["subject"] = subject
    user["message"] = message
    user["timestamp"] = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    user["postImg"] = postImage
    datastore_client.put(user)
    
    print(user)
    print("successfully updated Post")



#FLASK RELATED

app = Flask(__name__)
app.secret_key = "helloworld"
app.config['UPLOAD_FOLDER'] = "/static/img"

#this routes the pages as per tutorial 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if "user" in session:
            
            print(session["user"])
            return redirect(url_for('forumMain'))
            #return redirect(url_for('forumMain'))
        
        else:
        
            #take the user input id and password from the html form and store it for validation
            login_id = request.form.get("loginid")
            login_pw = request.form.get("loginpw")
            
            results = validateLogin(login_id, login_pw)
            
            if len(results) > 0:
                
                print("valid login credentials")
                user = setUser(login_id,login_pw)
                session["user"] = user.getUsername()
                
                return redirect(url_for('forumMain'))
                
            else:
                
                print("invalid login credentials")
                return render_template("index.html", error_message = "incorrect id or password")
    else:        

        session.clear()
        return render_template("index.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    
    if request.method == 'POST':      
        
        regoId = request.form.get("regId")
        regoUname = request.form.get("regUsername")
        regoPword = request.form.get("regPword")
        file = request.files["filename"]

        if (len(checkId(regoId)) > 0):
            
            return render_template("registration.html", error_message = "The ID already exists")
        
        elif (len(checkUname(regoUname)) > 0):
                
            return render_template("registration.html", error_message = "The username already exists")
            
        else:
             
            uploadImg("profile", regoId, file)
            addUser(regoId, regoUname, regoPword)
            session.clear()
            return redirect(url_for('index'))
    
    else:
           
        return render_template("registration.html") 
 

@app.route("/userAdmin", methods=['GET', 'POST'])
def userAdmin():
    
    times = getPostsByUser(session["user"])
    
    imageSrc = getProfileImgSrc(session["user"])
    
    if "user" in session:
        
        if request.method == 'POST':
            
            selection = request.form.get("postID")
            
            if selection == "0":
                
                print("got this far")
                oldPword = request.form.get("oldPword")
                newPword = request.form.get("newPword")
                
                tempList = checkUname(session["user"])
                
                for item in tempList:
                    if item["password"] == oldPword:
                        
                        
                        updatePassword(session["user"], newPword)  
                        session.clear()
                        return redirect(url_for('index'))
                    
                    else:
                        
                        print("old password mismatch")
                        return render_template("userAdmin.html", name = session["user"], error_message = "incorrect password", times = times, imageSrc = imageSrc)  
            
            elif selection =="1":
                
                postNumber = request.form.get("postID")
                subject = request.form.get("postSubject")
                message = request.form.get("editPostMessage")
                postOldImg = request.form.get("postImgSrc")
                postNewImg = request.files["filename"]

                try:
                    
                    editForumPost(postNumber, subject, message, postOldImg, postNewImg)
                    
                except:

                    editForumPost(postNumber, subject, message, postOldImg, "NA")
                
                return redirect(url_for('forumMain')) 
               
        elif request.method == 'GET':
            
            print("GET")
            postID = request.form.get("postID")
            print(postID)
            
            
            return render_template("userAdmin.html", name = session["user"], times = times, imageSrc = imageSrc)
    
    else:
        
        return redirect(url_for('index'))
    
    
@app.route("/forumMain", methods=['GET', 'POST'])
def forumMain():
    
    imageSrc = getProfileImgSrc(session["user"])
    
    times = getPosts(10)
    
    if request.method == 'POST':
        
        subject = request.form.get("newSubject")
        message = request.form.get("newMessage")
        file = request.files["filename"]

        try: 
            
            addForumPost(subject, message, file)
            
        except:

            addForumPost(subject, message, "NA")
            
    return render_template("forumMain.html", name = session["user"], times = times, imageSrc = imageSrc)
        
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    

  
    
