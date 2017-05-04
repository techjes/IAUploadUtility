"""Functions related to uploading to the ftp server are contained here"""
from ftplib import FTP
import re
import os
import datetime

class FTPConnect:
    """This class defines easy methods for connecting to the server"""
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.ftps = FTP(self.server)
        self.seen = set()
        self.seen_count = 1
        self.new_names = []
    def __rename_file__(self, file):
        try:
            log_file = open(file, 'r')
            success = True
        except IOError as ex:
            print('%s') % ex
            pass
        while success:
            lineRead = log_file.readline()
            if 'MSG' not in lineRead:
                lineRead = log_file.readline()
            else:
                container = re.search('(( ([0-9]{8})){3})', lineRead)
                if container != None:
                    success = False
                    file_name = (container.group(1)+ " " +
                                 datetime
                                 .datetime
                                 .fromtimestamp(os.path.getmtime(file))
                                 .strftime('%Y-%m-%d %H:%M:%S' + ".log"))
                    
                    if file_name in self.seen:
                        file_name = self.__insert_string__(file_name, (len(file_name)-4), self.seen_count)
                        self.seen_count += 1
                    self.seen.add(file_name)
                    self.new_names.append(file_name)
                    return file_name

    def __insert_string__(self, string, index, number):
        self.seen_count += 1
        return string[:index] + "copy"+str(number) + string[index:]
    def connect(self):
        """Establishes connection to server"""
        try:
            self.ftps.login(self.username, self.password)
            self.ftps.cwd("Logs")
            return True
        except Exception as ex:
            print("Connection Failed : %s" % ex)
            return False

    def upload_file(self, file):
        """Uploads the given file"""
        new_name = self.__rename_file__(file)
        with open(file, 'rb') as f:
            self.ftps.storbinary('STOR %s' % new_name, f)

    