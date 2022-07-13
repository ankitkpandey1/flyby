# Flyby
Flyby is open source library which allows distributed task processing with dyanmic queues.

# Dynamic Queues
Consider following problem:
There are ticket counters for fights A,B,C. Each ticket counters are exactly identical except that they serve ticket for given three fights.
Ticket counter can be defined as function get_ticket(flight)->Ticket. Depending on flight param, it will return Ticket object.
When counters are opened, there are followng peoples: 
Person 1 wants ticket A, Person 2 wants ticket A, Person 3 wants ticket B and Person 4 wants ticket A again.
In above cases, queue look like: Queue A: Person 1, Person 2, Person 4, Queue B: Person 3

We can note following points from above example:
1. Queue length can grow/shrink. We can add more flights or reduce it as per as need, anytime.
2. If there is no one waiting for queue (empty), there is no need to setup a counter.
3. Functions performed (ticket counter) isn't tightly coupled with queue.
4. Finally, we need a queue. If n numbers of tasks are needed to performed, they should be performed sequentially.

All of the above are supported by Flyby.
1. Enqueue any data by enqueue(queue name, task: payload)
2. Map task with some function.
3. Task will pick up (FIFO) from queue (as given in queue name) and process the payload.
4. Queues will get created, appended and deleted (if empty), all handled by flyby runtime.
