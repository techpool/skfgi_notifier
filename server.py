# Let's get this party started!
import falcon
import scrap
import json
import migrate
import clock
from query import query, querytojson

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class NotificationResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        params = req.params
        limit = 0
        query_result = []

        try:
        	limit = int(params['limit'])
        except (KeyError, ValueError) as e:
        	limit = None
        finally:
        	if limit == 0 or limit == None:
        		query_result = query.get_all_notice()
        	else:
        		query_result = query.get_n_recent_notice(limit)

        json_data = querytojson.json_wrapper(query_result)
        resp.body = (str(json_data))

class ScrapNow(object):
	
	def on_post(self, req, resp):
		json_response = scrap.scrap()
		resp.status = falcon.HTTP_200
		resp.body = json_response

class TableDropper(object):
    """docstring for TableDropper"""
    def on_post(self, req, resp):
        json_response = migrate.drop_table()
        resp.status = falcon.HTTP_200
        resp.body = json_response

class TableCreater(object):
    """docstring for TableCreater"""
    def on_post(self, req, resp):
        json_response = migrate.create_table()
        resp.status = falcon.HTTP_200
        resp.body = json_response

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
notifications = NotificationResource()
scraproute = ScrapNow()
droptable = TableDropper()
createtable = TableCreater()


app.add_route('/notify', notifications)
app.add_route('/scrap', scraproute)
app.add_route('/droptable', droptable)
app.add_route('/createtable', createtable)