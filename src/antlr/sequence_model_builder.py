from antlr.SequenceDiagramVisitor import SequenceDiagramVisitor
from antlr.SequenceDiagramParser import SequenceDiagramParser


class SequenceModelBuilder(SequenceDiagramVisitor):

    def visitSequence(self, ctx: SequenceDiagramParser.SequenceContext):
        model = {
            "participants": {},
            "messages": []
        }

        for statement_ctx in ctx.statement():
            item = self.visit(statement_ctx)

            if item is None:
                continue

            if item["type"] == "participant":
                model["participants"][item["name"]] = item["class_name"]
            else:
                model["messages"].append(item)

        return model

    def visitParticipantDecl(self, ctx: SequenceDiagramParser.ParticipantDeclContext):
        ids = ctx.ID()

        return {
            "type": "participant",
            "name": ids[0].getText(),
            "class_name": ids[1].getText()
        }

    def visitCallStmt(self, ctx: SequenceDiagramParser.CallStmtContext):
        ids = ctx.ID()

        return {
            "type": "call",
            "from": ids[0].getText(),
            "to": ids[1].getText(),
            "method": ids[2].getText()
        }

    def visitReturnStmt(self, ctx: SequenceDiagramParser.ReturnStmtContext):
        ids = ctx.ID()

        return {
            "type": "return",
            "from": ids[0].getText(),
            "to": ids[1].getText(),
            "value": ids[2].getText()
        }

    def visitSelfCallStmt(self, ctx: SequenceDiagramParser.SelfCallStmtContext):
        ids = ctx.ID()

        return {
            "type": "self",
            "object": ids[0].getText(),
            "method": ids[1].getText()
        }

    def visitAltStmt(self, ctx):
        result = {
            "type": "alt",
            "condition": ctx.condition().getText(),
            "then": [],
            "else": []
        }

        for statement_ctx in ctx.statement():
            item = self.visit(statement_ctx)
            if item:
                result["then"].append(item)

        else_ctx = ctx.elseBlock()
        if else_ctx:
            for statement_ctx in else_ctx.statement():
                item = self.visit(statement_ctx)
                if item:
                    result["else"].append(item)

        return result

    def visitLoopStmt(self, ctx):
        result = {
            "type": "loop",
            "condition": ctx.condition().getText(),
            "body": []
        }

        for statement_ctx in ctx.statement():
            item = self.visit(statement_ctx)
            if item:
                result["body"].append(item)

        return result