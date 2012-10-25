#longest with anonyuser10b

#metrics we might want to look at:
#fluency on impression / collection
#percentage of PDF views

#time spent on each page
#about visualizing the citation chaining graph and calculating width / depth, we don't have to do it now, but I still would like to recommend graphviz as a tool for easily creating graph visualizations.

###very easy
#total page views
#total number of expands
#total viewing time...

''' '''

import json
print "testing"

#input_file = open("browser-log.txt")
input_file = open("aggregatelog.txt")
#input_file = open("nony10.txt")
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


def expand_or_crumb_to_dend(item):
    item = item['item']
    dend = {}
    source = None
    try:
        source = item['source']['title']
    except:
        return None
    
    if 'parents' in item:
        current_children = None
    if len(item['parents']) == 0:
        print "breaking"
        return {'name':source}
    parents = item['parents']
    print "Dos parents",parents,len(parents)
    if parents > 1:
        parents = parents.reverse()
    for parent in item['parents']:
        if current_children is None:
            current_children = []
            dend['name'] = parent['title']
            dend['children'] = current_children
        else:
            new_children = []
            current_children.append({'name':parent['title'],'children':new_children})
            current_children = new_children
    current_children.append({'name':source})        
    #for child in item['item']['parents']:#maybe need to reverse....
    #    print parent
    return dend

def long_dend_length(dend):
    length = 1
    children = None
    if "children" in dend:
        children = dend['children']
    else:
        return length
    while children is not None:
        length += 1
        if "children" in children[0]:
            children = children[0]['children']
        else:
            break
    return length


total_extension_max = 0

print "TRY OUT MAKING AN OUTPUT FILE....MAN"
outfile = open("output/data/dend_data.js","w")

for user in users_in_order:
    total_events = 0
    sum_of_length = 0
    print "den for user",user
    title_to_dend = {}
    all_dends = []
    u_children = []
    ultimate = {'name':'root','children':u_children}
    for event in by_user[user]['incontext_expand_crumb']:
#        dend = json.dumps(expand_or_crumb_to_dend(event),indent = 4)
        dend = expand_or_crumb_to_dend(event)
        if dend is None:
            continue
        longness = long_dend_length(dend)
        print dend['name'],"->",longness
        if total_extension_max < longness:
            total_extension_max = longness
#goal here is to follow chain of children until not found starting with source... title should always be added if not exists already in root.
        #make sure root doc exists in root
        if not dend['name'] in title_to_dend:
            print "Adding to root:",dend['name']
            start_page_dend = {'name': dend['name'], 'children':[]}
            title_to_dend[dend['name']] = start_page_dend
            u_children.append(start_page_dend)
        print "Attempt to print all children in order:"
        children = None
        parent = None
        if "children" in dend:
            children = dend['children']
            parent = dend['name']
        else:
            continue
        while children is not None:
            if "children" in children[0]:
                #parent, here must be indexed
                #if I already exists, skip adding part
                ##adding part
                if not children[0]['name'] in title_to_dend:
                    parent_dend = title_to_dend[parent]
                    print "pre existing parent",parent_dend
                    print children[0]['name']
                    child_dend = {'name': children[0]['name'], 'children': []}
                    title_to_dend[children[0]['name']] = child_dend
                    parent_dend['children'].append(child_dend)
                parent = children[0]['name']
                children = children[0]['children']
            else:
                break
        
        #print all children
        
        #we now have a guarentee that the root doc will exist... next, iterate over all children, finding the right spot to add self
#        if dend['name'] in title_to_dend:
#            if not 'children' in title_to_dend:
#                title_to_dend['children'] = []
#            if 'children' in dend:
#                print "extending children..."
#                title_to_dend['children'].extend(dend['children'])#need to check each child as well...
#        else:
#            title_to_dend[dend['name']] = dend
#            u_children.append(dend)
#user_dends.push({name: "meh", value: {boop:"beep"}});
    outfile.write("user_dends.push({name: '"+user+"', value: "+json.dumps(ultimate,indent = 4)+"});\n\n\n")
        #always add, but where?
#print by_user
print "longest",total_extension_max