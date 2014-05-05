from doublylinkedlist import CircularDoublyLinkedList, Node

class LRUCache(object):
    
    def __init__(self, maxsize=5):
        self.cache_list = CircularDoublyLinkedList()
        self.cache_table = {}
        self.misses = 0
        self.hits = 0
        self.requests = 0
        self.maxsize = maxsize

    def get_size(self):
        """
        >>> x = LRUCache(maxsize=2)
        >>> myfunc = lambda x, y: x + y
        >>> x.get_size()
        0
        >>> x.save_and_return(myfunc, 1,2)
        3
        >>> x.get_size()
        1
        >>> x.save_and_return(myfunc, 1,2)
        3
        >>> x.get_size()
        1
        >>> x.save_and_return(myfunc, 2,2)
        4
        >>> x.get_size()
        2
        >>> x.save_and_return(myfunc, 2,3)
        5
        >>> x.get_size()
        2
        """
        if self.cache_list.root == None:
            return 0
        else:
            i = 1
            item = self.cache_list.root.next
            while item != self.cache_list.root:
                i += 1
                item = item.next
            return i

    def save_and_return(self, func, *args, **kwargs):
        """
        >>> x = LRUCache()
        >>> myfunc = lambda x, y: x + y
        >>> x.save_and_return(myfunc, 1, 2)
        3
        >>> print x.get_first().value
        3
        >>> print x.get_last().value
        3
        >>> hashed_name = hash(repr([myfunc, (1, 2), {}]))
        >>> x.cache_table[hashed_name] == x.get_first() == x.get_last()
        True
        """
        key = self.make_hashed_func_object(func, *args, **kwargs)
        if self.cache_table.get(key, None) != None:
            # already in cache
            desired_node = self.cache_table[key]
            self.hits += 1
        else:
            # not in cache
            desired_node = Node(func(*args, **kwargs))
            self.cache_table[key] = desired_node
            self.misses += 1
            if self.is_full():
                self.delete_oldest()
        self.mark_most_recent(desired_node)
        return desired_node.value

    def delete_oldest(self):
        oldest = self.cache_list.root.previous
        oldest.previous.next = self.cache_list.root
        self.cache_list.root.previous = oldest.previous
        oldest = None
        

    def is_full(self):
        """
        >>> x = LRUCache(maxsize=2)
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        2
        >>> x.is_full()
        False
        >>> x.save_and_return(foo, 3)
        3
        >>> x.is_full()
        True
        """
        if self.get_size() >= self.maxsize:
            return True
        return False

    def mark_most_recent(self, recent_node):
        """
        >>> x = LRUCache()
        >>> foo = lambda y: y
        >>> x.save_and_return(foo, 4)
        4
        >>> print x.cache_list.root.value
        4
        >>> x.save_and_return(foo, 5)
        5
        >>> print x.cache_list.root.value
        5
        >>> x.mark_most_recent(x.cache_list.root.next)
        >>> print x.cache_list.root.value
        4
        """
        if self.cache_list.root == None:
            # list is empty
            recent_node.previous = recent_node.next = recent_node
            self.cache_list.root = recent_node
        elif recent_node.next != None and recent_node.previous != None:
            # node is already in list somewhere
            self.remove_from_middle(recent_node)
            self.add_to_head(recent_node)
        else:
            # node not in list
            self.add_to_head(recent_node)

    def add_to_head(self, new_root):
        old_root = self.cache_list.root
        tail = old_root.previous
        tail.next = new_root
        new_root.previous = tail
        old_root.previous = new_root
        new_root.next = old_root
        self.cache_list.root = new_root

    def remove_from_middle(self, new_root):
        new_root.next.previous = new_root.previous
        new_root.previous.next = new_root.next


    def make_hashed_func_object(self, func, *args, **kwargs):
        """
        >>> x = LRUCache()
        >>> foo = lambda x, y: x + y
        >>> hashed_fun = x.make_hashed_func_object(foo, (1, 2))
        >>> hashed_fun == hash(repr([foo, ((1, 2),), {}]))
        True
        """
        return hash(repr([func, args, kwargs]))

    def get_first(self):
        """
        >>> x = LRUCache()
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        2
        >>> print x.get_first().value
        2
        >>> x.save_and_return(foo, 6)
        6
        >>> print x.get_first().value
        6
        """
        return self.cache_list.root

    def get_last(self):
        """
        >>> x = LRUCache()
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        2
        >>> print x.get_last().value
        2
        >>> x.save_and_return(foo, 6)
        6
        >>> print x.get_last().value
        2
        """
        return self.cache_list.root.previous

    def get_cache_list(self):
        """
        >>> x = LRUCache(maxsize=3)
        >>> x.get_cache_list()
        []
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        2
        >>> print x.get_cache_list()
        [2]
        >>> x.save_and_return(foo, 6)
        6
        >>> print x.get_cache_list()
        [6, 2]
        >>> x.save_and_return(foo, 1)
        1
        >>> print x.get_cache_list()
        [1, 6, 2]
        >>> x.save_and_return(foo, 6)
        6
        >>> x.get_cache_list()
        [6, 1, 2]
        >>> x.save_and_return(foo, 4)
        4
        >>> x.get_cache_list()
        [4, 6, 1]
        """
        l = []
        item = self.cache_list.root
        if item == None:
            return []
        while item.next != self.cache_list.root:
            l.append(item.value)
            item = item.next
        l.append(item.value)
        return l


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #doctest.run_docstring_examples(LRUCache.make_hashed_func_object, globals())
