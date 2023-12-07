
import redis
from flyby.brokers.base import TaskQueue


class RQueue(TaskQueue):
    def __init__(self, url: str, namespace="flyby") -> None:
        """
        Initialize Redis Queue broker

        Args:
            url (str): redis connection url, eg: redis://localhost?db=0
            namespace (str, optional): namespace for queue names. Defaults to "flyby".
        """
        self.store = redis.Redis.from_url(url=url)
        self.namespace = namespace
        self.all_queues = f"{self.namespace}:queues"

    def enqueue(self, queue: str, param: str) -> int:
        """
        Adds a task into a queue.
        param is defined as
        { task_name: task_arguments }
        Add queue to all_queues as well.

        Args:
            queue (str): queue name
            param (str): param (json serialised)

        Returns:
            int: no. of items enqueue, i.e. 1
        """
        queue = f"{self.namespace}:{queue}"

        all_queues = self.get_all_active_queues()

        if not all_queues or queue not in all_queues:
            self.store.lpush(self.all_queues, queue)

        return self.store.rpush(queue, param)

    def dequeue(self, queue: str) -> dict:
        """
        Pops off element from the queue.
        Removes queue from all_queues if queue is empty

        Args:
            queue (str): queue name should contain namespace

        Returns:
            dict: _description_
        """
        resp = self.store.lpop(queue)
        result = resp.decode() if resp else "{}"

        l = self.store.llen(queue)
        if l == 0:
            self.remove_queue(queue)

        return result

    def reset_queue(self, queue: str) -> None:
        self.store.delete(f"{self.namespace}:{queue}")
        
    def remove_queue(self, queue: str) -> None:
        self.store.lrem(self.all_queues, 1, queue)

    def get_queue_length(self, queue: str) -> int:
        """
        gets length of the queue

        Args:
            queue (str): queue name

        Returns:
            int: length
        """
        return self.store.llen(queue)

    def get_all_active_queues(self) -> list:
        """
        returns deserialized queues in all_queues

        Returns:
            list: list of queues
        """
        all_queues = self.store.lrange(self.all_queues, 0, -1)
        all_queues = [q.decode() for q in all_queues]
        return all_queues
