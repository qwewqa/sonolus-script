parser grammar ScriptParser;

options { tokenVocab = ScriptLexer; }

scriptFile
    : NL* importList anysemi* (topLevelObject (anysemi+ topLevelObject?)*)? EOF
    ;

importList
    : importHeader*
    ;

importHeader
    : IMPORT simpleIdentifier semi?
    ;

topLevelObject
    : functionDeclaration
    | constantDeclaration
    | structDeclaration
    | scriptDeclaration
    | propertyDeclaration
    ;

structDeclaration
    : modifierList? STRUCT NL* simpleIdentifier
    structFields
    NL* structBody
    ;

structBody
    : LCURL NL* structMemberDeclaration* NL* RCURL
    ;

structMemberDeclaration
    : (functionDeclaration
    | propertyDeclaration
    | constantDeclaration) anysemi*
    ;

structFields
    : LPAREN (structField (COMMA structField)*)? RPAREN
    ;

structField
    : CONST? simpleIdentifier COLON userType
    ;

scriptDeclaration
    : SCRIPT NL* simpleIdentifier
    NL* scriptBody
    ;

scriptBody
    : LCURL NL* scriptMemberDeclaration* NL* RCURL
    ;

scriptMemberDeclaration
    : (functionDeclaration
    | propertyDeclaration
    | constantDeclaration
    | callbackDeclaration) anysemi*
    ;

propertyDeclaration
    : modifierList? (VAR | VAL)
    simpleIdentifier
    (NL* (ASSIGNMENT) NL* expression)?
    (NL* semi? NL* (getter (semi setter)? | setter (semi getter)?))?
    ;

callbackDeclaration
    : CALLBACK
    NL* simpleIdentifier
    NL* functionBody
    ;

functionDeclaration
    : modifierList? FUN
    (NL* userType NL* DOT)?
    NL* simpleIdentifier
    NL* functionParameters
    NL* functionBody
    ;

functionParameters
    : LPAREN (functionParameter (COMMA functionParameter)*)? RPAREN
    ;

functionParameter
    : parameter
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
    | propertyDeclaration
    | constantDeclaration
    ;

getter
    : modifierList? GETTER
    | modifierList? GETTER NL* LPAREN RPAREN (NL* COLON NL* userType)? NL* functionBody
    ;

setter
    : modifierList? SETTER
    | modifierList? SETTER NL* LPAREN (simpleIdentifier | parameter) RPAREN NL* functionBody
    ;

constantDeclaration
    : modifierList? CONST
    simpleIdentifier
    NL* (ASSIGNMENT) NL* expression
    ;

parameter
    : simpleIdentifier
    | simpleIdentifier COLON userType
    ;

userType
    : simpleIdentifier
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
    : exponentiationExpression (multiplicativeOperation NL* exponentiationExpression)*
    ;

exponentiationExpression
    : prefixUnaryExpression (POW NL* prefixUnaryExpression)*
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
    : expression
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

modifierList
    : modifier+
    ;

modifier
    : (PUBLIC
    | PRIVATE
    | SHARED
    | STATIC
    | OPERATOR
    | DATA) NL*
    ;

identifier
    : simpleIdentifier (NL* DOT simpleIdentifier)*
    ;

simpleIdentifier
    : Identifier
    //soft keywords:
    | DATA
    | GETTER
    | IMPORT
    | OPERATOR
    | PRIVATE
    | PUBLIC
    | SETTER
    //strong keywords
    | CONST
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