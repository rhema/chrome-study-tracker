###between... done, no change.  ##pairwise comparisons first
#distance of what is collected .  Done
#clean data by hand only.... throw out and justify... test for reasonable ness  DONE
#aov using method and dataset for each metric using R automagically.  DONE

# variety of impressions, and collected documents by url with no get params
# vareity based on keywords....  ?? classifications, but probably not     ... distance as a metric for variety




# is data normalized????.. don't care until significance found, but showing distributions is good in general... maybe coor the points/graphs and juxtapose?
#  

''' '''
#the road they took.   how much time...  measured with R, but lost on means and no difference measured

import json
import csv
import sys
import time,datetime
import re
import numpy

sys.path.append('citeulike_collection')

import download_and_save_users

csv_output_file = "file.csv"
csv_header = []
collection_metrics = ['subject','dataset','method','collected','experiment_order']
metrics = ['total_time','pdf_time','paper_page_time','start_page_time','collecting_time','transitional_page_time','depth_mean','depth_max', 'collected_depth','page_impression']
nov_metrics = ['keyword_variety','collection_novelty']

#longnesses...

csv_header = collection_metrics+metrics+nov_metrics
test_pages = ['http://dl.acm.org/citation.cfm?id=1118704','ICE.html']#two states here....
ends = ['docs.google.com', 'chrome-extension','chrome://chrome/settings/']
posting_partials = [ 'http://www.citeulike.org/posturl','http://www.citeulike.org/post_popup_success','http://www.citeulike.org/post_succes','show_msg=already_posted','http://www.citeulike.org/post_unknown.adp','http://www.citeulike.org/post_error']
transitions_and_indexes = [ 'http://dl.acm.org/author_page.cfm','http://dl.acm.org/ccs.cfm', "http://citeseerx.ist.psu.edu/showciting",'http://dl.acm.org/results.cfm?query','http://pubget.com/search?q=doi' ]
###http://www.citeulike.org/search/all
###http://www.deepdyve.com/lp ? don't know... http://www.deepdyve.com/lp/acm/building-bridges-for-web-query-classification-GMSTxmJSKe?key=citeulike


paper_regexes = [re.compile("http://portal.acm.org/citation.cfm.*"),
                 re.compile("http://dl.acm.org/citation.cfm.*"),
                 re.compile("http://citeseerx.ist.psu.edu/viewdoc/summary.*"),
                 re.compile("http://citeseerx.ist.psu.edu/viewdoc/similar.*"),
                 re.compile("http://citeseerx.ist.psu.edu/viewdoc/versions.*"),
                 re.compile("http://ieeexplore.ieee.org/xpl/articleDetails.jsp.*"),
                 re.compile("http://ieeexplore.ieee.org/stamp/stamp.jsp.*"),
                 re.compile("http://ieeexplore.ieee.org:80/xpl/articleDetails.jsp.*"),
                 re.compile("http://www.citeulike.org/user/.*/article/.*"),
                 re.compile("http://www.sciencedirect.com/science/article.*"),
                 re.compile("http://www.nowpublishers.com/product.aspx?product.*"),
                 re.compile("http://www.nowpublishers.com/product.*"),
                 ]

#input_file = open("browser-log.txt")
#input_file = open("aggregatelog.txt")
input_file = open("aggregatelog_hand_clean.json")
#input_file = open("aggregatelog7a.txt")
#input_file = open("nony10.txt")
input_lines = input_file.readlines()
print "Input has",str(len(input_lines)),"entries"

seenit = {}#make sure unique by hash
users_in_order = []
by_user = {}#each user has three kinds of lists...
log_events = ['page_load_crumb','tab_focus_event', 'page_load_raw','incontext_expand_crumb']
analysis_datas = ['start','end','duration_minutes']
#throw_out_partials = ['http://achilles.cse.tamu.edu/study/webbrowser.mov','docs.google.com','http://achilles.cse.tamu.edu/study/ice.mov','http://achilles.cse.tamu.edu/study/intro.mov','http://achilles.cse.tamu.edu/study/webbrowser.mov','chrome-extension']
paper_title_to_depth = {}


#throw_out_partials = ['anonyuser1a','anonyuser1b','set1.html','set2.html']
start_web = ['user/anonyuser1a','user/anonyuser1b']
start_ice= ['set1.html','set2.html']
start_any = start_web + start_ice

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

