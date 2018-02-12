'''
Created on Feb 21, 2016

@author: CNelson Colin Wu
'''
import os
import sys

def ignoreCaseAndPunc(word):
    '''return a word in lower case and punctuation removed'''
    word_revised = word.strip(',;:?!.').lower()
    return word_revised

def findWordInDictionary(word,fileName):
    '''check if the word is present in the dictionary'''
    f = open(fileName)
    dictlst = []
    for line in f:
        line = line.strip().lower()
        dictlst.append(line)
    f.close()
    word_check = ignoreCaseAndPunc(word)
    return word_check in dictlst
    
def getWordsOfSimLength(word,fileName,n):
    '''get words with length +/- value n'''
    length = len(word)
    word_simlen = []
    f = open(fileName)
    dictlst = []
    for line in f:
        line = line.strip()
        dictlst.append(line)
    f.close()
    for word_dict in dictlst:
        if length - n <= len(word_dict) <= length + n:
            word_simlen.append(word_dict)
    return word_simlen
    
def getWordsWithSameStart(word,wordList,n):
    '''get words with same start n characters'''
    word_samst = []
    word = ignoreCaseAndPunc(word)
    for words in wordList:
        lower_words = ignoreCaseAndPunc(words)
        if word[0:n] == lower_words[0:n]:
            word_samst.append(words)
    return word_samst

def getWordsWithCommonLetters(word,wordList,n):
    '''get words with n or more common letters'''
    word = ignoreCaseAndPunc(word)
    word_com = set(word)
    word_comlet = []
    for words in wordList:
        lower_words = ignoreCaseAndPunc(words)
        words_com = set(lower_words)
        letter_com = word_com.intersection(words_com)
        if len(letter_com) >= n:
            word_comlet.append(words)
    return word_comlet
    
def getSimilarityMetric(word1,word2):
    '''get the average similarity of to words'''
    word1 = ignoreCaseAndPunc(word1)
    word2 = ignoreCaseAndPunc(word2)
    length = min(len(word1),len(word2))
    lcount = 0
    rcount = 0
    for lletter in range(0,length):
        if word1[lletter] == word2[lletter]:
            lcount = lcount + 1
    for rletter in range(0,length):
        if word1[len(word1) - rletter - 1] == word2[len(word2) - rletter - 1]:
            rcount = rcount + 1
    return (lcount + rcount) / 2.0

def getSimilarityDict(word,wordList):
    '''get a similarity dictionary'''
    simDict = {}
    for words in wordList:
        similarity = getSimilarityMetric(word, words)
        simDict[words] = similarity
    return simDict

def getBestWords(similarityDictionary,n):
    '''get top n in terms if the similarity'''
    listOfTuples = similarityDictionary.items()
    listOfTuples.sort(sortIn2D,reverse=True)
    return getListOfFirstComponents(listOfTuples)[0:n]

def sortIn2D(tup1,tup2):
    '''compare just the second component'''
    x = tup1[1]
    y = tup2[1]
    return cmp(x, y)
    
def getListOfFirstComponents(tupleList):
    '''return the first component of the tuples'''
    word_lst = []
    for tup in tupleList:
        word_lst.append(tup[0])
    return word_lst

def getWordSuggestionsV1(word,fileName,n,commonPercent,topN):
    '''get a list of legal word suggestions'''
    words_simlen = getWordsOfSimLength(word, fileName, n)
    word = ignoreCaseAndPunc(word)
    word_s = set(word)
    words_commonP = []
    for words in words_simlen:
        lower_words = ignoreCaseAndPunc(words)
        words_s = set(lower_words)
        common = len(word_s.intersection(words_s))
        distinct = len(word_s.union(words_s))
        percent = common / (distinct + 0.0)
        if percent >= (commonPercent / 100.0):
            words_commonP.append(words)
    simDict = getSimilarityDict(word, words_commonP)
    return getBestWords(simDict, topN)

def getWordSuggestionsV2(word,fileName,n,topN):
    '''get another list of legal word suggestions'''
    words_simlen = getWordsOfSimLength(word, fileName, 1)
    words_samst = getWordsWithSameStart(word, words_simlen, n)
    word = ignoreCaseAndPunc(word)
    words_samed = []
    for words in words_samst:
        lower_words = ignoreCaseAndPunc(words)
        if word[(len(word)- n):len(word)] == lower_words[(len(lower_words) - n):len(lower_words)]:
            words_samed.append(words)
    simDict = getSimilarityDict(word, words_samed)
    return getBestWords(simDict, topN)
    
