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
### Ali ura objave vpliva na uspešnost le te?
Ali ura ob kateri objavimo na določen podbralnik vpliva na izid objave? Izid objave si interpretiramo z njeno uspešnostjo, le to se meri z številom 'upvotes'. Tako je naprimer objava, ki je v celoti prejela 20 'upvotes' manj uspešna, kot nekatera druga, ki jih je prejela 1000+. Na Redditu lahko opazimo, da je število uspešnih objav majhno v primerjavi z ne uspešnimi. Za tem verjetno leži algoritem sortiranja, to gre nekako po skupinah(new, rising, hot), najbolše objave se premikajo po le teh, vendar le naj uspešnejše se premaknejo v naslednjo. V vsaki skupini se tako objava prikaže vedno večjemu številu ostalih uporabnikov, ter ima tako možnost prejeti večje število 'upvotes'.

No, če se vrnemo k vprašanju. Zbrali smo podatke o urah vseh objav, prav tako smo si shranili tudi uspešnosti('upvotes'). 
Spodaj sta prikazana dva grafa. Na zgornjem je povprečno število uspešnosti objave, ki je bila objavljena v določeni uri. V spodnjem pa število objav v posamezni uri izmed vseh 
 
![slika1](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/post_upvotes_all.png)

Opazimo, da grafa nista linearna, prav tako bomo kasneje pokazali, da sta si verjetno odvisna.
Če se osredotočimo na spodnji graf:
Predpostavimo, da število objav narašča z številom uporabnikov, ki se v določeni uri nahajajo na spletni strani. To bi verjetno držalo, saj v primeru, da je več uporabnikov na strani jih tako tudi več poda objavo.
Opazimo dva vrhova in dve dolini. Tako je v določenih urah več uporabnikov, kot v ostalih. Npr. okoli 15h in med 20h - 3h je tako veliko več uporabnikov, kot v ostalih urah. Iz zbranih podatkov težko predpostavimo zakaj bi bilo tako. Zato bomo v prihodnje primerjali med različnimi skupinami podbralnikov.

Če primerjamo obe 'krivulji' v določeni uri, prikazano odspodaj:

![slika2](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/post_upvotes_all_1.png)

Med 10. in 11. uro (zelena navpična črta) so objave povprečno prejele več 'upvotes'. Opazimo, da jo to ravno pred porastom števila uporabnikov. To si lahko logično razlagamo, ob tisti uri število uporabnikov narašča. Objave, ki so bile takrat objavljene tako vidi več oseb in jim tako ahko več oseb dodeli 'upvote'. To seveda velja v povprečju, objava mora ne glede na to še vedno biti kvalitetna. 
Če pogledamo rdečo navpično črto opazimo, da objave objavljene v tisti uri povprečno prejmejo manj 'upvotes', saj se število uporabnikov in s tem posledično vidljivost objave drastično zmanjša. Tako lahko zaključimo, da čas objave vpliva na njeno uspešnost.

### Zakaj se število uporabnikov tako razlikuje? 
Ker je Reddit svetovno znana spletna stran, nam prejšnji graf v relaciji z časom pri tem ne pomaga. Ker smo te delili v skupine lahko tako primerjamo podbralnike dveh različnih, skupin.

Tako bomo primerjali med podbralniki Evropskih držav in Severno Ameriških.

![slika3](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/compare_post_upvotes.png)

Opazimo podobnost spodnjih 'krivulj', obe imata dva vrhova, in sicer enega malo večjega od drugega z edino razliko, da sta si med seboj zamaknjeni po času. Na sliki sicer ne piše vendar je čas podan po UTC. Vidimo, da je vrh pri Evropskih podbralnikih okoli 12. ure, pri Severno Ameriških pa okrog 20. ure. Torej se ujemata, saj je v Ameriki povprečno čas +8 UTC, v Evropi pa okrog 0 UTC. To pomeni, da vrhova nastaneta okrog kosila.
Ker sta si zelo podobni lahko trdimo, da gre pri obeh za iste razloge rasti. 
To bi sicer malo težje dokazali, vendar lahko sklepamo:
- Število uporabnikov začne naraščati zjutraj, ko se večina uporabnikov zbudi.
- Okoli kosila se število zmanjša, verjetno zaradi kosila.
- Ponovno začne naraščati proti večeru, ko se večina ljudi poda v pojsteljo pred tem pa še malo pobrska po telefonu.

## Lastnosti različnih skupin podbralnikov
Ogledali si bomo nekaj grafov razpršenosti objav. In sicer: števila komentarjev v odvisnosti od števila 'upvotes', z barvo je prikazan 'upvote/downvote ratio'(Procent števila 'upvotes' v primerjavi z vsemi ocenami, torej 'upvotes' + 'downvotes' in je med 0 in 1). Objave z velikimi števili komentarjev in 'upvotes' so uspešne in imajo ponavadi večji upvote/downvote ratio. 
Ker imajo različne skupine/podbralniki različno število sledilcev se ne bomo osredotočali na velikosti prej omenjenih števil. 

