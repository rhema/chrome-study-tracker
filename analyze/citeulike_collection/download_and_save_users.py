import urllib2
import os
import json

rel_save_directory = "users"
citeulike_path_prepend_me = "http://www.citeulike.org/user/"
service_path_prepend_me = "http://ecology-service/ecologylabSemanticService/metadata.json?url="

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

def download_citeulike(user,path):
    outfile = open(path,"w")
    get_url = service_path_prepend_me+citeulike_path_prepend_me+user
    print "starting to download...",get_url
    response = urllib2.urlopen(get_url)
    downloaded_json = response.read()
    print "Here you go!!!",downloaded_json
    outfile.write(downloaded_json)
    outfile.close()

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
            download_citeulike(user,user_json_filepath)
        else:
            print "have file",user_json_filepath,"already"
            print "Trying for the next download..."
#        user_object = json.load(open(user_json_filepath))
#        citulike_user_object_to_stats(user_object)
download_cite_u_like_user_data()