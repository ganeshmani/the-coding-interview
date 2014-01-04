import sys
from collections import defaultdict
import copy

class Chest(object):
    def __init__(self, id, content):
        self.id, self.content = id, content

def get_data():
  numcases = int(sys.stdin.readline())
  for case in range(1,numcases+1):
      num_keys, num_chests = map(int, sys.stdin.readline().split())
      keyring = list(map(int, sys.stdin.readline().split()))
      # Store chests in dictionary
      chests = defaultdict(list)
      for id in range(1,num_chests+1):
        chest_data = list(map(int, sys.stdin.readline().split()))
        unlock_key, content = chest_data[0], chest_data[2:]
        chest = Chest(id, content)
        chests[unlock_key].append(chest)
      yield (case, keyring, chests)

def count(d):
    """ Count number of values in dict """
    return sum(len(v) for v in d.values())

def remove_chest(chests, id):
    for index, chest in enumerate(chests):
        if chest.id == id:
            del chests[index]
            return

def unlock(key, chest, chests):
    """ Remove chest with matching key type from all chests """
    new_chests = copy.deepcopy(chests)
    print("Search for ", chest.id, "in", key)
    for k, v in new_chests.items():
        print(k, ",".join(str(c.id) for c in v))
    remove_chest(new_chests[key], chest.id)
    print("---")
    for k, v in new_chests.items():
        print(k, ",".join(str(c.id) for c in v))
    return new_chests

def get_all_paths(keyring, locked_chests, path = []):
    # Try each key from keyring.
    for key in set(keyring):
        print("Selecting key", key)
        for chest in locked_chests[key]:
            print(locked_chests[key])
            print("Selecting chest", chest.id)
            # Add chest to path
            new_path = path + [chest.id]
            # "Unlock" chest i.e. remove chest from dict.
            remaining_chests = unlock(key, chest, locked_chests)
            # Have all chests been unlocked yet?
            if not count(remaining_chests):
                yield path # We are done
                print("after yield")
            else:
                # Get keys from chest
                new_keyring = keyring + chest.content
                print("Got new keys!", chest.content)
                # Remove used key from keyring
                new_keyring.remove(key)
                print("Keyring", new_keyring)
                yield from get_all_paths(new_keyring, remaining_chests, new_path)

def best_path(paths):
    if not paths:
        return "IMPOSSIBLE"
    rank = sorted(paths)
    print(rank)
    return " ".join(str(chest) for chest in rank[0])

def solve(keyring, locked_chests):
    paths = [p for p in get_all_paths(keyring, locked_chests) if p]
    return best_path(paths)

def main():
  for case, keys, locked_chests in get_data():
    print("Case #{}: {}".format(case, solve(keys, locked_chests)))

if __name__ == "__main__":
  main()
