"""
David Archuleta Jr.
"""
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox

import os
import getpass
from fuzzywuzzy import process # type: ignore

from . import utility_functions as uf

class DirectoryFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        # Variables
        self.downloads_directory = os.path.expanduser("~\\Downloads")
        self.directory_text = tk.StringVar()
        self.information = []
        self.current_user = getpass.getuser()
        self.monthly_report_string = 'monthly reports'

        # Choose Directory Label Frame
        label_frame = tk.LabelFrame(self, text="Choose Directory")
        choose_directory_label = ttk.Label(label_frame, text="Choose Directory:")
        choose_directory_label.grid(row=0, column=0, sticky=(tk.W + tk.E))
        directory_text = ttk.Label(label_frame, textvariable=self.directory_text)
        directory_text.grid(row=1, column=0, sticky=tk.W)
        choose_directory_btn = ttk.Button(label_frame, text="Choose Directory", command=self.on_choose_dir)
        choose_directory_btn.grid(row=1, column=1, sticky=tk.E)
        label_frame.grid(row=0, column=0, sticky=(tk.W + tk.E))
        # end section

        # Run File Move Section
        file_move = tk.LabelFrame(self, text="Run File Move")
        run_file_move_btn = ttk.Button(file_move, text="Move Files", command=self.run)
        run_file_move_btn.grid(row=0, column=0, sticky=(tk.W+tk.E))
        file_move.grid(row=1, column=0, sticky=(tk.W+tk.E))
        #  end section

        self.columnconfigure(0, weight=1)
    
    def on_choose_dir(self) -> None:
        self.downloads_directory = tk.filedialog.askdirectory()
        if not self.downloads_directory:
            messagebox.showerror(title="error", message="Please choose a directory", detail="exiting...")
            exit()
        self.directory_text.set(self.downloads_directory)
        self.information = os.listdir(self.downloads_directory)
    
    def ask_run(self) -> None:
        run_files = messagebox.askyesno(title="Move Files?",
            message="Would you like to move the files?",
            detail="Click NO to quit")
        if not run_files:
            exit()
        else:
            self.run()

    def run(self) -> None:
        """
        # get current working directory
        # get current user
        # all filenames in download directory
        # make sure to only get the excel files
        # if there are none then this isn't the correct folder
        # remove file extensions and underscores
        # make a dictionary with the clean file names as keys and the excel reports as values.
        # dropbox directory where we will place the new files
        # TODO: check if it is the correct directory
        # dict with project folder name as key and its full path as the value
        # string to fuzzy match with dropbox sub folders
        # for each downloaded file, match a dropbox folder and move it there
        # project is the clean filename for the report
        # match is the corresponding dropbox folder for the project
        # match is a tuple with the dropbox folder name first and the percentage match second
        # get folder name only
        # we want to get a dict of subfolders so we can find where the monthly report folder is
        # we should do it with a defaultdict so that empty values can be
        # walk through all subfolders of the project's directory
        # dropbox_dict with dropbox_folder_name as its key is the full path to the project folder in dropbox
        # so basically, for every directory in the dropbox project folder
        # final 'monthly report' folder that we place the monthly reports in
        # this is the new filename that we will rename the original downloaded report as in dropbox
        # this is the final path including the filename that we will mv original_file final_path
        """
        only_reports = [file for file in self.information if uf.is_excel_file(file)]
        if not only_reports:
            messagebox.showerror(
                title="Error",
                message="This directory contains no excel files, exiting",
                detail="ask david for assistance")
            print("exiting...")
            exit()
        clean_file_names = uf.clean_downloaded_filenames(only_reports)
        reports_dictionary = uf.match_names_with_files(clean_file_names, only_reports)
        dropbox_directory = r"C:\Users\{}\Dropbox (AfGJ)\Fiscal Sponsorship\Project FOLDERS".format(self.current_user)
        dropbox_dict  = uf.get_dict_of_dropbox_dirs(dropbox_directory)
        final = {}
        for project in reports_dictionary.keys():
            match = process.extractOne(project, dropbox_dict.keys())
            dropbox_folder_name = match[0]
            dict_of_subfolders = {}
            for root, dirs, _ in os.walk(dropbox_dict[dropbox_folder_name], topdown=False):
                for name in dirs:
                    dict_of_subfolders[name] = os.path.join(root, name)
                if not dirs:
                    dict_of_subfolders[dropbox_folder_name] = root
            monthly_report_subfolder = process.extractOne(self.monthly_report_string, dict_of_subfolders.keys())
            final_filename = uf.get_final_filename(reports_dictionary[project]) # returns filename without extra fluff and xls extension
            original_file = os.path.join(self.downloads_directory,  reports_dictionary[project]).replace("/", "\\")
            original_file = uf.convert_xls_to_xlsx(original_file)
            if not original_file:
                print("error ocurred")
                exit()
            final_path = dict_of_subfolders[monthly_report_subfolder[0]] + '\\' + final_filename
            final[original_file] = final_path
            print("{}, {}".format(original_file, final[original_file]))
        title = "Confirm Continue"
        message = "The following files will be created. Are you sure you want to continue?"
        detail = "* {}".format('\n * '.join(final.values()))
        should_continue = messagebox.askyesno(title=title, message=message, detail=detail)
        print("success")
        if not should_continue:
            print("exiting...")
            exit()
        else:
            for report, path in final.items():
                successful = uf.move_file(report, path)
                if not successful:
                    messagebox.showerror(title="File Move Error", message="Error on {}".format(path), detail="Please contact david.")
        exit()