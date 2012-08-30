import sys
class Counter(object):
    def __init__(self):
        self.cnt= 0
    
    def add(self, n=1):
        self.cnt+=n

    def __repr__(self):
        return repr(self.cnt)

class Int(int):
    def __new__(cls, number, counter, history):
        return super(Int, cls).__new__(cls, number)

    def __init__(self, number, counter, history):
        self.counter= counter
        self.history= history
        
        int.__init__(self)

    def __cmp__(self, other):
        self.counter.add()
        self.history.append('cmp')
        return super(Int, self).__cmp__(other)

class List(list):
    def __init__(self, *args, **kwargs):
        self.counter= kwargs.pop('counter', Counter())
        self.history= kwargs.pop('history', [])

        super(List, self).__init__(*args, **kwargs)

    @classmethod
    def from_list(cls, l):
        counter= Counter()
        history= []
        for i, e in enumerate(l):
            l[i]= Int(e, counter, history)

        l= cls(l, counter=counter, history= history)
        return l

    def crear_temporal(self, size=None):
        self.counter.add(len(self))
        self.history.extend(['cmp' for k in xrange(len(self))])
        if size is None: size=len(self)
        return List(range(size), counter= self.counter, history=self.history)

    def __getitem__(self, i):
        self.history.append(('read', i))
        self.counter.add()
        return super(List, self).__getitem__(i)

    def __setitem__(self, i, v):
        self.history.append(('write', i, v))
        super(List, self).__setitem__(i, v)
        self.counter.add()
        return v

    def __getslice__(self, i, j):
        if j == sys.maxint: j=len(self)
        self.counter.add(j-i)
        self.history.extend(['cmp' for k in xrange(j-i)])
        return List(super(List, self).__getslice__(i, j), counter=self.counter, history=SliceHistory(i, self.history))

class SliceHistory(list):
    def __init__(self, i, l):
        self.i= i
        self.l= l
    
    def append(self, e):
        if isinstance(e, tuple):
            e= list(e)
            e[1]+= self.i
            e= tuple(e)
        self.l.append(e)


