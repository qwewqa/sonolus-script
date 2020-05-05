# Generated from ScriptParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ScriptParser import ScriptParser
else:
    from ScriptParser import ScriptParser

# This class defines a complete listener for a parse tree produced by ScriptParser.
class ScriptParserListener(ParseTreeListener):

    # Enter a parse tree produced by ScriptParser#scriptFile.
    def enterScriptFile(self, ctx:ScriptParser.ScriptFileContext):
        pass

    # Exit a parse tree produced by ScriptParser#scriptFile.
    def exitScriptFile(self, ctx:ScriptParser.ScriptFileContext):
        pass


    # Enter a parse tree produced by ScriptParser#importList.
    def enterImportList(self, ctx:ScriptParser.ImportListContext):
        pass

    # Exit a parse tree produced by ScriptParser#importList.
    def exitImportList(self, ctx:ScriptParser.ImportListContext):
        pass


    # Enter a parse tree produced by ScriptParser#importHeader.
    def enterImportHeader(self, ctx:ScriptParser.ImportHeaderContext):
        pass

    # Exit a parse tree produced by ScriptParser#importHeader.
    def exitImportHeader(self, ctx:ScriptParser.ImportHeaderContext):
        pass


    # Enter a parse tree produced by ScriptParser#topLevelObject.
    def enterTopLevelObject(self, ctx:ScriptParser.TopLevelObjectContext):
        pass

    # Exit a parse tree produced by ScriptParser#topLevelObject.
    def exitTopLevelObject(self, ctx:ScriptParser.TopLevelObjectContext):
        pass


    # Enter a parse tree produced by ScriptParser#structDeclaration.
    def enterStructDeclaration(self, ctx:ScriptParser.StructDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#structDeclaration.
    def exitStructDeclaration(self, ctx:ScriptParser.StructDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#structBody.
    def enterStructBody(self, ctx:ScriptParser.StructBodyContext):
        pass

    # Exit a parse tree produced by ScriptParser#structBody.
    def exitStructBody(self, ctx:ScriptParser.StructBodyContext):
        pass


    # Enter a parse tree produced by ScriptParser#structMemberDeclaration.
    def enterStructMemberDeclaration(self, ctx:ScriptParser.StructMemberDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#structMemberDeclaration.
    def exitStructMemberDeclaration(self, ctx:ScriptParser.StructMemberDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#structFields.
    def enterStructFields(self, ctx:ScriptParser.StructFieldsContext):
        pass

    # Exit a parse tree produced by ScriptParser#structFields.
    def exitStructFields(self, ctx:ScriptParser.StructFieldsContext):
        pass


    # Enter a parse tree produced by ScriptParser#structField.
    def enterStructField(self, ctx:ScriptParser.StructFieldContext):
        pass

    # Exit a parse tree produced by ScriptParser#structField.
    def exitStructField(self, ctx:ScriptParser.StructFieldContext):
        pass


    # Enter a parse tree produced by ScriptParser#scriptDeclaration.
    def enterScriptDeclaration(self, ctx:ScriptParser.ScriptDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#scriptDeclaration.
    def exitScriptDeclaration(self, ctx:ScriptParser.ScriptDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#scriptBody.
    def enterScriptBody(self, ctx:ScriptParser.ScriptBodyContext):
        pass

    # Exit a parse tree produced by ScriptParser#scriptBody.
    def exitScriptBody(self, ctx:ScriptParser.ScriptBodyContext):
        pass


    # Enter a parse tree produced by ScriptParser#scriptMemberDeclaration.
    def enterScriptMemberDeclaration(self, ctx:ScriptParser.ScriptMemberDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#scriptMemberDeclaration.
    def exitScriptMemberDeclaration(self, ctx:ScriptParser.ScriptMemberDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#propertyDeclaration.
    def enterPropertyDeclaration(self, ctx:ScriptParser.PropertyDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#propertyDeclaration.
    def exitPropertyDeclaration(self, ctx:ScriptParser.PropertyDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#callbackDeclaration.
    def enterCallbackDeclaration(self, ctx:ScriptParser.CallbackDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#callbackDeclaration.
    def exitCallbackDeclaration(self, ctx:ScriptParser.CallbackDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:ScriptParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:ScriptParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#functionParameters.
    def enterFunctionParameters(self, ctx:ScriptParser.FunctionParametersContext):
        pass

    # Exit a parse tree produced by ScriptParser#functionParameters.
    def exitFunctionParameters(self, ctx:ScriptParser.FunctionParametersContext):
        pass


    # Enter a parse tree produced by ScriptParser#functionParameter.
    def enterFunctionParameter(self, ctx:ScriptParser.FunctionParameterContext):
        pass

    # Exit a parse tree produced by ScriptParser#functionParameter.
    def exitFunctionParameter(self, ctx:ScriptParser.FunctionParameterContext):
        pass


    # Enter a parse tree produced by ScriptParser#functionBody.
    def enterFunctionBody(self, ctx:ScriptParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by ScriptParser#functionBody.
    def exitFunctionBody(self, ctx:ScriptParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by ScriptParser#block.
    def enterBlock(self, ctx:ScriptParser.BlockContext):
        pass

    # Exit a parse tree produced by ScriptParser#block.
    def exitBlock(self, ctx:ScriptParser.BlockContext):
        pass


    # Enter a parse tree produced by ScriptParser#statements.
    def enterStatements(self, ctx:ScriptParser.StatementsContext):
        pass

    # Exit a parse tree produced by ScriptParser#statements.
    def exitStatements(self, ctx:ScriptParser.StatementsContext):
        pass


    # Enter a parse tree produced by ScriptParser#statement.
    def enterStatement(self, ctx:ScriptParser.StatementContext):
        pass

    # Exit a parse tree produced by ScriptParser#statement.
    def exitStatement(self, ctx:ScriptParser.StatementContext):
        pass


    # Enter a parse tree produced by ScriptParser#declaration.
    def enterDeclaration(self, ctx:ScriptParser.DeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#declaration.
    def exitDeclaration(self, ctx:ScriptParser.DeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#getter.
    def enterGetter(self, ctx:ScriptParser.GetterContext):
        pass

    # Exit a parse tree produced by ScriptParser#getter.
    def exitGetter(self, ctx:ScriptParser.GetterContext):
        pass


    # Enter a parse tree produced by ScriptParser#setter.
    def enterSetter(self, ctx:ScriptParser.SetterContext):
        pass

    # Exit a parse tree produced by ScriptParser#setter.
    def exitSetter(self, ctx:ScriptParser.SetterContext):
        pass


    # Enter a parse tree produced by ScriptParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:ScriptParser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by ScriptParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:ScriptParser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by ScriptParser#parameter.
    def enterParameter(self, ctx:ScriptParser.ParameterContext):
        pass

    # Exit a parse tree produced by ScriptParser#parameter.
    def exitParameter(self, ctx:ScriptParser.ParameterContext):
        pass


    # Enter a parse tree produced by ScriptParser#userType.
    def enterUserType(self, ctx:ScriptParser.UserTypeContext):
        pass

    # Exit a parse tree produced by ScriptParser#userType.
    def exitUserType(self, ctx:ScriptParser.UserTypeContext):
        pass


    # Enter a parse tree produced by ScriptParser#expression.
    def enterExpression(self, ctx:ScriptParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#expression.
    def exitExpression(self, ctx:ScriptParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#disjunction.
    def enterDisjunction(self, ctx:ScriptParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by ScriptParser#disjunction.
    def exitDisjunction(self, ctx:ScriptParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by ScriptParser#conjunction.
    def enterConjunction(self, ctx:ScriptParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by ScriptParser#conjunction.
    def exitConjunction(self, ctx:ScriptParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by ScriptParser#equalityComparison.
    def enterEqualityComparison(self, ctx:ScriptParser.EqualityComparisonContext):
        pass

    # Exit a parse tree produced by ScriptParser#equalityComparison.
    def exitEqualityComparison(self, ctx:ScriptParser.EqualityComparisonContext):
        pass


    # Enter a parse tree produced by ScriptParser#comparison.
    def enterComparison(self, ctx:ScriptParser.ComparisonContext):
        pass

    # Exit a parse tree produced by ScriptParser#comparison.
    def exitComparison(self, ctx:ScriptParser.ComparisonContext):
        pass


    # Enter a parse tree produced by ScriptParser#infixFunctionCall.
    def enterInfixFunctionCall(self, ctx:ScriptParser.InfixFunctionCallContext):
        pass

    # Exit a parse tree produced by ScriptParser#infixFunctionCall.
    def exitInfixFunctionCall(self, ctx:ScriptParser.InfixFunctionCallContext):
        pass


    # Enter a parse tree produced by ScriptParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:ScriptParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:ScriptParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:ScriptParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:ScriptParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#exponentiationExpression.
    def enterExponentiationExpression(self, ctx:ScriptParser.ExponentiationExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#exponentiationExpression.
    def exitExponentiationExpression(self, ctx:ScriptParser.ExponentiationExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#prefixUnaryExpression.
    def enterPrefixUnaryExpression(self, ctx:ScriptParser.PrefixUnaryExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#prefixUnaryExpression.
    def exitPrefixUnaryExpression(self, ctx:ScriptParser.PrefixUnaryExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#postfixUnaryExpression.
    def enterPostfixUnaryExpression(self, ctx:ScriptParser.PostfixUnaryExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#postfixUnaryExpression.
    def exitPostfixUnaryExpression(self, ctx:ScriptParser.PostfixUnaryExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#atomicExpression.
    def enterAtomicExpression(self, ctx:ScriptParser.AtomicExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#atomicExpression.
    def exitAtomicExpression(self, ctx:ScriptParser.AtomicExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#parenthesizedExpression.
    def enterParenthesizedExpression(self, ctx:ScriptParser.ParenthesizedExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#parenthesizedExpression.
    def exitParenthesizedExpression(self, ctx:ScriptParser.ParenthesizedExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#callSuffix.
    def enterCallSuffix(self, ctx:ScriptParser.CallSuffixContext):
        pass

    # Exit a parse tree produced by ScriptParser#callSuffix.
    def exitCallSuffix(self, ctx:ScriptParser.CallSuffixContext):
        pass


    # Enter a parse tree produced by ScriptParser#valueArguments.
    def enterValueArguments(self, ctx:ScriptParser.ValueArgumentsContext):
        pass

    # Exit a parse tree produced by ScriptParser#valueArguments.
    def exitValueArguments(self, ctx:ScriptParser.ValueArgumentsContext):
        pass


    # Enter a parse tree produced by ScriptParser#valueArgument.
    def enterValueArgument(self, ctx:ScriptParser.ValueArgumentContext):
        pass

    # Exit a parse tree produced by ScriptParser#valueArgument.
    def exitValueArgument(self, ctx:ScriptParser.ValueArgumentContext):
        pass


    # Enter a parse tree produced by ScriptParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:ScriptParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:ScriptParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#ifExpression.
    def enterIfExpression(self, ctx:ScriptParser.IfExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#ifExpression.
    def exitIfExpression(self, ctx:ScriptParser.IfExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#controlStructureBody.
    def enterControlStructureBody(self, ctx:ScriptParser.ControlStructureBodyContext):
        pass

    # Exit a parse tree produced by ScriptParser#controlStructureBody.
    def exitControlStructureBody(self, ctx:ScriptParser.ControlStructureBodyContext):
        pass


    # Enter a parse tree produced by ScriptParser#loopExpression.
    def enterLoopExpression(self, ctx:ScriptParser.LoopExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#loopExpression.
    def exitLoopExpression(self, ctx:ScriptParser.LoopExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#whileExpression.
    def enterWhileExpression(self, ctx:ScriptParser.WhileExpressionContext):
        pass

    # Exit a parse tree produced by ScriptParser#whileExpression.
    def exitWhileExpression(self, ctx:ScriptParser.WhileExpressionContext):
        pass


    # Enter a parse tree produced by ScriptParser#modifierList.
    def enterModifierList(self, ctx:ScriptParser.ModifierListContext):
        pass

    # Exit a parse tree produced by ScriptParser#modifierList.
    def exitModifierList(self, ctx:ScriptParser.ModifierListContext):
        pass


    # Enter a parse tree produced by ScriptParser#modifier.
    def enterModifier(self, ctx:ScriptParser.ModifierContext):
        pass

    # Exit a parse tree produced by ScriptParser#modifier.
    def exitModifier(self, ctx:ScriptParser.ModifierContext):
        pass


    # Enter a parse tree produced by ScriptParser#identifier.
    def enterIdentifier(self, ctx:ScriptParser.IdentifierContext):
        pass

    # Exit a parse tree produced by ScriptParser#identifier.
    def exitIdentifier(self, ctx:ScriptParser.IdentifierContext):
        pass


    # Enter a parse tree produced by ScriptParser#simpleIdentifier.
    def enterSimpleIdentifier(self, ctx:ScriptParser.SimpleIdentifierContext):
        pass

    # Exit a parse tree produced by ScriptParser#simpleIdentifier.
    def exitSimpleIdentifier(self, ctx:ScriptParser.SimpleIdentifierContext):
        pass


    # Enter a parse tree produced by ScriptParser#literalConstant.
    def enterLiteralConstant(self, ctx:ScriptParser.LiteralConstantContext):
        pass

    # Exit a parse tree produced by ScriptParser#literalConstant.
    def exitLiteralConstant(self, ctx:ScriptParser.LiteralConstantContext):
        pass


    # Enter a parse tree produced by ScriptParser#additiveOperator.
    def enterAdditiveOperator(self, ctx:ScriptParser.AdditiveOperatorContext):
        pass

    # Exit a parse tree produced by ScriptParser#additiveOperator.
    def exitAdditiveOperator(self, ctx:ScriptParser.AdditiveOperatorContext):
        pass


    # Enter a parse tree produced by ScriptParser#multiplicativeOperation.
    def enterMultiplicativeOperation(self, ctx:ScriptParser.MultiplicativeOperationContext):
        pass

    # Exit a parse tree produced by ScriptParser#multiplicativeOperation.
    def exitMultiplicativeOperation(self, ctx:ScriptParser.MultiplicativeOperationContext):
        pass


    # Enter a parse tree produced by ScriptParser#prefixUnaryOperation.
    def enterPrefixUnaryOperation(self, ctx:ScriptParser.PrefixUnaryOperationContext):
        pass

    # Exit a parse tree produced by ScriptParser#prefixUnaryOperation.
    def exitPrefixUnaryOperation(self, ctx:ScriptParser.PrefixUnaryOperationContext):
        pass


    # Enter a parse tree produced by ScriptParser#postfixUnaryOperation.
    def enterPostfixUnaryOperation(self, ctx:ScriptParser.PostfixUnaryOperationContext):
        pass

    # Exit a parse tree produced by ScriptParser#postfixUnaryOperation.
    def exitPostfixUnaryOperation(self, ctx:ScriptParser.PostfixUnaryOperationContext):
        pass


    # Enter a parse tree produced by ScriptParser#memberAccessOperator.
    def enterMemberAccessOperator(self, ctx:ScriptParser.MemberAccessOperatorContext):
        pass

    # Exit a parse tree produced by ScriptParser#memberAccessOperator.
    def exitMemberAccessOperator(self, ctx:ScriptParser.MemberAccessOperatorContext):
        pass


    # Enter a parse tree produced by ScriptParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:ScriptParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by ScriptParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:ScriptParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by ScriptParser#equalityOperation.
    def enterEqualityOperation(self, ctx:ScriptParser.EqualityOperationContext):
        pass

    # Exit a parse tree produced by ScriptParser#equalityOperation.
    def exitEqualityOperation(self, ctx:ScriptParser.EqualityOperationContext):
        pass


    # Enter a parse tree produced by ScriptParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:ScriptParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by ScriptParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:ScriptParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by ScriptParser#semi.
    def enterSemi(self, ctx:ScriptParser.SemiContext):
        pass

    # Exit a parse tree produced by ScriptParser#semi.
    def exitSemi(self, ctx:ScriptParser.SemiContext):
        pass


    # Enter a parse tree produced by ScriptParser#anysemi.
    def enterAnysemi(self, ctx:ScriptParser.AnysemiContext):
        pass

    # Exit a parse tree produced by ScriptParser#anysemi.
    def exitAnysemi(self, ctx:ScriptParser.AnysemiContext):
        pass



del ScriptParser