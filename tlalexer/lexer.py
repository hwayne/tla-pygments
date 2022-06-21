from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import *

__all__ = ['TlaLexer']

# TODO: THEOREM, ~>, WF_(, SF_(

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
            (r'[a-zA-Z_]\w*', Name),
            ('[!{}\']', Name),
        ],
        'root': [
            (r'(\-+)(\s*)(MODULE)(\s*)(\w*)(\s*)(\-+)',
                bygroups(Comment.PreProc, Text, Comment.PreProc, Text, Comment.PreProc, Text, Comment.PreProc)),
            (r'====+', Comment.PreProc),
            include('pluscal'),
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
            (r'ASSUME', Keyword.Namespace),
            (r'VARIABLES?', Keyword.Namespace),
            (r'INSTANCE', Keyword.Namespace),
            (r'WITH', Keyword.Namespace),
            (words(("IF", "THEN", "ELSE", "CASE", "OTHER", "LET"), suffix=r'\b'), Keyword.Conditional),
            (words(("CHOOSE", "UNION", "\\A", "\\E", "\\X", "\\in", "\\notin", "=>", "<=>"), suffix=r'\b'), String), # eh
            (words(("CHOOSE", "UNION", "\\A", "\\E", "\\X", "\\in", "\\notin", "=>", "<=>"), suffix=r'\b'), String), 
            (r'\\\w+', Name.Builtin), #ok for now
            (r'\\\/|\/\\', Operator),
            (r'\|\->|\->', Operator), #TODO make this words
            (r'\[\]|<>[^>]', Name.Entity),
            (r'>=|<=|:=|\/=|[.\\\-~+/*%&^|#]', Operator),
            (r'=|<|>', Operator),
            (r'(").*?\1', String),
            (r'[:\[\](),;]', Punctuation),
            (r'-?\d+', Number),
            ],
        'pluscal': [
            (r'\(\*\s?\-\-(fair\s)?\s?algorithm.*', Name.Function),
            (r'end algorithm.*', Name.Function),
            include('comment'),
            include('tla'),
            (r'begin', Name.Function),
            (r'^\s*[A-Z]\w*?\:', Name.Tag),
            (r'(fair+?\s)?process', Name.Tag),
            (r'(end\s)?(macro|procedure|define|return|process)', Name.Function),
            (words(("with", "do", "if", "else", "elsif", "then", "while", "end", "either", "or", "call", "goto"), suffix=r'\b'), Keyword),
            (words(("await","when"), suffix=r'\b'), Literal.Date), #lol
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
