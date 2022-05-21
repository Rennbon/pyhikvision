import configparser
import platform


class Config:
    SDKPath = ""
    User = "admin"
    Password = "12345"
    Port = 8000
    IP = "127.0.0.1"
    Plat = "0"  # 0-Linux，1-windows
    Suffix = ".so"

    def InitConfig(self, path):
        cnf = configparser.ConfigParser()
        cnf.read(path)
        self.SDKPath = cnf.get("DEFAULT", "SDKPath")
        self.User = cnf.get("DEFAULT", "User")
        self.Password = cnf.get("DEFAULT", "Password")
        self.Port = cnf.getint("DEFAULT", "Port")
        self.IP = cnf.get("DEFAULT", "IP")
        if platform.system() == "Windows":
            self.Plat = "1"
            self.Suffix = ".dll"
        return
