import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from tags.request import create_tag
from posts import create_post, update_post, delete_post
from rare_users import get_all_rare_users, get_single_rare_user, create_rare_user, delete_rare_user, update_rare_user
from posts import get_all_posts, get_single_post
from login import login_auth, register_rare_user
from tags import get_all_tags, get_single_tag, create_tag
from categories import get_all_categories, get_single_category, create_category, delete_category, update_category
from comments import get_comments_by_post, get_all_comments, create_comment, update_comment, delete_comment

#    get_all_locations, get_single_location, create_location,
#    delete_location, update_location)
# from customers import (
#    get_all_customers, get_single_customer, create_customer,
#    delete_customer, update_customer, get_customers_by_email)


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """sets the path"""
        # Just like splitting a string in JavaScript. If the
        # path is "/rare_user/1", the resulting list will
        # have "" at index 0, "rare_user" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /rare_user
        except ValueError:
            pass  # Request had trailing slash: /rare_user/

        return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response
        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/rare_users` or `/rare_users/2`
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "rare_users":
                if id is not None:
                    response = f"{get_single_rare_user(id)}"
                else:
                    response = f"{get_all_rare_users()}"

            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"

            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"

            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"

            elif resource == "comments":
                if id is not None:
                    response = f"{get_all_comments()}"
                else:
                    response = []

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?

            if resource == "comments" and key == "post_id":
                intValue = (int(value))
                response = f"{get_comments_by_post(intValue)}"

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, _) = self.parse_url(
            self.path)  # pylint:disable=(unbalanced-tuple-unpacking)

        # Initialize new rare_user
        new_item = None
        new_rare_user = None
        rare_user_login = None

        # Add a new rare_user to the list. Don't worry about
        # the orange squiggle, you'll define the create_rare_user
        # function next.

        if resource == "login":
            rare_user_login = login_auth(
                post_body['email'], post_body['password'])
            self.wfile.write(f"{rare_user_login}".encode())

        if resource == "register":
            new_rare_user = register_rare_user(post_body)
            self.wfile.write(f"{new_rare_user}".encode())

        if resource == "rare_user":
            new_rare_user = create_rare_user(post_body)
        # Encode the new rare_user and send in response
            self.wfile.write(f"{new_rare_user}".encode())

        if resource == "posts":
            new_item = create_post(post_body)
        if resource == "categories":
            new_item = create_category(post_body)
        if resource == "comments":
            new_item = create_comment(post_body)
        if resource == "tags":
            new_item = create_tag(post_body)
        # if resource == "locations":
        #    new_item = create_location(post_body)
        # if resource == "customers":
        #    new_item = create_customer(post_body)

        # Encode the new rare_user and send in response
        self.wfile.write(f"{new_item}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, _) = self.parse_url(self.path)

        success = False

        # Update a single rare_user from the list
        if resource == "rare_users":  # conditional
            success = update_rare_user(id, post_body)

        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)
        # if resource == "employees":
        #    update_employee(id, post_body)
        # if resource == "locations":
        #    update_location(id, post_body)
        # if resource == "customers":
        #    update_customer(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handles DELETE requests to the server
        """
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id, _) = self.parse_url(self.path)

        # Delete a single rare_user from the list
        if resource == "rare_users":
            delete_rare_user(id)

        if resource == "posts":
            delete_post(id)

        if resource == "categories":
            delete_category(id)

        if resource == "comments":
            delete_comment(id)

        # Encode the new rare_user and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
