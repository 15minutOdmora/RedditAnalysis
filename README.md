# Reddit Analysis
## Osnovna ideja projekta je uporabiti analizirane podatke za optimizacijo dodajanja objav.

## Na kratko o Redditu:
Spletna platforma Reddit je sestavljena iz več podbralnikov, ki se delijo na teme (npr.
politika, slike narave, "memes"...). 
V vsak podbralnik lahko uporabniki deiljo objavo, na katero lahko komentirajo, ji dodelijo "upvote" ali "downvote". 
Slednji predstavljajo sistem točkovanja uspešnosti objave. Glede na uspešnost objave, se te ločijo na naslednje kategorije; "new", "rising", "hot", "top". Vsaka objava se najprej pojavi v rubriki "new". Uspešnejše objave se premaknejo v rubriko "rising". 
Iz tod se jih nato le peščica prebije do "hot". Vsak podbralnik ima nato še možnost sortiranja objav pod "top", kjer so le
najuspešnejše objave vseh časov. Objave so lahko tudi nagrajene z "awards", za katere uporabniki plačajo.
Uporabniki lahko nagradijo tudi komentarje drugih, ki so tudi točkovani z "upvotes"/"downvotes". Uporabniki
glede na neke algoritme uspešnosti objave ali komentarjev nabirajo "karmo"(predstavljeno s
številom/točkami) npr. 10 karme = malo, 200000 karme = dosti.

## Na kratko o poteku dela
Celoten potek dela je potekal v angleškem jeziku, ter sva ga razdelila na dva dela:
- Daily data (dnevni podatki), Liam Mislej.
- User data (podatki zbrani iz raznih profilov), Gašper kovačič.

### Daily data
Ker se na Redditu dnevno pojavi na tisoče objav in nebi bilo mogoče vseh prebrati. Sva sestavla program, ki dnevno prebira razne objave iz različnih podbralnikov. Pred tem sva sestavila seznam podbralnikov, katere bova brala. 
In sicer sva jih ločila na 4 skupine:
- normal, najbolših 178 podbralnikov po število sledilcev.
- nsfw, najbolših 21 "nsfw"(not safe for work) podbralnikov, večinoma gre tle za podbrlnike, ki prikazujejo goloto.
- europe, naključno izbranih 15 podbralnikov evropskih držav.
- usa, najbolših 24 podbralnikov po številu sledilcev Severno Ameriških držav(kljub temu, da piše "usa").
Skupno je tako bilo dnevno pregledanih 238 podbralnikov, število objav je variralo za posamezen podbralnik vse med 0 in 100. 
Po enajstih dnevih je bilo prebranih skupno 126,093 objav, kar je približno 11,463 na dan. 

Tako sva program imenovan reading_daily_data.py pognala 11 dni zapored ob približno enaki uri. Ta je nato za vsak podbralnik iz omenjenih skupin prebral podatke od do 100 najbolših objav iz preteklih 24 ur. Kot zanimivost je to v povprečju trajalo približno 2 uri. 
Ker razni podbrlniki prejmejo dnevno več kot 1000 objav, ni bilo mogoče prebrati vseh. Tako ne predstavljajo vsi podatki celotne 'populacije'.

Pri dnevnem prebiranju podatkov smo za posamezno objavo prebrali in shranili naslednje podatke:
- število 'upvotes'
- število komentarjev
- čas objave
- dolžina naslova objave(V besedah in znakih).
- ime avtorja(username), kasneje uporabljeni pri User data.
- upvote downvote ratio (Procent števila 'upvotes' v primerjavi z vsemi ocenami, torej z 'downvotes').
- število prejetih nagrad(awards).
- število 'upvotes' 10 naj boljših komentarjev.

### User data 
...

## Uporabljeni programi
V repozitoriju se nahajata dve mapi: main in secondary.
V mapi **main** so shranjeni vsi programi in razne datoteke, ki so potrebni za pogon programa main.py, z le tem si je mogoče ogledati vse prikazane grafe, histograme,... V programu je sestavljen enostaven uporabniški vmesnik, preko katerega je mogoče izrisati vse v nadalnem prikazane podatke. To je mogoče za prej omenjene skupine podbralnikov(normal, nsfw...), posamezne podbralnike ali pa za vse skupaj.
V mapi **secondary** se nahajajo vsi programi, ki so bili uporabljeni za zbiranje in urejanje podatkov.

## Uporabljene knjižnice:
#### Niso potrebne za delovanje programa main.py:
- praw (API za zbiranje podatkov iz Reddita)
- prawcore
#### So potrebni za delovanje programa main.py:
- json
- numpy
- matplotlib

## Analiza
### Ali čas objave vpliva na uspešnost le te?
![slika1](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/post_upvotes_all.png)



