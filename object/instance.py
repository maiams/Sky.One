from object.user import User


class Instance:
    def __init__(self) -> None:
        """
        Defines the max_user, min_user and connected_user
        """
        self.max_user = 10
        self.min_user = 1
        self.connected_user = []

    def user_connect(self, user: User) -> bool:
        if len(self.connected_user) < self.max_user:
            self.connected_user.append(user)
            return True
        else:
            return False

    def user_disconnect(self, user: User) -> None:
        self.connected_user.remove(user)

    def user_online(self) -> int:
        return len(self.connected_user)

    def user_free_spots(self) -> int:
        return self.max_user - len(self.connected_user)

    def run_processes(self) -> int:
        max_task_time = 0
        for user in self.connected_user:
            user.task_running()
            if user.task_time > max_task_time:
                max_task_time = user.task_time

            if user.task_done():
                self.user_disconnect(user)

        return max_task_time


