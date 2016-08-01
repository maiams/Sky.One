class User:

    def __init__(self) -> None:
        self.task_time = 5

    def task_done(self) -> bool:
        if self.task_time >= 0:
            return False
        else:
            return True

    def task_running(self) -> None:
        self.task_time -= 1
