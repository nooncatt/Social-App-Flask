from . import USERS, POSTS


class User:
    def __init__(self, id, first_name, last_name, email, posts=None, total_reactions=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.posts = [] if posts is None else posts
        self.total_reactions = total_reactions  # total_reactions у пользователя = сколько реакций ПОЛУЧИЛИ все его посты от других пользователей.

    @staticmethod
    def is_valid_id(user_id):
        return isinstance(user_id, int) and 0 <= user_id < len(USERS)

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

    @staticmethod
    def is_valid_author_id(author_id):
        return isinstance(author_id, int) and 0 <= author_id < len(USERS)

    def change_total_reactions(self, amount):
        self.total_reactions += amount

    def repr(self):
        return f"{self.id} {self.first_name} {self.last_name}"


class Post:
    def __init__(self, id, author_id, text, reactions=None):
        self.id = id
        self.author_id = author_id
        self.text = text
        self.reactions = [] if reactions is None else reactions

    @staticmethod
    def is_valid_post_id(post_id):
        return isinstance(post_id, int) and 0 <= post_id < len(POSTS)

    def add_or_update_reaction(self, user_id, reaction):
        reaction = str(reaction).lower()

        for r in self.reactions:
            if r["user_id"] == user_id:
                if r["reaction"] == reaction:
                    return "noop"
                r["reaction"] = reaction
                return "updated"
        self.reactions.append({"user_id": user_id, "reaction": reaction})
        return "new"

    @staticmethod
    def is_valid_reaction(reaction):
        return str(reaction).lower() in [
            "heart",
            "like",
            "dislike",
            "boom",
            "angry",
            "haha",
            "wow",
        ]

    def reactions_counter(self):
        return len(self.reactions)

    def repr(self):
        return f"text:{self.text}, author:{USERS[self.author_id]}, reactions: {[r['reaction'] for r in self.reactions]}"
