from exceptions import PermissionDenied
from post import Post
from thread import Thread
from forum import Forum


forum = Forum()
thread = forum.publish('Battle of Zela', 'Veni, vidi, vici!', 'Caesar')
try:
  thread.set_tags(['battle'], 'Cleopatra')
except PermissionDenied:
  print('PermissionDenied correctly raised.')
except:
  print('An exception that was not PermissionDenied was incorrectly raised!')
else:
  print('Cleopatra should not be allowed to change the tags.')
print(thread.get_tags())
try:
  thread.set_tags(['battle'], 'Caesar')
except PermissionDenied:
  print('PermissionDenied incorrectly raised.')
except:
  print('An exception that was not PermissionDenied was incorrectly raised!')
else:
  print('Caesar correctly allowed to change the tags.')
print(thread.get_tags())
thread.set_tags(['battle', 'brag'], 'Caesar')
print(thread.get_tags())
thread.set_tags(['battle', 'battle', 'battle'], 'Caesar')
print(thread.get_tags())
thread.set_tags(['drama', 'battle', 'action', 'latin'], 'Caesar')
print(thread.get_tags())
thread.set_tags([], 'Caesar')
print(thread.get_tags())
