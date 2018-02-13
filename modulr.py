import sublime
import sublime_plugin
import os.path
import json
from pprint import pprint

class modulrdefineCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        sz = self.view.window().active_view().size()

        if (sz > 0):
            sublime.error_message('File is not empty!\nYou can only define on empty files.')
        else:
            conf_path = self.get_config_path()
            if (conf_path == False):
                sublime.error_message('This path does not have a modulr config.')
            elif (conf_path == "error|nofile"):
                sublime.error_message('You need to save this edit window to a filename first.')
            else:
                define_code = self.generate_define(conf_path)
                if (define_code == False):
                    sublime.error_message('Your config file is missing properties.')
                else:
                    self.view.insert(edit, self.view.sel()[0].begin(), define_code)

    def get_curr_path(self):
        return self.view.window().active_view().file_name()


    def get_config_path(self):
        curr = self.get_curr_path()

        if (curr == None):
            return "error|nofile"

        sp = curr.split("/")
        sp.pop()

        path = False
        found = 0

        while len(sp) > 0:
            check = "/".join(sp) + "/.modulrc"
            if (os.path.isfile(check) == True):
                path = check
                found = 1
                break
            else:
                sp.pop()


        return path

    def generate_define(self, conf_path):

        # load conf path
        data = json.load(open(conf_path))
        appPath = conf_path.split("/")
        appPath.pop()
        appPath = "/".join(appPath)

        res = False
        uid = False
        basePath = "/app" # defaults to /app
        mstr = False

        if ("uid" in data):
            uid = data["uid"]

        if ("basePath" in data):
            basePath = data["basePath"]

        if (uid != False and basePath != False):
            appPath = appPath + basePath
            mstr = "Modulr.define('${path}', [\n\t'require'\n], function(require){\n\n\n});"
            mstr = mstr.replace("${path}", uid + ":")
            # todo finish here
        return mstr
