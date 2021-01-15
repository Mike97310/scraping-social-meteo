# scraping_social_meteo
projet scraping meteo et réseaux sociaux par Mickaël Rebeau, Franck Madola Benae et Hugo Algaba

Le repository contien 7 fichiers:
* reddit.py
* twitter2.py
* weather.py
* reddit_AustinFC.csv
* twitter_AustinFC.csv
* weather_AustinFC.csv
* scraping.ipynb
* twitter.py

Les fichiers python reddit.py et twitter2.csv peuvent être lancés séparément en premier lieu.
Ils permettent de générer les fichiers csv reddit et twitter (noms d'enregistrement à changer si scraping sur une nouvelle source)
## reddit.py
Le programme est réalisé à l'aide de l'API praw
* Pour un scraping sur une nouvelle source: 
 * modifier 'AustinFC' dans la ligne "for post in reddit.subreddit('AustinFC').hot(limit=1000):"
 * modifier reddit_AustinFC.csv' dans la ligne "posts.to_csv('reddit_AustinFC.csv')" pour ne pas écraser le fichier existant

## twitter2.py
Le programme est réalisé à l'aide de l'API twint
* Pour un scraping sur une nouvelle sourcec:
 * modifier 'AustinFC' dans la ligne "Username = "AustinFC"  # filter by username"
 * modifier 'twitter_AustinFC.csv' dans la ligne "c.Output = "twitter_AustinFC.csv"  # name of the desired output"
 * relancer le programme plusieurs fois en changeant les dates pour avoir un fichier csv complet (ne rajoute que les nouvelles lignes à chaque fois)

Une fois les scraping effectués sur au moins un des sites, le programme weather.py peut être lancé.

## weather.py
Pour récupérer de nouvelles dates:
* modifier 'reddid_AustinFC.csv' dans la ligne "reddit = pd.read_csv("reddit_AustinFC.csv")" pour charger le csv réalisé avec reddit.py
* modifier 'twitter_AustinFC.csv dans la ligne "twitter = pd.read_csv("twitter_AustinFC.csv")" pour charger le csv réalisé avec twitter2.py
* modifier les instances de 'weather_AustinFC.csv' dans le programme (ligne 51, 131, 132, 134)
* modifier l'url ligne 74 avec la bonne cible en se rendant sur le site wunderground

## reddit_AustinFC.csv twitter_AustinFC.csv weather_AustinFC.csv
Fichiers csv tests récupérés à l'aide des programmes

## scraping.ipynb
Analyse des fichiers csv et data-visualisation sur jupyter

## twitter.py
programme d'analyse de twitter avec scrolling par Selenium
* Utilisable sur de petits comptes car le scrolling prend énormément de temps sur des comptes twitter avec beaucoup de tweets
* Fonctionnel mais quelques lignes à modifier dans le fichier principal pour lire la date (date au format dd/mm/yyyy vs yyyy-mm-dd à l'issue de twitter2.py)
 * commenter les lignes 40 et 41 du programme weather.py
