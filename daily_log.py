from log_entry import LogEntry

class TreeNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = None
        self.right = None

class DailyLog:
    def __init__(self):
        self.root = None

    def add_entry(self, timestamp, location, amount_kg):
        """Public method to insert a new log."""
        new_entry = LogEntry(timestamp, location, amount_kg)
        if self.root is None:
            self.root = TreeNode(new_entry)
        else:
            self._insert_recursive(self.root, new_entry)

    def _insert_recursive(self, current_node, new_entry):
        """Recursive helper to find the correct spot in the tree."""
        if new_entry.timestamp < current_node.entry.timestamp:
            # Go Left (Earlier time)
            if current_node.left is None:
                current_node.left = TreeNode(new_entry)
            else:
                self._insert_recursive(current_node.left, new_entry)
        else:
            # Go Right (Later time)
            if current_node.right is None:
                current_node.right = TreeNode(new_entry)
            else:
                self._insert_recursive(current_node.right, new_entry)

    def generate_report(self):
        """
        Performs an In-Order Traversal (Left -> Root -> Right).
        This prints the logs in perfect chronological order.
        """
        print("\n--- Daily Waste Collection Report (Sorted by Time) ---")
        self._inorder_recursive(self.root)
        print("------------------------------------------------------")

    def _inorder_recursive(self, node):
        if node is not None:
            self._inorder_recursive(node.left)  # Visit earlier times
            print(node.entry)                   # Visit current
            self._inorder_recursive(node.right) # Visit later times