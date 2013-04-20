'''
Created on Jun 15, 2012

Unit-test of the method for the Unzip project

@author: Gaylord Cherencey
'''
from proxy import extraction, functions
import unittest

class Test(unittest.TestCase):

    def testBadFile(self):
        '''Test when a wrong file name is put as a argument in the main module'''

        pass
        print "\n****************Test with bad file*********************\n"
        self.assertEqual(extraction.main(["filename.tgz", "mydb.db"]), extraction.FAILURE)
        print "Test with bad file... OK"

    def testVerboseMode(self):
        '''Test if the verbose mode goes well in the main module'''

        pass
        print "\n****************Test verbose mode*********************\n"
        self.assertEqual(functions.defineParser(["-v", "00018400_0000_2012-06-02.tgz", "mydb.db"])[1], 20)
        print "Extraction and verbose mode... OK"

    def testDebugMode(self):
        '''Test if the debug mode goes well in the main module'''

        pass
        print "\n****************Test debug mode*********************\n"
        self.assertEqual(functions.defineParser(["-d", "00018400_0000_2012-06-02.tgz", "mydb.db"])[1], 10)
        print "Extraction and debug mode... OK"

    def testDebugAndVerbose(self):
        '''Test if the verbose mode and the debug goes well as the same time '''

        pass
        print "\n****************Test debug and verbose mode in the same time*********************\n"
        print "#1 CASE (-d -v) :\n"
        self.assertEqual(functions.defineParser(["-d","-v","00018400_0000_2012-06-02.tgz", "mydb.db"])[1], 20)
        print "\n#2 CASE (-v -d) :\n"
        self.assertEqual(functions.defineParser(["-v","-d","00018400_0000_2012-06-02.tgz", "mydb.db"])[1], 10)
        print "Extraction and debug mode... OK"

    def testHelpMode(self):
        '''Test if the help mode goes well in the main module'''

        pass
        print "\n****************Test help option*********************\n"
        try:
            extraction.main(["-h", "00018400_0000_2012-06-02.tgz"])
        except SystemExit, e:
                self.assertEquals(type(e), type(SystemExit()))
                self.assertEquals(e.code, 0)
                print "\nHelp mode... OK"

    def testWrongMode(self):
        '''Test if the wrong option case is handle in the main module'''

        pass
        print "\n****************Test wrong option*********************\n"
        try:
            extraction.main(["-a", "00018400_0000_2012-06-02.tgz"])
        except SystemExit, e:
                self.assertEquals(type(e), type(SystemExit()))
                self.assertEquals(e.code, 2)
                print "\nWrong option... OK"

    def testNoNameForDatabase(self):
        '''Test if the wrong option case is handle in the main module'''

        pass
        print "\n****************Test no name for database*********************\n"
        try:
            extraction.main(["00018400_0000_2012-06-02.tgz"])
        except SystemExit, e:
                self.assertEquals(type(e), type(SystemExit()))
                self.assertEquals(e.code, 2)
                print "\nTest no name for database... OK"

    def testNoFileName(self):
        '''Test if the no file name case is handle in the main module'''

        pass
        print "\n****************Test no file name*********************\n"
        try:
            extraction.main(["-v"])
        except SystemExit, e:
                self.assertEquals(type(e), type(SystemExit()))
                self.assertEquals(e.code, 2)
                print "\nNo file name... OK"

    def testTooManyArguments(self):
        '''Test if the too many arguments case is handle in the main module'''

        pass
        print "\n****************Test too many arguments*********************\n"
        try:
            extraction.main(["-v","toto", "00018400_0000_2012-06-02.tgz"])
        except SystemExit, e:
                self.assertEquals(type(e), type(SystemExit()))
                self.assertEquals(e.code, 2)
                print "\nToo many arguments... OK"

    def testisThisTypeOfFile(self):
        '''Test the method IsTheTarfile from the functions module'''

        pass
        print "\n****************Test if the file is a tar file*********************\n"
        self.assertFalse(functions.isThisTypeOfFile("test.taz",".tgz"))
        self.assertTrue(functions.isThisTypeOfFile("Brunel_25_222_1.log","log"))
        print 'Test of the function... OK\n'

    def testmycondition_2(self):
        '''Test the method IsTheTarfile from the functions module'''

        pass
        print "\n****************Test if the file is a tar file*********************\n"
        self.assertEqual(extraction.myCondition_2("test.taz"),0)
        self.assertEqual(extraction.myCondition_2("job.info"),1)
        self.assertEqual(extraction.myCondition_2("Brunel_25_2_1.xml"),2)
        self.assertEqual(extraction.myCondition_2("Brunel_25_2_1.log"),3)
        print 'Test of the function... OK\n'

    def testmycondition_1(self):
        '''Test the method IsTheTarfile from the functions module'''

        pass
        print "\n****************Test if the file is a tar file*********************\n"
        self.assertFalse(extraction.myCondition_1("test.taz"))
        self.assertTrue(extraction.myCondition_1("jtest.tgz"))
        print 'Test of the function... OK\n'

if __name__ == "__main__":
    unittest.main()