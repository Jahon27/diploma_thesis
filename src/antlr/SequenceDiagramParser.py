# Generated from ./src/antlr/SequenceDiagram.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,10,95,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,5,0,24,8,0,10,0,12,0,27,
        9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,35,8,1,1,2,1,2,1,2,3,2,40,8,2,1,
        3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,
        6,1,6,1,7,1,7,1,7,5,7,63,8,7,10,7,12,7,66,9,7,1,7,3,7,69,8,7,1,7,
        1,7,1,8,1,8,3,8,75,8,8,1,8,5,8,78,8,8,10,8,12,8,81,9,8,1,9,1,9,1,
        9,5,9,86,8,9,10,9,12,9,89,9,9,1,9,1,9,1,10,1,10,1,10,0,0,11,0,2,
        4,6,8,10,12,14,16,18,20,0,0,94,0,25,1,0,0,0,2,34,1,0,0,0,4,39,1,
        0,0,0,6,41,1,0,0,0,8,45,1,0,0,0,10,50,1,0,0,0,12,55,1,0,0,0,14,59,
        1,0,0,0,16,72,1,0,0,0,18,82,1,0,0,0,20,92,1,0,0,0,22,24,3,2,1,0,
        23,22,1,0,0,0,24,27,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,28,1,
        0,0,0,27,25,1,0,0,0,28,29,5,0,0,1,29,1,1,0,0,0,30,35,3,6,3,0,31,
        35,3,4,2,0,32,35,3,14,7,0,33,35,3,18,9,0,34,30,1,0,0,0,34,31,1,0,
        0,0,34,32,1,0,0,0,34,33,1,0,0,0,35,3,1,0,0,0,36,40,3,8,4,0,37,40,
        3,10,5,0,38,40,3,12,6,0,39,36,1,0,0,0,39,37,1,0,0,0,39,38,1,0,0,
        0,40,5,1,0,0,0,41,42,5,1,0,0,42,43,5,9,0,0,43,44,5,9,0,0,44,7,1,
        0,0,0,45,46,5,2,0,0,46,47,5,9,0,0,47,48,5,9,0,0,48,49,5,9,0,0,49,
        9,1,0,0,0,50,51,5,3,0,0,51,52,5,9,0,0,52,53,5,9,0,0,53,54,5,9,0,
        0,54,11,1,0,0,0,55,56,5,4,0,0,56,57,5,9,0,0,57,58,5,9,0,0,58,13,
        1,0,0,0,59,60,5,5,0,0,60,64,3,20,10,0,61,63,3,2,1,0,62,61,1,0,0,
        0,63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,65,68,1,0,0,0,66,64,
        1,0,0,0,67,69,3,16,8,0,68,67,1,0,0,0,68,69,1,0,0,0,69,70,1,0,0,0,
        70,71,5,6,0,0,71,15,1,0,0,0,72,74,5,7,0,0,73,75,3,20,10,0,74,73,
        1,0,0,0,74,75,1,0,0,0,75,79,1,0,0,0,76,78,3,2,1,0,77,76,1,0,0,0,
        78,81,1,0,0,0,79,77,1,0,0,0,79,80,1,0,0,0,80,17,1,0,0,0,81,79,1,
        0,0,0,82,83,5,8,0,0,83,87,3,20,10,0,84,86,3,2,1,0,85,84,1,0,0,0,
        86,89,1,0,0,0,87,85,1,0,0,0,87,88,1,0,0,0,88,90,1,0,0,0,89,87,1,
        0,0,0,90,91,5,6,0,0,91,19,1,0,0,0,92,93,5,9,0,0,93,21,1,0,0,0,8,
        25,34,39,64,68,74,79,87
    ]

