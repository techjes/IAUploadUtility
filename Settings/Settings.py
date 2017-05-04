
import os.path, sys, tkinter.constants
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

class Settings:
    """Contains functions and variables related to program settings"""
    def __init__(self):
        self.__logfolderpath__ = None
        self.__processed_logs__ = None
        self.__server_address__ = None
        self.__username__ = None
        self.__password__ = None
        self.window = None
        self.log_var = None
        self.processed_var = None
        self.__settings_path__ = sys.path[0]+'\\Settings.cfg'
        #Holds username and password, suggest hashing in the future
        self.__loguser_path__ = sys.path[0]+'\\LogUser.cfg'
        self.__load_settings__()
        self.__load_userpass__()

    def __check_files_exist__(self):
        if not os.path.isfile(self.__settings_path__):
            try:
                with open(self.__settings_path__, 'w+') as settings_file:
                    settings_file.write(sys.path[0])
                    settings_file.write("\n" + sys.path[0])
                    settings_file.write("Change.To.Server.Path")
            except IOError:
                pass
        if not os.path.isfile(self.__loguser_path__):
            try:
                with open(self.__loguser_path__, 'w+') as createfile:
                    createfile.write("")
            except IOError:
                pass

    def __load_settings__(self):
        """loads the log folder and the processed folder from cfg files"""
        self.__check_files_exist__()
        ls = None
        try:
            with open(self.__settings_path__, 'r') as sett:
                sett.seek(0)
                self.__logfolderpath__ = sett.readline().rstrip()
                self.__processed_logs__ = sett.readline().rstrip()
                self.__server_address__ = sett.readline().rstrip()

        except IOError as i:
            print(i)

    def __load_userpass__(self):
        #ToDo: Hashing logic should go here
        try:
            with open(self.__loguser_path__, 'r') as userpass:
                userpass.seek(0)
                self.__username__ = userpass.readline().rstrip()
                self.__password__ = userpass.readline().rstrip()
        except IOError as i:
            print(i)

    def __browse_logs__(self):
        path = askdirectory(title='Logs Directory', mustexist=TRUE)
        if path is not "":
            self.log_var.set(path)
    
    def __browse_processed__(self):
        path = askdirectory(title='Processed logs',mustexist=TRUE)
        if path is not "":
            self.processed_var.set(path)

    def __confirm_save__(self):
        if askyesno(title="Confirm Settings", message="Would you like to save these changes?"):
            self.set_log_path(self.log_var.get())
            self.set_processed_path(self.processed_var.get())
            self.window.destroy()

    def __load_widgets__(self):
        middle_frame = Frame(self.window)
        bottom_frame = Frame(self.window)
        lbl_log = Label(self.window, text='Log File Directory')
        lbl_process = Label(middle_frame, text='Uploaded Logs Directory')
        log_path_entry = Entry(self.window, textvariable=self.log_var, width=50)    
        processed_path_entry = Entry(middle_frame, textvariable=self.processed_var, width=50)
        browse_log = Button(self.window, text='Browse', command=self.__browse_logs__, width=10, height=5)    
        browse_processed = Button(middle_frame, text='Browse,', command=self.__browse_processed__, width=10, height=5)
        cancel_button = Button(bottom_frame, text='Cancel', command=self.window.destroy, width=25, height=5)
        save = Button(bottom_frame, text='Save', command=self.__confirm_save__, width=25, height=5)

        bottom_frame.pack(side=BOTTOM, fill=X)
        middle_frame.pack(side=BOTTOM, fill=X)
        browse_log.pack(side=RIGHT)
        browse_processed.pack(side=RIGHT)
        lbl_log.pack(side=LEFT, expand=TRUE)
        lbl_process.pack(side=LEFT, expand=TRUE)
        log_path_entry.pack(side=RIGHT)
        processed_path_entry.pack(side=RIGHT)
        save.pack(side=RIGHT)
        cancel_button.pack(side=LEFT)

    def launch(self):
        """Launches the settings window"""
        self.window = Toplevel()
        self.window.minsize(500, 100)
        
        self.log_var = StringVar()
        self.processed_var = StringVar()

        self.__load_widgets__()

        self.window.grab_set()
        self.log_var.set(self.__logfolderpath__)
        self.processed_var.set(self.__processed_logs__)

    def get_log_path(self):
        """Returns the log folder path"""
        return self.__logfolderpath__
    def get_processed_folder(self):
        """Returns the folder for processed logs"""
        return self.__processed_logs__

    def get_server_address(self):
        """Returns current server address"""
        return self.__server_address__

    def set_log_path(self, new_path):
        """Sets a new path to the logs folder and saves it to the config file"""
        self.__logfolderpath__ = new_path
        s = open(self.__settings_path__, 'r+')
        lines = s.readlines()
        s.close()
        s = open(self.__settings_path__, 'w')
        lines[0] = new_path
        for i in lines:
            s.write(i+"\n")
        s.close()
    def set_processed_path(self, new_path):
        """Sets a new path to the processed logs folder and saves it to the config file"""
        self.__processed_logs__ = new_path
        s = open(self.__settings_path__, 'r+')
        lines = s.readlines()
        s.close()
        s = open(self.__settings_path__, 'w')
        lines[1] = new_path
        for i in lines:
            s.write(i)
        s.close()

    def set_server_address(self, new_path):
        """Sets the server address and writes to config file"""
        self.__server_address__ = new_path
        s = open(self.__settings_path__, 'r+')
        lines = s.readlines()
        s.close()
        s = open(self.__settings_path__, 'w')
        lines[2] = new_path
        for i in lines:
            s.write(i)
        s.close()
    def get_username(self):
        """returns current username"""
        return self.__username__
    
    def get_password(self):
        """Returns current password"""
        return self.__password__

    def set_login_info(self, username, password):
        """Writes the new username and password to the LogUser.cfg file"""
        #ToDo: Hashing logic should go here
        s = open(self.__loguser_path__, 'r')
        lines = s.readlines()
        s.close()
        s = open(self.__loguser_path__, 'w')
        s.seek(0)
        if len(lines) is not 0:
            lines[0] = username
            lines[1] = password
            for i in lines:
                s.write(i+"\n")
        else:
            s.write(username+"\n")
            s.write(password)
        s.close()




