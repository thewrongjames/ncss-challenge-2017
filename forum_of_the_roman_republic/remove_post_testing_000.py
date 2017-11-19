from exceptions import PermissionDenied
from post import Post
from thread import Thread


first_post = Post('Veni, vidi, vici!', 'Caesar')
thread = Thread('Battle of Zela', first_post)
next_post = Post('Braggart!', 'Brutus')
thread.publish_post(next_post)
last_post = Post('Nice work.', 'Cleopatra')
thread.publish_post(last_post)
print([p.get_author() for p in thread.get_posts()])
try:
  thread.remove_post(next_post, 'Brutus')
except PermissionDenied:
  print('PermissionDenied incorrectly raised.')
except:
  print('An exception that was not PermissionDenied was incorrectly raised!')
  raise
else:
  print('Post by Brutus allowed to be removed.')
print([p.get_author() for p in thread.get_posts()])
