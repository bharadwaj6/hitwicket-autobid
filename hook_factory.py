def hook_factory(*factory_args, **factory_kwargs):
    def print_response(response, *request_args, **request_kwargs):
        if r.status_code == 200:
            print "success for player: ", url
        else:
            print "failed for player: ", url
            print r.content
