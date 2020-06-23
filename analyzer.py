import re
import ast
import string
import tokenize
import collections


class PyAnalyzer(ast.NodeVisitor):
    def __init__(self, source):
        self._stats = {"names": [], "loops": [], "logic": [], "comments": []}
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
        for token in tokens:
            start = pos
            diff = token.end[1] - token.start[1]
            end = pos + diff
            pos += diff
            if token.type == 60:
                self._stats["comments"].append(token.string)
                parser_tokens.append(ParserTokenInfo(token.type, "", start,
                                                     end, token.line, token.string))
            elif token.type == 1:
                if token.string not in self._stats["names"]:
                    self._stats["names"].append(token.string)
                parser_tokens.append(ParserTokenInfo(token.type, "v", start,
                                                     end, token.line, token.string))
            else:
                parser_tokens.append(ParserTokenInfo(token.type, re.sub(r"\s+", "", token.string.lower()), start,
                                                     end, token.line, token.string))
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

    @property
    def names(self):
        return self._stats["names"]

    @property
    def comments(self):
        return self._stats["comments"]

    def get_code_from_parsed(self, k, pos):
        index = 0
        for token in self._parser_tokens:
            if index <= pos:
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
            elif pos < index < pos + k:
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