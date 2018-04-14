"""
How to process rendered HTML: The expander interprets texts and macros.
Anything wrapped in a {{ }} is interpreted as a macro; otherwise it is
interpreted as text. Below is the syntax of the template language (written in
EBNF):
    html =
        { text | content_macro } ;
    content_macro =
        macro_start "content" macro_end;
    macro_start =
        "{{" ;
    macro_end =
        "}}" ;
    text =
        <any character> {<any character>} ;

Below is the process of how the expander interprets its source input:

  --source--> (Tokenize) --tokenlist--> (Parse) --abstract-list--> ...
  ... (Analyze) --analyzed-abstract-list--> (Code Generation) --target-->
"""

import sys
import re

"""
the coordinator: This coordinates the operations of the process.
"""
class Preprocessor:

    def __init__(self, template, content):
        self.template = template
        self.content = content

    def process(self):
        # Call the lexer to get the tokens.
        lexer = Lexer(self.template)
        tokens = lexer.tokenize()
        # Parse the tokens to get the nodes.
        parser = Parser(tokens, self.content)
        nodes = parser.parse()
        # Get the HTML
        emitter = Emitter(nodes)
        return emitter.html()

"""
code generator: Analysis means looking for macros to interpret
and expand. We traverse the node list and expand each node and rebuild an
HTML string. The string is then returned as the processed template HTML.

- The expansion of the TextNode involves retrieving the text stored in it.
- The expansion of the ContentMacroNode involves retrieving the rendered
  markdown stored in it.
"""
class Emitter:

    def __init__(self, nodes):
        self._html = ''
        self.nodes = nodes
        for node in nodes:
            self._html += node.value()

    def html(self):
        return self._html


"""
a value object.
"""
class Node:

    def __init__(self, node_type, value):
        self._value = value
        self._type = node_type

    def value(self):
        return self._value

    def type(self):
        return self._type

"""
a value object.
"""
class ContentMacroNode(Node):

    def __init__(self, value):
        Node.__init__(self, 'content-macro', value)

"""
a value object.
"""
class TextNode(Node):

    def __init__(self, value):
        Node.__init__(self, 'text', value)

"""
This is a recursive-decent parser. It has three two: syntatic analysis
and semantic analysis. The parser works by a list of nodes which are then
returned to the caller.
- Text is saved as TextNode
- The semantic analysis of the ContentMacroNode involves storing the rendered
  markdown in it.
"""
class Parser:

    def __init__(self, tokens, content):
        self.content = content
        self.tokens = tokens
        self.len = len(self.tokens)
        self.index = 0

    def parse(self):
        self.nodes = []
        self.html()
        return self.nodes

    def match(self, token_type):
        if (self.lookahead().type().value() == token_type.value()):
            self.look = self.next_token()
            return True
        else:
            return False

    def lookahead(self):
        if (self.index < self.len):
            token = self.tokens[self.index]
            return token
        else:
            return None

    def next_token(self):
        if (self.index < self.len):
            token = self.tokens[self.index]
            self.index += 1
            return token
        else:
            return None

    def html(self):
        while (self.lookahead().type() == Lexer.VARSTART or self.lookahead().type() == Lexer.TEXT):
            if (self.lookahead().type() == Lexer.VARSTART):
                self.content_macro()
            elif (self.lookahead().type() == Lexer.TEXT):
                self.text()
        self.eos()
        return

    def content_macro(self):
        self.macro_start()
        if (not (self.match(Lexer.IDENTIFIER)) and self.lookahead().lexeme().value().lower() != 'content'):
            self.expected(Lexer.CONTENT, self.lookahead())
        self.macro_end()
        self.nodes.append(ContentMacroNode(self.content))

    def macro_start(self):
        if (not self.match(Lexer.VARSTART)):
            self.expected(Lexer.VARSTART, self.lookahead())
    def macro_end(self):
        if (not self.match(Lexer.VAREND)):
            self.expected(Lexer.VAREND, self.lookahead())

    def text(self):
        target_token = self.lookahead()
        if (not self.match(Lexer.TEXT)):
            self.expected(Lexer.TEXT, self.lookahead())
        self.nodes.append(TextNode(target_token.lexeme().value()))

    def eos(self):
        if (not self.match(Lexer.ENDMARKER)):
            self.expected(Lexer.ENDMARKER, self.lookahead())

    def fail(self, message):
        sys.exit("{program}: error: {message}".format(program=sys.argv[0], message=message))

    def report(self, message):
        self.fail("{message}".format(message=message))

    def expected(self, expected, found):
        self.report("expected: {expected}; found {found} ({lexeme})".format(expected=expected.description(), found=found.type().description(), lexeme=found.lexeme().value()))


