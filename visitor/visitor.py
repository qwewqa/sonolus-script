from .nodes import *
from grammar.ScriptParser import ScriptParser
from grammar.ScriptParserVisitor import ScriptParserVisitor


class ScriptVisitor(ScriptParserVisitor):
    def visitScriptFile(self, ctx: ScriptParser.ScriptFileContext):
        return ScriptFileNode(
            self.tryVisit(ctx.importList(), []),
            self.tryVisitList(ctx.topLevelObject())
        )

    def visitImportList(self, ctx: ScriptParser.ImportListContext):
        return self.tryVisitList(ctx.importHeader())

    def visitImportHeader(self, ctx: ScriptParser.ImportHeaderContext):
        return ImportHeaderNode(self.visit(ctx.simpleIdentifier()))

    def visitSimpleIdentifier(self, ctx: ScriptParser.SimpleIdentifierContext):
        return SimpleIdentifierNode(ctx.getText())

    def visitIdentifier(self, ctx: ScriptParser.IdentifierContext):
        return IdentifierNode(self.tryVisitList(ctx.simpleIdentifier()))

    def visitTopLevelObject(self, ctx: ScriptParser.TopLevelObjectContext):
        return self.visit(
            ctx.functionDeclaration() or
            ctx.constantDeclaration() or
            ctx.structDeclaration() or
            ctx.scriptDeclaration() or
            ctx.propertyDeclaration()
        )

    def visitStructDeclaration(self, ctx: ScriptParser.StructDeclarationContext):
        return StructDeclarationNode(
            self.tryVisit(ctx.modifierList()),
            self.visit(ctx.simpleIdentifier()),
            self.visit(ctx.structFields()),
            self.visit(ctx.structBody())
        )

    def visitStructFields(self, ctx: ScriptParser.StructFieldsContext):
        return self.tryVisitList(ctx.structField())

    def visitStructField(self, ctx: ScriptParser.StructFieldContext):
        return StructFieldNode(ctx.CONST() is not None, self.visit(ctx.simpleIdentifier()), self.visit(ctx.userType()))

    def visitStructBody(self, ctx: ScriptParser.StructBodyContext):
        return self.tryVisitList(ctx.structMemberDeclaration())

    def visitStructMemberDeclaration(self, ctx: ScriptParser.StructMemberDeclarationContext):
        return self.visit(
            ctx.functionDeclaration() or
            ctx.propertyDeclaration() or
            ctx.constantDeclaration()
        )

    def visitScriptDeclaration(self, ctx: ScriptParser.ScriptDeclarationContext):
        return ScriptDeclarationNode(
            self.visit(ctx.simpleIdentifier()),
            self.visit(ctx.scriptParameters()),
            self.visit(ctx.scriptBody())
        )

    def visitScriptParameters(self, ctx:ScriptParser.ScriptParametersContext):
        return self.tryVisitList(ctx.scriptParameter())

    def visitScriptParameter(self, ctx:ScriptParser.ScriptParameterContext):
        return self.visit(ctx.simpleIdentifier())

    def visitScriptBody(self, ctx: ScriptParser.ScriptBodyContext):
        return self.tryVisitList(ctx.scriptMemberDeclaration())

    def visitScriptMemberDeclaration(self, ctx: ScriptParser.ScriptMemberDeclarationContext):
        return self.visit(
            ctx.functionDeclaration() or
            ctx.propertyDeclaration() or
            ctx.constantDeclaration() or
            ctx.callbackDeclaration()
        )

    def visitCallbackDeclaration(self, ctx: ScriptParser.CallbackDeclarationContext):
        return CallbackDeclarationNode(self.visit(ctx.simpleIdentifier()), self.visit(ctx.functionBody()))

    def visitPropertyDeclaration(self, ctx: ScriptParser.PropertyDeclarationContext):
        return PropertyDeclarationNode(
            self.tryVisit(ctx.modifierList(), []),
            (ctx.VAR() or ctx.VAL() or ctx.PIT()).getText(),
            self.visit(ctx.simpleIdentifier()),
            self.tryVisit(ctx.expression()),
            self.tryVisit(ctx.getter()),
            self.tryVisit(ctx.setter())
        )

    def visitGetter(self, ctx: ScriptParser.GetterContext):
        return GetterNode(
            self.tryVisit(ctx.modifierList(), []),
            self.tryVisit(ctx.functionBody())
        )

    def visitSetter(self, ctx: ScriptParser.SetterContext):
        return SetterNode(
            self.tryVisit(ctx.modifierList(), []),
            self.tryVisit(ctx.simpleIdentifier()),
            self.tryVisit(ctx.functionBody())
        )

    def visitConstantDeclaration(self, ctx: ScriptParser.ConstantDeclarationContext):
        return ConstantDeclarationNode(
            self.tryVisit(ctx.modifierList(), []),
            self.visit(ctx.simpleIdentifier()),
            self.visit(ctx.expression())
        )

    def visitFunctionDeclaration(self, ctx: ScriptParser.FunctionDeclarationContext):
        return FunctionDeclarationNode(
            self.tryVisit(ctx.modifierList(), []),
            self.tryVisit(ctx.userType()),
            self.visit(ctx.simpleIdentifier()),
            self.visit(ctx.functionParameters()),
            self.visit(ctx.functionBody())
        )

    def visitFunctionParameters(self, ctx: ScriptParser.FunctionParametersContext):
        return self.tryVisitList(ctx.functionParameter())

    def visitFunctionParameter(self, ctx: ScriptParser.FunctionParameterContext):
        return self.visit(ctx.parameter())

    def visitFunctionBody(self, ctx: ScriptParser.FunctionBodyContext):
        return self.visit(ctx.block())

    def visitParameter(self, ctx: ScriptParser.ParameterContext):
        return ParameterNode(self.visit(ctx.simpleIdentifier()), self.tryVisit(ctx.userType()))

    def visitModifierList(self, ctx: ScriptParser.ModifierListContext):
        return self.tryVisitList(ctx.modifier())

    def visitModifier(self, ctx: ScriptParser.ModifierContext):
        return ctx.getText()

    def visitBlock(self, ctx: ScriptParser.BlockContext):
        return self.visit(ctx.statements())

    def visitStatements(self, ctx: ScriptParser.StatementsContext):
        return self.tryVisitList(ctx.statement())

    def visitStatement(self, ctx: ScriptParser.StatementContext):
        return self.visit(ctx.expression())

    def visitDeclaration(self, ctx: ScriptParser.DeclarationContext):
        return self.visit(ctx.functionDeclaration() or ctx.propertyDeclaration() or ctx.constantDeclaration())

    def visitExpression(self, ctx: ScriptParser.ExpressionContext):
        return self.visitGenericInfixExpression(ctx, right_associative=True)

    def visitDisjunction(self, ctx: ScriptParser.DisjunctionContext):
        return self.visitGenericInfixExpression(ctx)

    def visitConjunction(self, ctx: ScriptParser.ConjunctionContext):
        return self.visitGenericInfixExpression(ctx)

    def visitEqualityComparison(self, ctx: ScriptParser.EqualityComparisonContext):
        return self.visitGenericInfixExpression(ctx)

    def visitComparison(self, ctx: ScriptParser.ComparisonContext):
        return self.visitGenericInfixExpression(ctx)

    def visitInfixFunctionCall(self, ctx: ScriptParser.InfixFunctionCallContext):
        return self.visitGenericInfixExpression(ctx)

    def visitAdditiveExpression(self, ctx: ScriptParser.AdditiveExpressionContext):
        return self.visitGenericInfixExpression(ctx)

    def visitMultiplicativeExpression(self, ctx: ScriptParser.MultiplicativeExpressionContext):
        return self.visitGenericInfixExpression(ctx)

    def visitExponentiationExpression(self, ctx: ScriptParser.ExponentiationExpressionContext):
        return self.visitGenericInfixExpression(ctx)

    def visitPrefixUnaryExpression(self, ctx: ScriptParser.PrefixUnaryExpressionContext):
        children = [c for c in ctx.getChildren()]
        expr = self.visit(children.pop())
        while children:
            expr = UnaryExpressionNode(expr, children.pop().getText())
        return expr

    def visitPostfixUnaryExpression(self, ctx: ScriptParser.PostfixUnaryExpressionContext):
        children = [c for c in ctx.getChildren()]
        expr = self.visit(children.pop(0))
        while children:
            expr = UnaryExpressionNode(expr, self.visit(children.pop(0)))
        return expr

    def visitPostfixUnaryOperation(self, ctx: ScriptParser.PostfixUnaryOperationContext):
        if ctx.callSuffix():
            return self.visit(ctx.callSuffix())
        elif ctx.memberAccessOperator():
            return MemberAccessNode(self.visit(ctx.postfixUnaryExpression()))
        else:
            return ctx.getText()

    def visitCallSuffix(self, ctx: ScriptParser.CallSuffixContext):
        return self.visit(ctx.valueArguments())

    def visitValueArguments(self, ctx: ScriptParser.ValueArgumentsContext):
        return self.tryVisitList(ctx.valueArgument())

    def visitValueArgument(self, ctx: ScriptParser.ValueArgumentContext):
        return self.visit(ctx.expression())

    def visitAtomicExpression(self, ctx: ScriptParser.AtomicExpressionContext):
        return self.visit(
            ctx.parenthesizedExpression() or
            ctx.literalConstant() or
            ctx.conditionalExpression() or
            ctx.loopExpression() or
            ctx.simpleIdentifier()
        )

    def visitParenthesizedExpression(self, ctx: ScriptParser.ParenthesizedExpressionContext):
        return self.visit(ctx.expression())

    def visitLiteralConstant(self, ctx: ScriptParser.LiteralConstantContext):
        if ctx.FloatLiteral() or ctx.IntegerLiteral():
            return NumberLiteralNode(float(ctx.getText()))
        elif ctx.BooleanLiteral():
            return BooleanLiteralNode(ctx.getText() == 'true')

    def visitConditionalExpression(self, ctx: ScriptParser.ConditionalExpressionContext):
        return self.visit(ctx.ifExpression())

    def visitIfExpression(self, ctx: ScriptParser.IfExpressionContext):
        branches = ctx.controlStructureBody()
        if len(branches) == 1:
            return IfExpressionNode(self.visit(ctx.expression()), self.visit(branches[0]), None)
        else:
            return IfExpressionNode(self.visit(ctx.expression()), self.visit(branches[0]), self.visit(branches[1]))

    def visitLoopExpression(self, ctx: ScriptParser.LoopExpressionContext):
        return self.visit(ctx.whileExpression())

    def visitWhileExpression(self, ctx: ScriptParser.WhileExpressionContext):
        return WhileExpressionNode(self.visit(ctx.expression()), self.visit(ctx.controlStructureBody()))

    def visitControlStructureBody(self, ctx: ScriptParser.ControlStructureBodyContext):
        if ctx.expression():
            return [self.visit(ctx.expression())]
        else:
            return self.visit(ctx.block())

    def visitGenericInfixExpression(self, ctx, right_associative=False):
        children = [c for c in ctx.getChildren()]
        if not right_associative:
            expr = self.visit(children.pop(0))
            while children:
                op = children.pop(0).getText()
                rhs = self.visit(children.pop(0))
                expr = InfixExpressionNode(expr, op, rhs)
        else:
            expr = self.visit(children.pop())
            while children:
                op = children.pop().getText()
                lhs = self.visit(children.pop())
                expr = InfixExpressionNode(lhs, op, expr)
        return expr

    def tryVisit(self, tree, default=None):
        return (tree and self.visit(tree)) or default

    def tryVisitList(self, tree):
        try:
            iter(tree)
        except TypeError:
            return []
        return (tree and [self.visit(b) for b in tree]) or []
