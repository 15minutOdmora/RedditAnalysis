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
- normal, najbolših 178 podbralnikov po število sledilcev
- nsfw, najbolših 21 "nsfw"(not safe for work) podbralnikov, večinoma gre tle za podbrlnike, ki prikazujejo goloto.
- europe, naključno izbranih 15 podbralnikov evropskih držav.
- usa, najbolših 24 podbralnikov po številu sledilcev Severno Ameriških držav(kljub temu, da piše "usa").

### User data 
...

