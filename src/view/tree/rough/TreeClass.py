
class TreeNode(object):
    '''
    standard node class.
    '''
    def __init__(self, key, val, label=None, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.label = label
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        
    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

class TreeNodeUtil():            
    def minDepth(self, root):
        # Corner Case.Should never be hit unless the code is 
        # called on root = NULL
        if root is None:
            return 0
         
        # Base Case : Leaf node.This acoounts for height = 1
        if root.leftChild is None and root.rightChild is None:
            return 1
         
        # If left subtree is Null, recur for right subtree
        if root.leftChild is None:
            return self.minDepth(root.rightChild) + 1
         
        # If right subtree is Null , recur for left subtree
        if root.rightChild is None:
            return self.minDepth(root.leftChild) + 1
         
        return min(self.minDepth(root.leftChild), self.minDepth(root.rightChild)) + 1
                    
class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self,key,val):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1
    
    def _put(self,key,val,currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,val,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val,parent=currentNode)
                
    def __setitem__(self,k,v):
        self.put(k,v)
        
    def get(self,key):
        if self.root:
            res = self._get(key,self.root)
            if res:
                    return res.payload
            else:
                    return None
        else:
            return None

    def _get(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key,currentNode.leftChild)
        else:
            return self._get(key,currentNode.rightChild)
    
    def __getitem__(self,key):
        return self.get(key)

    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    def delete(self,key):
        if self.size > 1:
            nodeToRemove = self._get(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')
    
    def __delitem__(self,key):
        self.delete(key)
    
    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                    self.parent.leftChild = None
            else:
                    self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                    if self.isLeftChild():
                        self.parent.leftChild = self.leftChild
                    else:
                        self.parent.rightChild = self.leftChild
                    self.leftChild.parent = self.parent
            else:
                    if self.isLeftChild():
                        self.parent.leftChild = self.rightChild
                    else:
                        self.parent.rightChild = self.rightChild
                    self.rightChild.parent = self.parent
    
    def findSuccessor(self):
        
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ
    
    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current
    
    def remove(self,currentNode):
        if currentNode.isLeaf(): #leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): #interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        
        else: # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                       currentNode.leftChild.payload,
                                       currentNode.leftChild.leftChild,
                                       currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                       currentNode.rightChild.payload,
                                       currentNode.rightChild.leftChild,
                                       currentNode.rightChild.rightChild)
                    
if __name__=='__main__':
    print('main')
    binarySearchTree= BinarySearchTree()
    print(binarySearchTree.length())
    root = TreeNode(0, 'root', label='connections')
    root.leftChild = TreeNode(1,'child-0', label='con1', parent=root)
    root.leftChild.rightChild = TreeNode(2, 'child-2', label='con2', parent=root.leftChild)
#     n3 = TreeNode(3, 'child-3', label='con3', parent=n2)
#     n3 = TreeNode(3, 'child-3', label='con3', parent=n3)
    
    print(TreeNodeUtil().minDepth(root))
#     print(root.to_dict())