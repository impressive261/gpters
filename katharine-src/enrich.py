"""Build bilingual cards from the existing, actually generated pronunciation corpus."""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent.parent; A=R/'katharine'; A.mkdir(exist_ok=True)
m=json.loads((A/'audio-manifest.json').read_text())
rows='''저|I / me (humble)|I drink water.
나|I / me (casual)|I eat a meal.
여기|here|It is here.
거기|there (near you / previously mentioned)|We meet there.
저기|over there|I go over there.
어디|where|Where are you going?
여러분|you all / everyone (addressing a group)|I speak to you all.
누구|who|Who is coming?
친구|friend|A friend is coming.
학생|student|The student studies.
선생님|teacher|The teacher writes the answer.
사람|person|There are many people.
가족|family|The family looks at photos.
아이|child / kid|A child is coming.
부모님|parents (respectful)|My parents drink coffee.
동생|younger sibling|My younger sibling eats a meal.
이름|name|I write my name.
책|book|I read a book.
공책|notebook|I look at the notebook.
연필|pencil|I write my name with a pencil.
가방|bag|The bag is big.
사진|photo|I look at photos.
숙제|homework|I do homework.
물|water|I drink water.
밥|cooked rice / meal|I eat a meal.
커피|coffee|I drink coffee.
집|home / house|The house is big.
학교|school|The school is big.
회사|company / workplace|I go to work.
한국|Korea|I go to Korea.
한국어|Korean language|Korean is difficult.
시간|time|I have time.
날씨|weather|The weather is good.
문제|problem / exercise question|The question is difficult.
답|answer / solution|I write the answer.
오다|come|A friend is coming.
가다|go|I go to school.
먹다|eat|I eat a meal.
마시다|drink|I drink water.
보다|see / watch / look at|I look at photos.
읽다|read|I read a book.
쓰다|write; use; wear (a hat / glasses)|I write my name with a ballpoint pen.
하다|do|I do homework.
좋아하다|like|I like coffee.
공부하다|study|I study Korean.
있다|exist / have; stay (verb use)|I have time.
없다|not exist / not have|I do not have time.
좋다|be good|The weather is good.
크다|be big|The bag is big.
작다|be small|The notebook is small.
많다|be many / much|There are many people.
쉽다|be easy|The question is easy.
어렵다|be difficult|Korean is difficult.
재미있다|be fun / interesting|Korean is interesting.
아프다|be sick / hurt|The child is sick.
오늘|today|I have plenty of time today.
방|room|I am in the room.
교실|classroom|I study in the classroom.
식당|restaurant|I eat at a restaurant.
카페|cafe|We meet at a cafe.
가게|store / shop|I buy water at a store.
병원|hospital / clinic|I go to a hospital.
공원|park|I rest in the park.
도서관|library|I read books at the library.
편의점|convenience store|I buy water at a convenience store.
은행|bank|I go to the bank.
약국|pharmacy|I buy medicine at a pharmacy.
우체국|post office|I go to the post office.
역|station|I wait at the station.
공항|airport|I arrive at the airport.
화장실|restroom / bathroom|I go to the restroom.
시장|market|I buy apples at a market.
미용실|hair salon|I go to the hair salon.
서점|bookstore|I buy books at a bookstore.
영화관|movie theater|I watch a movie at a movie theater.
부엌|kitchen|I drink water in the kitchen.
거실|living room|I rest in the living room.
침실|bedroom|I am in the bedroom.
사무실|office|I work in an office.
회의실|meeting room|We meet in the meeting room.
엘리베이터|elevator|Someone is in the elevator.
계단|stairs|I wait on the stairs.
앞|front / in front|We meet in front of the school.
뒤|back / behind|It is behind the school.
안|inside (noun)|It is inside the room.
밖|outside|It is outside the house.
위|top / above / on|It is on the desk.
아래|bottom / below / under|It is under the desk.
살다|live|I live in Korea.
일하다|work|I work in an office.
기다리다|wait|I wait at the station.
쉬다|rest|I rest at home.
사다|buy|I buy water at a convenience store.
만나다|meet|I meet a friend at a cafe.
운동하다|exercise|I exercise in the park.
도착하다|arrive|I arrive at the airport.
가깝다|be near / close|My home is near the station.
멀다|be far|My workplace is far from home.
자주|often|We often meet at a cafe.
같이|together|We rest together in the park.
혼자|alone / by oneself|I am alone in the room.
먼저|first / before others|I go to the classroom first.
버스|bus|I go to school by bus.
지하철|subway|I go to work by subway.
택시|taxi|I go to the hospital by taxi.
자동차|car|I go to the airport by car.
자전거|bicycle|I go to the park by bicycle.
기차|train|I go by train.
비행기|airplane|I go to Korea by plane.
배|boat / ship|I go by boat.
오토바이|motorcycle|I go by motorcycle.
오른쪽|right side|I go to the right.
왼쪽|left side|I go to the left.
동쪽|east|I go east.
서쪽|west|I go west.
남쪽|south|I go south.
북쪽|north|I go north.
펜|pen|I write with a pen.
볼펜|ballpoint pen|I write my name with a ballpoint pen.
종이|paper|I make it out of paper.
칼|knife|I cut an apple with a knife.
가위|scissors|I cut paper with scissors.
숟가락|spoon|I eat rice with a spoon.
젓가락|chopsticks|I eat with chopsticks.
컵|cup|I drink water from a cup.
카메라|camera|I take a photo with a camera.
전화|phone / phone call|I speak over the phone.
컴퓨터|computer|I search using a computer.
인터넷|internet|I search on the internet.
카드|card / payment card|I pay by card.
영어|English language|I speak in English.
중국어|Chinese language|I speak in Chinese.
일본어|Japanese language|I speak in Japanese.
나무|wood / tree|I make a desk out of wood.
유리|glass (material)|I make a cup out of glass.
플라스틱|plastic|I make it out of plastic.
쇠|iron / metal|I make it out of metal.
의사|doctor|I work as a doctor.
요리사|cook / chef|I work as a chef.
가수|singer|I work as a singer.
배우|actor|I work as an actor.
직원|employee / staff member|I work as an employee.
말하다|speak / say|I speak in English.
보내다|send|I send a photo to a friend.
만들다|make|I make it out of paper.
자르다|cut|I cut an apple with a knife.
찍다|take a photo|I take a photo with a camera.
찾다|look for / find|I look for information on the internet.
바꾸다|change / switch / convert|I change the English into Korean.
이동하다|move / travel between places|I travel by bus.
빨리|quickly|I go to the right quickly.
천천히|slowly|I go to the left slowly.
아버지|father|It is my father's watch.
어머니|mother|It is my mother's mobile phone.
형|older brother (male speaker)|My older brother is a student too.
누나|older sister (male speaker)|My older sister is coming too.
언니|older sister (female speaker)|It is my older sister's gift.
오빠|older brother (female speaker)|Only my older brother is coming.
할머니|grandmother|It is my grandmother's umbrella.
할아버지|grandfather|My grandfather is going too.
남자|man|A man is coming too.
여자|woman|Only women are coming.
휴대폰|mobile phone|I only have a mobile phone.
지갑|wallet|I have a wallet too.
돈|money|I have money.
열쇠|key|I have a key too.
시계|watch / clock|I only look at the clock.
옷|clothes|I buy clothes too.
신발|shoes|I only buy shoes.
모자|hat|I wear a hat too.
안경|glasses|I wear glasses.
우산|umbrella|I have an umbrella too.
선물|gift / present|I give a gift to a friend.
꽃|flower|I like flowers too.
음식|food|I like Korean food.
사과|apple|I only eat apples.
빵|bread|I eat bread too.
우유|milk|I only drink milk.
주스|juice|I drink juice too.
영화|movie|I watch movies too.
음악|music|I listen to music.
게임|game|I play games too.
노래|song|I only listen to songs.
수업|class / lesson|I have class too.
시험|exam / test|I take an exam.
단어|word|I write words too.
문장|sentence|I only read sentences.
페이지|page|I look at this page.
주다|give|I give a gift to a friend.
받다|receive|I receive a gift.
빌리다|borrow|I borrow books too.
잃어버리다|lose / misplace|I often lose my keys.
고르다|choose|I choose a gift.
입다|wear / put on clothes|I put on clothes.
같다|be the same / alike|The hats are the same too.
다르다|be different|Only the shoes are different.
필요하다|be necessary / needed|I need an umbrella too.
중요하다|be important|The exam is important too.
비싸다|be expensive|The clothes are expensive.
싸다|be cheap / inexpensive|The shoes are inexpensive too.
또|again / also (adverb)|I meet my friend again.
가끔|sometimes|I sometimes watch movies too.
손님|guest / customer|I give water to the guest.
사장님|boss / business owner (respectful)|I contact the boss.
경찰|police / police officer|I ask a police officer for directions.
간호사|nurse|I ask the nurse a question.
남편|husband|I call my husband.
아내|wife|I give my wife a gift.
아들|son|I give my son a book.
딸|daughter|I give my daughter a letter.
아기|baby|I give the baby milk.
어린이|child / children (neutral-polite term)|I give an apple to the child.
어른|adult / grown-up|I greet an adult.
친척|relative|I contact a relative.
이웃|neighbor|I help a neighbor.
동료|colleague / coworker|I send an email to a colleague.
선배|senior / more experienced peer|I ask a senior colleague.
후배|junior / less experienced peer|I tell a junior colleague.
교수|professor|I ask the professor a question.
직장인|working adult / company employee|Working people need time.
외국인|foreigner / person from another country|I teach Korean to a foreigner.
한국인|Korean person|I ask a Korean person.
동물|animal|I give water to an animal.
강아지|puppy / pet dog|I feed the dog.
고양이|cat|I give water to the cat.
편지|letter|I give a friend a letter.
이메일|email|I send an email to a colleague.
문자|text message|I send my husband a text.
메시지|message|I send my wife a message.
전화번호|phone number|I tell the customer the phone number.
주소|address|I tell my friend the address.
질문|question (something asked)|I ask a senior colleague a question.
대답|answer / reply (to someone)|I answer the teacher.
도움|help / assistance|I help a neighbor.
연락|contact / communication|I contact the boss.
이야기|story / talk|I tell a story to the child.
약속|promise / appointment|I make a promise to a friend.
소식|news / update|I share news with my family.
정보|information|I give information to the customer.
조언|advice|I give advice to a junior colleague.
인사|greeting|I greet an adult.
전화하다|call (by phone)|I call my father.
연락하다|contact / get in touch|I contact the boss.
묻다|ask (not bury)|I ask a police officer for directions.
대답하다|answer / reply|I answer the teacher.
부탁하다|ask a favor / request|I ask a friend for help.
알려주다|tell / inform / let someone know|I tell a junior colleague the address.
가르치다|teach|I teach Korean to a foreigner.
고맙다|be thankful / grateful|I am grateful to my senior colleague.
친절하다|be kind / helpful|I am kind to customers.
약|medicine|I buy medicine at a pharmacy.
책상|desk|There is a book on the desk.
근처|vicinity / nearby area|There is a cafe near my home.
옆|side / next to|The pharmacy is next to the hospital.
길|road / way / directions|I ask a police officer for directions.
서울|Seoul|I send it to Seoul.
파일|file (computer)|I send a file using a computer.
차|tea (drink)|I drink tea too.
현금|cash|I pay in cash.
아침|morning / breakfast|I eat bread in the morning.
생일|birthday|I give a gift on a birthday.
여권|passport|The passport is inside the bag.
여행|trip / travel|I send an update about my trip.
여행지|travel destination|I take photos at my travel destination.
주말|weekend|What do you do on weekends?
물건|thing / item / belonging|Which item is expensive?
일|work / task (noun)|I work today too.
운동|exercise (noun)|I eat after exercising.
그다음|the next step / after that|Where do you go after that?
중|among / middle (bound noun)|Who in your family likes coffee?
후|after (bound noun)|I drink water after exercising.
적|past experience / occasion (bound noun)|Have you ever traveled by boat?
수|possibility / ability (bound noun)|I can go by bus.
뭐|what (conversational)|What do you eat?
무엇|what (full form)|What do you read?
이것|this thing|This is my bag.
언제|when|When do you come home?
이|this (before a noun)|This bag is big.
그|that / previously mentioned (before a noun)|I send a message to that person.
어떤|what kind of / which (before a noun)|What kind of gift is it?
제|my (humble; 저의)|It is my bag.
지금|now|Where are you now?
가까이|nearby / close by (adverb)|My friend lives nearby.
많이|a lot (adverb)|I know many words.
어떻게|how|How do you go to school?
얼마나|how much / to what extent|How long do you stay?
오래|for a long time|I stay at the cafe for a long time.
네|yes (polite)|Yes, I drink coffee.
아니요|no (polite answer)|No, I only drink water.
배우다|learn|I learn Korean from the teacher.
듣다|listen / hear|I listen to music.
외우다|memorize|I memorize only this word.
질문하다|ask a question|I ask the teacher a question.
물어보다|ask / inquire|I ask a Korean person.
전하다|pass on / convey|I share news with my family.
인사하다|greet|I greet an adult.
알다|know|I know Korean words.
모르다|not know|I do not know this word.
타다|ride / take (transport)|I take a taxi.
여행하다|travel|I travel by train.
사용하다|use|I use cash.
가지다|have / possess / take|I have my mobile phone with me.
넣다|put in|I put a book in the bag.
이야기하다|talk / tell a story|I talk with a friend.
보여주다|show (to someone)|I show a photo to a friend.
편하다|be comfortable / convenient|The subway is convenient.
싶다|want to (after -고)|I want to go to Korea.
이다|be (identity; after a noun)|I am a student.'''
translations={a:(b,c) for a,b,c in (line.split('|') for line in rows.splitlines())}
adj=set('있다 없다 좋다 크다 작다 많다 쉽다 어렵다 재미있다 아프다 가깝다 멀다 같다 다르다 필요하다 중요하다 비싸다 싸다 고맙다 친절하다 편하다'.split())
pron=set('저 나 여기 거기 저기 어디 여러분 누구 뭐 무엇 이것 언제'.split())
adv=set('자주 같이 혼자 먼저 빨리 천천히 또 가끔 지금 가까이 많이 어떻게 얼마나 오래'.split())
det=set('이 그 어떤 제'.split());bound=set('중 후 적 수'.split())
aliases={'누구':['누가'],'뭐':['뭘','뭐를','뭐가','뭐로','뭐예요','뭐라고'],'이것':['이거','이건'],'저':['저는','제가','저의'],'나':['나는','내가','내','나의'],'같다':['같은'],'모르다':['모르는'],'가다':['가는','갈','가세요'],'사다':['산'],'잃어버리다':['잃어버렸어요'],'교수':['교수님'],'알려주다':['알려 주다','알려 줘요'],'보여주다':['보여 주다','보여 줘요']}
notes={'있다':'Adjective for existence/possession; also a verb for staying.','오늘':'A noun used as a time expression; it may function adverbially.','쓰다':'Name: write. Pencil: use. Hat/glasses: wear. The spelling and polite form are the same.','가지다':'가지고 있어요 is the usual expression for currently having an item with you; 가져요 is not an automatic replacement.','교수':'Use 교수님 when respectfully referring to or addressing a professor.','묻다':'Asking: 물어요. The homograph meaning bury has 묻어요 and is not tested here.'}
groups=[(1,8,'Pronouns'),(9,16,'People and family'),(17,23,'Study and items'),(24,26,'Food and drink'),(27,30,'Places'),(31,35,'Languages and general'),(36,45,'Everyday actions'),(46,55,'States and descriptions'),(56,56,'Time'),(57,82,'Places'),(83,88,'Position'),(89,96,'Location and actions'),(97,98,'Distance'),(99,102,'Manner and frequency'),(103,111,'Transport'),(112,117,'Direction'),(118,130,'Tools and media'),(131,133,'Languages'),(134,137,'Materials'),(138,142,'Jobs'),(143,150,'Actions and communication'),(151,152,'Speed'),(153,162,'People and family'),(163,174,'Belongings and clothing'),(175,179,'Food and drink'),(180,188,'Entertainment and study'),(189,194,'Giving and belongings'),(195,200,'Comparison'),(201,202,'Frequency'),(203,222,'People and relationships'),(223,225,'Animals'),(226,241,'Communication'),(242,248,'Communication actions'),(249,250,'People and feelings'),(251,269,'Added everyday vocabulary'),(270,273,'Added bound nouns'),(274,281,'Added questions and pointing'),(282,289,'Added short expressions'),(290,308,'Added actions and forms')]
words=[]
for n in range(1,309):
 id=f'w{n:03}'; ko=m['generated'][id+'-word']['text']; ex=m['generated'][id+'-example']['text']; yo=m['generated'].get(id+'-polite',{}).get('text','').replace('. ',' / ').rstrip('.')
 if ko=='이다':yo='이에요 / 예요'
 en,exe=translations[ko];pos='Adjective' if ko in adj else 'Auxiliary' if ko=='싶다' else 'Copula' if ko=='이다' else 'Verb' if yo else 'Pronoun' if ko in pron else 'Adverb' if ko in adv else 'Determiner' if ko in det else 'Dependent noun' if ko in bound else 'Interjection' if ko in ['네','아니요'] else 'Noun'
 ch=1 if n<=56 else 2 if n<=102 else 3 if n<=152 else 4 if n<=202 else 5 if n<=250 else 0
 group=next(g for a,b,g in groups if a<=n<=b)
 words.append(dict(id=id,ko=ko,yo=yo,en=en,example=ex,exampleEn=exe,pos=pos,group=group,ch=ch,source='Original vocabulary' if n<=250 else 'Added from source sentence',aliases=aliases.get(ko,[]),note=notes.get(ko,'')))
assert len(words)==len(translations)==308
assert sum(bool(w['yo']) for w in words)==78
assert m['complete'] and len(m['generated'])==694
(A/'words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
(A/'audio-manifest.js').write_text('window.KATHARINE_AUDIO='+json.dumps(m,ensure_ascii=False,separators=(',',':'))+';')
with (A/'Vocabulary_Complete.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);wr.writerow(['ID','Part of speech','Group','Chapter','Dictionary / word','Polite form','English','Korean example','English example','Source','Notes'])
 for w in words:wr.writerow([w[k] for k in ['id','pos','group','ch','ko','yo','en','example','exampleEn','source','note']])
print('308 bilingual entries; 78 polite forms; 694 existing neural recordings')
