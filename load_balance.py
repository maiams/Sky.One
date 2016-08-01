from object.instance import Instance
from object.user import User


class LoadBalance:
    def __init__(self) -> None:
        """
        Defines the LB. Its runs until all tasks are done.
        :self.instances: Array of Instance
        :self.user_connection: Array of int
        :self.ticks: int total ticks
        :self.total_cost: int total cost of execution of all instances of Instance
        """
        self.instances = []
        self.user_connection = [int(line.strip()) for line in open("input.txt", 'r')]
        self.ticks = 0
        self.total_cost = 0

    def instance_add(self, instance: Instance) -> None:
        self.instances.append(instance)

    def run(self) -> int:
        """
        Main method.
        Step 1: Add Users to Instances if possible.
        Step 2: Add Users to new Instances.
        Step 3: Run Instances.
        Step 4: Reallocation of Users when possible.
        Step 5: Remove unused Instances.
        """
        tmp_user = User()

        while self.ticks < (len(self.user_connection) + tmp_user.task_time):
            if self.ticks < len(self.user_connection):
                if self.user_connection[self.ticks] > 0:
                    ''' Step 1 '''
                    remaining_users = self.__add_user_to_running_instance(self.user_connection[self.ticks])

                    ''' Step 2 '''
                    while remaining_users > 0:
                        remaining_users = self.__add_user_to_new_instance(remaining_users)

            ''' Step 3 '''
            for instance in self.instances:
                instance.run_processes()

            ''' Step 4 '''
            self.__reallocate_user()

            ''' Step 5 '''
            for instance in self.instances:
                if instance.user_online() == 0:
                    self.instances.remove(instance)

            self.ticks += 1
            self.__log_lb()

        self.__log_lb_detailed()

        return self.ticks

    def __add_user_to_running_instance(self, user_count: int) -> int:
        for instance in self.instances:
            while instance.user_free_spots() > 0 and user_count > 0:
                instance.user_connect(User())
                user_count -= 1

        return user_count

    def __add_user_to_new_instance(self, user_count: int) -> int:
        instance = Instance()
        while instance.user_free_spots() > 0 and user_count > 0:
            instance.user_connect(User())
            user_count -= 1

        self.instance_add(instance)
        return user_count

    def __reallocate_user(self) -> None:
        for instance in self.instances:
            if instance.user_free_spots() > 0:
                for instance2 in self.instances:
                    for user in instance2.connected_user:
                        if instance != instance2:
                            if instance.user_free_spots() < instance2.user_free_spots():
                                if instance.user_connect(user):
                                    instance2.connected_user.remove(user)

    def __log_lb(self) -> None:
        output = open("output.txt", 'a')

        temp_text = ""
        for instance in self.instances:
            if instance.user_online():
                self.total_cost += 1

            temp_text += str(instance.user_online()) + ','

        temp_text = temp_text[:-1] + "\n"
        output.write(temp_text)
        output.close()

        output.close()

    def __log_lb_detailed(self) -> None:
        output = open("output.txt", 'a')
        temp_text = "\n"
        temp_text += "Total cost USD " + str(self.total_cost) + ".00"

        output.write(temp_text)

        output.close()
