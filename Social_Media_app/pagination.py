from rest_framework.pagination import LimitOffsetPagination

class CustomPagination(LimitOffsetPagination):
    default_limit=6
    limit_query_param='myparam' #specifies the number of resources that a single response page contains
    offset_query_param='myoffset'#Skip the previous data
    max_limit=5

    
#PNP = set pagenumber/limit item
#LOP = default limit/offset/ max limit/myparams
#CP = previous/next/ordering