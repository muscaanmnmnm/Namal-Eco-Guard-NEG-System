from bin_info import BinInfo

class BinRegistry:
    def __init__(self, size=15): # Increased size for more departments
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        """
        Custom Hash: Sum of ASCII values * Position Weight
        This prevents 'AB' and 'BA' from hashing to the same slot.
        """
        hash_val = 0
        for i, char in enumerate(key):
            hash_val += ord(char) * (i + 1)
        return hash_val % self.size

    def add_bin(self, bin_obj):
        index = self._hash_function(bin_obj.bin_id)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == bin_obj.bin_id:
                bucket[i] = (bin_obj.bin_id, bin_obj)
                return
        
        bucket.append((bin_obj.bin_id, bin_obj))

    def get_bin(self, bin_id):
        index = self._hash_function(bin_id)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == bin_id:
                return v
        return None

    def display_registry(self):
        print("\n--- Bin Registry Status (Hash Table) ---")
        for i, bucket in enumerate(self.table):
            if bucket: # Only print non-empty buckets
                print(f"Slot {i}: {[bin_obj.bin_id for _, bin_obj in bucket]}")