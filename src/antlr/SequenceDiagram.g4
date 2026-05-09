grammar SequenceDiagram;

sequence
    : statement* EOF
    ;

statement
    : participantDecl
    | messageStmt
    | altStmt
    | loopStmt
    ;

messageStmt
    : callStmt
    | returnStmt
    | selfCallStmt
    ;

participantDecl
    : 'participant' ID ID
    ;

callStmt
    : 'call' ID ID ID
    ;

returnStmt
    : 'return' ID ID ID
    ;

selfCallStmt
    : 'self' ID ID
    ;

altStmt
    : 'alt' condition statement* elseBlock? 'end'
    ;

elseBlock
    : 'else' condition? statement*
    ;

loopStmt
    : 'loop' condition statement* 'end'
    ;

condition
    : ID
    ;

ID
    : [a-zA-Z_][a-zA-Z0-9_]*
    ;

WS
    : [ \t\r\n]+ -> skip
    ;