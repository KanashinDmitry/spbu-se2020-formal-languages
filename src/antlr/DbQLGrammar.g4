grammar DbQLGrammar;

script : (stmt SEMICOLON)* EOF;

stmt : CONNECT STRING
     | DEC STRING pattern
     | SELECT objective FROM graph
     ;

graph : graph INTERSECT r_intersect_graph
      | r_intersect_graph
      ;

r_intersect_graph : LBR graph RBR
                  | QUERY query_type
                  | G_NAME STRING
                  | SET_START_FINAL vertices vertices graph
                  ;

query_type : pattern
           | GRAMMAR
           ;

vertices : SET_T LBR set_e RBR
         | RANGE LBR INT COMMA INT RBR 
         | RANGE LBR INT RBR
         | NONE
         ;

set_e : INT COMMA set_e
      | INT
      | EPS
      ;

objective : edges
          | COUNT edges
          ;

edges : FILTER LBR condition RBR edges
      | EDGES_T
      ;

condition : LBR v_ident COMMA e_ident COMMA v_ident RBR sat bool_expr ;

sat : OP_MINUS OP_GT ;

v_ident : VAR_STRING ;

e_ident : VAR_STRING ;

bool_expr : bool_expr OP_OR l_or_bool_expr
          | l_or_bool_expr
          | LBR bool_expr RBR 
          ;

l_or_bool_expr : l_or_bool_expr OP_AND l_and_bool_expr  
               | l_and_bool_expr
               ;

l_and_bool_expr : OP_NOT l_and_bool_expr 
                | bool_simple
                ;

bool_simple : e_ident WITH_LABEL STRING
            | IS_START e_ident
            | IS_FINAL e_ident
            ;

pattern : pattern OP_ALT conc_pattern
        | conc_pattern
        ;

conc_pattern : conc_pattern OP_CONCAT times_pattern
             | times_pattern
             ;

times_pattern : times_pattern OP_STAR
              | times_pattern OP_PLUS
              | times_pattern OP_OPTIONAL
              | nested_pattern
              | EPS
              ;

nested_pattern : LBR pattern RBR
               | simple_value
               ;

simple_value : TERM LBR STRING RBR
             | VARIABLE LBR STRING RBR
             ;

EPS : 'epsilon' ;
CONNECT : 'connect' ;
DEC : 'declare' ;
SELECT : 'select' ;
FROM : 'from' ;
INTERSECT : 'intersect' ;
QUERY : 'query' ;
GRAMMAR : 'grammar' ;
G_NAME : 'graph_name' ;
SET_START_FINAL : 'set_start_final' ;
EDGES_T : 'edges' ;
COUNT : 'count' ;
SET_T : 'set' ;
COMMA : ',' ;
SEMICOLON : ';' ;
RANGE : 'range' ;
NONE : 'none' ;
FILTER : 'filter' ;
LBR : '(' ;
RBR : ')' ;
WITH_LABEL : 'with_label' ;
IS_START : 'is_start' ;
IS_FINAL : 'is_final' ;
OP_NOT : 'not' ;
OP_OR : 'or' ;
OP_AND : 'and' ;
OP_GT : '>' ;
OP_MINUS : '-' ;
OP_PLUS : '+' ;
OP_STAR : '*' ;
OP_OPTIONAL : '?' ;
OP_ALT : '|' ;
OP_CONCAT : '.' ;
TERM : 'terminal' ;
VARIABLE : 'variable' ;

INT : [1-9][0-9]* 
    | '0'
    ;

STRING : '"' [a-zA-Z] ([a-zA-Z]|[0-9]|('.'|'_'|'/'))* '"';
VAR_STRING : [a-zA-Z] ([a-zA-Z]|[0-9]|('_'))* ;

WS : [ \r\n\t]+ -> skip ;