V naslednjih grafih je posamezna pika ena objava, na y-osi je predstavljeno njeno število komentarjev, na x-osi število upvotes z barvo pa njen 'upvote/downvote ratio'(večji je bolše je). Osi so podane logaritemsko(logaritmic scale), ker so podatki precej razpršeni.

#### Podbralniki iz skupine normal. 
Veliko raznolikosti v delovanju določenih podbralnikov iz te široke skupine, vendar nam še vedno poda nekaj informacij.
![slika4](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_normal.png)

Opazimo obliko, število komentarjev narašča z številom 'upvotes'. To lahko zasledimo že z gledanjem objav na Redditu, ko objavo vidi več uporabnikov, tako prejme več 'upvote'ov in hkrati več komentarjev. 

Zasledimo tudi obarvanost, na levi strani, kjer so objave z manjšim številom komentajev/'upvote'ov so bolj obarvane zeleno. Kar pomeni ,da imajo slabši 'ud ratio'. To pripisujemo k algoritmom sortiranja objav na Redditu. Objave z slabšim 'ud ratio'm so ponavadi slabše in jih tako ne vidi veliko oseb, ker se ne premikajo po skupinah sortiranja(new, rising, hot...).

#### Podbralniki skupine nsfw
V to skupino podbralnikov spadajo vsi tisti, ki niso primerni "za v javnost". Večinoma se tukaj objavlja pornografija pri nekaterih pa dekleta ali moški objavljajo svoje gole slike. 

Če si ogledamo, kako bi zgledal graf razprešenosti:

![slika5](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_nsfw.png)

Zanimivo je bolj obarvan rumeno, kar pomeni, da so objave bolše ocenjene. Hkrati je tudi manj komentarjev, v primerjavi z katerimi drugimi skupinami, to se sicer ne vidi takoj, vendar če se ozremo na števila pri oseh to opazimo. 
Zakaj je tako nebi mogel povedati z gotovostjo, vendar sklepam, da osebe bolje sprejmejo goloto.

#### Podbralniki različnih držav 

![slika6](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_europe.png) ![slika7](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_usa.png)

Pojavita se dve 'veji'. Desna je predvsem normalna kot smo opazili do zdej. Leva pa nakazuje večje število komentarjev. Hkrati je vse skupaj obarvano bolj zeleno, kar pomeni, da so objave slabše ocenjene. To bi blo predvsem zato, ker se v takih podbralnikih večinoma objavlja razna uprašanja, politična mnenja ali novice. Pri tem je razlika v osebnih mnenjih velika, posledično več komentarjev in slabše ocene.

#### Nekaj zanimivih oblik pri raznih podbralnikih 

##### Askreddit
Ta podbralnik je namenjem vprašanjem uporabnikov namenjenim ostalim uporabnicom. Tako je bolj zasnovan na komentarjih objav, kot pa na sami vsebini objav. Same objave zajemajo le eno vprašanje.

![slika8](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_askreddit.png)

Na levi strani vidimo velik 'skok' navzgor, to si lahko razložimo z tem, da je podbralnik bolj osredotočen na komentarje. Če si sam podbralnik ogledamo opazimo, da objave prvotno dobijo veliko koentarjev ter nato šele 'upvotes'. To bi razložilo tisti 'skok'. 

##### Politics 

Podbralnik je namenjen političnim novicam in mnenjem. 

![slika9](https://github.com/15minutOdmora/RedditAnalysis/blob/master/slike/scatter_politics.png)

Dokaj linearna oblika, komentarji naraščajo z številom 'upvotes', vendar jih je nekoliko več, kot pri normalnih podbralnikih. Vidimo tudi nekaj pik(ojav), ki odstopajo, tam se je verjetno v komentarjih razvilo, kar nekaj pogovorov glede na naravo podbralnika. 

#### Zaključek 

Pri vseh zgoraj prikazanih grafih lahko zasledimo, da so bolj obarvani zeleno(sllabše ocenjeni) na levi strani, ter, da so ponavadi objave z več komentarji slabše ocenjene. To si lahko razlagamo s tem, da kontroverzne objave sprožijo več različnih menenj in so tako uporabniki bolj nagnjeni h komentiranju. 

### Sortiranje
Sledi prikaz dveh vrst stolpičnih diagramov, podbralnikov razverščenih po različnih parametrih.

#### Nagrade 
V Redditu poznamo nagrade, razlikujejo se po vrednosti ter prikazu. Če je uporabniku objava zelo všeč ji lahko podari eno izmed mnogih nagrad. Nagrade se sicer plača z Reddit valuto imenovano coins katero kupimo z pravim denarjem.

Tukaj bomo uporabili le tiste klasične kot so:
- silver      100 coins    0,40€
- gold        500 coins    2,30€
- platinum    1800 coins   7,00€

#### 




