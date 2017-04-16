import rdflib, json

def myQuery(q, onto_file):
    g = rdflib.Graph()
    g.load(onto_file)

    rows = g.query(q)
    j = rows.serialize(format="json")
    JSON = json.loads(j)

    columns = JSON['head']['vars']
    columnLength = len(columns)

    results = JSON['results']['bindings']
    resultLength  = len(results)

    print 'Result Length:',resultLength
    result=''
    result += '\t\t'.join(columns)+'\n'+'------------------\n'
    for i in range(resultLength):
        for attribute in columns:
            try:
                result+=results[i][attribute]['value'].split('#')[1]+'\t\t'
            except:
                pass
        result+='\n'

    print 'Answer to Query : ',result
    return result


# onto_file = "temp_ontology.owl"
# q = """ PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# #PREFIX : <http://www.semanticweb.org/axat/ontologies/2016/9/skill#>
# PREFIX : <http://www.semanticweb.org/axat/ontologies/2016/9/untitled-ontology-37#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# select * where {
# ?class a owl:Class; rdfs:subClassOf ?superclass .
#
# # FILTER ( ?class in (:android,:java, :spring,:spring-mvc,:hibernate) )
# # FILTER ( ?superclass in (:android,:java, :spring,:spring-mvc,:hibernate) && ?superclass != ?class)
#
# FILTER ( ?class in (:android,:java, :spring,:spring-mvc,:hibernate) )
# FILTER ( ?superclass in (:android,:java, :spring,:spring-mvc,:hibernate) && ?superclass != ?class)
# }"""
#
# js = myQuery(q, onto_file)
