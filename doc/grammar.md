# Language Spec

- Objects declared outside the program are array.
- Objects declared in the program are variables.
- Filter expression is left associated.

# Compiler notes

* Symbol table
  * Names represent
    * Variables - which have the following attributes:
      * type
      * line where declared
      * scope
      * lines where referenced
    * Array - which have the following attributes:
      * # of dimensions
* Symbol tables are assigned to blocks. The symbol table for a block is assigned to the block's node so that the symbol table may be easily found and looked up.

* Variables is a Python hash that stores the variables declared in the program. It is used during the target generation phase of the preprocessor. 
* **Injected Variables** is a Python dictionary used to store dotted names declared outside the program. By outside names, I mean names injected by the preprocessor. A dotted name represents a multi-dimensional array. A dotted name is basically a map to Injected Variables. For instance `this.dotted.name` maps directly to `injected_variables["this"]["dotted"]["name"]`.

# Types

* Int
* Float
* String
* Nil
* Bool: `true` and `false`

# Grammar

Written in EBNF

```
content =
    tags | text ;

{* STATIC TEXT *}

text =
    <any US-ASCII character except '{' and '}'>

{* TAGS *}

tags =
    print_tag |
    if_tag |
    unless_tag |
    for_tag |
    assign_tag |
    capture_tag ;

print_tag =
    "{{" print_expr "}}" ;

if_tag =
    "{%" "if" cond_expr "%}" content
    {"{%" "elif" cond_expr %}" content}
    ["{%" "else" "%}" content]
    "{%" "endif" "%}" ;

unless_tag =
    "{%" "unless" cond_expr "%}"
        content
    "{%" "endunless" "%}"

for_tag =
    "{%" "for" name "in" for_set {for_params} "%}"

for_set =
    atom_expr | "(" atom_expr ".." atom_expr ")" ;

for_params =
    ("limit" ":" atom_expr) |
    ("offset" ":" atom_expr) |
    "reversed" ;

assign_tag =
    "{%" "assign" name "=" atom_expr "%}" ;

capture_tag =
    "{%" "capture" "%}"
        content
    "{%" "endcapture" "%}" ;

increment_tag =
    "{%" "increment" atom_expr "%}" ;

decrement_tag =
    "{%" "decrement" atom_expr "%}" ;

{* RELATIONAL EXPRESSION *}

{* Condition expression *}
cond_expr =
    or_expr ;

{* Logical OR expression *}
or_expr  =
    and_expr {"or" and_expr} ;

{* Logical AND expression *}
and_expr =
    sameness_expr {"and" sameness_expr} ;

{* Sameness expression *}
sameness_expr =
    order_expr {("==" | "!=") order_expr} ;

{* Order expression *}
order_expr =
    atom_expr {("<" | ">" | "<=" | ">=") atom_expr} ;

{* PRINT EXPRESSION *}

print_expr =
    atom_expr {"|" filter} ;

filter =
    append_filter |
    sort_filter ;

abs_filter =
    "abs" ;

append_filter =
    "append" ":" atom_expr ;

sort_filter =
    "sort" ;

upcase_filter =
    "upcase";

lowcase_filter =
    "lowcase" ;

capitalize_filter =
    "capitalize" ;

divide_by_filter =
    "divide_by" ;

{* ATOM EXPRESSION *}

atom_expr =
    atom {trailer} ;

trailer =
    "[" subscript "]" ;

subscript =
    atom_expr | name | number | string ;

atom =
    name | number | string | "null" | "true" | "false" ;

{* TOKENS *}

name =
    letter | "_" {digit | letter | "_"} ;

number =
    int | float ;

int =
    digit {digit} ;

float =
    {digit} "." digit {digit} ;

string =
    "'" string_body "'" | '"' string_body '"' ;

string_body =
    {ascii_char | escape_seq} ;

escape_seq =
    "\" ascii_char ;

{* CHARACTER LEVEL *}

ascii_char =
    <any US-ASCII character from 0x00-0x7F>

letter =
    <A-Z> | <a-z> ;

digit =
    <0-9> ;
```
