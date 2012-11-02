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

#if you expanded it, they looked at it
#

''' '''

#the road they took.   how much time...
#what you have to do to figure out depth
#the path they could take VS the path they did take
#measuring the citation chaining...s

import json
import csv
import sys
import time,datetime
sys.path.append('citeulike_collection')

import download_and_save_users

csv_output_file = "file.csv"
csv_header = ['user','dataset','method','collected']

#input_file = open("browser-log.txt")
input_file = open("aggregatelog.txt")
#input_file = open("nony10.txt")
input_lines = input_file.readlines()
print "Input has",str(len(input_lines)),"entries"

seenit = {}#make sure unique by hash
users_in_order = []
by_user = {}#each user has three kinds of lists...
types_of_events = ['page_load_crumb','tab_focus_event', 'page_load_raw','incontext_expand_crumb']
#throw_out_partials = ['http://achilles.cse.tamu.edu/study/webbrowser.mov','docs.google.com','http://achilles.cse.tamu.edu/study/ice.mov','http://achilles.cse.tamu.edu/study/intro.mov','http://achilles.cse.tamu.edu/study/webbrowser.mov','chrome-extension']



#throw_out_partials = ['anonyuser1a','anonyuser1b','set1.html','set2.html']
start_web = ['user/anonyuser1a','user/anonyuser1b']
start_ice= ['set1.html','set2.html']
test_pages = ['http://dl.acm.org/citation.cfm?id=1118704','ICE.html']#two states here....
ends = ['docs.google.com', 'chrome-extension']

#set1  anonyuser1a

#below pasted from google doc.
places = '''anonyuser2a    ice + pagerank
anonyuser3a    web + pagerank
anonyuser4a    ice + query log
anonyuser5a    web + query log
anonyuser6a    ice + pagerank
anonyuser7a    web + pagerank
anonyuser8a    web + query log
anonyuser9a    ice + pagerank
anonyuser10a    web + pagerank
anonyuser1b    ice + pagerank
anonyuser2b    web + query log
anonyuser3b    ice + query log
anonyuser4b    web + pagerank
anonyuser5b    ice + pagerank
anonyuser6b    web + query log
anonyuser7b    ice + query log
anonyuser8b    ice + pagerank
anonyuser9b    web + query log
anonyuser10b    ice + query log'''

##throw out 9... bleh
#places = '''anonyuser2a    ice + pagerank
#anonyuser3a    web + pagerank
#anonyuser4a    ice + query log
#anonyuser5a    web + query log
#anonyuser6a    ice + pagerank
#anonyuser7a    web + pagerank
#anonyuser8a    web + query log
#anonyuser10a    web + pagerank
#anonyuser1b    ice + pagerank
#anonyuser2b    web + query log
#anonyuser3b    ice + query log
#anonyuser4b    web + pagerank
#anonyuser5b    ice + pagerank
#anonyuser6b    web + query log
#anonyuser7b    ice + query log
#anonyuser8b    ice + pagerank
#anonyuser10b    ice + query log'''

any_user = {}
web_users = []
ice_users = []
rank_users = []
log_users = []

#########
for line in places.split('\n'):
    left,data_set = line.split('+')
    user,method = left.split()
    user = user.strip()
    method = method.strip()
    data_set = data_set.strip()
    if not user in any_user:
        any_user[user] = {'web': False, 'ice':False, 'log':False,'rank':False}
    if method == "web":
        web_users.append(user)
        any_user[user]['web'] = True
    if method == "ice":
        ice_users.append(user)
        any_user[user]['ice'] = True
    if data_set == "pagerank":
        rank_users.append(user)
        any_user[user]['rank'] = True
    if data_set == "query log":
        log_users.append(user)
        any_user[user]['log'] = True
#    print user,method,data_set


print "blah"
csvfile = open('file.csv','wb')
csv_out = csv.writer(csvfile)
csv_out.writerow(csv_header)

download_and_save_users.download_cite_u_like_user_data()

#['user','dataset','method','collected']
def generate_collected_csv():
    for user in any_user:
#        print "w user",user
        stat = download_and_save_users.citulike_user_object_to_stats(json.load(open('citeulike_collection/users/'+user+'.json')))
#        print stat
        out_row = [user[:-1]]
        for set in ['rank','log','web','ice']:
            if any_user[user][set]:
                out_row.append(set)
        out_row.append(stat['collected'])
        csv_out.writerow(out_row)

generate_collected_csv()
print web_users,ice_users,rank_users,log_users
#exit()

user_type_tag = {}

##TBD add cleaning function
def parse_logs():
    running_count = 0
    new_user = False
    start = None
    end = None
    for line in input_lines:
        line = line.strip()
        #print line
        line = unicode(line, 'Windows-1252')#via http://stackoverflow.com/questions/7873556/utf8-codec-cant-decode-byte-0x96-in-python
        ob = None
        try:
            ob = json.loads(line)
        except:
