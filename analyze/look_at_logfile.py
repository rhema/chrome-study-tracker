#metrics we might want to look at:
#fluency on impression / collection
#percentage of PDF views

#time spent on each page
#about visualizing the citation chaining graph and calculating width / depth, we don't have to do it now, but I still would like to recommend graphviz as a tool for easily creating graph visualizations.

###very easy
#total page views
#total number of expands
#total viewing time...

import json
print "testing"

#input_file = open("browser-log.txt")
input_file = open("aggregatelog.txt")
input_lines = input_file.readlines()
print "Input has",str(len(input_lines)),"entries"

seenit = {}#make sure unique by hash
users_in_order = []
by_user = {}#each user has three kinds of lists...
types_of_events = ['page_load_crumb','tab_focus_event', 'page_load_raw','incontext_expand_crumb']
throw_out_partials = ['http://achilles.cse.tamu.edu/study/webbrowser.mov','docs.google.com','http://achilles.cse.tamu.edu/study/ice.mov','http://achilles.cse.tamu.edu/study/intro.mov','http://achilles.cse.tamu.edu/study/webbrowser.mov','chrome-extension']

##TBD add cleaning function

for line in input_lines:
    line = line.strip()
    #print line
    line = unicode(line, 'Windows-1252')#via http://stackoverflow.com/questions/7873556/utf8-codec-cant-decode-byte-0x96-in-python
    ob = None
    try:
        ob = json.loads(line)
    except:
        print line
        print "Above failed to parse..."
        continue
    user = ob['uid']
    hash = ob['hash']
    if hash in seenit:
        continue
    seenit[hash] = 1
    if not user in by_user:
        event_holder = {}
        for event in types_of_events:
            event_holder[event] = []
        by_user[user] = event_holder
        users_in_order.append(user)
    skip = False
    if "url" in ob['item']:
        for partial in throw_out_partials:
            if partial in ob['item']['url']:
                skip = True
    if skip:
        continue
    by_user[user][ob['type']].append(ob)



for user in users_in_order:
    print "---stats for user---",user
    for event in types_of_events:
        print str(len(by_user[user][event])),event,"events"
    total_tab_time = 0
    for tab_event in by_user[user]['tab_focus_event']:
        seconds = float(tab_event['item']['duration_seconds'])
#        if seconds > 30:
#            print tab_event['item']
#        print tab_event['item']['url']
#        if "acm" in by_user[user]['item']['url']:
#            print tab_event
        total_tab_time += seconds
    print "Total tab time:",total_tab_time/60.0
#print by_user