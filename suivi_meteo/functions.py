
### 

def url_from_string(date:'string'):
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