#            print line
#            print "Above failed to parse..."
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
            new_user = True
            start = None
            end = None
        skip = False
        running_count += 1
        
        stamp = datetime.datetime.fromtimestamp(float( ob['timestamp'] ) * .001)
        #print stamp
        if "url" in ob['item']:
            item = ob['item']
            if ob['type'] == 'page_load_raw':
                url = item['url']
                partials = None
                if user in ice_users:
                    partials = start_ice
                if user in web_users:
                    partials = start_web
                #find starts
                for partial in partials:
                    if partial in url:
                        if start is None:
                            start = stamp#how to do end?
                            print stamp,"START",user,url
                if start is not None and end is None:
                    for partial in ends:
                        if partial in url:
                            print stamp,"END",user,url
                            end = stamp
                            print "duration is",(end - start).seconds/60.0,"minutes"
                            if (end - start).seconds < 120:
                                print ""#end = None
                        
                            
#        if "url" in ob['item']:
#            for partial in throw_out_partials:
#                if partial in ob['item']['url']:
#                    skip = True                    
#                    #print "Skipping between ------>      ",user,partial,running_count
#                    if running_count > 0:
#                        print "Found!!!! between ------>      ",user,partial,any_user[user]['web'],running_count, "                   ... "+ob['item']['url']
#                    running_count = 0
#        if skip:
#            continue
        by_user[user][ob['type']].append(ob)

def print_simple_stats():
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
#        print "breaking"
        return {'name':source}
    parents = item['parents']
#    print "Dos parents",parents,len(parents)
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

###print "TRY OUT MAKING AN OUTPUT FILE....MAN"
outfile = open("output/data/dend_data.js","w")


#for user in users_in_order:#start function here?
def get_dend(user,event_type):
    total_events = 0
    sum_of_length = 0
#    print "den for user",user
    title_to_dend = {}
    all_dends = []
    u_children = []
    ultimate = {'name':'root','children':u_children}
    for event in by_user[user][event_type]:
#        dend = json.dumps(expand_or_crumb_to_dend(event),indent = 4)
        dend = expand_or_crumb_to_dend(event)
        if dend is None:
            continue
        longness = long_dend_length(dend)
#        print dend['name'],"->",longness
#        if total_extension_max < longness:
#            total_extension_max = longness
#goal here is to follow chain of children until not found starting with source... title should always be added if not exists already in root.
        #make sure root doc exists in root
        if not dend['name'] in title_to_dend:
#            print "Adding to root:",dend['name']
            start_page_dend = {'name': dend['name'], 'children':[]}
            title_to_dend[dend['name']] = start_page_dend
            u_children.append(start_page_dend)
#        print "Attempt to print all children in order:"
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
#                    print "pre existing parent",parent_dend
#                    print children[0]['name']
                    child_dend = {'name': children[0]['name'], 'children': []}
                    title_to_dend[children[0]['name']] = child_dend
                    parent_dend['children'].append(child_dend)
                parent = children[0]['name']
                children = children[0]['children']
            else:
                break
    return ultimate

def save_dend():
    for user in users_in_order:#start function here?
        dend = get_dend(user, 'incontext_expand_crumb')
        if len(dend['children']) > 0:
            outfile.write("user_dends.push({name: '"+user+"-ICE', value: "+json.dumps(dend,indent = 4)+"});\n\n\n")
    for user in users_in_order:#start function here?
        dend = get_dend(user, 'page_load_crumb')
        if len(dend['children']) > 0:
            outfile.write("user_dends.push({name: '"+user+"-WEB', value: "+json.dumps(dend,indent = 4)+"});\n\n\n")
            #always add, but where?
#print by_user
#print "longest",total_extension_max


parse_logs()

# GOOD STARTS
#http://www.citeulike.org/user/anonyuser1a/library OR http://www.citeulike.org/user/anonyuser1b/library

##save_dend()
##print_simple_stats()


#http://www.citeulike.org/user/anonyuser7b/article/3376379  this changes multiple times I think its a forwarding link
###   posturl2 posts things
def print_loads(users):
    for user in users:
        print "---stats for user---",user
        for load_event in by_user[user]['page_load_raw']:
            url = load_event['item']['url']
            if not "dl.acm.org" in url and "posturl2" not in url and "post_popup_success.adp" not in url and not "citeseerx.ist.psu.edu" in url and "http://www.citeulike.org/user/anonyuser1a" not in url and not "http://www.citeulike.org/user/anonyuser1b" in url and not "http://achilles/study/" in url:
                print url
            #seconds = float(tab_event['item']['duration_seconds'])
#print_loads(["anonyuser2b"])
def print_pdf_loads(users):
    for user in users:
        print "---stats for user---",user
        for load_event in by_user[user]['page_load_raw']:
            url = load_event['item']['url']
            if "pdf" in url.lower():
                print url
                
def print_user_tab_events(users):
    for user in users:
        print "---stats for user---",user
        for event in by_user[user]['tab_focus_event']:
            url = event['item']['url']
            item = event['item']
            if "pdf" in url.lower():
                print item['duration_seconds'],url
                #print load_event

def get_study_endpoints():
    print "testing for input"

#print_loads(users_in_order)
#print_user_tab_events(users_in_order)