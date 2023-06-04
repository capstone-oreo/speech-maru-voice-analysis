# -*- coding: utf-8 -*-

import pandas as pd
from krwordrank.word import KRWordRank
from kiwipiepy import Kiwi

#MEANINGLESS_WORDS=['아니', '막', '진짜', '사실', '근데']
# 1. 길이가 긴 문장 
# 2. 키워드
# 3. 자주 사용한 단어 

class text_preprocessor:
    
    def __init__(self, text):
        # 침묵 구간으로 쪼개진 텍스트 배열 
        self.sentences=text 
        self.kiwi=Kiwi()

        # 하나의 텍스트 
        self.total_text=''.join(text)

        # 문장 분리
        self.sentence_arr=[]
        kiwi_sentences=self.kiwi.split_into_sents(self.total_text)
        for sentence in kiwi_sentences:
           self.sentence_arr.append(sentence.text)
      

    def concat_sentences(self):
        text=' '.join(self.sentences)
        return text 
    
    # (침묵) 추가한 통 문장 
    def concat_silence_sentences(self):
        self.silence_added_text='(침묵)'.join(self.sentences)
        return self.silence_added_text


MAIN_TAG=['NNG','NNP','NP','VV','VA','XR','SL','MAG','MAJ']

class text_analyzer(text_preprocessor):
    imp_words=[]

    # 빈도수 높은 단어
    def frequentword_extract(self, num=5):
      self.imp_words=[]
      tagging=self.kiwi.tokenize(self.total_text)
      for token in tagging:
         if token.tag in MAIN_TAG:
            self.imp_words.append(token.form)
      imp_word_df = pd.DataFrame({'words': self.imp_words, 'count': len(self.imp_words)*[1]})
      imp_word_df = imp_word_df.groupby('words').count()
      tmp=imp_word_df.sort_values('count', ascending=False).head()
      return tmp.index.tolist()
    
    #길이가 긴 문장
    def longsent_extract(self, max_length=60):
      long_sentences=[]
      
      for sentence in self.sentence_arr:
        if len(sentence)>max_length:
          long_sentences.append(sentence)
      # 길이가 긴 문장 갯수, 총 문장 갯수
      return len(self.sentence_arr), len(long_sentences)

    def get_one_text_with_silence(self):
       text_with_silence=self.concat_silence_sentences()
       self.one_text_with_silence=self.sentence_tokenize(text_with_silence)
       return self.one_text_with_silence
    
    
    def keyword_extract(self):
      keywords=[]
      min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
      max_length = 10 # 단어의 최대 길이
      wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)
      beta = 0.85    # PageRank의 decaying factor beta
      max_iter = 10
      keyword, rank, graph = wordrank_extractor.extract(self.sentence_arr, beta, max_iter)
      for word, r in sorted(keyword.items(), key=lambda x:x[1], reverse=True)[:10]:
        keywords.append(word)
      return keywords