"""
a value object.
"""
class TokenType:
    def __init__(self, token_type, description, pattern):
        self._type = token_type
        self._description = description
        self._pattern = pattern

    def value(self):
        return self._type

    def description(self):
        return self._description

    def pattern(self):
        return self._pattern

    def match(self, test):
        match = re.match(self._pattern, test)
        if (match):
            print (match.groups())
        else:
            print ("No match found")

"""
a value object.
"""
class Token:

    def __init__(self, type, lexeme):
        self._type = type
        self._lexeme = Lexeme(lexeme)

    def type(self):
        return self._type

    def set_type(self, toktype):
        self._type = toktype

    def lexeme(self):
        return self._lexeme

"""
a value object.
"""
class Lexeme:
    def __init__(self, lexeme):
        self._lexeme = lexeme

    def push(self, c):
        self._lexeme += c

    def drop(self):
        self._lexeme = self._lexeme[:-1]

    def flush(self):
        self._lexeme = ''

    def value(self):
        return self._lexeme

    def create():
        return Lexeme()

"""
a value object.
"""
class Source:
    ENDMARKER = '\x00'

    def __init__(self, source):
        # The source to translate
        self.source = source
        # Append end-of-file indicator
        self.source += self.ENDMARKER
        # Index pointer for the source
        self.i = 0

    def currchar(self):
        return self.source[self.i]

    def nextchar(self):
        if (self.i < len(self.source)):
            c = self.source[self.i]
            self.i += 1
            return c
        else:
            return -1

    def skipchar(self):
        self.nextchar();

    def lookahead(self):
        if (self.i < len(self.source)):
            c = self.source[self.i]
            return c
        else:
            return -1

    def is_endmarker(self):
        print("sl({}) = i=({})".format(len(self.source),self.i))
        if (self.source[self.i] == self.ENDMARKER):
            return True
        else:
            return False

    def value(self):
        return self.source

    def index(self):
        return self.i

    def increment(self, incremental):
        self.i += incremental

