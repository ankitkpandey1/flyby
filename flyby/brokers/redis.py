import redis
from flyby.brokers.base import TaskQueue


class RQueue(TaskQueue):
    def __init__(self, url, namespace="flyby") -> None:
        self.store = redis.Redis.from_url(url=url)
        self.namespace = namespace
        self.all_queues = f"{self.namespace}:queues"

    def enqueue(self, queue, param):
        queue = f"{self.namespace}:{queue}"

        all_queues = self.get_all_active_queues()

        if not all_queues or queue not in all_queues:
            self.store.lpush(self.all_queues, queue)

        return self.store.rpush(queue, param)

    def dequeue(self, queue) -> dict:
        resp = self.store.lpop(queue)
        result = resp.decode() if resp else "{}"

        l = self.store.llen(queue)
        if l == 0:
            self.store.lrem(self.all_queues, 1, queue)

        return result

    def reset_queue(self, queue):
        self.store.delete(f"{self.namespace}:{queue}")

    def get_queue_length(self, queue):
        return self.store.llen(queue)

    def get_all_active_queues(self):
        all_queues = self.store.lrange(self.all_queues, 0, -1)
        all_queues = [q.decode() for q in all_queues]
        return all_queues
