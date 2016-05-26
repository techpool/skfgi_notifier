import json
import query

def json_wrapper(query_obj):
	data = []
	for query_tuble in query_obj:
		json_obj = {
			"heading": str(query_tuble[0]),
			"sub_heading": str(query_tuble[1]),
			"url": str(query_tuble[2]),
			"update_time": str(query_tuble[3])
		}
		data.append(json_obj)
	data = json.dumps(data)

	return data