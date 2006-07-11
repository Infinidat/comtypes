import unittest as ut
import time
import comtypes.client

# XXX leaks references.

import ctypes.test
ctypes.test.requires("ui")


class Test(ut.TestCase):

    def setUp(self):
        self._events = []

    # Word Application Event
    def DocumentChange(self, this, *args):
##        print "DocumentChange", args
        self._events.append("DocumentChange")

    def test(self):
        # create a word instance
        word = comtypes.client.CreateObject("Word.Application")
        from comtypes.gen import Word
        
        # Get the instance again, and receive events from that
        w2 = comtypes.client.GetActiveObject("Word.Application",
                                             sink=self)

        word.Visible = 1

        doc = word.Documents.Add()
        wrange = doc.Range()
        for i in range(10):
            wrange.InsertAfter("Hello from comtypes %d\n" % i)

        for i, para in enumerate(doc.Paragraphs):
            f = para.Range.Font
            f.ColorIndex = i+1
            f.Size = 12 + (2 * i)

        time.sleep(0.5)

        doc.Close(SaveChanges = Word.wdDoNotSaveChanges)

        word.Quit()
        del word, w2

        time.sleep(0.5)

##        self.failUnlessEqual(self._events, ["DocumentChange", "DocumentChange"])

if __name__ == "__main__":
    unittest.main()
