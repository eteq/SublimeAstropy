import ast
import sublime, sublime_plugin


class UpdateNumpydocstrForFuncCommand(sublime_plugin.TextCommand):
    """
    This command finds all functions in the selection region and updates their
    docstrings to reflect the interface.
    """
    def run(self, edit):
        fncregions = self.view.find_by_selector('meta.function.python')

        fncset = set()
        for region in self.view.sel():
            st, end = region.begin(), region.end()

            if (self.view.score_selector(st, 'source.python') < 1 or
                self.view.score_selector(end, 'source.python') < 1):
                print("Selected region is not Python code!")
            else:
                #find all the function regions that are in the selection zone
                for fr in fncregions:
                    fst, fend = fr.begin(), fr.end()
                    if (fst < st < fend or fst < end < fend or
                        st < fst < end or st < fend < end):
                        fncset.add((fst, fend))  # sets require hashable types

        wholefile = self.view.substr(sublime.Region(0, self.view.size()))
        tree = ast.parse(wholefile)

        stlinetoastfunc = dict([(n.lineno, n) for n in ast.walk(tree)
                                if isinstance(n, ast.FunctionDef)])

        print('fnc',fncset)
        for sti, endi in fncset:
            stline = self.view.rowcol(sti)[0] + 1
            astfunc = stlinetoastfunc[stline]
            docstr = ast.get_docstring(astfunc, False)

            if docstr is None:
                #no docstring present - need to create it
                newdocstr = self.get_new_docstr(astfunc)
                self.view.insert(edit, endi, newdocstr)
                self.view.insert(edit, endi, '\n')
            else:
                reg = self.view.find(docstr, endi, sublime.LITERAL)
                newdocstr = self.get_modified_docstr(astfunc, docstr)

                self.view.replace(edit, reg, newdocstr)

    def get_new_docstr(self, astfunc):
        """
        Returns a string with the new "shell" docstring
        """
        params, defaults = self.get_params_and_defaults(astfunc)

        tabspace = '    '

        indentstr = (astfunc.col_offset * ' ') + tabspace

        lines = []
        lines.append('"""')
        lines.append('DESCRIPTION.')
        lines.append('')
        lines.append('Parameters')
        lines.append('----------')
        for pi, di in zip(params, defaults):
            lines.append(pi + ' : TYPE' + (', optional' if di else ''))
            lines.append(tabspace + 'DESCRIPTION OF <{0}>'.format(pi))
        lines.append('')
        lines.append('Returns')
        lines.append('-------')
        lines.append('RETVAL : TYPE')
        lines.append(tabspace + 'RETDESCRIPTION')
        lines.append('')
        lines.append('"""')

        return '\n'.join([('' if l == '' else indentstr) + l for l in lines])


    def get_modified_docstr(self, astfunc, olddoc):
        """
        Returns a string with the new docstring
        """
        params, defaults = self.get_params_and_defaults(astfunc)
        print("Can't modify docstrings yet")

        return olddoc

    def get_params_and_defaults(self, astfunc):
        params = [a.arg for a in astfunc.args.args]
        defaults = list(astfunc.args.defaults)
        for _ in range(len(astfunc.args.args) - len(defaults)):
            defaults.insert(0, None)

        if astfunc.args.vararg:
            params.append(astfunc.args.vararg)
            defaults.append(None)
        if astfunc.args.kwarg:
            params.append(astfunc.args.kwarg)
            defaults.append(None)

        return params, defaults

