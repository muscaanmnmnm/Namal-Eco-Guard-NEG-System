class UrgencyHeap:
    def __init__(self):
        self.heap = []

    def insert(self, request):
        self.heap.append(request)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)
        max_request = self.heap.pop()
        self._heapify_down(0)
        return max_request

    def is_empty(self):
        return len(self.heap) == 0

    def peek(self):
        return self.heap[0] if self.heap else None

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index].urgency_score > self.heap[parent_index].urgency_score:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if (left_child < len(self.heap) and 
            self.heap[left_child].urgency_score > self.heap[largest].urgency_score):
            largest = left_child

        if (right_child < len(self.heap) and 
            self.heap[right_child].urgency_score > self.heap[largest].urgency_score):
            largest = right_child

        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]