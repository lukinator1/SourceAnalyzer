import re
import ast
import string
import tokenize
import collections


class PyAnalyzer(ast.NodeVisitor):
    def __init__(self, source):
        source.seek(0)
        tokens = tokenize.generate_tokens(source.readline)
        self._parser_tokens = self.__init_tokens(tokens)
        self._parsed_code = self.__get_parsed_code(self._parser_tokens)
        self._code = self.__get_code(self._parser_tokens)

    def __init_tokens(self, tokens):
        ParserTokenInfo = collections.namedtuple("ParserTokenInfo", ['type', 'string', 'start', 'end', 'line',
                                                                     'old_string'], rename=False, defaults=[None])
        parser_tokens = []
        pos = 0
        loop_line = False
        boiler_plate = ['(', ')', ':', 'def']
        indent_next = False
        for token in tokens:
            replace = re.sub(r"\s+", "", token.string.lower())
            start = pos
            end = pos + (diff := token.end[1] - token.start[1])
            pos += diff
            try:
                if token.type == 5:
                    parser_tokens.append(ParserTokenInfo(token.type, "", start, end, token.line, "" +
                                                         (" " if token.line[token.end[1]] == " " else "")))
                    continue
                elif token.type == 6:
                    continue
                elif token.type in [4, 61]:
                    indent_next = True
                    parser_tokens.append(ParserTokenInfo(token.type, replace, start,
                                                         end, token.line,token.string +
                                                         (" " if token.line[token.end[1]] == " " else "")))
                    continue
                elif loop_line or token.type == 60 or token.string in boiler_plate:
                    if token.string == ':' and token.type == 54:
                        loop_line = False
                    replace = ""
                elif token.type == 1:
                    if token.string == 'if' or token.string == 'elif' or token.string == 'else':
                        replace = "c"
                    elif token.string == 'for' or token.string == 'while':
                        if ':' in token.line:
                            loop_line = True
                        replace = "l"
                    elif token.line[token.end[1]] == '(':
                        replace = "f"
                    else:
                        replace = "v"
                indent = len(token.line) - len(token.line.lstrip(" "))
                parser_tokens.append(ParserTokenInfo(token.type, replace, start, end, token.line,
                                                     ((" " * indent) if indent_next else "") +
                                                     token.string + (" " if token.line[token.end[1]] == " " else "")))
                if indent_next:
                    indent_next = False
            except IndexError:
                parser_tokens.append(ParserTokenInfo(token.type, re.sub(r"\s+", "", token.string.lower()), start,
                                                     end, token.line, token.string))
        """for p in parser_tokens:
            print(p)"""
        return parser_tokens

    def __get_parsed_code(self, parser_tokens):
        parsed_code = ""
        for token in parser_tokens:
            parsed_code += token.string
        return parsed_code

    def __get_code(self, parser_tokens):
        code = ""
        for token in parser_tokens:
            code += token.old_string
        return code

    @property
    def parsed_code(self):
        return self._parsed_code

    @property
    def code(self):
        return self._code

    def get_code_from_parsed(self, k, pos):
        index = 0
        for token in self._parser_tokens:
            if index < pos:
                # if a token is a string
                if token.type == 3 and pos < index + len(token.string):
                    for ch in token.old_string:
                        if ch == string.whitespace and index <= pos:
                            pos += 1
                            index += 1
                        elif ch == string.whitespace and index <= pos+k:
                            k += 1
                            index += 1
                        else:
                            index += 1
                else:
                    pos += len(token.old_string) - len(token.string)
            elif pos <= index < pos + k:
                if token.type == 3 and pos + k < index + len(token.string):
                    for ch in token.old_string:
                        if ch == string.whitespace and index <= pos+k:
                            k += 1
                            index += 1
                        else:
                            index += 1
                else:
                    k += len(token.old_string) - len(token.string)
            else:
                break
            index += len(token.old_string)
        return self._code[pos:pos+k]


def get_text_substring(pos, k, text):
    i = 0
    spaces_pos = []
    newlines_pos = []
    for ch in text:
        if ch == ' ':
            spaces_pos.append(i)
        if ch == '\n':
            newlines_pos.append(i)
        i += 1
    for space_pos in spaces_pos + newlines_pos:
        if space_pos < pos:
            pos += 1
        if pos <= space_pos < pos + k:
            k += 1
    return text[pos:pos+k]


def build_indent(indent):
    whitespace = ""
    for space in indent:
        whitespace += space
    return whitespace