class SequenceDiagramParser ( Parser ):

    grammarFileName = "SequenceDiagram.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'participant'", "'call'", "'return'", 
                     "'self'", "'alt'", "'end'", "'else'", "'loop'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ID", "WS" ]

    RULE_sequence = 0
    RULE_statement = 1
    RULE_messageStmt = 2
    RULE_participantDecl = 3
    RULE_callStmt = 4
    RULE_returnStmt = 5
    RULE_selfCallStmt = 6
    RULE_altStmt = 7
    RULE_elseBlock = 8
    RULE_loopStmt = 9
    RULE_condition = 10

    ruleNames =  [ "sequence", "statement", "messageStmt", "participantDecl", 
                   "callStmt", "returnStmt", "selfCallStmt", "altStmt", 
                   "elseBlock", "loopStmt", "condition" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    ID=9
    WS=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(SequenceDiagramParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceDiagramParser.StatementContext)
            else:
                return self.getTypedRuleContext(SequenceDiagramParser.StatementContext,i)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_sequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSequence" ):
                listener.enterSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSequence" ):
                listener.exitSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSequence" ):
                return visitor.visitSequence(self)
            else:
                return visitor.visitChildren(self)




    def sequence(self):

        localctx = SequenceDiagramParser.SequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 318) != 0):
                self.state = 22
                self.statement()
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(SequenceDiagramParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def participantDecl(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ParticipantDeclContext,0)


        def messageStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.MessageStmtContext,0)


        def altStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.AltStmtContext,0)


        def loopStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.LoopStmtContext,0)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SequenceDiagramParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 30
                self.participantDecl()
                pass
            elif token in [2, 3, 4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.messageStmt()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 32
                self.altStmt()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 4)
                self.state = 33
                self.loopStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MessageStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def callStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.CallStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ReturnStmtContext,0)


        def selfCallStmt(self):
            return self.getTypedRuleContext(SequenceDiagramParser.SelfCallStmtContext,0)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_messageStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMessageStmt" ):
                listener.enterMessageStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMessageStmt" ):
                listener.exitMessageStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMessageStmt" ):
                return visitor.visitMessageStmt(self)
            else:
                return visitor.visitChildren(self)




    def messageStmt(self):

        localctx = SequenceDiagramParser.MessageStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_messageStmt)
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.callStmt()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 37
                self.returnStmt()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 3)
                self.state = 38
                self.selfCallStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParticipantDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(SequenceDiagramParser.ID)
            else:
                return self.getToken(SequenceDiagramParser.ID, i)

        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_participantDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParticipantDecl" ):
                listener.enterParticipantDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParticipantDecl" ):
                listener.exitParticipantDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParticipantDecl" ):
                return visitor.visitParticipantDecl(self)
            else:
                return visitor.visitChildren(self)




    def participantDecl(self):

        localctx = SequenceDiagramParser.ParticipantDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_participantDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(SequenceDiagramParser.T__0)
            self.state = 42
            self.match(SequenceDiagramParser.ID)
            self.state = 43
            self.match(SequenceDiagramParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(SequenceDiagramParser.ID)
            else:
                return self.getToken(SequenceDiagramParser.ID, i)

        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_callStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallStmt" ):
                listener.enterCallStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallStmt" ):
                listener.exitCallStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallStmt" ):
                return visitor.visitCallStmt(self)
            else:
                return visitor.visitChildren(self)




    def callStmt(self):

        localctx = SequenceDiagramParser.CallStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_callStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(SequenceDiagramParser.T__1)
            self.state = 46
            self.match(SequenceDiagramParser.ID)
            self.state = 47
            self.match(SequenceDiagramParser.ID)
            self.state = 48
            self.match(SequenceDiagramParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(SequenceDiagramParser.ID)
            else:
                return self.getToken(SequenceDiagramParser.ID, i)

        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = SequenceDiagramParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.match(SequenceDiagramParser.T__2)
            self.state = 51
            self.match(SequenceDiagramParser.ID)
            self.state = 52
            self.match(SequenceDiagramParser.ID)
            self.state = 53
            self.match(SequenceDiagramParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelfCallStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(SequenceDiagramParser.ID)
            else:
                return self.getToken(SequenceDiagramParser.ID, i)

        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_selfCallStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelfCallStmt" ):
                listener.enterSelfCallStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelfCallStmt" ):
                listener.exitSelfCallStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelfCallStmt" ):
                return visitor.visitSelfCallStmt(self)
            else:
                return visitor.visitChildren(self)




    def selfCallStmt(self):

        localctx = SequenceDiagramParser.SelfCallStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_selfCallStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(SequenceDiagramParser.T__3)
            self.state = 56
            self.match(SequenceDiagramParser.ID)
            self.state = 57
            self.match(SequenceDiagramParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AltStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ConditionContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceDiagramParser.StatementContext)
            else:
                return self.getTypedRuleContext(SequenceDiagramParser.StatementContext,i)


        def elseBlock(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ElseBlockContext,0)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_altStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAltStmt" ):
                listener.enterAltStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAltStmt" ):
                listener.exitAltStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAltStmt" ):
                return visitor.visitAltStmt(self)
            else:
                return visitor.visitChildren(self)




    def altStmt(self):

        localctx = SequenceDiagramParser.AltStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_altStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(SequenceDiagramParser.T__4)
            self.state = 60
            self.condition()
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 318) != 0):
                self.state = 61
                self.statement()
                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 68
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==7:
                self.state = 67
                self.elseBlock()


            self.state = 70
            self.match(SequenceDiagramParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ConditionContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceDiagramParser.StatementContext)
            else:
                return self.getTypedRuleContext(SequenceDiagramParser.StatementContext,i)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_elseBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElseBlock" ):
                listener.enterElseBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElseBlock" ):
                listener.exitElseBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseBlock" ):
                return visitor.visitElseBlock(self)
            else:
                return visitor.visitChildren(self)




    def elseBlock(self):

        localctx = SequenceDiagramParser.ElseBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_elseBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(SequenceDiagramParser.T__6)
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 73
                self.condition()


            self.state = 79
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 318) != 0):
                self.state = 76
                self.statement()
                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LoopStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condition(self):
            return self.getTypedRuleContext(SequenceDiagramParser.ConditionContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceDiagramParser.StatementContext)
            else:
                return self.getTypedRuleContext(SequenceDiagramParser.StatementContext,i)


        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_loopStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoopStmt" ):
                listener.enterLoopStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoopStmt" ):
                listener.exitLoopStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLoopStmt" ):
                return visitor.visitLoopStmt(self)
            else:
                return visitor.visitChildren(self)




    def loopStmt(self):

        localctx = SequenceDiagramParser.LoopStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_loopStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(SequenceDiagramParser.T__7)
            self.state = 83
            self.condition()
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 318) != 0):
                self.state = 84
                self.statement()
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 90
            self.match(SequenceDiagramParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(SequenceDiagramParser.ID, 0)

        def getRuleIndex(self):
            return SequenceDiagramParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = SequenceDiagramParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(SequenceDiagramParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





