from pyzabbix import ZabbixAPI
import requests
import json


                #CONFIGURATION ZBX SERVERS
#####################################################################
#input server                                                       #
server = 'https://zabbix.input.server/api_jsonrpc.php'              #
user = 'Admin'                                                      #
password = 'zabbix'                                                 #
                                                                    #
                                                                    #
                                                                    #
                                                                    #
                                                                    #
#output server                                                      #
server2 = 'http://zabbix.output.server/api_jsonrpc.php'             #
user2 = 'Admin'                                                     #
password2 = 'zabbix'                                                #
#####################################################################
                                                                      





z = ZabbixAPI(server)
z.login(user, password)





z2 = ZabbixAPI(server2)
z2.login(user2, password2)








hgresult = z.hostgroup.get()

hg_db = {}


for elem in range (0, len(hgresult)):

    group_id = hgresult[elem]["groupid"]
    group_name = hgresult[elem]["name"]

    hg_db[group_id] = group_name






    

ugresult = z.usergroup.get(
    selectRights = ["permission", "id"],
    selectUsers = ["userid","alias","name"]
)






for elem in range (0, len(ugresult)):

    for elem2 in range (0, len(ugresult[elem]["rights"])):

        grp_id = ugresult[elem]["rights"][elem2]["id"]

        if grp_id in hg_db:
            hgname = hg_db[grp_id]  

        ugresult[elem]["rights"][elem2]["name"] = hgname 

        try:
            z2.hostgroup.create(name=hgname)
        except Exception:
            pass






hgresult2 = z2.hostgroup.get()

hg_db2 = {}


for elem in range (0, len(hgresult2)):

    group_id = hgresult2[elem]["groupid"]
    group_name = hgresult2[elem]["name"]

    hg_db2[group_name] = group_id








for elem in range (0, len(ugresult)):

    rights_list = []

    grp_name = ugresult[elem]["name"]


    for elem2 in range (0, len(ugresult[elem]["rights"])):

        hgrp_name = ugresult[elem]["rights"][elem2]["name"]
        hgrp_acl = ugresult[elem]["rights"][elem2]["permission"]
        hgrp_id = hg_db2[hgrp_name]  

        rights_list.append({'permission': hgrp_acl,'id': hgrp_id})



    try:
        z2.usergroup.create(
            name=grp_name,
            gui_access=2,
            rights=rights_list
        )
    except Exception:
        pass 



    rights_list.clear()







#copy mediatypes

mediaresult = z.mediatype.get(
)
                    


for elem in range (0, len(mediaresult)):

    del mediaresult[elem]["mediatypeid"] 

    try:
        z2.mediatype.create(mediaresult[elem])
    except Exception:
        pass







mediaresult2 = z2.mediatype.get()


media_db = {}


for elem in range (0, len(mediaresult2)):

    media_id = mediaresult2[elem]["mediatypeid"]
    media_name = mediaresult2[elem]["name"]

    media_db[media_name] = media_id








ugresult2 = z2.usergroup.get()


usergroup_db = {}


for elem in range (0, len(ugresult2)):

    usergroup_id = ugresult2[elem]["usrgrpid"]
    usergroup_name = ugresult2[elem]["name"]

    usergroup_db[usergroup_name] = usergroup_id








userid_list = []


for elem in range (0, len(ugresult)):

    for elem2 in range (0, len(ugresult[elem]["users"])):

        user_id = ugresult[elem]["users"][elem2]["userid"]

        userid_list.append(user_id)









useresult = z.user.get(
    selectMediatypes=["name","type"],
    selectMedias=["sendto","active","severity","period", "mediatypeid"],
    selectUsrgrps=["name"]
)
                    







for elem in range (0, len(useresult)):

    usrgrps_list = []

    medias_list = []


    for elem2 in range (0, len(useresult[elem]["usrgrps"])):
        
        usr_grp_name = useresult[elem]["usrgrps"][elem2]["name"]

        usrgrps_list.append({"usrgrpid": usergroup_db[usr_grp_name]})



    for elem3 in range (0, len(useresult[elem]["medias"])):

        mediatype_oldid = useresult[elem]["medias"][elem3]["mediatypeid"]

        mediatype_db = {}



        for elem4 in range (0, len(useresult[elem]["mediatypes"])):


            if mediatype_oldid == useresult[elem]["mediatypes"][elem4]["mediatypeid"]:

                mtname = useresult[elem]["mediatypes"][elem4]["name"]

                mtid = useresult[elem]["mediatypes"][elem4]["mediatypeid"]

                mediatype_db[mtid] = mtname  




        mnew_id_raw = mediatype_db[mediatype_oldid]
        mnew_id = media_db[mnew_id_raw]
        
        useresult[elem]["medias"][elem3]["mediatypeid"] = mnew_id

        medias_list.append(useresult[elem]["medias"][elem3])

        mediatype_db.clear() 






    user_alias = useresult[elem]["alias"]
    user_name = useresult[elem]["name"]
    user_surname = useresult[elem]["surname"]
    user_url = useresult[elem]["url"]
    user_autologin = useresult[elem]["autologin"]
    user_autologout = useresult[elem]["autologout"]
    user_lang = useresult[elem]["lang"]
    user_refresh = useresult[elem]["refresh"]
    user_type = useresult[elem]["type"]
    user_theme = useresult[elem]["theme"]
    user_rows_per_page = useresult[elem]["rows_per_page"]


    try:

        z2.user.create(

            alias = user_alias,
            name = user_name,
            surname = user_surname,
            url = user_url,
            autologin = user_autologin,
            autologout = user_autologout,
            lang = user_lang,
            refresh = user_refresh,
            type = user_type,
            theme = user_theme,
            rows_per_page = user_rows_per_page,
            usrgrps = usrgrps_list,
            user_medias = medias_list

        )

    except Exception:
        pass




    usrgrps_list.clear()

    medias_list.clear()