places = '''anonyuser2a    ice + pagerank
anonyuser3a    web + pagerank
anonyuser4a    ice + query log
anonyuser5a    web + query log
anonyuser6a    ice + pagerank
anonyuser7a    web + pagerank
anonyuser8a    web + query log
anonyuser9a    ice + pagerank
anonyuser10a    web + pagerank
anonyuser11a    ice + query log
anonyuser12a    web + query log
anonyuser13a    ice + pagerank
anonyuser14a    ice + query log
anonyuser15a    web + pagerank
anonyuser2b    web + query log
anonyuser3b    ice + query log
anonyuser4b    web + pagerank
anonyuser5b    ice + pagerank
anonyuser6b    web + query log
anonyuser7b    ice + query log
anonyuser8b    ice + pagerank
anonyuser9b    web + query log
anonyuser10b    ice + query log
anonyuser11b    web + pagerank
anonyuser12b    ice + pagerank
anonyuser13b    web + query log
anonyuser14b    web + pagerank
anonyuser15b    ice + query log'''

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
print "what is anyuser?",any_user
csvfile = open('file.csv','wb')
csv_out = csv.writer(csvfile)
csv_out.writerow(csv_header)

download_and_save_users.download_cite_u_like_user_data()

def init_metrics_by_user():#add init_metrics_by_user() instead?
    for user in any_user:
        if not user in by_user:
            by_user[user] = {}
        for item in csv_header:
            by_user[user][item]=None

def compute_collection_metrics():
    for user in any_user:
        print "Computing collected for...",user
        stat = download_and_save_users.citulike_user_object_to_stats(json.load(open('citeulike_collection/users/'+user+'.json')))
        out_row = [user[:-1]]#[user]#[user[:-1]]
        for set in ['rank','log','web','ice']:
            if any_user[user][set]:
                out_row.append(set)
        out_row.append(stat['collected'])
        out_row.append(user[len(user)-1])
        #out_row.append()
        keywords = {}
        for paper in stat['papers']:
            if "keywords" in paper:
                print "paper keywords",paper['keywords']
                for keyword in paper['keywords']:
                    keywords[keyword] = 1
        by_user[user]['keyword_variety'] = len(keywords.keys())
        print "out row",out_row
        for i in range(len(collection_metrics)):
            by_user[user][collection_metrics[i]] = out_row[i]
        collected_depths = []
        for paper in stat['papers']:
            print paper['title']#gbgbgbgbgb
            if paper['title'] in paper_title_to_depth:
                print paper_title_to_depth[paper['title']]
                collected_depths += [paper_title_to_depth[paper['title']]]
            else:
                title = "nonenone"
                if ":" in paper['title']:
                    title = paper['title'].split(":")[0]
                if title in paper_title_to_depth:
                    print paper_title_to_depth[title] 
                    collected_depths += [paper_title_to_depth[title]]
                else:
                    print "???"
        if len(collected_depths) > 0:
            by_user[user]['collected_depth'] = numpy.mean( collected_depths )
        else:
            by_user[user]['collected_depth'] = 0
#        print by_user

def save_by_user_metrics(filename):
    print "csv header is",csv_header
    csvfile = open(filename,'wb')
    csv_out = csv.writer(csvfile)
    csv_out.writerow(csv_header)
    for user in users_in_order:##any_user:
        out_row = []
        for col in csv_header:
            if col in by_user[user]:
                out_row += [by_user[user][col]]
            else:
                out_row += [""]
        csv_out.writerow(out_row)
    csvfile.close()


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

#generate_collected_csv()
#print web_users,ice_users,rank_users,log_users
#exit()

user_type_tag = {}

def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(float( timestamp ) * .001)


##The structure is wrong here somehow...
##
##
##

##TBD add cleaning function
def parse_logs():
    running_count = 0
    new_user = False
    start = None
    start_backup = None#10a case
    end = None
    seen_mov = False
    old_user = None
    first_time = None
    last_time = None
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
            #check for old...
            print user,"<- now   -> then",old_user
            if old_user is not None and old_user != user:
                if ((not 'start' in by_user[old_user]) or (not 'end' in by_user[old_user])):
                    if start is None:
                        start = first_time
                        by_user[old_user]['start'] = first_time
                        print "Hard restart for start...",old_user
                    if end is None:
    #                    last...a.a.a.a.aa
                        by_user[old_user]['end'] = last_time
                        print "Hard restart for end",old_user
                    by_user[old_user]['duration_minutes'] = (by_user[old_user]['end'] - by_user[old_user]['start']).seconds/60.0
                    print "Hard restart for duration...",old_user
                        
                else:
                    print "Got it all..."
            event_holder = {}
            for event in log_events:
                event_holder[event] = []
            by_user[user] = event_holder
            users_in_order.append(user)
            new_user = True
            start = None
            end = None
            seen_mov = False
            first_time = timestamp_to_datetime(ob['timestamp'])
        skip = False
        running_count += 1
        
        stamp = timestamp_to_datetime(ob['timestamp'])
        last_time = stamp
        #print stamp
        old_user = user
        if "url" in ob['item']:
            item = ob['item']
            if ob['type'] == 'page_load_raw':#'tab_focus_event':#'page_load_raw':
                url = item['url']
