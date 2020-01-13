import os
import shutil
import datetime

# typing
import mypy
from typing import List, Dict

def move_file(original_file, final_path):
    # assert original_file is legit
    # assert final_path is writable
    assert(os.access(os.path.dirname(final_path), os.W_OK))
    # shutil.move returns the written path if successful
    newPath = shutil.move(original_file, final_path)
    try:
        #print to gui label
        pass
    except:
        pass # display error


def get_current_month_and_year():
    """
    TODO: get last month, not this month
    """
    currentDT = datetime.datetime.now()
    return currentDT.strftime("%b-%Y")

def match_names_with_files(clean_names: List[str], excel_sheets: List[str]) -> Dict:
    """
    returns dictionary of clean names with the excel files
    """
    matched_names = dict(zip(clean_names, excel_sheets))
    return matched_names

def is_valid_name(filename: str) -> bool:
    """
    checks if a name in the dropbox directory is valid to list
    returns true is yes, false otherwise
    """
    if not filename.name.startswith('.') and filename.is_dir():
        return True
    else:
        return False

def get_list_of_dropbox_dirs(dropbox_directory: str) -> List[str]:
    """
    returns list of valid dropbox folder names
    """
    list_of_dropbox_dirs = []
    with os.scandir(dropbox_directory) as it:
        for entry in it:
            if entry.name == 'ifco projects':
                with os.scandir(entry) as it:
                    for name in it:
                        if is_valid_name(name):
                            list_of_dropbox_dirs.append(name.name)
            if is_valid_name(entry):
                list_of_dropbox_dirs.append(entry.name)
    return list_of_dropbox_dirs

def get_dict_of_dropbox_dirs(dropbox_directory: str) -> Dict[str, str]:
    dict_of_dropbox_dirs = {}
    with os.scandir(dropbox_directory) as it:
        for entry in it:
            if entry.name == 'ifco projects':
                with os.scandir(entry) as it:
                    for name in it:
                        if is_valid_name(name):
                            dict_of_dropbox_dirs[name.name] = name.path
            if is_valid_name(entry):
                dict_of_dropbox_dirs[entry.name] = entry.path
    return dict_of_dropbox_dirs


def clean_downloaded_filenames(reports_list: List[str]) -> List[str]:
    """
    cleans the filename strings of underscores, xls extensions and 'profit and loss' string.

    returns list
    """
    new_reports = []
    for report in reports_list:
        new_name = cut_xls_extension(report)
        if (ends_with_profitandloss(new_name)):
            new_name = cut_profitandloss_part(new_name)
        if ('_' in new_name):
            new_name = new_name.replace('_', ' ')
        new_reports.append(new_name)
    return new_reports

def is_excel_file(filename: str) -> bool:
    """
    checks to see if the file is an excel file
    or at least if it ends with '.xls'

    returns True if it has it, False if not.
    theres probably a better way to do this.
    """
    if (filename[-4:] == '.xls'):
        return True
    else:
        return False

def cut_xls_extension(filename: str) -> str:
    """
    remove '.xls' extension from filename
    returns string
    """
    if (is_excel_file(filename)):
        return filename[:-4]
    else:
        return filename

def ends_with_profitandloss(filename: str) -> bool:
    """
    checks to see if a filename ends with the '_Profit_and_Loss_Detail' string.
    returns True if yes, False otherwise
    """
    suffix = '_Profit_and_Loss_Detail'
    if filename.endswith(suffix):
        return True
    else:
        return False

def cut_profitandloss_part(filename: str) -> str:
    """
    remove the string '_Profit_and_Loss_Detail' from the filename.
    returns string
    """
    if (ends_with_profitandloss(filename)):
        return filename[:-23]
    else:
        return filename