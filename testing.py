# import pymongo
#
#
# with open('creds.txt', 'r') as f:
#     # Read Credentials
#     username = f.readline().strip()
#     password = f.readline().strip()
#     database = f.readline().strip()
# print(username, password, database)
#
# # set the connection parameters
# mongo_host = "192.168.44.132"
# mongo_port = 27017
# mongo_user = username
# mongo_password = password
# mongo_auth_source = "admin"
#
# # create the MongoClient instance
# client = pymongo.MongoClient(mongo_host, mongo_port, username=mongo_user, password=mongo_password, authSource=mongo_auth_source)
#
# # specify the database and collection you want to work with
# db = client["papa"]
# # create the collections
# # db.create_collection("posts")
# # db.create_collection("comments")
# # db.create_collection("notifications")
#
# # print the names of the collections in the database
# # print(db.list_collection_names())
#
#
# collection = db["users"]
#
# # perform operations on the collection
# cursor = collection.find({})
# for document in cursor:
#     print(document)
# # document = {"name": "Someone ", "age": 32}
# # result = collection.insert_one(document)
# # print("Inserted document with ID:", result.inserted_id)
#
import requests
from io import BytesIO
from PIL import Image

# Define the endpoint URL and the x-y data to generate the graph
x_data = '1, 2, 3'
y_data = '4, 5, 6'
url = "http://localhost:8000/generate_graph/" + x_data + "/" + y_data
print(url)
# import matplotlib.pyplot as plt
#
# # Define the x and y values to plot
# x = [1, 2, 3, 4, 5]
# y = [10, 20, 30, 25, 15]
#
# # Create a new figure and axis object using matplotlib
# fig, ax = plt.subplots(figsize=(8, 6))
#
# # Plot the x and y values on the axis object
# ax.plot(x, y, color='red', linewidth=2, linestyle='--', marker='o', markersize=8)
#
# # Set the axis labels and title
# ax.set_xlabel('X-axis', fontsize=14)
# ax.set_ylabel('Y-axis', fontsize=14)
# ax.set_title('Line Plot', fontsize=16)
#
# # Set the axis ticks and limits
# ax.set_xticks([1, 2, 3, 4, 5])
# ax.set_yticks([0, 10, 20, 30, 40])
# ax.set_xlim([0.5, 5.5])
# ax.set_ylim([0, 40])
#
# # Add a grid to the plot
# ax.grid(color='gray', linestyle='--', linewidth=0.5)
#
# # Add a legend to the plot
# ax.legend(['Data'], loc='upper right')
#
# # Display the plot
# plt.show()
