lexer grammar ScriptLexer;

import UnicodeClasses;

DelimitedComment
    : '/*' ( DelimitedComment | . )*? '*/'
      -> channel(HIDDEN)
    ;

LineComment
    : '//' ~[\u000A\u000D]*
      -> channel(HIDDEN)
    ;

WS
    : [\u0020\u0009\u000C]
      -> skip
    ;

NL: '\u000A' | '\u000D' '\u000A' ;

//SEPARATORS & OPERATIONS

DOT: '.' ;
COMMA: ',' ;
LPAREN: '(' -> pushMode(Inside) ;
RPAREN: ')' ;
LSQUARE: '[' -> pushMode(Inside) ;
RSQUARE: ']' ;
LCURL: '{' ;
RCURL: '}' ;
POW: '**' ;
MULT: '*' ;
MOD: '%' ;
DIV: '/' ;
ADD: '+' ;
SUB: '-' ;
INCR: '++' ;
DECR: '--' ;
CONJ: '&&' ;
DISJ: '||' ;
EXCL: '!' ;
COLON: ':' ;
COLONCOLON: '::' ;
SEMICOLON: ';' ;
ASSIGNMENT: '=' ;
ADD_ASSIGNMENT: '+=' ;
SUB_ASSIGNMENT: '-=' ;
MULT_ASSIGNMENT: '*=' ;
DIV_ASSIGNMENT: '/=' ;
MOD_ASSIGNMENT: '%=' ;
ARROW: '->' ;
DOUBLE_ARROW: '=>' ;
RANGE: '..' ;
HASH: '#' ;
AT: '@' ;
QUEST: '?' ;
ELVIS: '?:' ;
LANGLE: '<' ;
RANGLE: '>' ;
LE: '<=' ;
GE: '>=' ;
EXCL_EQ: '!=' ;
EQEQ: '==' ;
SINGLE_QUOTE: '\'' ;

//KEYWORDS

IMPORT: 'import' ;
STRUCT: 'struct' ;
FUN: 'fun' ;
SCRIPT: 'script' ;
CALLBACK: 'callback' ;
ARCHETYPE: 'archetype' ;
LEVELVAR: 'levelvar' ;
CONST: 'const' ;
VAR: 'var' ;
VAL: 'val' ;
PIT: 'pit' ;
IF: 'if' ;
ELSE: 'else' ;
WHILE: 'while' ;
GETTER: 'get' ;
SETTER: 'set' ;
AS: 'as' ;

//MODIFIERS

PUBLIC: 'public' ;
PRIVATE: 'private' ;
SHARED: 'shared' ;
STATIC: 'static' ;
OPERATOR: 'operator' ;
INLINE: 'inline' ;
SPAWNINIT: 'spawninit' ;

//

FloatLiteral
    : ( (DecDigit*)? '.'
      | ((DecDigit | '_')* DecDigit)? '.')
     ( DecDigit+
      | DecDigit (DecDigit | '_')+ DecDigit
     )
    ;

IntegerLiteral
    : DecDigit+
    | DecDigit (DecDigit | '_')* DecDigit
    ;

fragment DecDigit
    : UNICODE_CLASS_ND
    ;

BooleanLiteral
    : 'true'
    | 'false'
    ;

Identifier
    : (Letter | '_') (Letter | '_' | DecDigit)*
    | '`' ~('`')+ '`'
    ;

fragment Letter
    : UNICODE_CLASS_LL
    | UNICODE_CLASS_LM
    | UNICODE_CLASS_LO
    | UNICODE_CLASS_LT
    | UNICODE_CLASS_LU
    | UNICODE_CLASS_NL
    ;

mode Inside ;

Inside_RPAREN: ')' -> popMode, type(RPAREN) ;
Inside_RSQUARE: ']' -> popMode, type(RSQUARE);

Inside_LPAREN: LPAREN -> pushMode(Inside), type(LPAREN) ;
Inside_LSQUARE: LSQUARE -> pushMode(Inside), type(LSQUARE) ;

