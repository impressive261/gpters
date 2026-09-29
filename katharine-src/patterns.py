from pathlib import Path
import json
A=Path(__file__).resolve().parent.parent/'katharine';patterns=[]
def p(ch,title,form,meaning,text,tip=''):
 pairs=[x.split('|') for x in text.splitlines()]
 patterns.append(dict(id=f'P{len(patterns)+1:02}',ch=ch,title=title,form=form,en=meaning,examples=[dict(ko=a,en=b) for a,b in pairs],tip=tip))
p(1,'Who or what?','N이/가 + verb','Name the person or thing doing an action.','친구가 와요.|A friend is coming.\n학생이 책을 읽어요.|The student reads a book.\n선생님이 답을 써요.|The teacher writes the answer.','이 follows a final consonant; 가 follows a vowel. 누구 + 가 becomes 누가; 저 + 가 becomes 제가.')
p(1,'Describe something','N이/가 + adjective','Say what something is like.','날씨가 좋아요.|The weather is good.\n문제가 어려워요.|The question is difficult.\n한국어가 재미있어요.|Korean is interesting.\n사람이 많아요.|There are many people.','좋다 uses 이/가 for what is good; 좋아하다 takes 을/를 for what you like.')
p(1,'Set a topic','N은/는 + information','Give information about a topic or make a contrast.','저는 물을 마셔요.|I drink water.\n친구는 커피를 마셔요.|My friend drinks coffee.\n오늘은 시간이 많아요.|I have a lot of time today.\n책은 작아요.|The book is small.','은 follows a final consonant; 는 follows a vowel. A topic is not automatically the subject. 이/가 is not limited to new information.')
p(1,'Objects of actions','N을/를 + verb','Name what you eat, read, watch, write or study.','동생은 밥을 먹어요.|My younger sibling eats a meal.\n학생은 한국어를 공부해요.|The student studies Korean.\n가족은 사진을 봐요.|My family looks at photos.\n선생님은 답을 써요.|The teacher writes the answer.','을 follows a final consonant; 를 follows a vowel.')
p(1,'Have or do not have','N이/가 있어요 / 없어요','Say what exists or what you have.','시간이 있어요.|I have time.\n숙제가 없어요.|I do not have homework.\n가방이 있어요.|I have a bag.')
p(1,'Names and identities','N이에요 / 예요','Say what something or someone is.','저는 학생이에요.|I am a student.\n이건 제 가방이에요.|This is my bag.\n이름이 뭐예요?|What is your name?','이에요 follows a final consonant; 예요 follows a vowel. These forms already appeared in the source.')
p(2,'Where something is','Place에 있어요 / 없어요','Locate a person or thing.','저는 방에 있어요.|I am in the room.\n가방은 교실에 있어요.|The bag is in the classroom.\n친구는 학교에 있어요.|My friend is at school.')
p(2,'Destinations and arrival','Place에 가요 / 와요 / 도착해요','Name a destination.','친구는 학교에 가요.|My friend goes to school.\n택시는 공항에 도착해요.|The taxi arrives at the airport.\n친구가 집에 와요.|My friend comes to my home.')
p(2,'Where an action happens','Place에서 + action','Say where you study, eat, work or meet.','저는 도서관에서 공부해요.|I study at the library.\n친구는 카페에서 기다려요.|My friend waits at the cafe.\n학생은 교실에서 한국어를 배워요.|The student learns Korean in the classroom.\n저는 공원에서 운동해요.|I exercise at the park.')
p(2,'Relative positions','N + position + 에 / 에서','Use a location noun before the place particle.','약국은 편의점 앞에 있어요.|The pharmacy is in front of the convenience store.\n휴대폰이 가방 안에 있어요.|The phone is inside the bag.\n학교 앞에서 만나요.|We meet in front of the school.\n책이 책상 아래에 있어요.|The book is under the desk.')
p(2,'Home and distance','Place에 살아요 / N이 place에 가까워요','Talk about where you live and nearby places.','한국에 살아요.|I live in Korea.\n집이 역에 가까워요.|My home is near the station.\n회사가 집에서 멀어요.|My workplace is far from home.\n집 근처에 카페가 있어요.|There is a cafe near my home.','살다 can use 에 or 에서. 에서 also marks a reference/source point in the distance example; it is not always an action location.')
p(3,'Transportation','Vehicle(으)로 + place에 가요','Say how you travel.','저는 버스로 가요.|I go by bus.\n친구는 지하철로 와요.|My friend comes by subway.\n자전거로 학교에 가요.|I go to school by bicycle.\n비행기로 한국에 가요.|I go to Korea by plane.','으로 follows a final consonant except ㄹ. 로 follows a vowel or ㄹ: 버스로, 지하철로, 자동차로.')
p(3,'Directions and routes','Direction(으)로 가요','Say which way to go.','오른쪽으로 가요.|I go to the right.\n왼쪽으로 천천히 가요.|I go slowly to the left.\n동쪽으로 가요.|I go east.\n서울로 보내요.|I send it to Seoul.','에 emphasizes the destination; (으)로 can emphasize direction. They overlap in some contexts but not everywhere. The original request form 가세요 is listed in the grammar extension.')
p(3,'Tools and payment','Tool(으)로 + object을/를 + action','Say which tool or means you use.','볼펜으로 이름을 써요.|I write my name with a ballpoint pen.\n종이를 가위로 잘라요.|I cut paper with scissors.\n카메라로 사진을 찍어요.|I take photos with a camera.\n컴퓨터로 파일을 보내요.|I send a file using a computer.\n카드로 선물을 사요.|I buy a gift with a card.')
p(3,'Materials','Material(으)로 + object을/를 만들어요','Say what you make something out of.','나무로 책상을 만들어요.|I make a desk out of wood.\n종이로 선물을 만들어요.|I make a gift out of paper.\n유리로 컵을 만들어요.|I make a cup out of glass.\n플라스틱으로 컵을 만들어요.|I make a cup out of plastic.')
p(3,'Languages','Language(으)로 말해요 / 바꿔요','Name the language you use.','영어로 말해요.|I speak in English.\n한국어로 말해요.|I speak in Korean.\n한국어로 바꿔요.|I change it into Korean.')
p(3,'Roles and jobs','Job(으)로 일해요','Say in what role someone works.','의사로 일해요.|I work as a doctor.\n요리사로 일해요.|I work as a chef.\n직원으로 일해요.|I work as an employee.')
p(4,'Also / too','N도 + information','Add another person or thing to the same statement.','저도 학생이에요.|I am a student too.\n동생도 빵을 먹어요.|My younger sibling eats bread too.\n가방도 필요해요.|A bag is also needed.\n우유도 있어요.|There is milk too.','At this level, 도 replaces 이/가, 은/는 or 을/를. It may follow other particles: 집에서도, 친구한테도. This is not a universal ban on particle combinations.')
p(4,'Only','N만 + information','Limit the statement to a person or thing.','저는 커피만 마셔요.|I drink only coffee.\n친구는 빵만 먹어요.|My friend eats only bread.\n이 가방만 비싸요.|Only this bag is expensive.\n오늘은 수업만 있어요.|Today I only have class.\n저는 이 단어만 외워요.|I memorize only this word.','Compare the scope: 저만 커피를 마셔요 = only I drink coffee; 저는 커피만 마셔요 = coffee is the only thing I drink in this context.')
p(4,'Possession','Owner의 + noun','Connect an owner or relationship to a noun.','어머니의 우산이에요.|It is my mother’s umbrella.\n친구의 이름을 써요.|I write my friend’s name.\n선생님의 책이에요.|It is the teacher’s book.\n가족의 사진을 봐요.|I look at a family photo.','저의 often contracts to 제. 의 may be omitted in natural noun combinations: 한국어 단어 is more natural than 한국어의 단어 for Korean vocabulary.')
p(5,'Give to someone','Person에게/한테 + object을/를 줘요','Name the recipient of something.','친구한테 선물을 줘요.|I give my friend a gift.\n아기한테 우유를 줘요.|I give the baby milk.\n강아지한테 물을 줘요.|I give the dog water.\n손님에게 정보를 줘요.|I give the customer information.','한테 is conversational; 에게 is neutral/written. People and animals normally take these; ordinary places take 에.')
p(5,'Send to someone','Person에게/한테 + object을/를 보내요','Name who receives a message or item.','친구한테 편지를 보내요.|I send a letter to my friend.\n동료한테 메시지를 보내요.|I send a message to my colleague.\n교수님에게 이메일을 보내요.|I send an email to the professor.\n가족한테 사진을 보내요.|I send photos to my family.')
p(5,'Communicate with someone','Person에게/한테 + communication verb','Name who hears the information.','저는 아내한테 전화해요.|I call my wife.\n학생은 선생님에게 대답해요.|The student answers the teacher.\n이웃한테 도움을 부탁해요.|I ask my neighbor for help.\n친척한테 소식을 전해요.|I share news with a relative.')
p(5,'Tell and teach','Person에게/한테 + information을/를 + verb','Add both a recipient and the information.','간호사에게 주소를 알려줘요.|I tell the nurse the address.\n후배에게 전화번호를 알려줘요.|I tell the junior colleague the phone number.\n외국인에게 한국어를 가르쳐요.|I teach Korean to a foreign learner.\n경찰에게 길을 물어요.|I ask a police officer for directions.')
p(5,'Attitudes toward people','Person에게/한테 + adjective','Say who you feel thankful toward or treat kindly.','선배에게 고마워요.|I am grateful to my senior colleague.\n손님에게 친절해요.|I am kind to customers.\n직장인에게 시간이 필요해요.|Working people need time.')
p(5,'One connected story','Destination → action location → recipient','Use several short sentences instead of one overloaded sentence.','저는 버스로 카페에 가요.|I go to the cafe by bus.\n카페에서 친구를 만나요.|I meet a friend at the cafe.\n친구도 커피를 좋아해요.|My friend likes coffee too.\n친구한테 선물을 줘요.|I give my friend a gift.')
grammar=[]
for line in '''이/가|subject particle|Core
은/는|topic / contrast particle|Core
을/를|object particle|Core
에|location / destination; time in extensions|Core
에서|action location; source/reference point|Core
(으)로|means / direction / material / language / role|Core
도|also / too|Core
만|only|Core
의|possession / relationship|Core
에게/한테|recipient / person addressed|Core
-아요/-어요/-해요|polite present-style ending|Core
이에요/예요|polite forms of 이다|Core
-요|politeness ending/particle in relevant forms|Core
와/과|and / with after nouns|Extension
하고/(이)랑|and / with, conversational|Extension
까지|up to / as far as|Extension
-고|and / linking verbs|Extension
-고 있다|ongoing action / resulting state in selected verbs|Extension
-고 싶다|want to do|Extension
-(으)면|if / when|Extension
-는|present action modifying a noun|Extension
-(으)ㄴ|adjective or completed-action modifier|Extension
-(으)ㄹ|prospective modifier|Extension
-았-/-었-|past-tense marker|Extension
-(으)ㄹ 수 있다|can / be able to|Extension
-(으)ㄴ 적이 있다|have ever done|Extension
-(으)세요|polite request or honorific present form|Extension
-(으)시-|subject honorific marker|Extension
(이)라고|quotation particle, including 뭐라고|Extension
-게|adverb-forming ending|Teacher-only
-도록|so that / instruction purpose|Teacher-only
-보다|comparison pattern in teacher notes|Teacher-only
-님|respectful suffix for a person or title|Core'''.splitlines():
 ko,en,level=line.split('|');grammar.append(dict(ko=ko,en=en,level=level))
