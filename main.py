from elasticAsyncUtils import json_request_body_generator
from elasticAsync import search

def test_json_request_body_generator():
    exp_id = "63ea9306a1793526182c2448"
    tag = "voice"
    start_tfs = 5
    end_tfs = 10
    elastic_index = "soos-2"
    time_frame=5
    json_bodies = json_request_body_generator(exp_id, tag, start_tfs, end_tfs, elastic_index)
    return json_bodies

def test_search():
    json_bodies = test_json_request_body_generator()
    freq = '793'
    results = search(json_bodies, freq)
    return results
    

if __name__ == '__main__':
    print(test_search())
    
    

