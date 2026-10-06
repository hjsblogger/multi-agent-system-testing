from collections import defaultdict
SESSIONS=defaultdict(list); TRACES=defaultdict(list)
def get_messages(s): return SESSIONS[s]
def append_message(s,role,content): SESSIONS[s].append({"role":role,"content":content})
def save_trace(s,t): TRACES[s]=t
def get_trace(s): return TRACES.get(s,[])
