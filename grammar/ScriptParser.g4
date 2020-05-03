parser grammar ScriptParser;

options { tokenVocab = ScriptLexer; }

scriptFile
    : NL* anysemi* (topLevelObject (anysemi+ topLevelObject?)*)? EOF
    ;

topLevelObject
    : functionDeclaration
    | variableDeclaration
    ;

functionDeclaration
    : FUN
    NL* simpleIdentifier
    NL* functionParameters
    NL* functionBody
    ;

functionParameters
    : LPAREN (functionParameter (COMMA functionParameter)*)? RPAREN
    ;

functionParameter
    : simpleIdentifier // (ASSIGNMENT expression)?
    ;

functionBody
    : block
    ;

block
    : LCURL statements RCURL
    ;

statements
    : anysemi* (statement (anysemi+ statement?)*)?
    ;

statement
    : declaration
    | expression
    ;

declaration
    : functionDeclaration
    | variableDeclaration
    ;

variableDeclaration
    : VAR
    simpleIdentifier
    (NL* (ASSIGNMENT) NL* expression)
    ;

expression
    : disjunction (assignmentOperator disjunction)*
    ;

disjunction
    : conjunction (NL* DISJ NL* conjunction)*
    ;

conjunction
    : equalityComparison (NL* CONJ NL* equalityComparison)*
    ;

equalityComparison
    : comparison (equalityOperation NL* comparison)*
    ;

comparison
    : infixFunctionCall (comparisonOperator NL* infixFunctionCall)?
    ;

infixFunctionCall
    : additiveExpression (simpleIdentifier NL* additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression (additiveOperator NL* multiplicativeExpression)*
    ;

multiplicativeExpression
    : prefixUnaryExpression (multiplicativeOperation NL* prefixUnaryExpression)*
    ;

prefixUnaryExpression
    : prefixUnaryOperation* postfixUnaryExpression
    ;

postfixUnaryExpression
    : atomicExpression postfixUnaryOperation*
    ;

atomicExpression
    : parenthesizedExpression
    | literalConstant
    | conditionalExpression
    | loopExpression
    | simpleIdentifier
    ;

parenthesizedExpression
    : LPAREN expression RPAREN
    ;

callSuffix
    : valueArguments
    ;

valueArguments
    : LPAREN (valueArgument (COMMA valueArgument)*)? RPAREN
    ;

valueArgument
    : (simpleIdentifier NL* ASSIGNMENT NL*)? NL* expression
    ;

conditionalExpression
    : ifExpression
    ;

ifExpression
    : IF NL* LPAREN expression RPAREN NL* controlStructureBody? SEMICOLON?
    (NL* ELSE NL* controlStructureBody?)?
    ;

controlStructureBody
    : block
    | expression
    ;

loopExpression
    : whileExpression
    ;

whileExpression
    : WHILE NL* LPAREN expression RPAREN NL* controlStructureBody?
    ;

identifier
    : simpleIdentifier (NL* DOT simpleIdentifier)*
    ;

simpleIdentifier
    : Identifier
    ;

literalConstant
    : BooleanLiteral
    | IntegerLiteral
    | FloatLiteral
    ;

additiveOperator
    : ADD | SUB
    ;

multiplicativeOperation
    : MULT
    | DIV
    | MOD
    ;

prefixUnaryOperation
    : INCR
    | DECR
    | ADD
    | SUB
    | EXCL
    ;

postfixUnaryOperation
    : INCR | DECR | EXCL EXCL
    | callSuffix
    | NL* memberAccessOperator postfixUnaryExpression
    ;

memberAccessOperator
    : DOT
    ;

assignmentOperator
    : ASSIGNMENT
    | ADD_ASSIGNMENT
    | SUB_ASSIGNMENT
    | MULT_ASSIGNMENT
    | DIV_ASSIGNMENT
    | MOD_ASSIGNMENT
    ;

equalityOperation
    : EXCL_EQ
    | EQEQ
    ;

comparisonOperator
    : LANGLE
    | RANGLE
    | LE
    | GE
    ;

semi: NL+ | NL* SEMICOLON NL*;

anysemi: NL | SEMICOLON;
