import tkinter.constants
import threading
from tkinter import *
from tkinter.messagebox import askyesno
from Settings.Settings import *
from Upload.UpFunc import *
from os import listdir
from os.path import isfile, join
#connect = FTPConnect("home200935066.1and1-data.host")

class Main:
    def __init__(self):
        self.top = Tk()
        self.settings = Settings()
        self.server_var = None
        self.username_var = None
        self.password_var = None
        self.connect_window = None
        self.text_output = None
        self.__logs__ = []
    def __confirm_save__(self):
        if askyesno(title="Confirm Settings", message="Would you like to save these changes?"):
            self.settings.set_login_info(self.username_var.get(), self.password_var.get())
            self.settings.set_server_address(self.server_var.get())
            self.connect_window.destroy()

    def __load_connect_widgets__(self):
        frame_top = Frame(self.connect_window)
        frame_mid = Frame(self.connect_window)
        frame_bot = Frame(self.connect_window)
        lbl_server = Label(frame_top, text="Server Address")
        lbl_username = Label(frame_mid, text='Username')
        lbl_password = Label(frame_bot, text='Password')
        entry_server = Entry(frame_top, textvariable=self.server_var, width=50)
        entry_username = Entry(frame_mid, textvariable=self.username_var, width=50)
        entry_password = Entry(frame_bot, textvariable=self.password_var, exportselection=0, show='*', width=50)
        btn_save = Button(self.connect_window, text='Save', command=self.__confirm_save__, width=25, height=5)
        btn_cancel = Button(self.connect_window, text='Cancel', command=self.connect_window.destroy, width=25, height=5)

        frame_top.pack(side=TOP)
        frame_mid.pack(side=TOP)
        frame_bot.pack(side=TOP)
        lbl_server.pack(side=LEFT)
        lbl_username.pack(side=LEFT)
        lbl_password.pack(side=LEFT)
        entry_server.pack(side=RIGHT, expand=TRUE)
        entry_username.pack(side=RIGHT, expand=TRUE)
        entry_password.pack(side=RIGHT, expand=TRUE)
        btn_save.pack(side=RIGHT)
        btn_cancel.pack(side=LEFT)

    def __get_log_files__(self):
        self.text_output.delete(0.0, 255.255)
        self.text_output.insert(INSERT, "Scanning folder for files...\n")
        path = self.settings.get_log_path()
        logs = [a for a in listdir(path) if isfile(join(path, a))]
        self.text_output.insert(INSERT, str(len(logs)) + " files retrieved\n")
        self.text_output.insert(INSERT, "Press Upload File(s) to continue\n")
        self.__set_logs__(logs)
        return logs

    def __set_logs__(self, logs):
        for i in logs:
            self.__logs__.append(self.settings.get_log_path() + "/" + i)
        print(self.__logs__)

    def __check_settings__(self):
        if self.settings.get_log_path() is sys.path[0]:
            return "Warning! Log folder path has not been set up. Please change the folder path in settings."
        return "Press \"Prepare Files\" to begin"

    def __upload_files__(self):
        if len(self.__logs__) > 0:
            serve = self.settings.get_server_address()
            user = self.settings.get_username()
            passwo = self.settings.get_password()
            upload = FTPConnect(serve, user, passwo)
            self.text_output.insert(INSERT, "Attempting to connect...\n")
            result = upload.connect()
            if result:
                self.text_output.insert(INSERT, "Connection Successful!\n")
                for log in self.__logs__:
                    upload.upload_file(log)
                    self.text_output.insert(INSERT, "Log successfully uploaded.\n")
                self.__move_files(upload.new_names)
                upload.ftps.close()
            else:
                self.text_output.insert(INSERT, "Connection has failed!\n")
                self.text_output.insert(INSERT, "Check connection settings!\n")
        else:
            self.text_output.insert(INSERT, "There are no files ready to be uploaded!\n Either press \"Prepare Files\" or check the log folder path settings")

    def __move_files(self, new_names):
        for i in range(len(self.__logs__)):
            os.rename(self.__logs__[i], self.settings.get_processed_folder()+ "/" + new_names[i].replace(" ", "", 1).replace(":", "-"))
        self.__logs__.clear()
    def run(self):
        """Main Loop"""

        frame = Frame(self.top)
        bottom_frame = Frame(frame, bg='darkgrey')
        settingsbutton = Button(bottom_frame, text='Settings', width=25, height=5, command=self.settings.launch)
        connection_button = Button(bottom_frame,text="Connection Settings", width=25, height=5, command=self.connect_settings)
        btn_get_files = Button(bottom_frame, text='Prepare Files', width=25, height=5, command=self.__get_log_files__)
        uploadbutton = Button(bottom_frame, text='Upload File(s)', width=25, height=5, command=self.__upload_files__)
        self.text_output = Text(frame)

        self.text_output.insert(0.0, self.__check_settings__())

        frame.pack()
        bottom_frame.pack(side=BOTTOM, fill=X)
        settingsbutton.pack(side=LEFT)
        connection_button.pack(side=LEFT)
        btn_get_files.pack(side=LEFT)
        uploadbutton.pack(side=RIGHT)
        self.text_output.pack(side=TOP)

        self.top.mainloop()

    def connect_settings(self):
        """Loads the connection settings window"""
        self.connect_window = Toplevel()
        self.connect_window.minsize(500, 100)
        self.server_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()

        self.__load_connect_widgets__()

        self.connect_window.grab_set()
        self.server_var.set(self.settings.get_server_address())
        self.username_var.set(self.settings.get_username())
        self.password_var.set(self.settings.get_password())

    
        
run = Main()
run.run()
