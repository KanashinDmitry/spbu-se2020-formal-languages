import os
import pytest
from antlr4 import InputStream
from src.antlr_parse import TreeAST


correct_scripts = [
    '''
    connect "database";
    select edges from graph_name "mygraph";
    ''', \
    '''
    connect "database";
    select edges from graph_name "my_graph1" intersect ( graph_name "mygrapha" intersect query grammar );
    ''', \
    '''
    connect "database";
    select edges from graph_name "mygraph" intersect ( set_start_final none none query grammar );
    ''', \
    '''
    connect "database";
    select edges from graph_name "mygraph" intersect ( set_start_final range ( 1 , 3 ) none query grammar );
    ''', \
    '''
    connect "database";
    select edges from graph_name "mygraph" intersect ( query grammar );
    ''', \
    '''
    connect "database";
    select filter ( ( vFrom , edge , vTo ) - > is_start vFrom ) edges from graph_name "mygraph";
    ''', \
    '''
    connect "database";
    select filter ( ( vFrom , edge , vTo ) - > edge with_label "myLabel" ) edges from graph_name "mygraph";
    ''', \
    '''
    connect "database";
    declare "S" ( terminal ( "a" ) . terminal ( "d" ) ) * . ( variable ( "C" ) ? . terminal ( "b" ) ) + ;
    declare "C" terminal ( "C" );  
    select filter ( ( vFrom , edge , vTo ) - > is_final vTo ) edges from graph_name "mygraph";
    ''', \
    '''
    connect "database";
    select filter ( ( vFrom , edge , vTo ) - > edge with_label "myLabel" and is_final vTo or is_start vFrom ) edges from graph_name "mygraph";
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 1 , 3 , 4 ) set ( 5 ) query grammar );
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 1 , 3 , 4 ) set ( 5 ) query grammar );
    ''', \
    '''
    select edges from ( query variable ( "S" ) + | terminal ( "d" ) * ) intersect ( set_start_final set ( 1 , 3 , 4 ) set ( 5 ) query grammar );
    ''', \
    '''
    select count edges from graph_name "mygraph";
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 2 , 3 ) range ( 2 ) query grammar );
    '''
]

incorrect_scripts = [
    '''
    select count count edges from graph_name "mygraph";
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( str , str ) set ( 5 ) query grammar );
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 2 , 3 ) set ( str ) query grammar );
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 2 , 3 ) range ( str , str ) query grammar );
    ''', \
    '''
    select edges from graph_name "mygraph" intersect ( set_start_final set ( 2 , 3 ) range ( ) query grammar );
    ''', \
    '''
    select edges graph_name "mygraph";
    ''', \
    '''
    select edges from query ( terminal ( "a" );
    ''', \
    '''
    select edges from query terminal ( "a" ) terminal "b";
    ''', \
    '''
    connect "database"
    '''
]


@pytest.fixture(scope='function', params=[(script, 'correct') if script in correct_scripts else (script, 'incorrect') \
                                          for script in correct_scripts + incorrect_scripts])
def init(request):
    script, name = request.param

    return {
        'script': script,
        'correctness': name
    }


def test_syntax_antlr(init):
    script, name = init['script'], init['correctness']
    tree_wrapper = TreeAST(InputStream(script))
    ast = tree_wrapper.tree
    
    if name == 'correct':
        assert ast is not None
    else:
        assert ast is None