import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
        
class SPCharacterExtractor:
    def __init__(self):
        pass
    
    def createFolder(self, sourcename):
        if not os.path.exists(sourcename):
            os.makedirs(sourcename)
    
    def extractFromSource1(self):
        sourcename = "source_1"
        self.createFolder(sourcename)
        url = "https://www.southparkstudios.com/w/index.php?title=List_of_Characters&oldid=14897"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            profile_div = soup.find_all("div" , class_="character")

            href_links = []

            for div in profile_div:
                soup = BeautifulSoup(str(div), "html.parser")
                profile_a = soup.find_all("img")
                
                href = profile_a[0].get("src")
                href = href.split('?')[0]
                href_links.append(href)

            cpt = 0;
            for href in href_links:
                cpt+=1
                #print(href)
                response = requests.get(href)
                if response.status_code == 200:
                    filename = sourcename+"/"+href.split("/")[-1]
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Image téléchargée : {filename}")
                else:
                    print(f"Échec du téléchargement de l'image : {href}")

        else:
            print(response.status_code)

    def extractFromSource2(self):
        sourcename = "source_2"
        self.createFolder(sourcename)
        api_url = "https://api.personality-database.com/api/v1/profiles?offset=50&limit=500&cid=7&pid=2&sub_cat_id=153&cat_id=7&property_id=2"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            for profile in data.get("profiles", []):
                try:
                    image_url = profile.get("profile_image_url")
                    mbti_profile = profile.get("mbti_profile")
                    filename = f"{mbti_profile}.png".replace('"', '').replace('/','')
                    filename = sourcename+"/"+filename
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        print(f"Image téléchargée : {filename}")
                    else:
                        print(f"Échec du téléchargement de l'image : {image_url}")
                except Exception:
                    pass

        else:
            print(response.status_code)

    def extractFromSource3(self):
        sourcename = "source_3"
        self.createFolder(sourcename)
        url = "https://dubdb.fandom.com/wiki/South_Park"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            profile_links = soup.find_all("a")
            href_links = []
            for link in profile_links:
                href = link.get("href")
                if 'https://static.wikia.nocookie.net/international-entertainment-project' in str(href) and str(href) != 'https://static.wikia.nocookie.net/international-entertainment-project/images/f/f1/South_Park_-_logo_%28English%29.png/revision/latest?cb=20200701234428':
                    href_links.append(href)
            cpt = 0;
            for href in href_links:
                cpt+=1
                print(href)
                response = requests.get(href)
                if response.status_code == 200:
                    filename = sourcename+"/"+str(cpt)+'.jpg'
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Image téléchargée : {filename}")
                else:
                    print(f"Échec du téléchargement de l'image : {href}")
        else:
            print(response.status_code)


    def runExtract(self):
        self.extractFromSource1()
        self.extractFromSource2()
        self.extractFromSource3()
        
        
SP = SPCharacterExtractor()
SP.runExtract()