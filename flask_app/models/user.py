# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# model the class after the friend table from our database
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Users:
    DB = "users_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append(cls(user))
        return users
        
    # the save method will be used when we need to save a new friend to our database
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email)
                VALUES (%(first_name)s, %(last_name)s, %(email)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        # print(result)
        return result
    
    @classmethod
    def get_one_user(cls, id):
        query = "SELECT * from users WHERE id = %(id)s;"
        result = connectToMySQL('users_schema').query_db(query, {"id":id})
        print(result)
        return cls(result[0])
    
    @classmethod
    def update(cls,user_data):
        query = """UPDATE users 
                SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s
                WHERE id = %(id)s
                ;"""
        return connectToMySQL(cls.DB).query_db(query,user_data)
    
    @classmethod
    def delete(cls, user_id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": user_id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 1:
            flash("first name can't be blank.")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("last name can't be blank")
            is_valid = False
        if len(user['email']) < 1:
            flash("email can't be blank")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
    
    # @staticmethod
    # def validate_email(user):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     if not EMAIL_REGEX.match(user['email']): 
    #         flash("Invalid email address!")
    #         is_valid = False
    #     return is_valid


