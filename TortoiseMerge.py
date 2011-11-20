import sublime
import sublime_plugin
import os
from subprocess import Popen

PATHS = ['TortoiseSVN', 'TortoiseGit']
EXEC = 'bin\\TortoiseMerge.exe'

class TortoiseMerge:
    filesToDiff = []
    _ = []

    def __init__(self):
        for item in PATHS:
            self._.append(os.environ['ProgramFiles'] + os.sep + item + os.sep + EXEC)
            self._.append(os.environ['ProgramFiles'] + ' (x86)' + os.sep + item + os.sep + EXEC)

    def addFile(self, name):
        self.filesToDiff.append(name)

        if len(self.filesToDiff) > 2:
            self.filesToDiff = self.filesToDiff[1:3:]

        return self

    def isRunable(self):
        if len(self.filesToDiff) != 2:
            return False

        if self.filesToDiff[0] == self.filesToDiff[1]:
            return False

        return True

    def diff(self):
        source = None

        for path in self._:        
            if os.path.exists(path):
                source = path
                break
      
        if not source:
            print "TortoiseMerge not found."
            return None
        
        if not self.isRunable():
            print "Sorry pal, not enough files to run diff."
            return None
      
        cmd = '%s "%s" "%s"' % (source, self.filesToDiff[0], self.filesToDiff[1])
        print "TortoiseMerge command: %s" % cmd
        Popen(cmd)

tm = TortoiseMerge()

class TortoiseMergeFileListener(sublime_plugin.EventListener):
    
    def on_activated(self, view):
        tm.addFile(view.file_name())

class TortoiseMergeCommand(sublime_plugin.ApplicationCommand):

    def run(self, files = []):
        if len(files) > 1:
            tm.addFile(files[1]).addFile(files[0])
        tm.diff()

    def is_visible(self, files):
        return len(files) > 1