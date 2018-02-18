# Language Spec

- All objects are array
- Filter expression is left associated.

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

or_expr  =
    and_expr {"or" and_expr} ;

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
abs =
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
