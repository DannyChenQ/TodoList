#! /usr/bin/python

def application(env,start_response):
    start_response("200 ok",[('Content_Type','text/html')])
    return "uwsgi test ok!"
