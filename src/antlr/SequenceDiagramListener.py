# Generated from ./src/antlr/SequenceDiagram.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SequenceDiagramParser import SequenceDiagramParser
else:
    from SequenceDiagramParser import SequenceDiagramParser

# This class defines a complete listener for a parse tree produced by SequenceDiagramParser.
class SequenceDiagramListener(ParseTreeListener):

    # Enter a parse tree produced by SequenceDiagramParser#sequence.
    def enterSequence(self, ctx:SequenceDiagramParser.SequenceContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#sequence.
    def exitSequence(self, ctx:SequenceDiagramParser.SequenceContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#statement.
    def enterStatement(self, ctx:SequenceDiagramParser.StatementContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#statement.
    def exitStatement(self, ctx:SequenceDiagramParser.StatementContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#messageStmt.
    def enterMessageStmt(self, ctx:SequenceDiagramParser.MessageStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#messageStmt.
    def exitMessageStmt(self, ctx:SequenceDiagramParser.MessageStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#participantDecl.
    def enterParticipantDecl(self, ctx:SequenceDiagramParser.ParticipantDeclContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#participantDecl.
    def exitParticipantDecl(self, ctx:SequenceDiagramParser.ParticipantDeclContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#callStmt.
    def enterCallStmt(self, ctx:SequenceDiagramParser.CallStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#callStmt.
    def exitCallStmt(self, ctx:SequenceDiagramParser.CallStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#returnStmt.
    def enterReturnStmt(self, ctx:SequenceDiagramParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#returnStmt.
    def exitReturnStmt(self, ctx:SequenceDiagramParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#selfCallStmt.
    def enterSelfCallStmt(self, ctx:SequenceDiagramParser.SelfCallStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#selfCallStmt.
    def exitSelfCallStmt(self, ctx:SequenceDiagramParser.SelfCallStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#altStmt.
    def enterAltStmt(self, ctx:SequenceDiagramParser.AltStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#altStmt.
    def exitAltStmt(self, ctx:SequenceDiagramParser.AltStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#elseBlock.
    def enterElseBlock(self, ctx:SequenceDiagramParser.ElseBlockContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#elseBlock.
    def exitElseBlock(self, ctx:SequenceDiagramParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#loopStmt.
    def enterLoopStmt(self, ctx:SequenceDiagramParser.LoopStmtContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#loopStmt.
    def exitLoopStmt(self, ctx:SequenceDiagramParser.LoopStmtContext):
        pass


    # Enter a parse tree produced by SequenceDiagramParser#condition.
    def enterCondition(self, ctx:SequenceDiagramParser.ConditionContext):
        pass

    # Exit a parse tree produced by SequenceDiagramParser#condition.
    def exitCondition(self, ctx:SequenceDiagramParser.ConditionContext):
        pass



del SequenceDiagramParser