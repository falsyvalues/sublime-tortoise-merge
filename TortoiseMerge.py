import sublime, sublime_plugin
import os
import subprocess

PATHS = ['TortoiseSVN', 'TortoiseGit']
EXEC = 'bin\\TortoiseMerge.exe'

class TortoiseMergeCommand(sublime_plugin.WindowCommand):
    def __init__(self, view):
        self._ = [];
        for item in PATHS:
            self._.append(os.environ['ProgramFiles'] + os.sep + item + os.sep + EXEC)
            self._.append(os.environ['ProgramFiles'] + ' (x86)' + os.sep + item + os.sep + EXEC)

    def run(self, files):
        source = None;
        for path in self._:        
            if os.path.exists(path):
                source = path
                break
      
        if not source:
            print "TortoiseMerge not found."
            return
      
        cmd = '%s "%s" "%s"' % (source, files[0], files[1])
        print "TortoiseMerge command: " + cmd
        subprocess.Popen(cmd)
   
    # We have 2 files selected
    def is_visible(self, files):
        return len(files) > 1
