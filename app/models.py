from . import USERS


class User:
    # todo: check email phone and do user class
    def __init__(self, id, first_name, last_name, email, posts=None, total_reactions=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.posts = [] if posts is None else posts
        self.total_reactions = total_reactions

    @staticmethod
    def is_valid_id(user_id):
        if user_id >= len(USERS) or user_id < 0:
            return False
        return True

    @staticmethod
    def check_email_validity(email):
        from email_validator import validate_email, EmailNotValidError

        try:
            emailinfo = validate_email(email, check_deliverability=True)
            # After this point, use only the normalized form of the email address,
            # especially before going to a database query.
            email = emailinfo.normalized
            return email

        except EmailNotValidError as e:
            # The exception message is human-readable explanation of why it's
            # not a valid (or deliverable) email address.
            print(str(e))
            return False
