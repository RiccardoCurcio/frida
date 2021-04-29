class Help:

    def __init__(self):
        self.__name = "Backup"
        self.__version = "develop"
        self.__help = {
            "usage": "python3 main.py [FLAGS] [OPTIONS]",
            "examples": [
                "python3 main.py -b",
                "python3 main.py -b -c",
                "python3 main.py -l",
                "python3 main.py --config=config.ini -b --only=mysql_db",
                "python3 main.py --config=config.ini -l --only=mongo_db",
                "python3 main.py --config=config.ini -c --only=mongo_db,mysql_db"
                "python3 main.py --config=config.ini -c --only=mongo_db,mysql_db --clear-interval=NOW"
            ],
            "flags": [
                ["-c", "--clear     ", "Clear old backups"],
                ["-b", "--backup    ", "run backup"],
                ["-l", "--list      ", "list of backup"],
                ["-h", "--help      ", "print this help"],
                ["-v", "--version   ", "print version"]
            ],
            "options": [
                ["--config            ", "specific ini file --config=/path/of/custom/fileini.ini"],
                ["--only              ", "list of sarvice --only=sevice_one,service_two"],
                ["--clear-interval    ", "Override clear interval value (alias NOW = 0) --clear-interval=10 "]
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
