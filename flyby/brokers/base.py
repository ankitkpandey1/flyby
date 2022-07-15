from abc import ABC, abstractmethod


class TaskQueue(ABC):
    """
    TaskQueue Abstract interface
    """
    @abstractmethod
    def enqueue(self, queue: str, param: str) -> int:
        """
        Allow enqueuing of tasks

        Args:
            queue (str): queue name
            param (str): task params

        Returns:
            int: no of task enqueued
        """
        ...

    @abstractmethod
    def dequeue(self, queue: str) -> dict:
        """
        Allow poping off elements from the queue

        Args:
            queue (str): queue name

        Returns:
            dict: payload
        """
        ...

    @abstractmethod
    def get_queue_length(self, queue: str) -> int:
        """
        Returns queue length

        Args:
            queue (str): queue name

        Returns:
            int: number of tasks in the queue
        """
        
        ...

    @abstractmethod
    def get_all_active_queues(self) -> list:
        """
        Returns list of active queues

        Returns:
            list: active queues
        """
        ...
