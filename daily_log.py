from log_entry import LogEntry

class TreeNode:
    def __init__(self, entry):
        self.entry = entry
        self.left = None
        self.right = None

class DailyLog:
    def __init__(self):
        self.root = None

    def add_entry(self, timestamp, location, waste_type, amount_kg):
        """Public method to insert a new compliance log."""
        new_entry = LogEntry(timestamp, location, waste_type, amount_kg)
        if self.root is None:
            self.root = TreeNode(new_entry)
        else:
            self._insert_recursive(self.root, new_entry)

    def _insert_recursive(self, current_node, new_entry):
        # Sort by Time string (e.g., "09:00" < "14:30")
        if new_entry.timestamp < current_node.entry.timestamp:
            if current_node.left is None:
                current_node.left = TreeNode(new_entry)
            else:
                self._insert_recursive(current_node.left, new_entry)
        else:
            if current_node.right is None:
                current_node.right = TreeNode(new_entry)
            else:
                self._insert_recursive(current_node.right, new_entry)

    def generate_report(self):
        """Prints the chronological compliance report."""
        print("\n=======================================================")
        print(" NAMAL UNIVERSITY - DAILY WASTE COMPLIANCE REPORT      ")
        print("=======================================================")
        self._inorder_recursive(self.root)
        print("=======================================================")

    def _inorder_recursive(self, node):
        if node is not None:
            self._inorder_recursive(node.left)
            print(node.entry)
            self._inorder_recursive(node.right)