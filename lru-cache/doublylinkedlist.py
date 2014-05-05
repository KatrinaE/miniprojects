
class Node(object):

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

class CircularDoublyLinkedList(object):
    """
    Implements a double, circular linked list
    """
    def __init__(self, value=None):
        if value == None:
            self.root = None
        else:
            self.root = Node(value)
            self.root.prev = self.root
            self.root.next = self.root


    def get_first(self):
        return self.root

    def get_last(self):
        return self.root.prev

    def insert_at_beginning(self, value):
        """
        >>> x = CircularDoublyLinkedList('old_root')
        >>> x.insert_at_beginning('new')
        >>> print x.root.value
        new
        >>> print x.root.prev.value
        old_root
        >>> print x.root.next.value
        old_root
        >>> print x.root.next.next.value
        new
        >>> print x.root.next.prev.value
        new
        """
        new = Node(value)
        if self.root == None:
            self.root = new
        new.next = self.root
        new.prev = self.root.prev
        self.root.prev.next = new
        self.root.prev = new
        self.root = new

    def insert_at_end(self, value):
        """
        >>> x = CircularDoublyLinkedList('old_root')
        >>> x.insert_at_end('a')
        >>> x.insert_at_end('b')
        >>> print x.root.value
        old_root
        >>> print x.root.next.value
        a
        >>> print x.root.next.next.value
        b
        >>> print x.root.next.next.next.value
        old_root
        >>> print x.root.prev.value
        b
        >>> print x.root.prev.prev.value
        a
        """
        new = Node(value)
        if self.root == None:
            self.root = new
        last = self.root.prev
        last.next = new
        new.prev = last
        new.next = self.root
        self.root.prev = new

    def remove_from_beginning(self):
        """
        >>> x = CircularDoublyLinkedList('root')
        >>> x.insert_at_end('a')
        >>> x.insert_at_end('b')
        >>> x.remove_from_beginning()
        >>> print x.root.value
        a
        >>> print x.root.prev.value
        b
        >>> print x.size()
        2
        """
        new_root = self.root.next
        new_root.prev = self.root.prev
        self.root.prev.next = new_root
        self.root = new_root

    def remove_from_end(self):
        """
        >>> x = CircularDoublyLinkedList('old_root')
        >>> x.insert_at_end('a')
        >>> x.insert_at_end('b')
        >>> print x.size()
        3
        >>> print x.root.prev.value
        b
        >>> x.remove_from_end()
        >>> print x.size()
        2
        >>> print x.root.prev.value
        a
        """
        self.get_last().prev.next = self.root
        self.root.prev = self.get_last().prev

    def size(self):
        """
        >>> x = CircularDoublyLinkedList('root')
        >>> print x.size()
        1
        >>> x.insert_at_beginning('foo')
        >>> x.insert_at_beginning('bar')
        >>> print x.size()
        3
        """
        if self.root == None:
            # list is empty
            return 0
        else:
            item = self.root
            i = 1
            while item.next != self.root:
                i += 1
                item = item.next
        return i

if __name__ == "__main__":
    import doctest
    doctest.testmod()
