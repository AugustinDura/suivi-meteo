import datetime
import requests
import bs4 as BeautifulSoup
import pandas as pd
### 


def url_from_string(date: str):
    # date must be string in the format "YYYY-MM-DD"
    year = date[0:4] 
    month = date[5:7]
    month = int(month)
    month = str(month-1) # because month index starts at 0
    day = date[8:10] 
    if day[0] == "0" :
        day = day[1:] # in the url single digit days are single digits
    url = "https://www.meteociel.fr/temps-reel/obs_villes.php?code2=63282001&jour2="+ day + "&mois2="+month+"&annee2="+year
    return url 

def url_from_datetime(date: datetime):
    year = str(date.year)
    month = str(date.month - 1)
    day = str(date.day)
    url = "https://www.meteociel.fr/temps-reel/obs_villes.php?code2=63282001&jour2="+ day + "&mois2="+month+"&annee2="+year
    return url 

def soup_from_url(url: str):
    page = requests.get(url)
    tree = str(page.content)
    soup = BeautifulSoup.BeautifulSoup(tree, features="lxml")
    return soup

def dataframe_from_soup(var: BeautifulSoup.BeautifulSoup):
    #result = pd.DataFrame(columns=['Time', 'Temperature', 'Precipitations'])
    list = []
    for row in var.find_all('tr'):    
    # Find all data for each column
        columns = row.find_all('td')
        if(columns != []):
            max_col_index = len(columns)-1 #header row has two merged cells
                                           #so next row has minus one column
            time = columns[0].text.strip()
            temperature = columns[2].text.strip()
            precipitations = columns[max_col_index].text.strip() #.span.contents[0].strip('&0.')
            list.append([time, temperature, precipitations])
            #newdf = pd.DataFrame({'Time':time, 'Temperature':temperature, 'Precipitations':precipitations})
            #result.concat(newdf)
            result = pd.DataFrame(list)  ### Pas idéal
    return result


def dataframe_cleanup(ugly_df: pd.DataFrame, day=pd.Timestamp):
    result = ugly_df.iloc[1:]
    result.rename(columns={0:"time", 1:"temperature", 2:"precipitations"}, inplace=True) # renommer première ligne
    
    result.loc[:,"temperature"]= result.loc[:,"temperature"].str[:-6] # on retire les horribles caracteres de degres
    result.loc[:,"temperature"] = result.loc[:,"temperature"].replace("", "100")
    result.loc[:,"time"]=result.loc[:,"time"].str[:-2] # on retire le caractère h 
    result.loc[:,"precipitations"] = result.loc[:,"precipitations"].replace("aucune", "0 mm")
    result.loc[:,"precipitations"] = result.loc[:,"precipitations"].replace("aucune (sur 3h)", "0 mm")
    result.loc[:,"precipitations"] = result.loc[:,"precipitations"].replace("", "0 mm")
    result.loc[:,"precipitations"] = result.loc[:,"precipitations"].str[:-2]
    #proper types
    result.loc[:,"temperature"]=result.loc[:,"temperature"].astype(float)
    result.loc[:,"precipitations"]=result.loc[:,"precipitations"].astype(float)
    # proper index
    result.loc[:,"time"]=str(day.year) + "-" + str(day.month) + "-" + str(day.day) + "-" +result.loc[:,"time"]
    result.index = pd.to_datetime(result["time"])
    return result