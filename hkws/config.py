import configparser

from hkws.core import env


class Config:
    SDKPath = ""
    User = "admin"
    Password = "12345"
    Port = 8000
    IP = "127.0.0.1"
    Suffix = ".so"

    def InitConfig(self, path):
        cnf = configparser.ConfigParser()
        cnf.read(path)
        self.SDKPath = cnf.get("DEFAULT", "SDKPath")
        self.User = cnf.get("DEFAULT", "User")
        self.Password = cnf.get("DEFAULT", "Password")
        self.Port = cnf.getint("DEFAULT", "Port")
        self.IP = cnf.get("DEFAULT", "IP")
        if env.isWindows():
            self.Suffix = ".dll"
        return
