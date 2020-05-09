# Generated from ScriptParser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ScriptParser import ScriptParser
else:
    from ScriptParser import ScriptParser

# This class defines a complete generic visitor for a parse tree produced by ScriptParser.

class ScriptParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ScriptParser#scriptFile.
    def visitScriptFile(self, ctx:ScriptParser.ScriptFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#importList.
    def visitImportList(self, ctx:ScriptParser.ImportListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#importHeader.
    def visitImportHeader(self, ctx:ScriptParser.ImportHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#topLevelObject.
    def visitTopLevelObject(self, ctx:ScriptParser.TopLevelObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#levelvarDeclaration.
    def visitLevelvarDeclaration(self, ctx:ScriptParser.LevelvarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#archetypeDeclaration.
    def visitArchetypeDeclaration(self, ctx:ScriptParser.ArchetypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#archetypeName.
    def visitArchetypeName(self, ctx:ScriptParser.ArchetypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#archetypeDefaults.
    def visitArchetypeDefaults(self, ctx:ScriptParser.ArchetypeDefaultsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#archetypeDefault.
    def visitArchetypeDefault(self, ctx:ScriptParser.ArchetypeDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#structDeclaration.
    def visitStructDeclaration(self, ctx:ScriptParser.StructDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#structBody.
    def visitStructBody(self, ctx:ScriptParser.StructBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#structMemberDeclaration.
    def visitStructMemberDeclaration(self, ctx:ScriptParser.StructMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#structFields.
    def visitStructFields(self, ctx:ScriptParser.StructFieldsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#structField.
    def visitStructField(self, ctx:ScriptParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#scriptDeclaration.
    def visitScriptDeclaration(self, ctx:ScriptParser.ScriptDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#scriptParameters.
    def visitScriptParameters(self, ctx:ScriptParser.ScriptParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#scriptParameter.
    def visitScriptParameter(self, ctx:ScriptParser.ScriptParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#scriptBody.
    def visitScriptBody(self, ctx:ScriptParser.ScriptBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#scriptMemberDeclaration.
    def visitScriptMemberDeclaration(self, ctx:ScriptParser.ScriptMemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#propertyDeclaration.
    def visitPropertyDeclaration(self, ctx:ScriptParser.PropertyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#callbackDeclaration.
    def visitCallbackDeclaration(self, ctx:ScriptParser.CallbackDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#callbackOrder.
    def visitCallbackOrder(self, ctx:ScriptParser.CallbackOrderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#functionDeclaration.
    def visitFunctionDeclaration(self, ctx:ScriptParser.FunctionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#functionParameters.
    def visitFunctionParameters(self, ctx:ScriptParser.FunctionParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#functionParameter.
    def visitFunctionParameter(self, ctx:ScriptParser.FunctionParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#functionBody.
    def visitFunctionBody(self, ctx:ScriptParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#block.
    def visitBlock(self, ctx:ScriptParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#statements.
    def visitStatements(self, ctx:ScriptParser.StatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#statement.
    def visitStatement(self, ctx:ScriptParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#declaration.
    def visitDeclaration(self, ctx:ScriptParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#getter.
    def visitGetter(self, ctx:ScriptParser.GetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#setter.
    def visitSetter(self, ctx:ScriptParser.SetterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#constantDeclaration.
    def visitConstantDeclaration(self, ctx:ScriptParser.ConstantDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#parameter.
    def visitParameter(self, ctx:ScriptParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#userType.
    def visitUserType(self, ctx:ScriptParser.UserTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#expression.
    def visitExpression(self, ctx:ScriptParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#disjunction.
    def visitDisjunction(self, ctx:ScriptParser.DisjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#conjunction.
    def visitConjunction(self, ctx:ScriptParser.ConjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#equalityComparison.
    def visitEqualityComparison(self, ctx:ScriptParser.EqualityComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#comparison.
    def visitComparison(self, ctx:ScriptParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#infixFunctionCall.
    def visitInfixFunctionCall(self, ctx:ScriptParser.InfixFunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:ScriptParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:ScriptParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#exponentiationExpression.
    def visitExponentiationExpression(self, ctx:ScriptParser.ExponentiationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#prefixUnaryExpression.
    def visitPrefixUnaryExpression(self, ctx:ScriptParser.PrefixUnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#postfixUnaryExpression.
    def visitPostfixUnaryExpression(self, ctx:ScriptParser.PostfixUnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#atomicExpression.
    def visitAtomicExpression(self, ctx:ScriptParser.AtomicExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#parenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:ScriptParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#callSuffix.
    def visitCallSuffix(self, ctx:ScriptParser.CallSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#valueArguments.
    def visitValueArguments(self, ctx:ScriptParser.ValueArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#valueArgument.
    def visitValueArgument(self, ctx:ScriptParser.ValueArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:ScriptParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#ifExpression.
    def visitIfExpression(self, ctx:ScriptParser.IfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#controlStructureBody.
    def visitControlStructureBody(self, ctx:ScriptParser.ControlStructureBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#loopExpression.
    def visitLoopExpression(self, ctx:ScriptParser.LoopExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#whileExpression.
    def visitWhileExpression(self, ctx:ScriptParser.WhileExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#modifierList.
    def visitModifierList(self, ctx:ScriptParser.ModifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#modifier.
    def visitModifier(self, ctx:ScriptParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#identifier.
    def visitIdentifier(self, ctx:ScriptParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#simpleIdentifier.
    def visitSimpleIdentifier(self, ctx:ScriptParser.SimpleIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#literalConstant.
    def visitLiteralConstant(self, ctx:ScriptParser.LiteralConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#additiveOperator.
    def visitAdditiveOperator(self, ctx:ScriptParser.AdditiveOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#multiplicativeOperation.
    def visitMultiplicativeOperation(self, ctx:ScriptParser.MultiplicativeOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#prefixUnaryOperation.
    def visitPrefixUnaryOperation(self, ctx:ScriptParser.PrefixUnaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#postfixUnaryOperation.
    def visitPostfixUnaryOperation(self, ctx:ScriptParser.PostfixUnaryOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#memberAccessOperator.
    def visitMemberAccessOperator(self, ctx:ScriptParser.MemberAccessOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:ScriptParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#equalityOperation.
    def visitEqualityOperation(self, ctx:ScriptParser.EqualityOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#comparisonOperator.
    def visitComparisonOperator(self, ctx:ScriptParser.ComparisonOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#semi.
    def visitSemi(self, ctx:ScriptParser.SemiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ScriptParser#anysemi.
    def visitAnysemi(self, ctx:ScriptParser.AnysemiContext):
        return self.visitChildren(ctx)



del ScriptParser