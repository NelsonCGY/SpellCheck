'''
Created on Feb 23, 2016

@author: CNelson
'''
import os
import sys
def search(path,file_check):
    '''search file and give the path'''
    for filename in os.listdir(path):
        filepath = os.path.join(path,filename)
        if os.path.isfile(filepath) and file_check == filename:
            return filepath
        elif os.path.isdir(filepath):
            search(filepath, file_check)
    return None
    
    
def main():
    '''main function of correction'''
    # get file path and read file
    prog_root = sys.argv[0]
    prog_root = prog_root.split('\\')
    print "Welcome to SpellChecker!\nPlease put your file-to-check in to the program's file.\n"
    while(1):
        file_check =raw_input("Please enter your filename:(ignore '.txt')")
        file_check_txt = file_check + '.txt'
        path = ''
        for files in prog_root[0:-1]:
            path = path + files + '\\'
        file_check_path = search(path, file_check_txt)
        if file_check_path != None:
            break
        else:
            print "Your file '%s' cannot be found! Please ensure that the file is in the program's file!\n"%file_check
    word_check = []
    file_to_check = open(file_check_path)
    print 'File found!\nThis is your original file:\n'
    for line in file_to_check:
        print line,
        word_check.extend(line.strip().split(' '))
        word_check.append('***nextline***')
    file_to_check.close()
    print word_check
    
main()