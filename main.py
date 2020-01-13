import os
import getpass
from fuzzywuzzy import process # type: ignore

# tkinter
from tkinter import filedialog, messagebox

# typing
import mypy
from typing import List, Dict

from utility_functions import (
    move_file,
    get_current_month_and_year,
    match_names_with_files,
    is_valid_name,
    get_list_of_dropbox_dirs,
    get_dict_of_dropbox_dirs,
    clean_downloaded_filenames,
    is_excel_file,
    cut_xls_extension,
    ends_with_profitandloss,
    cut_profitandloss_part
)

# GUI
from afgj_gui import MyApplication

def main() -> None:
    app = MyApplication()
    app.mainloop()
    #window.directory = filedialog.askdirectory()

    # get current working directory
    download_directory = os.getcwd()
    #download_directory = download_path.get()

    assert(download_directory)

    # get current user
    current_user = getpass.getuser()

    # all filenames in download directory
    all_filenames = os.listdir(download_directory)

    # make sure to only get the excel files
    # if there are none then this isn't the correct folder
    only_reports = [file for file in all_filenames if is_excel_file(file)]
    if not only_reports:
        print("no excel files found: please choose correct directory")
        exit(0)

    # remove file extensions and underscores
    clean_file_names = clean_downloaded_filenames(only_reports)

    # make a dictionary with the clean file names as keys and the excel reports as values.
    reports_dictionary = match_names_with_files(clean_file_names, only_reports)


    # dropbox directory where we will place the new files
    # TODO: check if it is the correct directory
    dropbox_directory = r"C:\Users\{}\Dropbox (AfGJ)\Fiscal Sponsorship\Project FOLDERS".format(current_user)

    # dict with project folder name as key and its full path as the value
    dropbox_dict  = get_dict_of_dropbox_dirs(dropbox_directory)

    # string to fuzzy match with dropbox sub folders
    monthly_report_string = 'monthly reports'

    # for each downloaded file, match a dropbox folder and move it there
    for project in reports_dictionary.keys():
        # project is the clean filename for the report
        # match is the corresponding dropbox folder for the project
        match = process.extractOne(project, dropbox_dict.keys())

        # match is a tuple with the dropbox folder name first and the percentage match second
        # get folder name only
        dropbox_folder_name = match[0]

        # we want to get a dict of subfolders so we can find where the monthly report folder is
        # we should do it with a defaultdict so that empty values can be
        dict_of_subfolders = {}
        
        # walk through all subfolders of the project's directory
        # dropbox_dict with dropbox_folder_name as its key is the full path to the project folder in dropbox
        # so basically, for every directory in the dropbox project folder
        for root, dirs, _ in os.walk(dropbox_dict[dropbox_folder_name], topdown=False):
            for name in dirs:
                dict_of_subfolders[name] = os.path.join(root, name)
            if not dirs:
                dict_of_subfolders[dropbox_folder_name] = root

        # final 'monthly report' folder that we place the monthly reports in
        monthly_report_subfolder = process.extractOne(monthly_report_string, dict_of_subfolders.keys())

        # this is the new filename that we will rename the original downloaded report as in dropbox
        final_filename = cut_profitandloss_part( cut_xls_extension( reports_dictionary[project] )) + "-" + get_current_month_and_year() + ".xls"

        # this is the final path including the filename that we will mv original_file final_path
        final_path = dict_of_subfolders[monthly_report_subfolder[0]] + '\\' + final_filename
    
        # this is our original, downloaded filename
        #original_file = reports_dictionary[project]

        # move file from source: (original_file) to destination: (final_path)
        #move_file(original_file, final_path)

if __name__ == "__main__":
    main()