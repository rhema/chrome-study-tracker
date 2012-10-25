import urllib2
import os

rel_save_directory = "users"
list_of_users = []
letters = ['a','b']
citeulike_path_prepend_me = "http://www.citeulike.org/user/"
service_path_prepend_me = "http://ecology-service/ecologylabSemanticService/metadata.json?url="


for i in range(1,11):
    for let in letters:
        user = 'anonyuser'+str(i)+let
        list_of_users.append(user)

if not os.path.exists(rel_save_directory):
    os.makedirs(rel_save_directory)

def download_citeulike(user,path):
#    outfile = open(path,"w")
    get_url = service_path_prepend_me+citeulike_path_prepend_me+user
    print "starting to download...",get_url
    response = urllib2.urlopen(get_url)
    downloaded_json = response.read()
    print "Here you go!!!",downloaded_json
    

print "Making sure information is downloaded for following users: ",list_of_users
for user in list_of_users:
    user_json_filepath = rel_save_directory+"/"+user+".json"
    if not os.path.exists(user_json_filepath):
        print "downloading for",user,"to",user_json_filepath
        download_citeulike(user,user_json_filepath)