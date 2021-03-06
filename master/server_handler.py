from master.scheduler import Scheduler
from common.serializer import serialize, deserialize
from master import partition

class ServerHandler:

    DEFAULT_PARTITIONS = 8
    
    def __init__(self):
        self.total_partitions = 0
        self.task_id = 0
        self.partition_id = 4
        self.task_progress = {}
        self.result = {}
        self.scheduler = Scheduler() 
        self.merger = {}

    def hand_shake(self, paritions):
        #self.total_partitions += paritions
        print("Slave Connected")

    def schedule_task(self, df, func, partitions, merger):
        self.task_id += 1
        print("Task %d Scheduled with partitions preference = %d" % (self.task_id, partitions))
        df, func, merger = deserialize(df), deserialize(func), deserialize(merger)
        task = {"df": df, "func": func, "priority": 0, "task_id": self.task_id}
        self.task_progress.setdefault(task["task_id"], {"total": 0, "progress": 0})
        splitted_task = partition.split_task(task, partitions)
        self.task_progress[task["task_id"]]["total"] += len(splitted_task) 
        if merger:
            self.merger[task["task_id"]] = merger
        self.scheduler.schedule_tasks(splitted_task)
        return self.task_id

    def submit_result(self, partition_id, res):
        print("Partition %s submitted" % partition_id)
        task_id = self.scheduler.finish_task(partition_id)
        if task_id != None:
            res = deserialize(res)
            self.task_progress[task_id]["progress"] += 1
            if task_id in self.merger:
                if task_id in self.result:
                    self.result[task_id] = self.merger[task_id](self.result[task_id], res)
                else:
                    self.result[task_id] = res
            else:
                self.result.setdefault(task_id, [])
                self.result[task_id].append(res)

    def offer_resources(self, partitions):
        assigned_tasks = self.scheduler.select_tasks(partitions)
        return serialize(assigned_tasks)

    def ready(self, task_id):
        return self.task_progress[task_id]["total"] == self.task_progress[task_id]["progress"]

    def progress(self, task_id):
        return self.task_progress[task_id]["progress"] * 100.0 / self.task_progress[task_id]["total"]

    def collect(self, task_id):
        return serialize(self.result[task_id])

