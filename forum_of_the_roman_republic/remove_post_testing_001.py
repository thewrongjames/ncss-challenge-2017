from exceptions import PermissionDenied
from post import Post
from thread import Thread


first_post = Post('Veni, vidi, vici!', 'Caesar')
thread = Thread('Battle of Zela', first_post)
other_post = Post('?', 'Flavia')
try:
  thread.remove_post(other_post, 'Flavia')
except PermissionDenied:
  print('PermissionDenied incorrectly raised.')
except:
  print('An exception that was not PermissionDenied was incorrectly raised!')
else:
  print('Post by Flavia should be ignored.')
print([p.get_author() for p in thread.get_posts()])
