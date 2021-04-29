import git
import os


class Help:

    def __init__(self):
        self.__version = None
        try:
            local_repo = git.Repo(path=os.getenv('PARENT_PATH'))
        finally:
            self.__version = local_repo.active_branch.name
        self.__name = "Frida"
        
        self.__help = {
            "usage": "python3 -m frida [FLAGS] [OPTIONS]",
            "examples": [
                "python3 -m frida -b",
                "python3 -m frida -b -c",
                "python3 -m frida -l",
                "python3 -m frida --config=config.ini -b --service=mysql_db",
                "python3 -m frida --config=config.ini -l --service=mongo_db",
                "python3 -m frida --config=config.ini -c --service=mongo_db,mysql_db",
                "python3 -m frida --config=config.ini -c --service=mongo_db,mysql_db --clear-interval=NOW",
                "python3 -m frida -c --service=mysql_service_name_2 --gateway=local --clear-gateway-except=custom.customgateway",
                "python3 -m frida -c --service=mysql_service_name_2 --clear-gateway-except"
            ],
            "flags": [
                ["-c", "--clear     ", "Clear old backups"],
                ["-b", "--backup    ", "run backup"],
                ["-l", "--list      ", "list of backup"],
                ["-h", "--help      ", "print this help"],
                ["-v", "--version   ", "print version"]
            ],
            "options": [
                ["--config                  ", "specific ini file ex. --config=/path/of/custom/fileini.ini"],
                ["--service                 ", "list of sarvice ex. --service=sevice_one,service_two"],
                ["--clear-interval          ", "Override clear interval value (alias NOW = 0) ex. --clear-interval=10 "],
                ["--gateway                 ", "Override gateway value ex. --gateway=gateway-name-one,gateway-name-two"],
                ["--clear-gateway-except    ", "Override clear gateway exception ex. --clear-gateway-except=gateway-name-one,gateway-name-two or --clear-gateway-except clear all excepions"]
            ]
        }
        pass

    def help(self):
        print(f"{self.__name} {self.__version}\n")

        print("USAGE")
        print(f'\t {self.__help.get("usage")}\n')

        print("EXAMPLE")
        for examples in self.__help.get("examples"):
            print(f"\t {examples}")

        print("FLAGS")
        for flags in self.__help.get("flags"):
            print(f"\t {flags[0]} {flags[1]} {flags[2]}")

        print("OPTIONS")
        for options in self.__help.get("options"):
            print(f"\t {options[0]} {options[1]}")

    def version(self):
        print(f"{self.__version}")
