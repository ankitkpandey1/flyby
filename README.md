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