"""


text=["갑자기 누가 카메라 안으로 쑥 들어오는 거예요 하오니 하오 이러는 거예요 중국어로 너무 귀찮은 거예요 이렇게 사귀고 있는 건지도 몰랐어요 안녕하세요 윤혜리입니다 오늘은 여러분들이 많이 요청을 해주셨던 Q&A를 가지고 왔어요 제가 조금 더 일찍 찍어보려고 했는데 좀 카메라 앞에서 말하는 게 아직 익숙하지 않다고 해야 되나 아직 프로 유튜버는 아니어서 조금 열심히 준비해보려고 미루고 미루다가 결국에 이렇게 찍게 됐어요 제가 아침부","더 Q&A를 찍겠다고 막 예쁘게 단장도 하고 삼각대도 세우고 이것저것 하다가","이렇게 해서는 뭔가 제 진짜 모습 아닌 것 같","고 너무 카메라 앞에서 얼어있는 제 모습도 싫고 해서 어떻게 하면 좀 자연스럽","편안하게 찍을 수 있을까 생각을 하다가 그냥 제가 평소에 그 이러고 찍는 것처럼 이렇","이렇게 누워서 여러분과 얘기하는 것처럼", "찍어보려고 해요 저를 처음 보시는 분들은 조금 당황스러우실 수","도 있겠지만 이렇", "이렇게 한번 찍어보도록 하겠습니다 제가 새해 이렇게 마이크도","구매를 했습니다 지금 처음으로 사용을 해보고 있어요","제가 사실은 목소리가 굉장히 콤플렉스인데 요즘 여러분들께서 목소리가 너무 좋다 듣기 좋다 편안하다라는 말씀 많이 해주셔서 이렇게 사용해보고 있습니다 어 여러분들이 좋아하시면 앞으로 마이크 사용하는 영상도 많이 가져가 보도록 할게요","저는 2019년 기준 25살이 된 95년생 유네린이고요 유네린","이거는 그냥 유튜브 이름이고 실","자 이름은 혜린이에요 해린","대학은 한국에서 다니고 있고 학과는 미디어커뮤니케이션 학과예요","일단 제 영상에서 나오고 있는 남자친구는 러시아 사람이고 95년생 저랑 동갑이에요","나이 차가 얼마나 나냐고 물어보시는 분들도 있었는데 어 놀랍게도 동갑입니다","저도 그렇게 동안이 아닌데 남자친구는 동안이 확실히 아니어서 어 약간","오해를 받을 때가 있어요 저도 처음 봤을 때 굉장히 오해했고 사실상 동갑입니다 여러분 동갑이에요","저희가 만난 지는 지금 1년이 넘었고","여러분들이 가장 많이 주시는 질문부터 대답을 해볼게요 첫 번째 질문 남자친구랑 어떻게 만나게 됐는지 궁금해요 이 질문을 굉장히 많이 해주셨어요 댓글을 봐도 이거에 대해 물어보시는 분들이 굉장히 많고","이 얘기를 하자면 정말 끝도 없이 떠들어야 될 것 같은데 조금 간추려서 이야기를 해보도록 하겠습니다","아무래도 오늘은 좀 TMI 파티가 될 거 같애요 때는 바야흐로 2000 2010","7년 가을 저는","중국으로 교환학생을 가게 됐어요 제가 간 도시는 상하이라는 도시였는데","놀러 다니고 막 되게 에너지가 넘치고 이런 생활이 전혀 아니었어요 맨날 집에서 공부하고","집에서 혼자 있고 막 이런 생활이 좀 반복이 됐는데 마침 옆","동네에서 함께 교환학생을 하고 있던 같은 과 친구가 있었어요 그 친구가 자기도 상해로 올","테니까 할로윈 파티를 가보자 상해에서 그렇게 말을 하는 거예요 그 당시에 근데 저는 뷰티 쪽에 관심이 좀 많아가지고 집에서 할로윈 메이크업을 좀 찾아봐서 막 연습을 했어요 근데 이건 진짜 대박이다 싶","을 정도로 제가 너무 잘하는 거예요 처음 해본 건데 그래서 이거는 이렇게 할로윈을 그냥 보낼 수 없다 내가","한 학생 온 김에 할로윈 파티","이상한 분장을 하고 한번 가보자 싶어서 그 친구와 이틀 연속으로 할로윈 파티에 가게 됩니다","파크하얏트 호텔인가 그랜드 하얏트 호텔인가 그 상의 야경이 펼쳐지는 그곳에 엄청 높","높은 고층 건물이 있어요 거기 90 몇 층","뮤직바에서 할로윈 파티를 한다는 소문을 들었어요 거기에 코스튬이나 메이", "업을 하고 오면 입장이 무료다 제한이 없다 이런 얘기를 듣고 쿠스","핵춤을 하고 친구랑 막 갔어요 갔는데 정말 고급스러운","그렇게 크지 않은 바에 음악을 뿜뿜뿜뿜 틀어주고 막 너무 멋있","이게 코스튬하고 분장을 한 사람들이 막 되게 막 간지하게 그 칵테일 같은 걸 들고 막 놀고 있는 거예요 근데 그 당시에","칵테일을 사 먹으려고 오빠에 갔는데 너무 비쌌어요","그리고 그렇게 딱히 술이 먹고 싶지 않았어요 저희는 막 놀러 온 게 주 목적이었기 때문에 그래서 친구랑 막 여기저기서 셀카 찍","이러고 놀고 있었어요 사람들은 막 춤을 추고 노는데 저희는","약간 찌질한 그 찌질한 마음 뭐라 해야 되지 찌질 너무 저희가 너무","찌질해서 그냥 찌질한 걸로 할게요 너무 찌질해서","춤도 못 추고 그런데 가본 적","어울리기가 어려워서 그냥 구석에서 막 셀까 찍으면서 막 재밌는 척을 하고 있었어요 술도 안 먹고 네 저희가 저희끼리 셀카 찍는 거는 한계가 있잖아요","어떻게 1시간 동안 저 셀카 100만장 찍고 친구랑 같이","한 100만장 찍고 재미가 없잖아요 그래서 야 그냥 우리 다른 사람들 한","함께 사진 찍자고 해보자 이래서 막 옆", "옆에 있는 코스튬 한 사람한테 우리 같이 사진 찍을래 하고 막 사진을 찍었어요","그중에 막 위키드 분장을 한 마녀분도 있었고","사진을 찍고 있었어요 사진을 저랑 그분이랑 제 친구랑 이렇게 셋이","찍고 있는데 갑자기 누가 카메라 안으로 쑥 들어오는 거예요","하이 이러면서 제가 이렇게 사진 찍고 있으면 옆에서 얼굴이 쑥 이렇게 들어오는 거예요 그래서 어 이게 뭐야 이랬는데 이제 카메라로 저는 보이잖아 이렇게 들고 있으니까","근데 남자애 2명이 카메라 안으로 들어왔","있더라고요 근데 제가 다른 데서도 조금 느꼈지만 외국 애들이 그런 거를 좀 많이 하더라고요 우리는 절대 남이 사진 찍을 때 먹지를 안 끼잖아요 외국 애들은 자연스럽게","들어와서 안녕 막 같이 사진 찍고 막 이래요 그래서 그냥 사진만 찍고 그냥","걔네가 또 사라졌어요 그래서 그 마법사 아저씨한테 막 고마워요 이렇게 하고 우리는 또 우리끼리 놀고 있었어요","그러고서 또 몇 분이 흘렀는데","갑자기 저희 사진을 끼어들었던 남자의 2명이 막 쿵짝쿵짝 두 둔치 두 움치 춤을 추면 봐주 이상한 춤을 추면서 저희한테 막 헤 이러면서 다가오는 거예요","안녕 이러는데 걔가 막 다가오면서 안녕니 하오니 하오 이러는 거예요 중국어로","제가 중국인인 줄 알았던 거죠","근데 보통 이렇게 유럽이나 어디 가서 지나가는 데니 하오 이러면 정말 기분이 나쁠 거란 말이에요 약간","일종의 인종차별 같은 일이잖아요 판단에 따라 다를 수 있지만 근데 상해에서는", "저를 중국인으로 아는 사람이 너무 많았어요 왜냐하면 거긴 중국이니까 저는 중국인처럼 생겼고 그냥 저를 중국인인 줄 아는 거죠 그래서 그때는 그렇게 기분 나쁘진 않았어요 왜냐면 중국인들도 저한테 길 물어볼 정도로 저는 중국 사람으로 오해를 많이 받았으니까 이하오 이러길래 저도 이하오 한실 뭐 부실중거란 이렇게 말했어요","영어로 했나 튼 저는 중국인이 아니라고 얘기를 했어요 그랬더니 걔가 깜짝 놀라면서","어 막 그럼 너는 어느 나라 사람이야 이래서 나는 코리안이야 라고 말을 했죠 그랬는데 너는 뭐하고 있니 상해에서 뭐하고 있니 이런 얘기를 하고 있었어요","근데 걔가 상해에서","중국어를 공부하고 있어라고 하는 거예요","근데 제가 만났던 서양 남자애들은 중국어를 잘 못하는 경우가 굉장히 많았거든요 중국어를 공부하지 않거나 중국어를 공부할 마음이 별로 없","거나 근데 걔가 중국어를 공부하고 있다라고 말하니까 영어를 잘 못", "좀 일단 마음이 조금 열리는 거예요 왜냐하면 제가 영어를 잘 못해도","중국어로 얘기를 할 수 있으니까 그래서 어 나도 중국어 공부하고 있다 그랬는데 걔가 너는 어디 학","학교에서 공부하고 있어 나는 어디 학교에서 공부하고 있어 이런 좀 평범한 진짜 처음 만난 사람들과 하는 대화를 막","나눴어요 그랬더니 걔가 자기는 중얼반에서 공부를 하고 있다는 거예요 중 2반인가 하여튼 중급 1 단계 이쯤에서 공부를 하고 있다는 거예요 근데 저도 그렇거든요 저도 딱","거기서 공부를 하고 있었어요 그래서 막 나도 그렇다 막", "되게 친구 만난 것처럼 왜냐하면","그 반에서 공부하고 있어 나도 비슷해 막 이렇게 얘기하다가 저희가 갑자기 중국어로 대화를 하기 시작했어요 막 지금 생각하면 진짜 오글거리고 별 내용도 아닌데 중국어로 갑자기 얘기를 막 하기 시작했어요 걔가","이제 물어봤어요 너 위챗 있어 해서", "내가 당연히 있지 미에서 이제 중","한국의 카카오톡처럼 중국에 있는 메신저 이름이거든요 어 나도 당연히 있지","얘기를 해서 걔가 그러면 나중에 우리 카페나 레스토랑에 함께 가서 얘기하지 않을래라고 물어보는 거예요","그래서 저는 어떤 생각을 했냐면","저한테 막 만나자고 하는 친구들이 몇 명 있었어요 근데 어떤 친구는","자기 우리 술 마시러 갈래 잘 모르는 사이인데 술 마시러 갈래 이렇게","물어보고 어떤 애는","한 번 만나서 밥을 먹는데 막 엄청 비싼 데를 데려가더니 자기 자랑을 엄청 하는 거예요 자기는 엄마는 어디 교수고 아빠는 어디","어디 대학교수고 자기는 이런 일도 하고 있고 돈 얼마 벌고 막 이러면서 막 혼자","TMI 엄청 썼고 어떤 애는 그냥 정말 친구였는데 갑자기 제 머리카락을","이렇게 만지는데","너무 소름이 돋아서","그 뒤로는 안 만났어요","그래서 막 얘기하고 헤어졌는데 다음날 제 이름도 기억 못하고 막 제가 교환학생이었는지 일하는 사람이었는지도 기억을 못","그다는 거예요 하여튼 그렇게 좀 여러 종류의 사람을 만나다 보니 얘는 조금 괜찮다라는 확신이 들었어요 왜냐하면 일단","나랑 그냥 평범한 대화로 대화를 시작했고","나한테 물어볼 때도 우리 카페나 레스토랑 가자 이렇","이렇게 말하길래 그냥 얘는 평범한 사람이구나 누구나 그렇듯이 약간","이렇게 정석을 밟아가는 그런 친구구나 해서 그런 친구 세길 생각으로 그때는"]
texts=text_analyzer(text)
#print(texts.longsent_extract())
#print(texts.keyword_extract())
print(texts.frequentword_extract())
"""