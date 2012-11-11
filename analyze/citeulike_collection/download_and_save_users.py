import urllib2
import os
import json

rel_save_directory = "users"
citeulike_path_prepend_me = "http://www.citeulike.org/user/"
service_path_prepend_me = "http://ecology-service.cs.tamu.edu/ecologylabSemanticService/metadata.json?url="

uh_ohs = {'http://portal.acm.org/citation.cfm?id=1135777.1136004':1,
          'http://portal.acm.org/citation.cfm?id=564376.564440z':1}

all_papers = []

def url_to_fname(url):
    url = url.replace("/","_").replace("?","").replace("=","").replace(":","").replace(";","").replace("&","").replace("%","").replace("(","").replace(")","")
    return url

def count_dl_papers():
    print "counting dl papers"
    acm_papers = [x for x in all_papers if "portal.acm" in x or"dl.acm" in x]
    non_acm_papers = [x for x in all_papers if not("portal.acm" in x or"dl.acm" in x)]
    print "All:",len(all_papers),"ACM:",len(acm_papers),"Non ACM",len(non_acm_papers)
    for p in non_acm_papers:
        print p,url_to_fname(p)

def download_all_papers():
    for p in all_papers:
        paper_json_filepath = rel_save_directory+"/"+url_to_fname(p)+".json"
        if not os.path.exists(paper_json_filepath):
#            if p in uh_ohs:
#                print p,"Marked as uh oh.  WIll skip"
#            print "wget -O",paper_json_filepath,service_path_prepend_me+p
            try:
                download_metadata(p,paper_json_filepath)
            except:
                print "Failure to download the metadata"
        else:
            ##print "have file",download_metadata_article,"already"
            try:
                paper_object = json.load(open(paper_json_filepath))
            except:
                print "rm",paper_json_filepath
            #print paper_object
#            print "Trying for the next download..."
#            download_metadata_article(user)
            

def citulike_user_object_to_stats(cite_u):
#    print json.dumps(cite_u,indent=2)
#    print str(len(cite_u['citeulike_user']['collected_papers']['citeulike_paper']))
#    print cite_u['citeulike_user']['name']
    number_collected = 0
    papers = []
    if "collected_papers" in cite_u['citeulike_user']:
#        print "GET TITLE--->",cite_u['citeulike_user']['collected_papers']['citeulike_paper']
#        for paper in cite_u['citeulike_user']['collected_papers']['citeulike_paper']:
#            print "Dat title",paper['title']
        number_collected = len(cite_u['citeulike_user']['collected_papers']['citeulike_paper'])
        papers = cite_u['citeulike_user']['collected_papers']['citeulike_paper']
    return {'name': cite_u['citeulike_user']['name'], 'collected':number_collected, 'papers':papers}

def citulike_article_to_stats(cite_u):
#    print "STERT COLLECTER",cite_u['citeulike_paper']
    if 'additional_locations' in cite_u['citeulike_paper']:
        al = cite_u['citeulike_paper']['additional_locations']['location']
#        print len(al)
        if len(al) > 0:
#            print al
#            print "Right paper???",al[0],al
            all_papers.append(al[0])

def download_metadata(location,path):
    outfile = open(path,"w")
    get_url = service_path_prepend_me+location
    print "starting to download...",get_url
    response = urllib2.urlopen(get_url,timeout=1)
    downloaded_json = response.read()
    print "Here you go!!!",downloaded_json
    outfile.write(downloaded_json)
    outfile.close()


def article_url_to_filename(url):
    return "_".join(url.split("/")[-3:])+".json"

def article_filename_to_url(filename):
    return 'http://www.citeulike.org/user/'+("/".join(filename.split(".")[0].split("_")))

def download_metadata_article(user):
    collection = citulike_user_object_to_stats(json.load(open('users/'+user+'.json')))
#    print "Blah...",collection
    for paper in collection['papers']:
        article_url = paper['location']
        fpath = 'users/'+article_url_to_filename(article_url)
#        print "checking for",fpath
        if not os.path.exists(fpath):
            print "Downloading",article_url
            download_metadata(article_url,fpath)
        else:
#            print "have it!!!",fpath
            article = json.load(open(fpath))
            citulike_article_to_stats(article)

def download_cite_u_like_user_data():
    list_of_users = []
    letters = ['a','b']
    for i in range(1,16):
        for let in letters:
            user = 'anonyuser'+str(i)+let
            list_of_users.append(user)
    print "Making sure information is downloaded for following users: ",list_of_users
    if not os.path.exists(rel_save_directory):
        os.makedirs(rel_save_directory)
    
    for user in list_of_users:
        user_json_filepath = rel_save_directory+"/"+user+".json"
        if not os.path.exists(user_json_filepath):
#            print "downloading for",user,"to",user_json_filepath
            download_metadata(citeulike_path_prepend_me+user,user_json_filepath)
        else:
#            print "have file",download_metadata_article,"already"
#            print "Trying for the next download..."
            download_metadata_article(user)
#        user_object = json.load(open(user_json_filepath))
#        citulike_user_object_to_stats(user_object)
download_cite_u_like_user_data()

#count_dl_papers()
download_all_papers()