from datetime import date

class Rare_User():
    """The design. For the user dictionaries that are currently hard-coded in your userS list"""
    # Class initializer. It has 6 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.

    def __init__(self, id, bio, profile_image_url, first_name, last_name, email, username, password):
        self.id = id
        self.bio = bio
        self.profile_image_url = profile_image_url        
        self.active = True
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = True
        self.created_on = date.today()

# new_rare_user = Rare_User(1, "New guy", "profile_image_url","Nick", "M", "nick@m.com", "Nick M", "password", {date.today().strftime("%m/%d/%Y")})

# bio
# profile_image_url
# created_on date
# active
# first_name
# last_name
# email
# username
# password
# is_admin