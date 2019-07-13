"""
Name: Log

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): Output the logs in console.

"""

NORMAL = 0
WARN = 1
ERROR = 2


# noinspection SpellCheckingInspection
def output(info_type=0, class_name=None, method_name=None, info=None):
    """
    introduction: Output the logs in console.
                  Format is: TIME CLASS_NAME -> METHOD_NAME: INFO.

    :param info_type: Type of information.
                      We have declared three types available now: NORMAL, WARN,
                      and ERROR. If the type is ERROR, we will end this program
                      immediately.

    :param class_name: Current class name, used to find the source of the information.
                        It is easy to get it by method "str(__name__)" in the classes you need to export logs to console.

    :param method_name: Current method name, used to find the source of the information.
                        It is easy to get it by method "str(sys._getframe().f_code.co_name)" in the classes you need to export logs to console.


    :param info: The information hat users want to display in console.
                  Type: String
    """

    if class_name == "" or method_name == "":
        string = info
    else:
        string = class_name + " -> " + method_name + " : " + info

    if info_type == NORMAL:
        # Print normal
        print(string)
    elif info_type == WARN:
        # Print yellow and high light.
        print("\033[1;32;0m" + string + "\033[0m")
        # End the program based on user selection
        choose = input(
            "Please enter whether you want to continue, 1 to continue, 0 to terminate: "
        )
        if int(choose) != 1:
            exit(1)
    elif info_type == ERROR:
        # Print red and high light.
        print("\033[1;31;0m" + string + "\033[0m")
        # End the program immediately.
        exit(1)
    else:
        # Print red and high light.
        print("\033[1;31;0m" + "Info type is wrong" + "\033[0m")
        # End the program immediately.
        exit(1)
