# Flyby
Flyby is an open source library which allows distributed task processing with dynamic queues.

## Dynamic Queues
Consider the following problem:
There are ticket counters for flights A,B, and C. Ticket counters are exactly identical except that they serve tickets for their respective flights.
Ticket counter can be defined as function get_ticket(flight)->Ticket. Depending on flight param, it will return Ticket object.
When counters are opened, consider the following scenario: 
Person 1 wants ticket A, Person 2 wants ticket A, Person 3 wants ticket B and Person 4 wants ticket A again.
In above cases, the queus look like: Queue A: Person 1, Person 2, Person 4, Queue B: Person 3

We can note following points from the above example:
1. Queue length can grow/shrink. We can add more flights or reduce as per need, anytime.
2. If there is no one waiting for at a counter, there is no need of the corresponding queue.
3. Functions performed (ticket counter) isn't tightly coupled with a queue.
4. Finally, we need a queue. If `n` number of tasks are needed to be performed, they need to be performed sequentially.

All of the above are supported by Flyby.
1. Enqueue any operation by enqueue(queue name, task: payload)
2. Map task with some function.
3. Task will get picked up (FIFO) from queue (as given in queue name) and process the payload.
4. Queues will get created, appended and deleted (if empty), all handled by flyby runtime.

## What do I need?
Flyby version 1.0 runs on,
<ul>
<li> Python (3.7, 3.8, 3.9, 3.10) </li>
<li> PyPy3.7 (7.3.7+) </li>
</ul>
Flyby is usually used with a message broker to send and receive messages. Currently, only redis is supported as message broker.
Broker,
<ul>
<li> Redis 6.0+ </li>
</ul>

## Get Started

Use sample_project given in repo to get used to bits and bolts of Flyby.

## Flyby 

Enqueue task by:
```python
from flyby.brokers.redis import RQueue

task_queue = RQueue(REDIS_URL)

def api_function():
    task_name = 'task'
    task_args = 'hello_world'
    param = {task_name: task_args}
    # param should be in format: {task_name: task_args(json)}
    # queue name can be anything
    queue='writer_1'
    task_queue.enqueue(queue=queue, param=json.dumps(param))
```
Create an env file:
```ini
# .env
REDIS_HOST=localhost # redis host
REDIS_PORT=6379
REDIS_DB=1
LOG_LOCATION=flyby.log # log location
```

Define a tasks.py which maps task_name with a corresponding function
```python
# some_module/tasks.py
def task(text_to_write: str):
    file = open('myfile.txt', 'w')
    # simply write input text to file
    file.write(text_to_write)
    file.close()
# map function with corresponding name which is used for enqueuing
# the task
task_config = {
    'task': task
}

```

Run the worker:
```shell
flyby some_module --config .env
```

Sample systemd service file:
```ini
[Unit]
Description=Flyby 
After=network.target

[Service]
PIDFile=/home/ubuntu/locks/flyby.pid
User=ubuntu
Group=ubuntu

WorkingDirectory=/home/ubuntu/some_module

StandardOutput=append:/home/ubuntu/logs/flyby_std.log
StandardError=append:/home/ubuntu/logs/flyby_err.log

ExecStart=/home/ubuntu/some_module/venv/bin/flyby some_module --config .env
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

## Installation

You can install Flyby from the source.

Install dependencies using pip:

    pip install -U setuptools

Run the setup:

    python setup.py install

## License
This software is licensed under the LGPL-2.1 License.