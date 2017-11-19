from exceptions import PermissionDenied


class Thread:
    def __init__(self, title, first_post):
        """
        Creates a new thread with a title and an initial first post.
        The author of the first post at the time of thread creation is the
        owner of the thread.
        The owner cannot change once the thread is created.
        """
        self._title = title
        self._posts = [first_post]
        self._tags = []
        self._owner = first_post.get_author()

    def get_owner(self):
        """
        Returns the owner of the thread.
        """
        return self._owner

    def get_title(self):
        """
        Returns the title of the thread.
        """
        return self._title

    def get_tags(self):
        """
        Returns a sorted list of unique tags (they are sorted when set).
        """
        return self._tags

    def get_posts(self):
        """
        Returns a list of Post objects in this thread, in the order they were
        published.
        """
        return self._posts

    def publish_post(self, post):
        """
        Adds the given Post object into the list of Posts in this thread.
        """
        self._posts.append(post)

    def remove_post(self, post, by_user):
        """
        Allows the given user to remove the Post from this thread.
        Does nothing if the Post is not in this thread.
        * raises PermissionDenied if the given user is not the author of the
        post.
        """
        if by_user != post.get_author():
            raise PermissionDenied
        try:
            self._posts.remove(post)
        except ValueError:
            pass

    def set_title(self, title, by_user):
        """
        Allows the given user to edit the thread title.
        * raises PermissionDenied if the given user is not the owner of the
        thread.
        """
        if by_user != self.get_owner():
            raise PermissionDenied
        self._title = title

    def set_tags(self, tag_list, by_user):
        """
        Allows the given user to replace the thread tags (list of strings).
        * raises PermissionDenied if the given user is not the owner of the
        thread.
        """
        if by_user != self.get_owner():
            raise PermissionDenied
        self._tags = []
        for tag in tag_list:
            if tag not in self._tags:
                self._tags.append(tag)
        self._tags.sort()
