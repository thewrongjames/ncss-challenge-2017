from post import Post
from thread import Thread


class Forum:
    def __init__(self):
        """
        Perform initialisation of a new Forum object, as needed.
        """
        self._threads = []

    def get_threads(self):
        """
        Returns a list of Threads in the Forum, in the order that they were
        published.
        """
        return self._threads

    def publish(self, title, content, author):
        """
        Creates a new Thread with the given title and adds it to the Forum.
        The content and author are provided to allow you to create the first
        Post object.
        Threads are stored in the order that they are published.
        Returns the new Thread object.
        """
        new_thread = Thread(title, Post(content, author))
        self._threads.append(new_thread)
        return new_thread

    def search_by_tag(self, tag):
        """
        Searches all forum Threads for any that contain the given tag.
        Returns a list of matching Thread objects in the order they were
        published.
        """
        return [thread for thread in self.get_threads() if tag in \
            thread.get_tags()]

    def search_by_author(self, author):
        """
        Searches all forum Threads for Posts by the given author.
        Returns a list of matching Post objects in any order you like.
        """
        all_posts = []
        for thread in self.get_threads():
            all_posts += thread.get_posts()
        return [post for post in all_posts if post.get_author() == author]
