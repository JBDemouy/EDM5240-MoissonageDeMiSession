# coding: utf-8

### Félicitations pour le soin apporté à la documentation!
### Très bon script, qui reprend pas mal une recette que je vous avais donnée, mais que tu cherches tout de même à pousser plus loin.

# Pour notre exercice de moissonnage, j'ai décidé de me concentrer sur l'API Twitter que j'ai créé.

# Différents import à faire, notamment les différentes clés auxquelles nous avons accès en créant notre API.
import csv
import json
import twitter
# from twit import cleAPI, cleSecreteAPI, jeton, jetonSecret
from twitterJHR import infos ### J'ai ajouté mes clés et «tokens» pour faire fonctionner ton script.

# Création de notre fichier .csv 
# fichier = "twitter_media_devoir3.csv"
fichier = "twitter_media_devoir3_JHR.csv"

# Cette variable du script est ce qui nous permet ensuite de pouvoir faire notre recherche "tweets"**
### Je remplace, bien sûr, avec mes propres infos
# t = twitter.Api(consumer_key=cleAPI,
# 	consumer_secret=cleSecreteAPI,
# 	access_token_key=jeton,
# 	access_token_secret=jetonSecret,
# 	tweet_mode="extended"
# 	)

t = twitter.Api(consumer_key=infos[0],
	consumer_secret=infos[1],
	access_token_key=infos[2],
	access_token_secret=infos[3],
	tweet_mode="extended"
	)

# Ici, on met une variable qui va nous donner l'opportunité de rentrer dans terminal les mots-clés recherchés
onCherche = input("qué!? ")

# ** Ici, notre variable tweets qui va aller chercher les infos nécessaires
tweets = t.GetSearch(term = onCherche,count = 500,result_type = "recent",return_json = True)

# On le met en comm rapidement mais cela nous donne plusieurs infos : 1. si ça marche / 2. récupérer les infos afin d'aller chercher les infos nécessaires pour nos prints
# print(json.dumps(tweets, indent=2, sort_keys=True))
# print("*"*60)

# Alors, j'ai tripé un peu sur l'affaire SNC Lavalin en récupérant plein de tweets.
# Mais je voulais avoir les différents mots-clés dans mon csv. Sur tes conseils, j'ai donc créé différentes variables pour ce faire.
hashtag1 = "SNCLavalin"
hashtag2 = "JodyWilsonRaybould"
hashtag3 = "TrudeauMustGo"
hashtag4 = "lavscam"
hashtag5 = "Puglaas"
hashtag6 = "JustinTrudeau" 

# Alors, en runnant mon script, je me suis rendu compte que je récupérais les tweets organiques en full_text mais seulement un extrait des retweets avec la mention RT avant chaque extrait.
# Après avoir perdu quelques bouclettes, j'ai trouvé plusieurs blogs qui parlaient de ce problème. J'ai donc trouvé cette formule qui m'a tout de même donné du fil à retordre...
# Ne sachant d'abord pas où la placer, je l'ai mise après ma fonction 'for tweet in tweets' et je ne récupérais rien.
# J'ai eu l'idée ensuite de la placer ici et tout semble fonctionner parfaitement. Seul hic qui me laisse pantois, c'est que je n'ai plus la mention RT. La fonction semble donc avoir le chic de me sortir uniquement les tweets organiques.
# Par sécurité, j'ai copié-collé le script trouvé sur le blog sans rien modifier...
def getText(tweet):       
    # Try for extended text of original tweet, if RT'd (streamer)
    try: text = tweet['retweeted_status']['extended_tweet']['full_text']
    except: 
        # Try for extended text of an original tweet, if RT'd (REST API)
        try: text = tweet['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try: text = tweet['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try: text = tweet['full_text']
                except:
                    # Try for basic text of original tweet if RT'd 
                    try: text = tweet['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try: text = tweet['text']
                        except: 
                            # Nothing left to check for
                            text = ''
    return text


# Ensuite, passons à notre fonction 'for in' afin de récupérer toutes nos infos nécessaires.
for tweet in tweets["statuses"]:
		cuicui = [] ### Hahaha! Savoureux nom de variable.

# Faire attention à n'actionner qu'un hashtag à la fois sinon, ils s'afficheront tous dans le csv.
# Ici, on utilise cuicui (variable définie au-dessus) .append() afin de consigner les données dans notre csv.
		# cuicui.append(hashtag1)
		# cuicui.append(hashtag2)
		# cuicui.append(hashtag3)
		# cuicui.append(hashtag4)
		# cuicui.append(hashtag5)
		# cuicui.append(hashtag6)

### Ici, au lieu de faire tous ces changements, il serait préférable de consigner le mot entré par l'utilisateur et consigné dans la variable onCherche:
		cuicui.append(onCherche)

# Ici, toutes les infos qu'on veut consigner dans notre csv
		cuicui.append(tweet["created_at"])

# Texte des tweets organiques sans la fonction 'def getText' -> Cette fonction est celle qui ne me laisse qu'un extrait des retweets.
		# s.append(tweet["full_text"])
# ce .append() me permet, en accord avec la fonction 'def getText' de récupérer tous mes tweets en full_text.
		cuicui.append(getText(tweet))
		cuicui.append(tweet["user"]["name"])

# J'ai ajouté "id" sur tes conseils afin de pouvoir, lorsqu'on traiterait ces informations, faire le tri avec des tweets qui seraient en double.
		cuicui.append(tweet["id"])
		cuicui.append(tweet["retweet_count"])
		cuicui.append(tweet["favorite_count"])
		cuicui.append(tweet["lang"])

# Ici, juste en ajoutant "location", il y a key error. Il fallait donc que je rajoute la clé "user" afin de récupérer l'info
		cuicui.append(tweet["user"]["location"])

# On print ce qu'on veut trouver.
		print("Date/Heure: ", tweet["created_at"])
		# print("Contenu: ", tweet["full_text"])
		print("tweet: ", getText(tweet))
		print("Pseudo: ", tweet["user"]["name"])
		print("IdUser: ", tweet["id"])
		print("Retweets: ", tweet["retweet_count"])
		print("P'tits coeurs: ", tweet["favorite_count"])
		print("Language: ", tweet["lang"]) ### Attention, «language» est en anglais; «langue», plus simplement :)
		print("Location: ", tweet["user"]["location"])

		print("*"*80)
	
	
# Fonction nécessaire afin de créer notre fichier csv.
		cool = open(fichier,"a")
		pouetpouet = csv.writer(cool)
		pouetpouet.writerow(cuicui)




