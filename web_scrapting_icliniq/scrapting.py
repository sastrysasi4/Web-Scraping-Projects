from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import pandas as pd

# pages definition
def pages(main_link):
    # main website url
    url="https://www.icliniq.com/"
    
    # BeatifulSoup function
    html_text = requests.get(main_link).text
    soup =BeautifulSoup(html_text,'lxml')

    # list of all doctors
    doc_list = soup.find_all("div",class_ = "ic-card-shadow mb-4")

    # arrays
    name=[]
    profile=[]
    pic= []
    degree =[]
    about_doc =[]
    special =[]
    yoe=[]
    language=[]
    qfee=[]
    vfee=[]
    review=[]
    loc=[]

    for lists in doc_list:
        # link of doctor full details
        doc_profile = url+lists.find("a", {'target':"_blank"})["href"]

        # profile page website
        profile_html = requests.get(doc_profile).text
        soup_profile=BeautifulSoup(profile_html,"lxml")

        # scrapting
        doc_name = soup_profile.find("h1",class_="doctor-name").text
        doc_pic = soup_profile.find("img",class_ = "img-thumbnail img-responsive text-center")['src']
        doc_degree = soup_profile.find("p",class_="font-20 m-0").text
        doc_yoe = soup_profile.find("p",class_="font-30 mb-0").text
        doc_lang = soup_profile.find_all("div",class_="col-lg-8 col-md-7 col-sm-8 col-xs-6 xs-text-left p-0") # yoe- year of experience
        lang=[]
        for k in doc_lang:
            lang.append(k.text)

        doc_special = soup_profile.find_all("div",class_="col-lg-12 col-md-12 col-sm-12 col-xs-12 xs-text-left p-0")
        sep=[]
        for i in doc_special:
            a = i.text
            if a != "\n ...\xa0\n\n":
                sep.append(a)
        about=[]
        doc_about = soup_profile.find_all("div", class_="col-xs-12 p-0 mt-2")
        for j in doc_about:
            b = j.text
            about.append(b)

        # fee
        # query and video fee
        doc_q_fee=lang[-2]
        doc_v_fee=lang[-1]

        doc_review = soup_profile.find("div",class_="text-center").find("i").text
        #doc_loc= soup_profile.find("div",class_="loaction mt-1").text


        name.append(doc_name)
        profile.append(doc_profile)
        pic.append(doc_pic)
        degree.append(doc_degree)
        about_doc.append(' '.join(about[1:]))
        special.append(' '.join(sep).replace(" "," "))
        yoe.append(doc_yoe)
        language.append(lang[1])
        qfee.append(doc_q_fee)
        vfee.append(doc_v_fee)
        review.append(doc_review)
        #loc.append(doc_loc)
        
    # DataFrame
    d_f = pd.DataFrame([name,profile,pic,degree,about_doc,special,yoe,language,qfee,vfee,review])

    return d_f

        

# main

df1= pages("https://www.icliniq.com/search/online-doctors-directory?page=1")
df2= pages("https://www.icliniq.com/search/online-doctors-directory?page=3")

df1= df1.transpose()  
df2= df2.transpose()

df1.append(df2)
df1.rename(columns={'0': 'Name','1':"Profile link",'2':"Picture",'3':'Degree','4':'About','5':'Specialization','6':"Years of Experience",'7':'Language','8':'Fee for query','9':'Fee for video query','10':'Review'}, inplace=True)
df1.to_csv("web_scrapting_icliniq.csv")