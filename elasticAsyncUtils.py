def get_body(exp_id, start_tfs, end_tfs, elastic_index, tag=None, **kwargs) -> dict:
    """returns json request body {'my_body': {}, 'my_index': {}}"""
    index = elastic_index
    my_body = {
        "from": 0,
        "size": 9999,
        "query": {
            "bool": {
                "must": [
                    {"match": {"tag": tag}},
                    {"match": {"exp_id": exp_id}}
                ],
                "filter": [
                    {"range": {"tfs": {"gte": start_tfs, "lte": end_tfs}}}
                ]
            }
        },
        "sort": {
            "tfs": "asc"
        }
    }
    return {
        "my_index": index,
        "my_body": my_body
    }


def get_start_end_tfs(start_tfs: int, end_tfs: int, gap: int, **kwargs):
    cmds = []
    while start_tfs + gap <= end_tfs:
        cmds.append((start_tfs, start_tfs + gap))
        start_tfs += gap
    return cmds


def json_request_body_generator(exp_id, tag, start_tfs, end_tfs, elastic_index, time_frame=5):
    cmds = get_start_end_tfs(start_tfs, end_tfs, time_frame)
    json_requests = [get_body(exp_id=exp_id, start_tfs=start, end_tfs=end, elastic_index=elastic_index, tag=tag) for
                     start, end in cmds]
    return json_requests
