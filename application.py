import datetime
import os
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.web
from bson import ObjectId
from pymongo import MongoClient
import hashlib
from tornado.auth import OAuthMixin

### Generate Secure key
import secrets

cookie_secret = secrets.token_hex(32)
print(f'{cookie_secret=}')
########



## Connect to MongoDB

with open('creds.txt', 'r') as f:
    # Read Credentials
    username = f.readline().strip()
    password = f.readline().strip()
    database = f.readline().strip()
print(username, password, database)

# set the connection parameters
mongo_host = "192.168.44.132"
mongo_port = 27017
mongo_user = username
mongo_password = password
mongo_auth_source = "admin"

# create the MongoClient instance
client = MongoClient(mongo_host, mongo_port, username=mongo_user, password=mongo_password, authSource=mongo_auth_source)

# specify the database and collection you want to work with
db = client["papa"]
users_collection = db["users"]

# # find all documents in the collection
# cursor = users_collection.find({})
# for document in cursor:
#     print(document)
# posts_collection = db["posts"]
# comments_collection = db["comments"]

#################################################
# notifications_collection = db["notifications"]
class NotificationsHandler(tornado.web.RequestHandler):
    async def get(self):
        user_id = self.get_secure_cookie("user")
        notifications = await notifications_collection.find({"recipient_id": user_id}).to_list(length=100)
        self.render("notifications.html", notifications=notifications)


# Modify the ReplyHandler to create a notification for the post author
class ReplyHandler(tornado.web.RequestHandler):
    async def post(self, post_id):
        user_id = self.get_secure_cookie("user")
        content = self.get_argument("content")
        new_comment = {"user_id": user_id, "post_id": ObjectId(post_id), "content": content}
        await comments_collection.insert_one(new_comment)

        post = await posts_collection.find_one({"_id": ObjectId(post_id)})
        if post["user_id"] != user_id:
            new_notification = {
                "recipient_id": post["user_id"],
                "user_id": user_id,
                "post_id": ObjectId(post_id),
                "type": "reply"
            }
            await notifications_collection.insert_one(new_notification)

        self.redirect(f"/forum/{post_id}")

##################################################

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html")

    async def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        email = self.get_argument("email")

        # Check if the user already exists
        # existing_user = await users_collection.find_one({"username": username})
        existing_user = users_collection.find_one({"username": username})
        existing_gmail = users_collection.find_one({"email": email})
        if existing_user is not None:
            self.write("User already Exists. Please Try another username or login.")
        elif existing_gmail is not None:
            self.write("User with provided email already exists. Please logining in.")
        else:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            new_user = {"username": username, "password": hashed_password, "email": email}
            users_collection.insert_one(new_user)
            self.write("Account Created! Welcome!")
            self.redirect("/community")

class LoginHandler(tornado.web.RequestHandler, OAuthMixin):
    def get(self):
        self.render("login.html")

    async def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        user = users_collection.find_one({"username": username})

        if user and user["password"] == hashlib.sha256(password.encode("utf-8")).hexdigest():
            self.set_secure_cookie("user", str(user["_id"]))
            self.redirect("/community")
        else:
            self.write("Invalid username or password")

class UserProfileHandler(tornado.web.RequestHandler):
    async def get(self, user_id):
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        self.render("user_profile.html", user=user)

    async def post(self, user_id):
        updated_user = {
            "username": self.get_argument("username"),
            "email": self.get_argument("email")
        }
        await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
        self.redirect("/community")

class RankingHandler(tornado.web.RequestHandler):
    def get(self):
        # Render the ranking page
        self.render('ranking.html')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", year=datetime.datetime.now().year)

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_query_argument("query", "")
        # TODO: Implement plant search logic here
        self.render("identify.html", year=datetime.datetime.now().year)

    def post(self):
        pass

class CommunityHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("community.html", year=datetime.datetime.now().year)

class IdentifyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("identify_plant.html", year=datetime.datetime.now().year)

    def post(self):
        image = self.request.files['image'][0]
        image_name = image['filename']
        image_body = image['body']

        images_path = 'images'
        if not os.path.exists(images_path):
            os.makedirs(images_path)

        with open(os.path.join(images_path, image_name), 'wb') as file:
            file.write(image_body)

        # TODO: Implement image recognition logic here
        self.render("identify_plant.html", year=datetime.datetime.now().year)

class CommentsHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/identify")

    def post(self):
        name = self.get_argument("name")
        comment = self.get_argument("comment")
        self.comments.append({"name": name, "comment": comment})
        self.redirect("/identify")

class ReviewHandler(tornado.web.RequestHandler):
    def post(self):
        title = self.get_argument("title")
        rating = int(self.get_argument("rating"))
        comment = self.get_argument("comment")
        # Save the review to a database or file
        # Redirect to the page displaying the resource being reviewed



def make_app():
    templates_path = os.path.join(os.getcwd(), "templates\\")
    static_path = os.path.join(os.getcwd(), "static")
    print(templates_path)

    return tornado.web.Application([
        (r"/", MainHandler),
        # (r"/favicon.ico", tornado.web.ErrorHandler, {"status_code": 404}),
        (r"/identify_plant", IdentifyHandler),
        (r"/search", SearchHandler),
        (r"/comments", CommentsHandler),
        (r"/community", CommunityHandler),
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler),
        (r"/notifications", NotificationsHandler),
        (r'/ranking', RankingHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path}),
    ], template_path=templates_path, static_path=static_path,cookie_secret=cookie_secret)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
