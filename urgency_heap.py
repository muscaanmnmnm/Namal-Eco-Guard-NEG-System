class UrgencyHeap:
    def __init__(self):
        self.heap = []

    def insert(self, request):
        """Adds a new request and bubbles it up to correct position."""
        self.heap.append(request)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        """Removes and returns the highest priority request."""
        if not self.heap:
            return None
        
        # 1. Swap the first (max) and last element
        self._swap(0, len(self.heap) - 1)
        
        # 2. Remove the last element (which was the max)
        max_request = self.heap.pop()
        
        # 3. Sink the new root down to its correct spot
        self._heapify_down(0)
        
        return max_request

    def is_empty(self):
        return len(self.heap) == 0

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index].urgency_score > self.heap[parent_index].urgency_score:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        # Check if left child exists and is greater than current largest
        if (left_child < len(self.heap) and 
            self.heap[left_child].urgency_score > self.heap[largest].urgency_score):
            largest = left_child

        # Check if right child exists and is greater than current largest
        if (right_child < len(self.heap) and 
            self.heap[right_child].urgency_score > self.heap[largest].urgency_score):
            largest = right_child

        # If the largest is not the root, swap and continue sinking down
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]