import sublime, sublime_plugin


class UpdateNumpydocstrForFuncCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """
        fasf
        """
        for region in self.view.sel():
            point = region.b
            print('scope:"{0!s}", sname:"{1!s}"'.format(
                  self.view.extract_scope(point),
                  self.view.scope_name(point)))