#                print "tab event",url
                partials = None
                if user in ice_users:
                    partials = start_ice
                if user in web_users:
                    partials = start_web
                #find starts
                #start goes away if we see test pages first...
                for partial in test_pages:
                    if partial in url:
                        print "Start is none again because:",url
                        start = None
                        start_backup = start
                for partial in partials:
                    if partial in url:
                        if start is None:
                            start = stamp#how to do end?
                            print stamp,"START",user,url
                            by_user[user]['start'] = start
                if start is not None and end is None:
                    for partial in ends:
                        if partial in url:
                            if start is None:
                                start = start_backup
                            print stamp,"END",user,url
                            end = stamp
                            print "duration is",(end - start).seconds/60.0,"minutes"
                            by_user[user]['start'] = start
                            by_user[user]['end'] = end
                            by_user[user]['duration_minutes'] = (end - start).seconds/60.0
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

def clean_logs_by_duration():
    #print "OK!!!"
    for user in by_user:
        #print user,by_user[user]['duration_minutes']
        print "cleaning by duration for",user
        start = by_user[user]['start']
        end = by_user[user]['end']
#        print "=========== getting rid of ============="
#        print start,end
        for event_type in log_events:
            for event in by_user[user][event_type]:
                by_user[user][event_type] = [x for x in by_user[user][event_type] if timestamp_to_datetime(x['timestamp']) > start and timestamp_to_datetime(x['timestamp']) < end ]
                #by_user[user][event_type] = []
#                event_time = timestamp_to_datetime(event['timestamp'])
#                extra = ""
#                if event['type'] in ['page_load_raw','tab_focus_event']:
#                    extra = event['item']['url']
#                if event_time <= start or event_time >= end:
#                    #print "delete",event
#                    by_user[user][event_type].remove(event)
#                    print event_time,"NIX",user,event_type,extra
#                else:
#                    #print "don't delete",event
#                    blah = 0
#                    print event_time,"KEEP",user,event_type,extra

def print_simple_stats():
    for user in users_in_order:
        print "---stats for user---",user
        for event in log_events:
            print "%4d" % len(by_user[user][event]),event,"events",
        total_tab_time = 0
        for tab_event in by_user[user]['tab_focus_event']:
            seconds = float(tab_event['item']['duration_seconds'])
    #        if seconds > 30:
    #            print tab_event['item']
#            print tab_event['item']['url'],seconds
    #        if "acm" in by_user[user]['item']['url']:
    #            print tab_event
            total_tab_time += seconds
        print "Total tab time:",total_tab_time/60.0,by_user[user]['duration_minutes']

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
        return {'name':source, 'url':item['source']['url']}
    parents = item['parents']
#    print "Dos parents",parents,len(parents)
    if parents > 1:
        parents = parents.reverse()
    for parent in item['parents']:
        if current_children is None:
            current_children = []
            dend['name'] = parent['title']
            dend['url'] = parent['url']
            dend['children'] = current_children
        else:
            new_children = []
            current_children.append({'name':parent['title'],'url':parent['url'],'children':new_children})
            current_children = new_children
    current_children.append({'name':source,'url':item['source']['url']})     
    #for child in item['item']['parents']:#maybe need to reverse....
    #    print parent
    return dend


def long_dend_papers(dend):
    length = 1
    children = None
    if "children" in dend:
        children = dend['children']
    else:
        return length
    while children is not None:
        length += 1
        
        if "children" in children[0] and is_url_paper(children[0]['url']):
            children = children[0]['children']
        else:
            break
    return length

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
        url = event['item']['source']['url']
        if not is_url_paper(url):
            continue
        dend = expand_or_crumb_to_dend(event)
        if dend is None:
            continue
        longness = long_dend_papers(dend)
        if not "depths" in by_user[user]:
            by_user[user]['depths'] = []
        by_user[user]['depths'] += [longness]
        paper_title_to_depth[event['item']['source']['title']] = longness
        if ":" in event['item']['source']['title']:
            paper_title_to_depth[event['item']['source']['title'].split(":")[0]] = longness
        if longness > 15:
            print event
        
        if not dend['name'] in title_to_dend:
            start_page_dend = {'name': dend['name'], 'children':[]}
            title_to_dend[dend['name']] = start_page_dend
            u_children.append(start_page_dend)
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
#                    print "pre existing parent",parent_densd
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
        print by_user
        for event in by_user[user]['tab_focus_event']:
            url = event['item']['url']
            item = event['item']
#            if "pdf" in url.lower():
            print timestamp_to_datetime(event['timestamp']),item['duration_seconds'],url
                #print load_event

#btzt...

def is_pdf(url):
    return ".pdf" in url.lower()

def is_url_paper(url):
    for reg in paper_regexes:
        if reg.match(url) is not None:
