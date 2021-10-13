class Worker:
    def __init__(self):
        self.status = 'idle'
        self.active_task = None
        self.complete_at = None

    def update_status(self, sec):
        if sec == self.complete_at:
            self.status = 'idle'
            self.active_task = None
            self.complete_at = None

a = [Worker() for _ in range(5)]
b = a[2]
print(b.status, b.complete_at, b.active_task)