Inside_LCURL: LCURL -> type(LCURL) ;
Inside_RCURL: RCURL -> type(RCURL) ;
Inside_DOT: DOT -> type(DOT) ;
Inside_COMMA: COMMA  -> type(COMMA) ;
Inside_MULT: MULT -> type(MULT) ;
Inside_POW: POW -> type(POW) ;
Inside_MOD: MOD  -> type(MOD) ;
Inside_DIV: DIV -> type(DIV) ;
Inside_ADD: ADD  -> type(ADD) ;
Inside_SUB: SUB  -> type(SUB) ;
Inside_INCR: INCR  -> type(INCR) ;
Inside_DECR: DECR  -> type(DECR) ;
Inside_CONJ: CONJ  -> type(CONJ) ;
Inside_DISJ: DISJ  -> type(DISJ) ;
Inside_EXCL: EXCL  -> type(EXCL) ;
Inside_COLON: COLON  -> type(COLON) ;
Inside_COLONCOLON: COLONCOLON  -> type(COLONCOLON) ;
Inside_SEMICOLON: SEMICOLON  -> type(SEMICOLON) ;
Inside_ASSIGNMENT: ASSIGNMENT  -> type(ASSIGNMENT) ;
Inside_ADD_ASSIGNMENT: ADD_ASSIGNMENT  -> type(ADD_ASSIGNMENT) ;
Inside_SUB_ASSIGNMENT: SUB_ASSIGNMENT  -> type(SUB_ASSIGNMENT) ;
Inside_MULT_ASSIGNMENT: MULT_ASSIGNMENT  -> type(MULT_ASSIGNMENT) ;
Inside_DIV_ASSIGNMENT: DIV_ASSIGNMENT  -> type(DIV_ASSIGNMENT) ;
Inside_MOD_ASSIGNMENT: MOD_ASSIGNMENT  -> type(MOD_ASSIGNMENT) ;
Inside_ARROW: ARROW  -> type(ARROW) ;
Inside_DOUBLE_ARROW: DOUBLE_ARROW  -> type(DOUBLE_ARROW) ;
Inside_RANGE: RANGE  -> type(RANGE) ;
Inside_HASH: HASH  -> type(HASH) ;
Inside_AT: AT  -> type(AT) ;
Inside_QUEST: QUEST  -> type(QUEST) ;
Inside_ELVIS: ELVIS  -> type(ELVIS) ;
Inside_LANGLE: LANGLE  -> type(LANGLE) ;
Inside_RANGLE: RANGLE  -> type(RANGLE) ;
Inside_LE: LE  -> type(LE) ;
Inside_GE: GE  -> type(GE) ;
Inside_EXCL_EQ: EXCL_EQ  -> type(EXCL_EQ) ;
Inside_EQEQ: EQEQ  -> type(EQEQ) ;
Inside_SINGLE_QUOTE: SINGLE_QUOTE  -> type(SINGLE_QUOTE) ;

Inside_VAL: VAL -> type(VAL) ;
Inside_VAR: VAR -> type(VAR) ;
Inside_PIT: PIT -> type(PIT) ;
Inside_CONST: CONST -> type(CONST) ;
Inside_IF: IF -> type(IF) ;
Inside_ELSE: ELSE -> type(ELSE) ;
Inside_WHILE: WHILE -> type(WHILE) ;

Inside_PUBLIC: PUBLIC -> type(PUBLIC) ;
Inside_PRIVATE: PRIVATE -> type(PRIVATE) ;
Inside_SHARED: SHARED -> type(SHARED) ;
Inside_STATIC: STATIC -> type(STATIC) ;
Inside_OPERATOR: OPERATOR -> type(OPERATOR) ;
Inside_INLINE: INLINE -> type(INLINE) ;
Inside_SPAWNINIT: SPAWNINIT-> type(SPAWNINIT) ;

Inside_BooleanLiteral: BooleanLiteral -> type(BooleanLiteral) ;
Inside_IntegerLiteral: IntegerLiteral -> type(IntegerLiteral) ;
Inside_FloatLiteral: FloatLiteral -> type(FloatLiteral) ;

Inside_Identifier: Identifier -> type(Identifier) ;
Inside_Comment: (LineComment | DelimitedComment) -> channel(HIDDEN) ;
Inside_WS: WS -> skip ;
Inside_NL: NL -> skip ;