def getCombinedWordSuggestions(word,fileName):
    '''combine the results of V1 and V2'''
    lst1 = getWordSuggestionsV1(word, fileName, 2, 75, 7)
    lst2 = getWordSuggestionsV2(word, fileName, 1, 7)
    set1 = set(lst1)
    set2 = set(lst2)
    word_set = set1.union(set2)
    setnum = len(word_set)
    simDict = getSimilarityDict(word, list(word_set))
    return getBestWords(simDict, 10)
    
def prettyPrint(lst):
    '''print out the suggestion words'''
    num = 1
    for word in lst:
        print '%d. %s\n'%(num,word),
        num = num + 1
    
def wordProcess(word,fileName):
    '''determine how an incorrect word will be dealt with'''
    word_suggest = getCombinedWordSuggestions(word, fileName)
    print 'The following suggestions are available:'
    prettyPrint(word_suggest)
    if word_suggest == []:
        while(1):
            choose = raw_input('No Suggestions!\nPlease choose a correct method:(a for ignore, t for input)')
            choose = choose.lower()
            if choose == 'a' or choose == 't':
                break   
    else:
        while(1):
            choose = raw_input('Please choose a correct method:(r for replace, a for ignore, t for input)')
            choose = choose.lower()
            if choose == 'r' or choose == 'a' or choose == 't':
                break   
    if choose == 'a':
        return word
    elif choose == 't':
        word = raw_input('Please input a word:')
        return word
    else:
        while(1):
            choose_num = input('Please choose a correct word:')
            if choose_num >= 1 and choose_num <= len(word_suggest):
                break
        word = word_suggest[choose_num - 1]
        return word
        
def search(path,file_check):
    '''search file and give the path'''
    for filename in os.listdir(path): # search all folds
        filepath = os.path.join(path,filename)
        if os.path.isfile(filepath) and file_check == filename:
            return filepath
        elif os.path.isdir(filepath):
            search(filepath, file_check) # recursion to search child folds
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
        for files in prog_root[0:-1]: # get program file location
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
        word_check.append('***nextline***') # get new line
    file_to_check.close()
    
    # check start
    file_punctuation = [] 
    fileName = 'engDictionary.txt'
    print '\nSpell check start!\n'
    for word_unchecked in word_check: # main check
        if word_unchecked != '***nextline***' and word_unchecked != '':
            if word_unchecked[-1] == ',':
                file_punctuation.append(', ')
            elif word_unchecked[-1] == ';':
                file_punctuation.append('; ')
            elif word_unchecked[-1] == ':':
                file_punctuation.append(': ')
            elif word_unchecked[-1] == '?':
                file_punctuation.append('? ')
            elif word_unchecked[-1] == '!':
                file_punctuation.append('! ')
            elif word_unchecked[-1] == '.':
                file_punctuation.append('. ')
            else:
                file_punctuation.append(' ') # get punctuation
            if findWordInDictionary(word_unchecked, fileName) == False:
                print "\nThe word '%s' in the file is not correct."%ignoreCaseAndPunc(word_unchecked)
                word_corrected = wordProcess(word_unchecked, fileName)
                num = word_check.index(word_unchecked)
                word_check[num] = word_corrected
                if word_corrected == word_unchecked:
                    file_punctuation[-1] = ' '
                if ignoreCaseAndPunc(word_unchecked) != ignoreCaseAndPunc(word_corrected):
                    print "\nThe word '%s' is corrected to '%s'."%(ignoreCaseAndPunc(word_unchecked),word_corrected)
            else:
                file_punctuation[-1] = ' '
        else:
            file_punctuation.append('')
    file_checked = open('correctJabberwocky.txt','w')
    p_num = 0
    for word_write in word_check: # write new file
        if word_write != '***nextline***':
            file_checked.write(word_write,)
            file_checked.write(file_punctuation[p_num],) # write punctuation
        else:
            file_checked.write('\n',) # write new line
        p_num = p_num + 1
    file_checked.close()
    
    # print corrected file
    print 'Your file is checked!\nHere is the result:\n'
    file_c = open('correctJabberwocky.txt')
    for line_c in file_c:
        print line_c,
      
     
if __name__ == '__main__':
    main() 
    raw_input('\n\n\npress enter to exit')
