def maxDepth(self, root):
    """
    :type root: TreeNode
    :rtype: int
    """
    return self.solve(root)


def solve(self, root, depth=0):
    if root == None:
        return depth
    return max(self.solve(root.left, depth + 1), self.solve(root.right, depth + 1))