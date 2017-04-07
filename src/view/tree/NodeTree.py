

class Node():
    '''
    
    '''
    def __init__(self, key, value, label=None, parent=None, leftNode=None, rightNode=None, payload=None):
        self.key = key
        self.value = value
        self.label = label
        self.parent = parent
        self.payload = payload
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.children = list()
        
    def isRoot(self):
        '''
        Is this node the root of a tree?
        Returns: 
            true if root, false if not
        '''
        return self.parent == None
    
    def hasLeftSibling(self):
        '''
        Has this node any neighbour nodes to its left?
        Returns:
            leftNode 
        '''
        return self.leftNode
        
    def hasRightSibling(self):
        '''
        Has this node any neighbour nodes to its right?
        Returns:
            rightNode
        '''
        return self.rightNode

    def hasChildren(self):
        '''
        Has this node any children at all?
        
        Returns:
            true if it has children
        ''' 
        hasChildren = False    
        if len(self.children) > 0:
            hasChildren = True
        return hasChildren  
    
    def equal(self):
        '''
        Compares two trees. The `==' equality operator will be used for the data fields
        Parameters:
            tree the other tree
        Returns:
            true if the trees have identical data / number of children
        '''
        pass

    

    def destroyAt(self, pos):
        '''
        Destroy the subtree at a particular position.
        
        Parameters:
            pos     the position
        retruns:
             removes and returns the Node at the given index. 
             
        '''
        return self.children.pop(pos)
    
    def position(self):
        '''
        Returns the position of this node in the parent node.
        
        Returns:
            the position in the parent node, 0 if this is a root node
        '''
        pos = None
        if self.isRoot():
            pos = 0
        else:
            pos = 1
            node = self
            while node.hasLeftSibling():
                node = node.leftNode
                pos = pos + 1
        return pos 
    

    
    def card(self):
        '''
        Returns the number of nodes.
        
        Returns:
        the number of nodes
        '''
        return

    def clone(self):
        '''
        Produce a copy of this tree. The data fields will be copied.
        
        Returns:
            the copy
        '''
        pass
    
    def appendAt(self, position, node):
        '''
        inserts the element at the given position, shifting node to the right.
        
        Parameters:
            pos     the position
            tree     the tree
        Exceptions:
            invalid_argument     if the tree has a different aryness from this
            invalid_argument     if the position is not empty
        '''
        
        self.children.insert(position, node)
    


    def childAt(self, position):
        '''
        Return a reference to the node/subtree at a particular position.
        
        Parameters:
            pos the position
        Returns:
            the subtree
        Exceptions:
            invalid_argument if the given position is empty
        '''
        pass

    def isLeaf(self):
        return len(self.children) == 0
    
    def addChild(self, node):
        self.children.append(node)
        
    def addLeftNode(self, node):
        self.children.append(node)
        
    def addRightMostNode(self, node):
        lastNode = node.parent.children[-1]
        lastNode.rightNode = node
        node.leftNode = lastNode


if __name__ == '__main__':
    
    root = Node(0, 'zero', label='Connection', parent=None)
    c1 = Node(1, 'one', label='db1', parent=root)
    c1.leftNode = Node(2, 'two', label='db2', parent=root)
    root.addRightMostNode(c1)
    print(root)
    pass
