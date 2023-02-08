#/usr/bin/env python

## An implementation for a priorityqueue
class PQ:
    def __init__(self):
        ## H contains pairs of the form (value, key)
        self.H = []
        ## Using index i we can access a pair as follows
        ## H[i] = (value, key)
        self.Index = {}

    def __contains__(self, key):
        if key in self.Index and self.Index[key] > 0:
            return True
        return False

    def empty(self):
        if len(self.H) > 0:
            return False
        return True
    
    ## Done = true if the key has been used before, but is no longer in use
    def done(self,key):
        if key in self.Index and self.Index[key] < 0:
            return True
        return False

    ## Push a pair (value, key) into the priority queue
    def push(self,a):
        key = a[1]
        value = a[0]
        if self.done(key):
            raise Exception("Error, re-insert")
        if key in self:
            self.update(a)
            return
        i = len(self.H)
        self.H.append(a)
        while i > 0:
            j = (i-1)/2
            if self.H[j] > a:
                self.H[i] = self.H[j]
                oldkey = self.H[i][1]
                self.Index[oldkey] = i
                self.H[j] = a
                i = j
            else:
                break
        self.Index[key] = i

    def pop(self):
        togo = self.H[0]
        a = self.H.pop()
        key = a[1]
        if a == togo:
            self.Index[key] = -1
            return a
        self.H[0] = a
        i = 0
        while (2*i + 1) < len(self.H):
            left = 2*i + 1
            right = 2*i + 2
            if self.H[left] < a:
                ## left is the smallest; left becomes the new i 
                if right >= len(self.H) or self.H[right] > self.H[left]:
                    self.H[i] = self.H[left]
                    self.H[left] = a
                    l_key = self.H[i][1]
                    self.Index[l_key] = i
                    i = left
                    continue
            if right < len(self.H) and self.H[right] < a:
                self.H[i] = self.H[right]
                self.H[right] = a
                r_key = self.H[i][1]
                self.Index[r_key] = i
                i = right
                continue
            break
        self.Index[a[1]] = i
        self.Index[togo[1]] = -1
        return togo

    def update(self, a):
        value = a[0]
        key = a[1]
        i = self.Index[key]
        oldvalue = self.H[i][0]
        oldkey = self.H[i][1]
        if oldvalue == value:
            return
        elif oldvalue < value:
            print "inserting " + str(a)
            print "found at index " + str(i)
            print "and the item is " + str(self.H[i])
            raise Exception("key value increase not allowed")

        self.H[i] = a 
        ## Decrease priority, i.e., move up
        while i > 0:
            j = (i-1) / 2
            if self.H[j] <= a:
                self.Index[key] = i
                return
            self.H[i] = self.H[j]
            self.H[j] = a
            nkey = self.H[i][1]
            self.Index[nkey] = i
            i = j
        self.Index[key] = 0
        ## Increase priority: Not allowed:
 
