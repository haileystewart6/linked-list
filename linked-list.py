class LinkedList:
    class Node:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior
            self.next  = next
    
    def __init__(self):
        self.head = LinkedList.Node(None) 
        self.head.prior = self.head.next = self.head 
        self.length = 0
       
    def prepend(self, value):
        n = LinkedList.Node(value, prior=self.head, next=self.head.next)
        self.head.next.prior = self.head.next = n
        self.length += 1
        
    def append(self, value):
        n = LinkedList.Node(value, prior=self.head.prior, next=self.head)
        n.prior.next = n.next.prior = n
        self.length += 1
            
            
    ### subscript-based access ### 
    
    def _normalize_idx(self, idx):
        nidx = idx
        if nidx < 0:
            nidx += len(self)
            if nidx < 0:
                nidx = 0
        return nidx
    
    def __getitem__(self, idx):
        """Implements `x = self[idx]`"""
        assert(isinstance(idx, int))
        idx = self._normalize_idx(idx)
        if idx > self.length or self.length == 0:
            raise IndexError
        out = self.head.next
        for _ in range(idx):
            out = out.next
        return out.val
        
    def __setitem__(self, idx, value):
        """Implements `self[idx] = x`"""
        assert(isinstance(idx, int))
        idx = self._normalize_idx(idx)
        if idx > self.length or self.length == 0:
            raise IndexError
        change = self.head.next
        for _ in range(idx):
            change = change.next
        change.val = value
        
        

    def __delitem__(self, idx):
        """Implements `del self[idx]`"""
        assert(isinstance(idx, int))
        idx = self._normalize_idx(idx)
        if idx > self.length or self.length == 0:
            raise IndexError
        dele = self.head.next
        for _ in range(idx):
            dele = dele.next
        dele.prior.next = dele.next #link forward gets attached to the next one
        dele.next.prior = dele.prior #link backward gets attached to the one before
        self.length -= 1
        

    ### cursor-based access ### 
    
    def cursor_get(self): 
        """retrieves the value at the current cursor position"""
        assert self.cursor is not self.head
        return self.cursor.val

    def cursor_set(self, idx): 
        """sets the cursor to the node at the provided index"""
        assert(idx < len(self))
        self.cursor = self.head.next
        for i in range(idx):
            self.cursor = self.cursor.next

    def cursor_move(self, offset): 
        """moves the cursor forward or backward by the provided offset 
        (a positive or negative integer); note that it is possible to advance 
        the cursor by further than the length of the list, in which case the 
        cursor will just "wrap around" the list, skipping over the sentinel 
        node as needed"""
        assert len(self) > 0
        if self.cursor is None:
            self.cursor = self.head.next
        if offset < 0:
            for i in range(abs(offset)):
                self.cursor = self.cursor.prior
                if self.cursor is self.head:
                    self.cursor = self.cursor.prior
        else:
            for i in range(offset):
                self.cursor = self.cursor.next
                if self.cursor is self.head:
                    self.cursor = self.cursor.next

    def cursor_insert(self, value): 
        """inserts a new value after the cursor and sets the cursor to the 
        new node"""
        n = LinkedList.Node(value,prior = self.cursor, next = self.cursor.next)
        n.prior.next = n
        n.next.prior = n 
        self.length += 1
        self.cursor = n

    def cursor_delete(self):
        """deletes the node the cursor refers to and sets the cursor to the 
        following node"""
        assert self.cursor is not self.head and len(self) > 0
        self.cursor.prior.next = self.cursor.next
        self.cursor.next.prior = self.cursor.prior
        self.length-= 1
        self.cursor = self.cursor.next 
        

    ### stringification ###
    
    def __str__(self):
        """Implements `str(self)`. Returns '[]' if the list is empty, else
        returns `str(x)` for all values `x` in this list, separated by commas
        and enclosed by square brackets. E.g., for a list containing values
        1, 2 and 3, returns '[1, 2, 3]'."""
        return '[' + ', '.join(str(x) for x in self) + ']'
        
        
    def __repr__(self):
        """Supports REPL inspection. (Same behavior as `str`.)"""
        return '[' + ', '.join(str(x) for x in self) + ']'
     


    ### single-element manipulation ### 
        
    def insert(self, idx, value):
        """Inserts value at position idx, shifting the original elements down the
        list, as needed. Note that inserting a value at len(self) --- equivalent
        to appending the value --- is permitted. Raises IndexError if idx is invalid."""
        idx = self._normalize_idx(idx)
        if idx > self.length:
            raise IndexError
        ins = self.head.next
        for _ in range(idx):
            ins = ins.next
        inse = LinkedList.Node(value, prior = ins.prior, next = ins)
        ins.prior.next = ins.prior = inse 
        self.length += 1
    def pop(self, idx=-1): 
        """Deletes and returns the element at idx (which is the last element,
        by default)."""
        idx = self._normalize_idx(idx)
        if idx > self.length or self.length == 0:
            raise IndexError
        out = self[idx]
        del self[idx]
        return out
        
    def remove(self, value):
        """Removes the first (closest to the front) instance of value from the
        list. Raises a ValueError if value is not found in the list."""
        rem = self.head.next
        for i in range(self.length):
            if rem.val == value:
                self.pop(i)
                return
            rem = rem.next
        raise ValueError
    

    ### predicates (T/F queries)
    
    def __eq__(self, other): 
        """Returns True if this LinkedList contains the same elements (in order) as
        other. If other is not an LinkedList, returns False."""
        if not isinstance(other, LinkedList) or self.length != other.length:
            return False
        for i in range(self.length):
            if self[i] != other[i]:
                return False
        return True

    def __contains__(self, value):
        """Implements `val in self`. Returns true if value is found in this list."""
        for x in self:
            if value == x:
                return True



    ### queries ### passed
    
    def __len__(self): 
        """Implements `len(self)`"""
        return self.length
    
    def min(self): 
        """Returns the minimum value in this list."""
        minimum = self.head.next.val
        check = self.head.next
        for _ in range(self.length):
            if check.val < minimum:
                minimum = check.val
            check = check.next
        return minimum
       
    def max(self): 
        """Returns the maximum value in this list."""
        maximum = self.head.next.val
        check = self.head.next
        for _ in range(self.length):
            if check.val > maximum:
                maximum = check.val
            check = check.next
        return maximum
        
    def index(self, value, i=0, j=None): 
        """Returns the index of the first instance of value encountered in
        this list between index i (inclusive) and j (exclusive). If j is not
        specified, search through the end of the list for value. If value
        is not in the list, raise a ValueError."""
        idx = self._normalize_idx(i)
        if j is None:
            j = self.length
        njdx = self._normalize_idx(j)
        check = self.head.next
        for _ in range(idx):
            check = check.next
        for i in range(idx, njdx):
            if value == check.val:
                return i
            check = check.next
        raise ValueError
        
    
    def count(self, value): 
        """Returns the number of times value appears in this list."""
        count = 0
        for x in self:
            if x == value:
                count += 1
        return count

    ### bulk operations ### passed

    def __add__(self, other): 
        """Implements `self + other_list`. Returns a new LinkedList
        instance that contains the values in this list followed by those 
        of other."""
        assert(isinstance(other, LinkedList))
        out = LinkedList()
        for x in self:
            out.append(x)
        for x in other:
            out.append(x)
        return out
          
    def clear(self): 
        """Removes all elements from this list."""
        for i in reversed(range(self.length)):
            del self[i]
           
    def copy(self): 
        """Returns a new LinkedList instance (with separate Nodes), that
        contains the same values as this list."""
        out = LinkedList()
        for x in self:
            out.append(x)
        return out

    def extend(self, other): 
        """Adds all elements, in order, from other --- an Iterable --- to this list."""
        for x in other:
            self.append(x)

            
    ### iteration ###
   
    def __iter__(self):
        """Supports iteration (via `iter(self)`)"""
        n = self.head.next
        while n is not self.head:
            yield n.val
            n = n.next