#            print reg.pattern,"matches",url
            return True
#        else:
#            print reg.pattern,"not match",url
    return False

def is_start_page(url):
    for partial in start_any:
        if partial in url:
            return True
    return False

def is_collecting(url):
    for partial in posting_partials:
        if partial in url:
            return True
    return False

def is_transition(url):
    for partial in transitions_and_indexes:
        if partial in url:
            return True
    return False

def total_tab_event_time(tab_events):
    total = 0.0
    for event in tab_events:
            total += event['item']['duration_seconds']
    return total/60.0

def compute_tab_stats():#metrics = ['total_time','pdf_time','paper_page_time', 'start_page', 'collecting_time','transitional_page_time']
    for user in users_in_order:
        print "---stats for user---",user
        
        tab_events = by_user[user]['tab_focus_event']
        by_user[user]['total_time'] = total_tab_event_time(tab_events) ##"NOPE"###by_user[user]['duration_minutes']
        
        pdf_tab_events = [x for x in tab_events if is_pdf( x['item']['url']) ]#(".pdf" in x['item']['url']) ]
        by_user[user]['pdf_time'] = total_tab_event_time(pdf_tab_events)

        paper_page_tab_events = [x for x in tab_events if  is_url_paper(x['item']['url']) ]#(".pdf" in x['item']['url']) ]
        by_user[user]['paper_page_time'] =  total_tab_event_time(paper_page_tab_events)
        
        start_page_tab_events = [x for x in tab_events if  is_start_page(x['item']['url']) ]
        by_user[user]['start_page_time'] =  total_tab_event_time(start_page_tab_events)
        
        collecting_tab_events = [x for x in tab_events if  is_collecting(x['item']['url']) ]
        by_user[user]['collecting_time'] =  total_tab_event_time(collecting_tab_events)
        
        transitional_tab_events = [x for x in tab_events if  is_transition(x['item']['url']) ]
        by_user[user]['transitional_page_time'] =  total_tab_event_time(transitional_tab_events)
        
        for event in tab_events:
            inlcuded = False
            for f in [is_pdf,is_url_paper,is_start_page,is_collecting,is_transition]:
                if f(event['item']['url']):
                    inlcuded = True
                    break
            if not inlcuded:
                print event['item']['url']

def add_depth():
    for user in any_user:
        print user,"depths"
        if "depths" in by_user[user]:
            by_user[user]['depth_mean'] = numpy.mean(by_user[user]['depths'])
            by_user[user]['depth_max'] = numpy.max(by_user[user]['depths'])
            by_user[user]['page_impression'] = len(by_user[user]['depths'])
            print numpy.median(by_user[user]['depths']), numpy.mean(by_user[user]['depths']),by_user[user]['depths']


def add_collection_novelty():#based on title
    all_paper_titles = {}#average novelty is 
    for user in any_user:
        print user
        stat = download_and_save_users.citulike_user_object_to_stats(json.load(open('citeulike_collection/users/'+user+'.json')))
        for paper in stat['papers']:
            title = paper['title'],paper
#            if not title in all_paper_titles:
#                all_paper_titles[title] = 1
#            else:
#                all_paper_titles[title] += 1


def add_collection_novelty():#based on title
    all_paper_titles = {}#average novelty is 
    for user in any_user:
        print user
        stat = download_and_save_users.citulike_user_object_to_stats(json.load(open('citeulike_collection/users/'+user+'.json')))
        for paper in stat['papers']:
            title = paper['title']
            if not title in all_paper_titles:
                all_paper_titles[title] = 1
            else:
                all_paper_titles[title] += 1
    for user in any_user:
        print user
        stat = download_and_save_users.citulike_user_object_to_stats(json.load(open('citeulike_collection/users/'+user+'.json')))
        paper_novelties = []
        for paper in stat['papers']:
            title = paper['title']
            paper_novelties += [1.0/ float(all_paper_titles[paper['title']])]
        nov = 0;
        if len(paper_novelties) > 0:
            nov = numpy.mean(paper_novelties)
        by_user[user]['collection_novelty'] = nov
        print nov,paper_novelties
            
#print by_user
#print "longest",total_extension_max

#init_by_user()
#
parse_logs()
#clean_logs_by_duration()
init_metrics_by_user()
save_dend()
compute_collection_metrics()
compute_tab_stats()
add_depth()
add_collection_novelty()
save_by_user_metrics("second.csv")
print paper_title_to_depth
#print_simple_stats()
#generate_collected_csv()


#print "......"
#print "......"
#print "......"
#print "......"
#print_simple_stats()

# GOOD STARTS
#http://www.citeulike.org/user/anonyuser1a/library OR http://www.citeulike.org/user/anonyuser1b/library

##save_dend()
##print_simple_stats()



