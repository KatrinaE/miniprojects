from doublylinkedlist import CircularDoublyLinkedList, Node

"""
Why use a lock?

The problem is that if you've got a query that takes 30 
seconds and you're executing the page every second, 
in the time it takes to populate the cache item, 29 
other requests will come in, all of which will attempt 
to populate the cache item with their own queries to 
the database. To solve this problem, you can add a 
thread lock to stop the other page executions from 
requesting the data from the database.
"""


"""
Generally a LRU cache could be implemented as a (linked) list with a
max. size of N.
On usage of an object this object will be moved to the top of the list
(and removed from the old position).
If it's not yet stored in the cache, you (fetch it from the source and)
add it on top and remove the last one, if the list exceeds N entries.

So you need to do two things:
1) Maintain a list: Use a (linked) list.
2) Random access to that list: Use a dict (hash), that also has to be
updated on removal/addition of objects.

http://bytes.com/topic/python/answers/691409-lru-cache
"""

class LRUCache(object):
    
    def __init__(self, maxsize=5):
        self.cache_list = CircularDoublyLinkedList()
        self.cache_table = {}
        self.misses = 0
        self.hits = 0
        self.requests = 0
        self.maxsize = maxsize

    def get_size(self):
        if self.root == None:
            return 0
        else:
            i = 1
            item = self.root.next
            while item != self.root:
                i += 1
            return i

    def get_first(self):
        """
        >>> x = LRUCache()
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        >>> print x.get_first().value
        2
        >>> x.save_and_return(foo, 6)
        >>> print x.get_first().value
        6
        """
        return self.root

    def get_last(self):
        """
        >>> x = LRUCache()
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        >>> print x.get_last().value
        2
        >>> x.save_and_return(foo, 6)
        >>> print x.get_last().value
        2
        """
        return self.root.prev

    def get_cache_list(self):
        """
        >>> x = LRUCache(maxsize=2)
        >>> x.get_cache_list()
        []
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        >>> print x.get_cache_list()
        [2]
        >>> x.save_and_return(foo, 6)
        >>> print x.get_cache_list()
        [6, 2]
        >>> x.save_and_return(foo, 1)
        >>> print x.get_cache_list()
        [1, 6]
        """
        l = []
        while item.next != self.root:
            l.append(item.value)
            item = item.next
        l.append(item.value)
        return l

    def is_full(self):
        """
        >>> x = LRUCache(maxsize=2)
        >>> foo = lambda x: x
        >>> x.save_and_return(foo, 2)
        >>> x.is_full()
        False
        >>> x.save_and_return(foo, 3)
        >>> x.is_full()
        True
        """
        if self.get_size() >= self.maxsize:
            return True
        return False

    def save_and_return(self, func, *args, **kwargs):
        """
        >>> x = LRUCache()
        >>> myfunc = lambda x, y: x + y
        >>> x.save_and_return(myfunc, [1, 2])
        >>> print x.get_first().value
        3
        >>> print x.get_last().value
        3
        >>> x.cache_table[hash(myfunc, [1, 2])] == x.get_first() == x.get_last()
        True
        
        """
        key = self.make_func_hash(func, *args, **kwargs)
        if cache_table[key] != None:
            # already in cache
            desired_node = self.cache_table[key]
            self.hits += 1
            self.mark_most_recent(desired_node)
            return desired_node.value
        else:
            # not in cache
            desired_node = Node(func(*args, **kwargs))
            self.cache_table[key] = desired_node
            self.misses += 1
            if self.is_full():
                self.delete_oldest()
            self.mark_most_recent(desired_node)
            return desired_node.value


    def mark_most_recent(self, recent_node):
        """
        >>> x = LRUCache()
        >>> def foo: lambda y, y
        >>> x.save_or_return(foo, 4)
        >>> print x.cache_list.root.value
        4
        >>> x.save_or_return(foo, 5)
        >>> print x.cache_list.root.value
        5
        >>> x.mark_most_recent(x.cache_list.root.next)
        >>> print x.cache_list.root.value
        4
        """
        if recent_node.next != None and recent_node.previous != None:
            # node is already in list somewhere
            recent_node.next.previous = recent_node.previous
            recent_node.previous.next = recent_node.next
        # append to head of list
        recent_node.next = self.cache_list.root
        recent_node.previous = self.cache_list.root.previous
        recent_node.previous.next = recent_node
        self.root.previous = recent_node
        self.root = recent_node


    def make_hashed_func_object(func, *args, **kwargs):
        """
        >>> foo = lambda x, y: x + y
        >>> hashed_fun = make_hashed_func_object(foo, [1, 2])
        >>> 
        """
        def f():
            return func(*args, **kwargs)
        return hash(f)



def make_func_hash(func, *args, **kwargs):
    """                                                                                                                                                                                     
    >>> foo = lambda x, y: x + y                                                                                                                                                            
    >>> hashed_fun = make_func_hash(foo, [1, 2])                                                                                                                                   
    >>> hashed_fun == -9223372036570986605
    True
    """
    def f():
        return func(*args, **kwargs)
    return hash(f)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
