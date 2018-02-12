import unittest
from spellChecker import *
import random

'''
    Author: Nelson Chen, Colin Wu
                                    '''

class Test_spellChecker(unittest.TestCase):

    def test_ignoreCaseAndPunc(self):
        ''' This test is used to examine whether ignoreCaseAndPunc is working
            properly.'''
        self.assertEqual('word',ignoreCaseAndPunc('WORD'))
        self.assertEqual('hello',ignoreCaseAndPunc('Hello!'))
        self.assertEqual('greetings',ignoreCaseAndPunc('greeTIngS....'))
        self.assertEqual('morning',ignoreCaseAndPunc('morning!?:;.,'))
        self.assertEqual('good_',ignoreCaseAndPunc('good_'))
        self.assertEqual('good-morning',ignoreCaseAndPunc('GooD-MornINg!'))
        self.assertNotEqual('yixin wu.',ignoreCaseAndPunc('Yixin Wu.'))
        self.assertNotEqual('Nelson Chen',ignoreCaseAndPunc('Nelson Chen?'))
        self.assertNotEqual('jj', ignoreCaseAndPunc('jk.,'))

    def test_findWordInDictionary(self):
        ''' This test is used to examine whether findWordInDictionary is working
            properly. '''
        self.assertEqual(True,findWordInDictionary('ACM','engDictionary.txt'))
        self.assertEqual(True,findWordInDictionary("African's",'engDictionary.txt'))
        self.assertEqual(False,findWordInDictionary("mamamama",'engDictionary.txt'))
        self.assertEqual(True,findWordInDictionary("zoos",'engDictionary.txt'))
        self.assertEqual(False,findWordInDictionary("SB",'engDictionary.txt'))
        self.assertEqual(False,findWordInDictionary("heyman",'engDictionary.txt'))
        self.assertNotEqual(True,findWordInDictionary("Jiajia Li",'engDictionary.txt'))
        self.assertNotEqual(True,findWordInDictionary("Yixin Wu",'engDictionary.txt'))
        self.assertNotEqual(False,findWordInDictionary("California",'engDictionary.txt'))

    def test_getWordsOfSimLength(self):
        ''' This test is used to examine whether getWordsOfSimLength is working properly.'''
        wordList = getWordsOfSimLength('man','engDictionary.txt',1)
        length = len(wordList)
        self.assertEqual(True, 2 <= len(wordList[0]) <= 4)
        self.assertEqual(True, 2 <= len(wordList[-1]) <= 4)
        self.assertEqual(True, 2 <= len(wordList[random.randint(0,length - 1)]) <= 4)

    def test_getWordsWithSameStart(self):
        ''' This test is used to examine whether getWordsWithSameStart is working properly.'''
        wordList = ['abc','def','ghijkl','[]3892','warcraft3','University of Pennsylvania','Georgia Tech','defer','god','abstract','abacus']
        self.assertEqual(set(['abc','abstract','abacus']),set(getWordsWithSameStart('ab',wordList,2)))
        self.assertEqual(['[]3892'], getWordsWithSameStart('[]3',wordList,3))
        self.assertEqual([], getWordsWithSameStart('unicorn', wordList, 4))
        self.assertEqual(['University of Pennsylvania'], getWordsWithSameStart('UNIVERSITY REALTY', wordList, 11))

    def test_getWordsWithCommonLetters(self):
        ''' This test is used to examine whether getWordsWithCommonLetters is working
            properly.'''
        wordList = ['abc','def','ghijkl','[]3892','warcraft3','University of Pennsylvania','Georgia Tech','defer','god','abstract','abacus']
        self.assertEqual(set(['abc','abstract','abacus']), set(getWordsWithCommonLetters('abc', wordList, 3)))
        self.assertEqual(set(['ghijkl', 'Georgia Tech','god']), set(getWordsWithCommonLetters('g', wordList,1)))
        self.assertEqual(set(['[]3892','warcraft3','def','University of Pennsylvania','Georgia Tech','defer']), set(getWordsWithCommonLetters('3e', wordList,1)))
        self.assertEqual([],getWordsWithCommonLetters('3e',wordList,2))
        self.assertEqual(['University of Pennsylvania'], getWordsWithCommonLetters('UPenn', wordList, 4))
        self.assertEqual(['Georgia Tech'], getWordsWithCommonLetters('GT', wordList, 2))

    def test_getSimilarityMetric(self):
        '''This test is used to examine whether getSimilarityMetric is working properly.'''
        self.assertEqual(4, getSimilarityMetric('word','word'))
        self.assertEqual(2, getSimilarityMetric('word','words'))
        self.assertEqual(0, getSimilarityMetric('game','over'))
        self.assertEqual(3.5, getSimilarityMetric('warcraft','STARCRAFT'))
        self.assertEqual(0, getSimilarityMetric('bloody','hell'))

    def test_getSimilarityDict(self):
        '''This test is used to examine whether getSimilarityDict is working properly.'''
        wordList = ['abc','cde','efg','ghi','room']
        similarityDictionary1 = getSimilarityDict('god', wordList)
        self.assertEqual({'abc': 0, 'cde': 0, 'efg': 0, 'ghi': 1, 'room': 1}, similarityDictionary1)
        similarityDictionary2 = getSimilarityDict('Evangelion', wordList)
        self.assertEqual({'abc': 0, 'cde': 0, 'efg': 0.5, 'ghi': 0, 'room': 0.5}, similarityDictionary2)
        similarityDictionary3 = getSimilarityDict('tornado', wordList)
        self.assertEqual({'abc': 0.5, 'cde': 0.5, 'efg': 0, 'ghi': 0, 'room': 0.5}, similarityDictionary3)

    def test_getBestWords(self):
        '''This test is used to examine whether getBestWords is working properly.'''
        wordList = ['abc','cde','efg','ghi','room']
        similarityDictionary1 = getSimilarityDict('god', wordList)
        self.assertEqual(set(getBestWords(similarityDictionary1, 2)),set(['ghi','room']))
        self.assertNotEqual(getBestWords(similarityDictionary1, 1), ['abc'])
        similarityDictionary2 = getSimilarityDict('Evangelion', wordList)
        self.assertEqual(set(getBestWords(similarityDictionary2, 2)),set(['efg','room']))
        self.assertNotEqual(['ghi'], getBestWords(similarityDictionary2, 1))
        similarityDictionary3 = getSimilarityDict('tornado', wordList)
        self.assertEqual(set(getBestWords(similarityDictionary3, 3)),set(['cde','room', 'abc']))
        self.assertNotEqual(['ghi','efg'], getBestWords(similarityDictionary2, 2))

    def test_sortIn2D(self):
        '''This test is used to examine whether sortIn2D is working properly.'''
        self.assertEqual(-1, sortIn2D((2,1),(1,2)))
        self.assertEqual(-1, sortIn2D(('Colin',1),('Julia',2)))
        self.assertEqual(0, sortIn2D((['mister'],1),(1,1)))
        self.assertEqual(0, sortIn2D((['mister'],1),((2,4),1)))
        self.assertEqual(1, sortIn2D(({1:2},2),({2:3},1)))
        self.assertEqual(1, sortIn2D((10,5),(11,1)))

    def test_getListOfFirstComponents(self):
        '''This test is used to examine whether getListOfFirstComponents is working
           properly. '''
        tuplelist1 = [(['mister'],'god'),('Jiajia Li', 'Yixin Wu'),('Yixin Wu', 'Jiajia Li'),((1,2),3)]
        self.assertEqual([['mister'], 'Jiajia Li', 'Yixin Wu', (1,2)], getListOfFirstComponents(tuplelist1))
        tuplelist2 = [(1,2),(3,4),(5,6),(7,8)]
        self.assertEqual(getListOfFirstComponents(tuplelist2),[1,3,5,7])
        tuplelist3 = [({'hello':'my name is elder price'},'The book of mormon'),
                      (['All that jazz', 'Cell block tango', 'razzle dazzle'],'Chicago'),
                      ('Kansas City','Oklahoma'),('mambo','West-side story'),(['I love broadway musical'],'Nelson Chen')]
        self.assertEqual(getListOfFirstComponents(tuplelist3),[{'hello':'my name is elder price'},
                                                               ['All that jazz', 'Cell block tango', 'razzle dazzle'],'Kansas City',
                                                               'mambo',['I love broadway musical']])

    def test_getWordSuggestionsV1(self):
        '''This test is used to examine whether getWordSuggestionsV1 is working properly.'''
        self.assertEqual(set(['gazed', 'egged', 'edged']), set(getWordSuggestionsV1('gzed','engDictionary.txt',1, 75, 3)))
        self.assertEqual(set(['bitch', 'batch']), set(getWordSuggestionsV1('bwtch','engDictionary.txt',0, 25, 2)))
        self.assertEqual([],getWordSuggestionsV1('mein','engDictionary.txt',0, 70, 0))
        self.assertEqual([],getWordSuggestionsV1('guten','engDictionary.txt',3, 100, 3))

    def test_getWordSuggestionsV2(self):    
        '''This test is used to examine whether getWordSuggestionsV2 is working properly.'''
        self.assertEqual(set(['bider', 'biker']), set(getWordSuggestionsV2('biger','engDictionary.txt',2,2)))
        self.assertEqual(set(['god', 'gad', 'good']) ,set(getWordSuggestionsV2('ged','engDictionary.txt',1,3)))
        self.assertEqual([], getWordSuggestionsV2('gepd','engDictionary.txt',4,4))
        self.assertEqual([], getWordSuggestionsV2('gepd','engDictionary.txt',1,0))

    def test_getCombinedWordSuggestions(self):
        '''This test is used to examine whether getCombinedWordSuggestions is working properly.'''
        self.assertEqual([],getCombinedWordSuggestions('','engDictionary.txt'))
        self.assertEqual([],getCombinedWordSuggestions('a','engDictionary.txt'))
        self.assertEqual(['aphid', 'applaud', 'append', 'aided', 'aired', 'acted', 'acrid', 'aimed', 'pallid', 'pall'],getCombinedWordSuggestions('appld','engDictionary.txt'))
        self.assertEqual(['ask', 'ark'], getCombinedWordSuggestions('ak','engDictionary.txt'))
                         
        
if __name__ == '__main__':
    unittest.main()
