import flask
import elasticsearch
import flask_cors
import json
import redis
import pysolr
import pprint

app=flask.Flask(__name__)
app.config["DEBUG"]=True
app.config["TOKEN"]="bharathkarkera"
app.secret_key = 'bharathkarkera'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = flask_cors.CORS(app, resources={r"/search": {"origins": "http://localhost:5000"}})

redis=redis.Redis(host='localhost',port=6379)

car_collection_connection=pysolr.Solr("http://localhost:8983/solr/car_details_collection")


MAX_SIZE=15

@app.route('/')
def index_path():
   redis.incr("hits")
   flask.flash(str(int(redis.get("hits")))+"th hit to the site")
   return flask.render_template("index.html")

@app.route('/display',methods=["GET"])
def display_function():
   redis.incr("hits")
   return f'Hi This is a test webserver and this is your {int(redis.get("hits"))}th visit to the website'


@app.route('/search',methods=["GET","POST"])
@flask_cors.cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def search_fun():
    query=flask.request.args["q"].lower()
    print(query)
    words=query.split(" ")
    print(words)
    #https://www.cleancss.com/python-beautify/

    q=f"name:*{query}*"
    rows=10
    filtered_results=car_collection_connection.search(q,**{'rows':rows})

    car_list=[]
    for i in filtered_results.docs:
        print(str(i['name'][0]))
        car_list.append(str(i['name'][0]))

    print(json.dumps(car_list))

    #return { "cars": search_results }


    return json.dumps(car_list)


app.run(host="0.0.0.0")
#solr create -c car_details_collection -p 8983
#curl -i 'http://localhost:8983/solr/car_details_collection/update?commit=true' --data-binary @/Users/bharathkarkera/practice/solr_search/car_details.csv -H 'Content-type:application/csv'
