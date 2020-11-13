# Mini language for graph db queries

#Syntax definiton

Script consists of queries distinguished by newline or whitespace
There are 3 queries:
- `connect "database_name" - connect to database with name database_name
- `declare production_head production_body` - add production to grammar with:
    - `production_head` as string 
    - `production_body` as some pattern in terms of regular expression
- `select obj from graph` - get specified objective from graph, where:
    - `obj` - objective, can be written as:
        - `count edges` - count edges from graph
        - `edges` - returns edges from graph like `(v_from, edge, v_to)`
        - `filter ( condition ) edges` - filtering edges from graph by some condition, where `condition` is look like `( vFrom , edge , vTo ) - > predicate` , where `predicate` is logical expression with terms:
            - `is_start vertice` - checking if vertice is in start set
            - `is_final vertice` - checking if vertice is in final set
            - `edge with_label label` checks if edge has specified label
    - `graph` - graph, which can be:
        - `firstGraph intersect secondGraph` - intersection of two graphs
        - `query pattern` - query in terms of regular expression
        - `query grammar` - query in terms of grammar that was defined previosly by defining patterns through `declare`
        - `graph_name graph` - graph with specified name in database
        - `set_start_final vertice vertice graph` - will take a graph with specified start and final set of vertices, where :
            - `set ( num , num )` - set of vertices
            - `range ( num , num ) ` - range of vertices
            - `none` - it means that all start or final set consists of all vertices
            
#Examples

```
    connect database
    declare S ( terminal ( a ) . terminal ( d ) ) * . ( variable ( C ) ? . terminal ( b ) ) +
    declare C terminal ( c )  
    select filter ( ( vFrom , edge , vTo ) - > is_final vTo ) edges from graph_name mygraph
    select edges from graph_name mygraph intersect ( set_start_final set ( 2 , 3 ) range ( 2 ) query grammar )    
```