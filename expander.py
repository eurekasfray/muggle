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

"""
the coordinator: This coordinates the operations of the process.
"""
class Expander:

    def __init__(self, template, content):
        self.template = template
        self.content = content

    def expand(self):
        lexer = Lexer(self.template)
        parser = Parser(lexer.tokens(), self.content)
        emitter = Emitter(parser.nodes())
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
        self.index = 0

    def nodes(self):
        self.node_list = []
        self.html()
        return self.node_list

    def match(self, token_type):
        if (self.lookahead().type().value() == token_type.value()):
            self.look = self.next_token()
            return True
        else:
            return False

    def lookahead(self):
        token = self.tokens[self.index]
        return token

    def next_token(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def html(self):
        while (self.lookahead().type() == Lexer.TT_MACRO_START or self.lookahead().type() == Lexer.TT_TEXT):
            if (self.lookahead().type() == Lexer.TT_MACRO_START):
                self.content_macro()
            elif (self.lookahead().type() == Lexer.TT_TEXT):
                self.text()
        self.eos()
        return

    def content_macro(self):
        self.macro_start()
        if (not (self.match(Lexer.TT_IDENTIFIER)) and self.lookahead().lexeme().value().lower() != 'content'):
            self.expected(Lexer.TT_CONTENT, self.lookahead())
        self.macro_end()
        self.node_list.append(ContentMacroNode(self.content))

    def macro_start(self):
        if (not self.match(Lexer.TT_MACRO_START)):
            self.expected(Lexer.TT_MACRO_START, self.lookahead())
    def macro_end(self):
        if (not self.match(Lexer.TT_MACRO_END)):
            self.expected(Lexer.TT_MACRO_END, self.lookahead())

    def text(self):
        target_token = self.lookahead()
        if (not self.match(Lexer.TT_TEXT)):
            self.expected(Lexer.TT_TEXT, self.lookahead())
        self.node_list.append(TextNode(target_token.lexeme().value()))

    def eos(self):
        if (not self.match(Lexer.TT_EOS)):
            self.expected(Lexer.TT_EOS, self.lookahead())

    def fail(self, s):
        sys.exit("{p}: error: {s}".format(p=sys.argv[0], s=s))

    def report(self, s):
        self.fail("{s}".format(s=s))

    def expected(self, assumption, actual):
        self.report("expected: {assumption}; found {actual} ({lexeme})".format(assumption=assumption.description(), actual=actual.type().description(), lexeme=actual.lexeme().value()))


"""
a value object.
"""
class TokenType:
    def __init__(self, token_type, description):
        self._type = token_type
        self._description = description

    def value(self):
        return self._type

    def description(self):
        return self._description

"""
a value object.
"""
class Token:

    def __init__(self, token_type, lexeme):
        self._type = token_type
        self._lexeme = lexeme

    def type(self):
        return self._type

    def lexeme(self):
        return self._lexeme

"""
a value object.
"""
class Lexeme:

    def __init__(self):
        self.lexeme = ''

    def push(self, c):
        self.lexeme += c

    def flush(self):
        self.lexeme = ''

    def value(self):
        return self.lexeme

    def create():
        return Lexeme()

"""
a value object.
"""
class Source:

    def __init__(self, source):
        # The source to translate
        self.source = source
        # Append EOL indicator
        self.source += '\x00'
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

    def lookahead(self):
        if (self.i < len(self.source)):
            c = self.source[self.i]
            return c
        else:
            return -1


    def is_end(self):
        if (len(self.source) >= self.i):
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

    TT_MACRO_START = TokenType("macro-start","macro initiator")
    TT_MACRO_END = TokenType("macro-end","macro terminator")
    TT_IDENTIFIER = TokenType("identifier","identifier")
    TT_TEXT = TokenType("text","body of text")
    TT_EOS = TokenType("eos","end-of-string")

    TT_CONTENT = TokenType("content","keyword")

    def __init__(self, source):
        # The source to translate
        self.source = Source(source)
        # The list to store tokens
        self.token_list = []

    def tokens(self):
        lexeme = Lexeme()
        next_state = 'S1'
        while (self.source.lookahead() != -1):
            current_state = next_state
            if (current_state == 'S1'): # Expect first {' or go collect text
                if (self.source.lookahead() == '{'):
                    lexeme.push(self.source.nextchar())
                    next_state = 'S1.1'
                elif (self.is_eos(self.source.lookahead())):
                    next_state = 'S3'
                else:
                    next_state = 'S2'
            elif (current_state == 'S1.1'): # Expect second '{' or go collect text
                if (self.source.lookahead() == '{'):
                    lexeme.push(self.source.nextchar())
                    self.token_list.append(Token(Lexer.TT_MACRO_START, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S1.1.1'
                else:
                    next_state = 'S2'
            elif (current_state == 'S1.1.1'): # Skip whitespace; expect first '}' or go collect a series of any character
                if (self.is_whitespace(self.source.lookahead())):
                    self.source.nextchar()
                    next_state = current_state
                elif (self.source.lookahead() == '}'):
                    lexeme.push(self.source.nextchar())
                    next_state = 'S1.1.2'
                else:
                    next_state = 'S1.1.3'
            elif (current_state == 'S1.1.2'): # Expect second '}'
                if (self.source.lookahead() == '}'):
                    lexeme.push(self.source.nextchar())
                    self.token_list.append(Token(Lexer.TT_MACRO_END, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S1'
                else:
                    next_state = 'S1.1.3'
            elif (current_state == 'S1.1.3'): # Expect a series of any character
                if (self.source.lookahead() == '}'):
                    self.token_list.append(Token(Lexer.TT_IDENTIFIER, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S1.1.1'
                elif (self.is_eos(self.source.lookahead())):
                    self.token_list.append(Token(Lexer.TT_IDENTIFIER, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S3'
                else:
                    lexeme.push(self.source.nextchar())
                    next_state = current_state
            elif (current_state == 'S2'): # Expect text (i.e. any character)
                if (self.source.lookahead() == '{'):
                    self.token_list.append(Token(Lexer.TT_TEXT, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S1'
                elif (self.is_eos(self.source.lookahead())):
                    self.token_list.append(Token(Lexer.TT_TEXT, lexeme))
                    lexeme = Lexeme.create()
                    next_state = 'S3'
                else:
                    lexeme.push(self.source.nextchar())
                    next_state = current_state
            elif (current_state == 'S3'): # Expect end-of-string
                if (self.is_eos(self.source.lookahead())):
                    lexeme.push('eos')
                    self.token_list.append(Token(Lexer.TT_EOS, lexeme))
                    lexeme = Lexeme.create()
                    break

        # Return token list
        return self.token_list

    def is_whitespace(self, c):
        if (c == '\n' or c == '\r' or c == '\t' or c == '\v' or c == ' '):
            return True
        else:
            return False

    def is_eos(self, c):
        if (c == '\x00'):
            return True
        else:
            return False
