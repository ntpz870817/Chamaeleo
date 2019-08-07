"""
Name: Progress Monitor

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Get the progress and the time left
"""

from datetime import datetime


class Monitor:

    def __init__(self):
        self.position = -1
        self.last_time = datetime.now()

    def restore(self):
        self.__init__()

    def output(self, current_length, total_length):
        """
        introduction: Print the progress bar for required "for" sentence.

        :param current_length: Current position of the "for" sentence.
                                Type: int

        :param total_length: Total length of the "for" sentence.
                              Type: int
        """
        position = int(current_length / total_length * 100)

        if self.position < position:
            self.position = position
            string = "["
            for index in range(100):
                if position + 1 > index:
                    string += "|"
                else:
                    string += " "
            string += "]  "
            if 10 < self.position + 1 < 100:
                string += " "
            elif self.position + 1 < 10:
                string += "  "

            time_left = (datetime.now() - self.last_time).total_seconds()

            if (self.position + 1) < 100:
                string += str(position + 1) + "%, will be completed in " + str(
                    round(time_left * (100 - position) / (position + 1), 2)) + " seconds."
            else:
                string += str(position + 1) + "%, was spent " + str(round(time_left, 2)) + " seconds."

            print("\r" + string, end=" ")

            if self.position + 1 >= 100:
                print()
