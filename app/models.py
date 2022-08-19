from app import db, login

# Import for Werkzeug Security
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Date Time Module
from datetime import datetime

#Imports for Login manager and User Mixin
from flask_login import UserMixin

# Create the current user_manager using the user_login function
# Which is a decorator (used in this case as callback function)
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    post = db.relationship('Post', backref = 'author', lazy = True)

    def __init__(self,**kwargs):
        # self.username = username
        # self.email = email
        # self.password = self.set_password(password)
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        # Open and insert into database
        db.session.add(self)
        # Save info into database
        db.session.commit()

    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'{self.username} has been created with {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, **kwargs):
        # self.title = title
        # self.content = content
        # self.user_id = user_id
        super().__init__(**kwargs)
        # Open and insert into database
        db.session.add(self)
        # Save info into database
        db.session.commit()

    def __repr__(self):
        return f'The title of the post is {self.title} \n and the content is {self.content}.'
    
    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in {'title', 'content'}:
                setattr(self, key, val)
        db.session.commit() # so the database changes as well 
        print('COMMITTING')
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()