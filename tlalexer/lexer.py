from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import *

__all__ = ['TlaLexer']

class TlaLexer(RegexLexer):

    name = 'TLA+'
    aliases = ['tla']
    filenames = ['*.tla']

    tokens = {
        'all': [
            (r'\n', Text),
            (r'\\\n', Text),
            (r'[^\S\n]+', Text),
            (r'[^\S\n]+', Text),
            ('[a-zA-Z_]\w*', Name),
        ],
        'root': [
            (r'(\-+)(\s*)(MODULE)(\s*)(\w*)(\s*)(\-+)',
                bygroups(Comment.PreProc, Text, Comment.PreProc, Text, Comment.PreProc, Text, Comment.PreProc)),
            (r'====+', Comment.PreProc),
            (r'\(\*\s\-\-algorithm.*', Name.Function, 'pluscal'),
            include('comment'),
            include('tla'),
            include('all'),
            # tag/end tag begin
        ],
        'tla': [
            # (r'==', Name.Function),
            (words(("TRUE", "FALSE", "BOOLEAN")), Name.Builtin.Pseudo),
            (r'EXTENDS?', Keyword.Namespace),
            (r'CONSTANTS?', Keyword.Namespace),
            (r'VARIABLES?', Keyword.Namespace),
            (r'INSTANCE', Keyword.Namespace),
            (words(("IF", "THEN", "ELSE", "CASE", "OTHER", "LET", "IN")), Keyword.Conditional),
            (words(("CHOOSE", "\A", "\E", "\X", "\in", "=>", "<=>"), suffix=r'\b'), String), # eh
            (r'\\\w+', Name.Builtin), #ok for now
            (r'\\\/|\/\\', Operator),
            (r'\|\->|\->', Operator),
            (r'[{}]|<<|>>', Name.Entity),
            (r'!=|>=|<=|:=|[.\\\-~+/*%&^|#]', Operator),
            (r'=|<|>', Name.Entity),
            (r'(\'|").*?\1', String),
            (r'[:\[\](),;]', Punctuation),
            (r'-?\d+', Number),
            ],
        'pluscal': [
            (r'end algorithm.*', Name.Function, '#pop'),
            include('comment'),
            include('tla'),
            (r'begin', Name.Function),
            (r'[A-Z]\w*?\:', Name.Tag),
            (r'(end\s)?(macro|procedure|define|return|process)', Name.Function),
            (words(("with", "do", "if", "else", "elsif", "while", "end", "either", "or", "call", "goto"), suffix=r'\b'), Keyword),
            (words(("await",), suffix=r'\b'), Literal.Date), #lol
            (words(("assert"), suffix=r'\b'), Keyword.Reserved),
            include('all'),
            ],
        'comment': [
                (r'\\\*\s.*', Comment),
                (r'\(\*', Comment.Multiline, 'multiline'),
                ],
        'multiline': [
                (r'\(\*', Comment.Multiline, '#push'),
                (r'\*\)', Comment.Multiline, '#pop'),
                (r'.|\n', Comment.Multiline),
                ],
        }
