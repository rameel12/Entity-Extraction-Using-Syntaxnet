from json import dumps
from flask import Flask, g, Response, request, send_from_directory
import query
import entity_extractor as cp
from graph import Graph
import pickle


def main():

    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        #db = get_db()
        ent = cp.NER(q)
        '''
        results = db.run("MATCH (n) where n.ROOT IN {words} WITH collect(n) as nodes UNWIND nodes as n  UNWIND nodes as m  WITH * WHERE n.LEVEL < m.LEVEL MATCH path =  (n)-[*..2]->(m) WITH Last(nodes(path)) as last,path MATCH p_fix = shortestPath((last)-[*..2]->(fix:FIX)) RETURN fix,max(length(path)) as length order by length desc", {"words":words})

        data = []
        for record in results:
            data.append(serialize_result(record['fix'],record['length']))
        '''
        return ent


if __name__ == '__main__':
    main()