(A/'patterns.json').write_text(json.dumps(patterns,ensure_ascii=False,indent=2));(A/'grammar.json').write_text(json.dumps(grammar,ensure_ascii=False,indent=2))
practice=[]
for p in patterns:
 for i,e in enumerate(p['examples'][:2],1):practice.append(dict(id=p['id']+f'-{i}',ch=p['ch'],ko=e['en'],model=e['ko'],extension=False,kind='sentence-practice',instruction='Say this in Korean. Change one detail and say your new sentence.'))
(A/'sentence_practice.json').write_text(json.dumps(practice,ensure_ascii=False,indent=2))
# All original word tests, now oral. Several Part C choices can be valid.
words=json.loads((A/'words.json').read_text());gloss={w['ko']:w['en'] for w in words};tests=[]
Awords=['저 나 친구 학생 선생님 사람 가족 아이','방 교실 식당 카페 가게 병원 공원 도서관','버스 지하철 택시 자동차 자전거 기차 비행기 배','아버지 어머니 형 누나 언니 오빠 할머니 할아버지','손님 사장님 경찰 간호사 남편 아내 아들 딸']
Bwords=['부모님 동생 이름 책 공책 연필 가방 사진','편의점 은행 약국 우체국 역 공항 화장실 시장','오토바이 오른쪽 왼쪽 동쪽 서쪽 남쪽 북쪽 펜','남자 여자 휴대폰 지갑 돈 열쇠 시계 옷','아기 어린이 어른 친척 이웃 동료 선배 후배']
C=[['____는 물을 마셔요. (저 / 가족 / 책)','____는 밥을 먹어요. (나 / 아이 / 공책)','____가 와요. (친구 / 부모님 / 연필)','____은 공부해요. (학생 / 동생 / 가방)','____이 답을 써요. (선생님 / 이름 / 사진)','____이 많아요. (사람 / 책 / 숙제)'],['____에 있어요. (방 / 공원 / 우체국)','____에서 공부해요. (교실 / 도서관 / 역)','____에서 먹어요. (식당 / 편의점 / 공항)','____에서 만나요. (카페 / 은행 / 화장실)','____에서 물을 사요. (가게 / 약국 / 시장)','____에 가요. (병원 / 우체국 / 미용실)'],['____로 학교에 가요. (버스 / 비행기 / 동쪽)','____로 회사에 가요. (지하철 / 배 / 서쪽)','____로 병원에 가요. (택시 / 오토바이 / 남쪽)','____로 공항에 가요. (자동차 / 오른쪽 / 북쪽)','____로 공원에 가요. (자전거 / 왼쪽 / 펜)','____로 가요. (기차 / 동쪽 / 볼펜)'],['____의 시계예요. (아버지 / 할머니 / 지갑)','____의 휴대폰이에요. (어머니 / 할아버지 / 돈)','____도 학생이에요. (형 / 남자 / 열쇠)','____도 와요. (누나 / 여자 / 시계)','____의 선물이에요. (언니 / 휴대폰 / 옷)','____만 와요. (오빠 / 지갑 / 신발)'],['____한테 물을 줘요. (손님 / 아들 / 친척)','____에게 연락해요. (사장님 / 딸 / 이웃)','____에게 말해요. (경찰 / 아기 / 동료)','____에게 질문해요. (간호사 / 어린이 / 선배)','____한테 전화해요. (남편 / 어른 / 후배)','____에게 선물을 줘요. (아내 / 친척 / 교수)']]
D=[['____를 해요. [homework]','____을 마셔요. [water]','____을 먹어요. [meal]','____를 마셔요. [coffee]','____이 좋아요. [home]','____가 커요. [school]','____는 커요. [company]','____은 좋아요. [Korea]'],['____에 가요. [hair salon]','____에서 책을 사요. [bookstore]','____에서 봐요. [movie theater]','____에서 물을 마셔요. [kitchen]','____에서 쉬어요. [living room]','____에 있어요. [bedroom]','____에서 일해요. [office]','____에서 만나요. [meeting room]'],['____으로 이름을 써요. [ballpoint pen]','____로 만들어요. [paper]','____로 잘라요. [knife]','____로 잘라요. [scissors]','____으로 먹어요. [spoon]','____으로 먹어요. [chopsticks]','____으로 물을 마셔요. [cup]','____로 사진을 찍어요. [camera]'],['____만 사요. [shoes]','____도 써요. [hat]','____만 써요. [glasses]','____도 있어요. [umbrella]','____만 줘요. [gift]','____도 좋아해요. [flower]','____도 좋아해요. [food]','____만 먹어요. [apple]'],['____님에게 질문해요. [professor]','____에게 시간이 필요해요. [working adult]','____에게 한국어를 가르쳐요. [foreigner]','____한테 물어봐요. [Korean person]','____에게 말해요. [you all]','____한테 줘요? [who]','____한테 물을 줘요. [animal]','____한테 밥을 줘요. [puppy]']]
ins={'A':'Say the English meaning. Then use the Korean word in a short sentence.','B':'Say the Korean word aloud. No written answer is needed.','C':'Choose any suitable option and say the whole sentence. Several choices may work; check the particle too.','D':'Complete the blank using the English hint. Say the whole Korean sentence.'}
for ch in range(1,6):
 sets={'A':Awords[ch-1].split(),'B':[gloss[w] for w in Bwords[ch-1].split()],'C':C[ch-1],'D':D[ch-1]}
 for part,items in sets.items():
  for i,s in enumerate(items,1):tests.append(dict(id=f'W{ch:03}-{part}-{i:02}',ch=ch,part=part,ko=s,instruction=ins[part],kind='word-test',extension=False))
assert len(tests)==150
(A/'word_tests.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2))
print('26 pattern sets; 33 grammar forms; 52 sentence prompts; 150 original word-test prompts')
