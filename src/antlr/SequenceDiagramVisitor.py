# Generated from ./src/antlr/SequenceDiagram.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SequenceDiagramParser import SequenceDiagramParser
else:
    from SequenceDiagramParser import SequenceDiagramParser

# This class defines a complete generic visitor for a parse tree produced by SequenceDiagramParser.

class SequenceDiagramVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SequenceDiagramParser#sequence.
    def visitSequence(self, ctx:SequenceDiagramParser.SequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#statement.
    def visitStatement(self, ctx:SequenceDiagramParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#messageStmt.
    def visitMessageStmt(self, ctx:SequenceDiagramParser.MessageStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#participantDecl.
    def visitParticipantDecl(self, ctx:SequenceDiagramParser.ParticipantDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#callStmt.
    def visitCallStmt(self, ctx:SequenceDiagramParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#returnStmt.
    def visitReturnStmt(self, ctx:SequenceDiagramParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#selfCallStmt.
    def visitSelfCallStmt(self, ctx:SequenceDiagramParser.SelfCallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#altStmt.
    def visitAltStmt(self, ctx:SequenceDiagramParser.AltStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#elseBlock.
    def visitElseBlock(self, ctx:SequenceDiagramParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#loopStmt.
    def visitLoopStmt(self, ctx:SequenceDiagramParser.LoopStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceDiagramParser#condition.
    def visitCondition(self, ctx:SequenceDiagramParser.ConditionContext):
        return self.visitChildren(ctx)



del SequenceDiagramParser