"""
The lexer/tokenizer works by building a list of tokens and retirns the list to
the caller.
"""
class Lexer:

    # Used to tokenize individual tokens
    VARSTART         = TokenType("varstart",  "variable start",     r"\{\{")
    VAREND           = TokenType("varend",    "variable end",       r"\}\}")
    TAGSTART         = TokenType("tagstart",  "tag start",          r"\{\%")
    TAGEND           = TokenType("tagend",    "tag end",            r"\%\}")
    NUMBER           = TokenType("number",    "number",             r"([0-9]*\.)?[0-9]+")
    STRING           = TokenType("str",       "string",             r"\".*?\"|\'.*?\'")
    COLON            = TokenType("colon",     "colon",              r":")
    PIPE             = TokenType("pipe",      "pipe",               r"\|")
    LESSTHAN         = TokenType("lt",        "less than",          r"\<(?!=)")
    LESSTHANEQUAL    = TokenType("lte",       "less than equal",    r"\<=")
    GREATERTHAN      = TokenType("gt",        "greater than",       r"\>(?!=)")
    GREATERTHANEQUAL = TokenType("gte",       "greater than equal", r"\>=")
    EQUAL            = TokenType("equ",       "equal",              r"==")
    NOTEQUAL         = TokenType("neq",       "not equal",          r"!=")
    LPAREN           = TokenType("lparen",    "left parenthesis",   r"\(")
    RPAREN           = TokenType("rparen",    "right parenthesis",  r"\)")
    LBRACKET         = TokenType("lbracket",  "left bracket",       r"\[")
    RBRACKET         = TokenType("rbracket",  "right bracket",      r"\]")
    ASSIGN           = TokenType("assign",    "assign",             r"=(?!=)")
    IDENTIFIER       = TokenType("id",        "identifier",         r"[A-Za-z_][A-Za-z0-9_]+")
    ENDMARKER        = TokenType("endmarker", "ENDMARKER",          r"".join([Source.ENDMARKER]))
    UNKNOWN          = TokenType("unknown",   "unknown",            r".*")

    # Identify static text (not used during scanning)
    TEXT             = TokenType("static",    "static text",        r".*")

    # Used to separate tags and static static from each other.
    PARTIAL_TEMPLATE_PARSER = r"".join([ "(" , TAGSTART.pattern() , ".*?" , TAGEND.pattern() , "|" , VARSTART.pattern() , ".*?" , VAREND.pattern() , ")" ])
    TEMPLATE_PARSER  = PARTIAL_TEMPLATE_PARSER

    def __init__(self, source):
        # The source to translate
        self.source = Source(source)
        # The list to store tokens
        self.tokens = []

    def tokenize(self):
        # Split source into tag partials and static text.
        regex = re.compile(self.PARTIAL_TEMPLATE_PARSER)
        chunks = regex.split(self.source.value())

        # For every tag partial met, break it down into tokens and add the token to the token list.
        # However, if static text is met, then add the static text to the token list.
        for chunk in chunks:

            if (regex.match(chunk)):
                scanner = re.Scanner([
                    (self.VARSTART.pattern(), lambda scanner, token: Token(self.VARSTART, token)),
                    (self.VAREND.pattern(), lambda scanner, token: Token(self.VAREND, token)),
                    (self.TAGSTART.pattern(), lambda scanner, token: Token(self.TAGSTART, token)),
                    (self.TAGEND.pattern(), lambda scanner, token: Token(self.TAGEND, token)),
                    (self.NUMBER.pattern(), lambda scanner, token: Token(self.NUMBER, token)),
                    (self.STRING.pattern(), lambda scanner, token: Token(self.STRING, token)),
                    (self.COLON.pattern(), lambda scanner, token: Token(self.COLON, token)),
                    (self.PIPE.pattern(), lambda scanner, token: Token(self.PIPE, token)),
                    (self.LESSTHAN.pattern(), lambda scanner, token: Token(self.LESSTHAN, token)),
                    (self.LESSTHANEQUAL.pattern(), lambda scanner, token: Token(self.LESSTHANEQUAL, token)),
                    (self.GREATERTHAN.pattern(), lambda scanner, token: Token(self.GREATERTHAN, token)),
                    (self.GREATERTHANEQUAL.pattern(), lambda scanner, token: Token(self.GREATERTHANEQUAL, token)),
                    (self.EQUAL.pattern(), lambda scanner, token: Token(self.EQUAL, token)),
                    (self.NOTEQUAL.pattern(), lambda scanner, token: Token(self.NOTEQUAL, token)),
                    (self.LPAREN.pattern(), lambda scanner, token: Token(self.LPAREN, token)),
                    (self.RPAREN.pattern(), lambda scanner, token: Token(self.RPAREN, token)),
                    (self.LBRACKET.pattern(), lambda scanner, token: Token(self.LBRACKET, token)),
                    (self.RBRACKET.pattern(), lambda scanner, token: Token(self.RBRACKET, token)),
                    (self.ASSIGN.pattern(), lambda scanner, token: Token(self.ASSIGN, token)),
                    (self.IDENTIFIER.pattern(), lambda scanner, token: Token(self.IDENTIFIER, token)),
                    #(self.ENDMARKER.pattern(), lambda scanner, token: Token(self.ENDMARKER, token)),
                    (r"\s+", lambda scanner, token: None),
                    ])
                for token in scanner.scan(chunk)[0]:
                    self.tokens.append(token)
            else:
                self.tokens.append(Token(self.TEXT, chunk))

            # The following is a hacked (duct tape) solution: For some mysterious reason,
            # the ENDMARKER token is never ever captured by the regex scanner, no matter
            # what character it is. Currently, ENDMARKER is currently defined as the NULL character (\x00).
            # In order to make the program work, I've 'duct taped' a solution to this
            # problem by hard coding the endmarker into the token list. Notice that the
            # code for parsing the endmarker in the scanner has been commented out.
            # With that said...
            #
            # If the endmarker is detected at the end of a chunk string, then
            # add the ENDMARKER token to the token list.
            if (chunk[-1:] == Source.ENDMARKER):
                self.tokens.append(Token(self.ENDMARKER, Source.ENDMARKER))

        # Return token list
        return self.tokens
