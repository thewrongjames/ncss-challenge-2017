from exceptions import PermissionDenied


class Post:
    def __init__(self, content, author):
        """
        Creates a new Post by the author with the given content.
        You will need to track up votes more cleverly than previously because
        a user is only allowed to vote *once*.
        """
        self._content = content
        self._author = author
        self._upvoters = set()

    def get_author(self):
        """
        Returns the author of the Post.
        """
        return self._author

    def get_content(self):
        """
        Returns the content of the Post.
        """
        return self._content

    def get_upvotes(self):
        """
        Returns a non-negative integer representing the total number of upvotes.
        """
        return len(self._upvoters)

    def set_content(self, content, by_user):
        """
        Called when the given user wants to update the content.
        * raises PermissionDenied if the given user is not the author.
        """
        if by_user != self.get_author():
            raise PermissionDenied
        self._content = content

    def upvote(self, by_user):
        """
        Called when the given user wants to upvote this post.
        A user can only perform an up vote *once*.
        """
        self._upvoters.add(by_user)
