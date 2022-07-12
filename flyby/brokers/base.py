from abc import ABC, abstractmethod

class TaskQueue(ABC):
    
    @abstractmethod
    def enqueue(self, queue: int, param: str)->int:
        ...
        
    @abstractmethod
    def dequeue(self, queue)->dict:
        ...
        
    @abstractmethod
    def get_queue_length(self, queue)->int:
        ...

    @abstractmethod
    def get_all_active_queues(self)->int:
        ...
        
    