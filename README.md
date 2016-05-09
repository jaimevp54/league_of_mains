![League of mains](http://image.prntscr.com/image/f520567c01e5402fb1da162f6a78acb5.png)
# League of Mains

Is a **League of Legends** statistics site focused on the summoner's main (most used) champion. 

Created as a submission for the Riot's **[API CHALLENGE 2016](https://developer.riotgames.com/)**.

## Table of contents

- [Features](#features)
- [Demo](#demo)
- [Programing language and Frameworks](#programming-language-and-frameworks)
- [Local Setup](#local-setup)
- [Api Usage](#api-usage)
- [Deployment](#deployment)
- [Developer](#developer)
- [Credits](#credits)
- [What's next?](#whats-next)
- [Questions and issues](#questions-and-issues)
- [Disclaimer](#disclaimer)

## Features

- Find out who is your most played champion (main).
- Champion Mastery data.
- Statistics for total data of ranked gamesplayed.
- Rwecent videos of youtube related to your main.
- Comparison between two summoners data.
- Fully responsive.


## Demo
![home page](http://image.prntscr.com/image/083781a9b62341718f9f4b34d9a101b2.png)

You can test a fully working live demo at http://leagueofmains.pythonanywhere.com, to see the stored data in the database you can go to the admin's page ( http://leagueofmains.pythonanywhere.com/admin )
it already has a test summoner that you can use. user: `leagueofmains` password: `aniviabestchamp`.

## Programming language and Frameworks

The site is implemented using [Python](https://www.python.org/) and the [Django](https://www.djangoproject.com) framework, [Bootstrap](http://getbootstrap.com/) for the *html* and *css* and the library **[Cassiopeia](https://github.com/meraki-analytics/cassiopeia)**  was used to comunicate with the Riot's API.

## Local setup

To test the project locally in your machine,  the next commands can be used.

- **Note**: Preferably working inside a virtual enviroment with python 3.5 installed.

```bash

git clone https://github.com/jaimevp54/league_of_mains.git

cd league_of_mains

pip install -r requirements.txt

python manage.py runserve

```

## Api usage
	
League of mains makes several api calls everytime data about a summoner is requested.
Specifically one call for each one of the following:
- The summoner  
- The summoner's mastery data
- The summoner's champion with the most mastery points.
- The summoner's match list for that champion.
- One extra call for each match that has not been yet analized.

This causes that the first time a summoner is searched will take significantly more time that the followings.

For more information about the API calls check it's [reference page](https://developer.riotgames.com/api/methods).

## Deployment

The demo is being hosted in www.pythonanywhere.com with a begginer (Free) account. This way the leagueofmains.pythonanywhere.com site will expire in a maximum of three months, this is enough time for submission porpuses.



## Developer

Hi! my name is Jaime Viñas from Dominican Republic, student of Telecomunications Engineering, Summoner name: Kyde and as it's made obvious in the [Demo](#demo) section, a Anivia's lover. Also planning to apply for a work on **Riot Games** when I finish my studies so maybe I get to know the people who judge this :D.

## Credits
Thanks to those that even on simple ways helped me in the development of this project

#### Testing and feedback

- Carlos Lizardo (zShinoda - Lan)
- Lisaril Morel (Raicedes - Lan)
- Yorman Rodriguez (Yormaan - Lan)
- Bernardo Sosa (Shnooflown - Lan)
- Jean Carlos Taveras (Jyan - Lan)
- Alfonso Ulloa (El Charlief - Lan )
- Jordany Filpo (JordMaster - Lan)
- Indhira Torres (PrincessZelda19 - Lan)
	
#### Art

- [inkinesss](http://inkinesss.deviantart.com) : Created the amazing art used as background for the home page, also the cute chibi Tresh.
 
	
## What's next?

For the later development of this project ( After the contest is finished on June 6th ) if possible new features will be added.

#### For example:
- More `related content` sections (Reddit, Fanart, etc...)
- Ranking section featuring all the summoners who share the same main champion.
- Log section with all the changes the champion has been through at each patch.
- Faq page.
- Fix some known bugs or issues.

## Questions and issues

Right now some minor issues exists that are not going to be adressed until the contest has ended.

- Page returns a error 500 when the summoner's name form is left blanc on the home page.
- Page returns a error 500 when a summoner that has not played after the champion mastery system was released is searched for.
- Some buttons dont work on very small screens.

## Disclaimer

League of Mains isn’t endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
