import os
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# You can add more extensions to this dictionary
dictionary_of_extension = {
    'Documents': ('.pdf', '.doc', '.xls', 'txt', '.csv', '.zip', '.xml',
                  '.zip', '.docx', '.DOCX', '.odt'),
    'Photos': ('.jpg', '.jpeg', '.png', '.JPG'),
    'Videos': ('.mp4', '.mkv', '.3gp', '.flv', '.mpeg'),
    'Audios': ('.mp3', '.wav', '.m4a'),
    'Programs': ('.py', '.cpp', '.c', '.sh', '.js'),
    'App': ('.exe', '.apk'),
}

# Declaring a global variable
browsed = False


class File_Organizer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("1280x800+0+0")
        self.root.config(bg="white")

        # =================Menu Bar=================
        self.menu = Menu(root, bg="light yellow")
        self.file = Menu(self.menu, tearoff=0)
        self.file.add_command(label='Open Folder', command=self.Open_Folder)
        self.file.add_command(label='Exit', command=self.Exit)

        self.help = Menu(self.menu, tearoff=0)
        self.help.add_command(label='Help', command=self.Help_Fuction)
        self.help.add_command(label='About', command=self.About_Fuction)

        self.menu.add_cascade(label='File', menu=self.file)
        self.menu.add_cascade(label='Help', menu=self.help)
        root.config(menu=self.menu)
        # ==========================================

        # =============Left Side Frame==============
        self.frame1 = Frame(self.root, bg="cyan")
        self.frame1.place(x=0, y=0, width=450, relheight=1)

        label1 = Label(self.frame1, text="File Organizer",
                       font=("times new roman", 25, "bold"), bg="cyan", fg="red").place(x=100, y=300)
        label2 = Label(self.frame1, text="Organize your messy folder",
                       font=("times new roman", 18, "bold"), bg="cyan", fg="blue").place(x=70, y=350)

        # ===========Right Sight Frame=============
        self.frame2 = Frame(self.root, bg="light yellow")
        self.frame2.place(x=450, y=0, relheight=1, relwidth=1)

        self.label3 = Label(self.frame2, text="Please choose the folder",
                            font=("times new roman", 30, "bold"), bg="light yellow", fg="black").place(x=170, y=80)
        self.path = Label(self.frame2, text="You Have Chosen: ",
                          font=("times new roman", 15, "bold"), bg="light yellow", fg="black").place(x=70, y=170)
        self.label4 = Label(self.frame2, text="Nothing!",
                            font=("times new roman", 15, "bold"), bg="light yellow", fg="red")
        self.label4.place(x=270, y=170)

        # ==================Buttons===============
        self.login_button = Button(self.frame2, text="Choose folder",
                                   command=self.Open_Folder, font=("times new roman", 15, "bold"), bd=0, cursor="hand2",
                                   bg="black", fg="white").place(x=280, y=230, width=150)

        self.sumbit = Button(self.frame2, text="Submit", command=self.action,
                             font=("times new roman", 15, "bold"), bd=0, cursor="hand2", bg="blue",
                             fg="white").place(x=280, y=630, width=150)

    def Help_Fuction(self):
        messagebox.showinfo("Help", "Please select the folder that you want \
        to organize. Next, press the 'click' button", parent=self.root)

    def About_Fuction(self):
        messagebox.showinfo('About', 'File Organizer 21.02\n~Developed by PySeek',
                            parent=self.root)

    def Open_Folder(self):
        global browsed
        self.browse_folder = filedialog.askdirectory()
        self.label4.config(text=self.browse_folder)

        # Checking if any directory has chosen or not
        if os.path.exists(self.browse_folder):
            browsed = True

    def Exit(self):
        root.destroy()

    def file_finder(self, folder_path, file_extensions):
        self.files = []
        for file in os.listdir(folder_path):
            for extension in file_extensions:
                if file.endswith(extension):
                    self.files.append(file)
        return self.files

    def action(self):
        # If no directory is chosen
        if not browsed:
            messagebox.showwarning('No folders are choosen',
                                   'Please select a folder at first')
            return

        try:
            self.cur_folder_path = self.browse_folder

            if os.path.exists(self.cur_folder_path):
                # folder_list1: stores all the folders that are already
                # presented in the selected directory.
                self.folder_list1 = []

                # folder_list2 stores newly created folders.
                self.folder_list2 = []
                self.flag = False

                for folder, extension_list in dictionary_of_extension.items():
                    self.folder_name = folder
                    self.folder_path = os.path.join(self.cur_folder_path,
                                                    self.folder_name)

                    # Change the directory to the current 
                    # folder path that we've selected.
                    os.chdir(self.cur_folder_path)

                    # If the folder is already present in that directory
                    if os.path.exists(self.folder_name):
                        self.folder_list1.append(self.folder_name)

                    # If the folder is not present in that directory,
                    # then create a new folder
                    else:
                        self.folder_list2.append(self.folder_name)
                        os.mkdir(self.folder_path)

                    for item in self.file_finder(self.cur_folder_path, extension_list):
                        self.file_old_path = os.path.join(self.cur_folder_path, item)
                        self.file_new_path = os.path.join(self.folder_path, item)

                        # Moving files to the specific folder.
                        shutil.move(self.file_old_path, self.file_new_path)
                        self.flag = True
            else:
                messagebox.showerror('Error!', 'Please enter a valid path!',
                                     parenr=self.root)

            # Checking files are separated or not
            if self.flag:
                messagebox.showinfo('Done!', 'Files have been separated.',
                                    parent=self.root)
            if not self.flag:
                messagebox.showinfo('Done!',
                                    'Folders have been created\nNo files are presented to move',
                                    parent=self.root)

        except Exception as e:
            messagebox.showerror("Error!", f"Error due to {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = File_Organizer(root)
    root.mainloop()
