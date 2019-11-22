from json import dumps
from flask import Flask, g, Response, request, send_from_directory
import query
import concept_extractor as cp
from graph import Graph
import pickle


app = Flask(__name__, static_url_path='/static/')

with open('val.pkl', 'rb') as handle:
    val= pickle.load(handle)


@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        #db = get_db()
        lmn,events,ent,verb = cp.get_merged_event(q)
        prob = val.get_recursive_concept(lmn,ent,verb)
        s = query.fixcause(prob)

        '''
        results = db.run("MATCH (n) where n.ROOT IN {words} WITH collect(n) as nodes UNWIND nodes as n  UNWIND nodes as m  WITH * WHERE n.LEVEL < m.LEVEL MATCH path =  (n)-[*..2]->(m) WITH Last(nodes(path)) as last,path MATCH p_fix = shortestPath((last)-[*..2]->(fix:FIX)) RETURN fix,max(length(path)) as length order by length desc", {"words":words})

        data = []
        for record in results:
            data.append(serialize_result(record['fix'],record['length']))
        '''
        return Response(dumps(s), mimetype="application/json")





@app.route("/")
def get_index():
    return app.send_static_file('index.html')

def serialize_result(result, length):
    return {
        'id': result.id,
        'name': result.properties['NAME'],
        'problem': result.properties['PROBLEM']
    }




if __name__ == '__main__':
    app.run(port=8080, debug=True)
