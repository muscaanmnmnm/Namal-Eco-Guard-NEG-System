from bin_info import BinInfo

class BinRegistry:
    def __init__(self, size=10):
        """
        Initialize hash table with fixed size buckets.
        Args:
            size (int): Number of buckets (default 10 for simulation)
        """
        self.size = size
        # Create a list of empty lists (Chains) for collision resolution
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        """
        Custom hash function: Sum of ASCII values of characters % size.
        """
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def add_bin(self, bin_obj):
        """Inserts a bin into the registry."""
        index = self._hash_function(bin_obj.bin_id)
        bucket = self.table[index]
        
        # Check if bin ID already exists and update it
        for i, (k, v) in enumerate(bucket):
            if k == bin_obj.bin_id:
                bucket[i] = (bin_obj.bin_id, bin_obj) # Update existing
                return
        
        # If not found, append to the end of the chain
        bucket.append((bin_obj.bin_id, bin_obj))

    def get_bin(self, bin_id):
        """
        Retrieves a bin object by ID in O(1) average time.
        Returns None if not found.
        """
        index = self._hash_function(bin_id)
        bucket = self.table[index]
        
        # Linear search within the specific bucket (Chain)
        for k, v in bucket:
            if k == bin_id:
                return v
        return None

    def display_registry(self):
        """Debug function to see how bins are distributed (Visualizing collisions)."""
        print("\n--- Registry Status (Hash Table Visualization) ---")
        for i, bucket in enumerate(self.table):
            print(f"Index {i}: {bucket}")