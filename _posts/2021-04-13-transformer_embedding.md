---

  layout: post
  title:  "대량의 게임 데이터를 임베딩 해보자!"
  date:   2021-04-13 09:43:00
  categories: Works
  author : DANBI
  cover:  "/assets/transformer.jpeg"

---



  ## Introduction

  NCSOFT Data Center에는 대량의 로그 데이터가 쌓여있습니다. 이를 활용해 Data Center의 분석가들은 다양한 주제의 분석 목표를 설정하고 인사이트를 도출하고 모델을 생성합니다. 이렇게 진행되고 있는 프로젝트들의 대부분은 다양한 종류의 로그 데이터 중 유저 행동 로그를 사용하여 주로 진행됩니다. 그렇다면, 많은 분석가들이 사용하는 유저 행동 로그 데이터를 그 특징과 정보를 잘 함축시킬 수 있게 임베딩 해 놓는다면 여러 프로젝트에서 분석하고 모델링하는데 좋지 않을까? 라는 생각에서 이 글은 출발하게 되었습니다.
  기본적으로 로그 데이터는 Sequential Data입니다. 시간에 따라 순차적으로 쌓이는 데이터이죠. 그렇다면 임베딩을 위하여 우선적으로 생각해볼 수 있는건 순차적인 데이터를 처리하는 시계열 분석 방법(ARIMA, 지수평활법) 혹은 RNN/LSTM 기반의 딥러닝 모델들이 있을 것입니다. Sequence Autoencoder도 그 중 하나가 될 수 있겠네요. 하지만 이번 시간에는 대량의 로그 데이터를 사용하다보니 전통적인 통계적 방법론보다는 대량의 데이터를 처리하는데 강점을 가진 딥러닝에 집중해보려 합니다.     

## Why Transformer?

 유저의 행동 로그 데이터를 자세히 살펴보면 정말 다양한 종류(게임 접속, 맵 이동, 아이템 획득, 게임머니 증가/감소 등)가 있습니다. 그렇기에 처음 시도한 방법은 모든 로그 데이터를 사용하기보다는 유저의 지역 이동 (ex) A지역 1층 → A지역 2층 → ...) 로그만을 이용하여 유저별로 임베딩하는 것이었습니다. 임베딩하기 위해서 시도했던 알고리즘은 LSTM 기반의 Seq2Seq-Autoencoder 입니다. Seq2Seq-Autoencoder 를 이용하여 추출한 임베딩 벡터를 사용하여 다른 프로젝트에 적용하였을 때, 기대한만큼의 좋은 성능을 나타냄을 확인할 수 있었습니다. 다만, LSTM 기반의 Seq2Seq-Autoencoder를 사용하니 다음과 같은 문제가 발생하였습니다. 

  

  1. LSTM 기반 모델의 특성상 Layer내에서 GPU를 사용한 병렬 처리가 효율적으로 이루어지지 않다보니, 학습 및 추론 시간이 무척 길어지는 현상이 발생했습니다. 학습에 사용할 사전(Dictionary)의 크기를 조절하여 이런 부분을 개선했지만 지역 이동 로그만 사용하지 않고 다른 종류의 로그들까지 같이 사용할 경우에는 사전의 크기가 매우 커져, 학습 소요 시간이 기하급수적으로 증가할 것으로 예상됩니다. 
  2. 임베딩 벡터(Context Vector)가 고정 길이로 추출되다보니, 임베딩 벡터를 다른 모델에 입력으로 넣는 것은 유용했으나, 역시 입력 차원보다 작은 차원으로 임베딩을 하다보니 정보 손실이 일어나는 부분이 존재했습니다. 대부분의 경우는 비슷한 행동(지역 이동)을 한 유저끼리는 임베딩 벡터간의 거리(Cosine similarity)가 가깝게 나왔으나, 흔히 말하는 작업장 캐릭터와 같은 비슷하거나 이상 행동을 반복하는 부정사용자와 전혀 다른 행동을 하는 일반 유저간의 임베딩 벡터간 거리가 가깝게 나타나는 경우도 발생했습니다. 
  3. 유저의 하루 동안의 로그 데이터는 보통 몇천~몇만개까지 쌓입니다. 우리의 목표는 유저별로 임베딩 데이터를 뽑아내는 것이기 때문에 제대로 유저의 특성이 반영된 벡터를 뽑아내려면 이 로그 데이터를 최대한 많이 사용하는 것이 유리할 수 밖에 없습니다. 물론, 필요없는 로그 데이터의 경우는 삭제를 하거나 도메인 지식에 기반하여 데이터 처리를 진행할 수 있지만 여전히 Input Data의 시퀀스 길이는 매우 길 수 밖에 없습니다. 그러다보니 매우 긴 시퀀스 길이를 입력으로 넣었을 경우 학습/추론 시간도 길어지고, 원하지 않는 방향으로 임베딩 벡터가 추출되기도 하였습니다. 이는 이전 Timestamp들을 참조하는 RNN/LSTM의 문제인 Long-Term-Dependency Problem을 그 원인으로 추측했습니다.   

  

  위의 문제들을 해결할 수 있는 방법으로 시도해본 알고리즘이 Transformer입니다. 현재 딥러닝계에서 가장 핫한 Transformer를 게임 데이터에도 사용해봐야겠죠?  'Attention is all you need' 논문에서 Transformer 구조가 나온 이후 현재 NLP분야에서는 Transformer 구조를 이용한 BERT, XLNET 등의 엄청나게 커다란 모델들이 다양한 Task에서 SOTA를 이루어내고 있습니다. 심지어 Attention Mechanism을 활용한 방법들은 작년부터 이미지/영상인식 쪽에도 사용되기 시작했죠. 그렇기에 우선적으로 생각해본 것이 BERT 구조였습니다. Self-Attention을 이용하여 긴 시퀀스도 잘 처리할 수 있고, LSTM 기반 Seq2seq-Autoencoder보다 정보를 더 잘 저장할 거라고 생각했습니다. 그런데, BERT를 이용하였을 경우에 MLM(Masked - Language Model), NSP(Next Sentence Prediction) 등의 학습 자체는 무척 잘되었으나 모델을 Fine-Tuning하여 다른 downstream Task에 적용하였을때 성능이 기대한만큼 나오지 않았습니다. 또한 Baseline Model로 학습한 LSTM 모델보다 성능 및 학습시간 측면에서도 상대적으로 밀리는 모습을 보여주었습니다. 물론 Downstream Task에서 사용된 모델의 구조나 Input이 이유가 될 수 있겠지만 전체적인 Task에서 성능이 잘 나오지 않았는데, 그 이유를 생각했을 때 아래의 두 가지로 추려볼 수 있었습니다.

   - 사용한 데이터의 Dictionary Size에 비해 모델이 너무 커서, 과적합이 이루어졌다.
   - 게임 유저의 행동 로그는 반복적인 행동을 하는 부분이 많다. 그러다보니, 유저의 행동 로그를 특정 기준으로 나누어 이전 문장의 다음을 예측하는 NSP의 경우는 게임 로그에는 적합하지 않은 방법이다. 

  물론, 위의 두가지 문제를 Input을 바꾸거나 NSP를 사용하지 않는 ALBERT 구조를 이용하는 방법도 있었지만, BERT보다는 조금 더 단순한 모델에 적합하는 것이 성능 측면에서 나을 것이라고 생각을 하였고, 학습/추론 시간이 너무 오래 걸리는 현상도 해결해야했기 때문에 기본적인 Transformer Encoder-Decoder + Autoencoder 구조를 이용해서 임베딩 해보는 방법을 생각하였습니다.

   

## Transformer-Autoencoder

#### 0. Transformer-Autoencoder Architecture



  

<p align="center">
<img src="/assets/works/transformer\image1.png" style="width:10in" />
    <br>
    출처: https://medium.com/platfarm/%EC%96%B4%ED%85%90%EC%85%98-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98%EA%B3%BC-transfomer-self-attention-842498fd3225
 </p>




 위의 그림은 Transformer를 이용하여 'I love you'라는 영어 문장을 '나는 너를 사랑해'로 번역하는 모델입니다. Transformer를 보신 분들이라면 많이 보셨을 그림일 것 같습니다. 사실, 전체적인 형태는 Seq2Seq와 같습니다. encoder에 입력 문장을 넣고 이를 통해 나온 context vector를 이용하여 decoder에서 teacher forcing과 label을 사용하여 학습하는 형태입니다. 여기서 주목할점은 encoder layer를 거쳐서 나온 임베딩 벡터가 각각의 decoder layer로 들어간다는 점입니다. 밑에서 attention score를 구할 때 하나의 score가 나오는 것이 아닌 decoder layer개수만큼 score가 나오는 것은 이 때문입니다. 아, 그리고 저희는 autoencoder로 Transformer 구조를 사용하기 때문에 입력과 출력이 같겠죠?

  

#### 1. Input

  Transformer - Autoencoder 구조의 입력(출력)으로는 Action Code(유저가 어떤 행동을 취했는지) + Context Code(Action Code를 더욱 세분화한 카테고리) + Zone Code(유저가 어떤 지역에서 행동을 했는지) , 이 3가지 Feature를 이용하여 데이터를 생성하고 사전(Dictionary)을 구축하였습니다. 당연히 위에서 시도한, 지역 이동 임베딩 데이터보다는 사전의 크기가 무척 커졌습니다. 지역 이동 데이터만을 사용하여 학습할 수도 있지만, Transformer 모델 크기에 비해 Dictionary의 크기가 상대적으로 작아 다른 Feature들도 같이 사용하면 더 나은 학습 효과를 얻을 것으로 생각했습니다. 이제 이렇게 입력을 넣는다면 각 사용자가 어떤 지역에서 어떤 행동을 하였는지에 대한 순차적인 정보를 내포하는 임베딩 벡터가 추출되겠죠? Feature들의 예시를 살펴보면 다음과 같습니다. 

  

   - Action Code : 게임머니 증가, 게임머니 감소, zone 이동, 로그아웃 등
   - Context Code : NPC상점판매, 혈맹 기부, Portal진입 등
   - Zone Code :  A지역 1층, B지역, C지역 등

  

  Transformer로 들어가는 Input data는 캐릭터별로  'Action Code_Context Code_Zone Code' 로 구성하였습니다.  다음 예시는 이해를 돕기위해 임의로 만들어본 예시입니다. 예를들어 캐릭터 1은 C지역에 있는 NPC상점에서 물건을 판매해 게임머니가 증가하였고 그 후 A지역1층에서 드랍아이템을 획득한 것입니다. 

​          캐릭터 1 =  [''**게임머니증가 _ NPC상점판매 _ C지역** '', **''아이템증가 _ 드랍아이템획득 _ A지역 1층''** ,  ''**아이템증가 _ 드랍아이템획득 _ A지역 2층**'' , ...  ]

​          캐릭터 2 =  [''**게임머니감소 _ 혈맹기부 _ A지역''** , ''**아이템증가 _ 드랍아이템획득 _B지역''** ,  ''**아이템증가 _ 드랍아이템획득 _ A지역 3층''** , ...  ]

  #### 2. Training Time

  Hyperparameter(인코더 레이어 층, Feed-Forward Layer의 Node 개수 등)에 따라 학습 시간은 천차만별이기에, NVIDIA-GPU를 사용하였을 때의 학습 시간 감소효과 정도만 소개하려고 합니다.
  LSTM 기반의 Seq2Seq-Autoencoder의 경우 Only CPU만을 사용하여 학습한 것과  GPU(1개)를 사용하여 학습한 것을 비교하였을 때 학습 시간 감소가 23%정도(Epoch당)밖에 줄어들진 않았지만, Transformer의 경우 1epoch당 Only CPU만 사용했을 경우 40분(Epoch당) 에서 10분(Epoch당)으로 줄어들었습니다. 거의 75%의 감소 효과를 이루어낸 것이죠! 이런 차이가 나타난 이유는 아래 그림을 통해서 설명할 수 있을 것 같습니다. 



​                                                                                                                               

<p align="center">
<img src="/assets/works/transformer\image2.png" style="width:10in" />
    <br>
    출처: https://20chally.tistory.com/222
 </p>









  'Attention is all you need' 논문에서 나온 계산 복잡도 부분을 뽑아왔습니다. 우선 레이어당 총 계산 복잡도는 n < d인 경우 self-attention이 더 적은 계산 복잡도를 가집니다. (그리고 대부분의 경우 n < d 입니다.) 그리고 GPU를 이용한 병렬 계산을 수행하기 위한 sequential operation의 최소수는 rnn만 O(n)의 복잡도를 가집니다. 즉, GPU 사용을 위해 얻을 수 있는 이득은 Self-Attention이 훨씬 큰 것입니다. 추가적으로 NLP Task에서 대부분의 경우 한 문장에서 단어의 개수는 모델의 dimension에 비해 월등히 작기 때문에 엄청난 계산적 이득을 얻는다고 볼 수 있는 것입니다. (여담으로, 필자는 Transformer 구조를 구현한데 있어서는 Tensorflow 보다는 Pytorch를 더 권장합니다. NLP에서 활용되는 모델들(Transformer, BERT, XLNET 등)은 아무래도 Huggingface처럼 대부분 Pytorch로 구현이 되어있는 라이브러리가 많다보니 학습하는데 있어 정신 건강에 이롭습니다. 더욱이 GPU는 잘 사용하길 바랍니다. 1개만 사용하지 말고 Multi-Gpu로 텐서 분산처리를 꼭 활용하시길.. 안 그렇다면 학습이 너무 오래 걸려 일 못하는 직원이 될 수도 있습니다... )

#### 3. 학습결과

  Transformer - Autoencoder는 비지도 학습이다보니 어떻게 성능을 평가할지에 대해서는 고민이 좀 더 필요합니다. 물론 다른 Downstream Task 모델의 Input으로 넣어 정확도나 F1-Score 등을 계산할 수는 있지만 이는 Task의 목적이나 모델의 구조에 따라 다르기 때문에 좀 더 정성적으로 평가할 수 있는 기준이 있으면 좋을 것 같습니다. 학습이 잘 되었는지를 확인하기 위해 Test Data에 대해서는 두가지 방법을 적용하였습니다.

   1. input을 넣었을때, context vector가 output을 얼마나 input에 가깝게 잘 생성해내는지
   2. Encoder - Decoder 간 attention score를 확인 (Autoencoder output의 sequence는 input과 동일하기 때문에 시퀀스 내 특정 위치의 데이터는 자기자신을 많이 참조할 것으로 추측하였습니다)

 Attention Score에 대해서 설명을 조금 더 직관적으로 돕기 위해, Pytorch로 구현한 번역 모델의 attention score 시각화 결과를 확인해보면 이해가 조금 더 편할 것입니다. 다음은 https://nlpinkorean.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/ 블로그에서 참조한 잘 학습된 번역 모델의 Attention Score 그림 예시입니다. 이 경우 입력은 영어 문장, 출력은 영어 문장을 번역한 불어 문장입니다. (이 경우에는 seq2seq 구조에 attention을 붙인 모델이지만 encoder - decoder 간의 attention score 계산 과정이나 결과 그래프 해석은 동일합니다)



<p align="center">
<img src="/assets/works/transformer\image3.png" style="width:10in" />
    <br>
    출처 : https://nlpinkorean.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/

 </p>




  흰색에 가까울수록 Attention Score가 높은 것입니다. 위 그림에서 볼 수 있듯이, output의 단어가 많이 집중(Attention)하는 부분은 같은 뜻을 가진 단어에 해당하는 부분을 많이 참조(높은 Attention Score)하는 것을 확인할 수 있습니다. 예를 들면 모델이 “European Economic Area”를 출력할 때 모델이 어떤 단어를 Attention(주의) 하고 있는지를 확인해보면 “européenne économique zone” 을 거꾸로 참조하는 것을 확인할 수 있습니다. 영어와는 달리 불어에서는 이 단어들의 순서가 반대이기 때문입니다. 이 외의 단어 순서는 입력/출력 모두 순서가 같다보니 Attention Score가 대각선 계단 형태(downward staircae) 로 나타납니다. 행동 로그를 이용해 Transformer 구조로 넣는 Input Data는 시퀀스 순서가 Input과 Output간 동일하니 위 그림과 비슷하게 대각선 계단 형태의 그래프가 나올 것으로 기대하였습니다.

  

<p align="center">
<img src="/assets/works/transformer\image4.png" style="width:10in" />
    </p>


 

 먼저, 사용한 모델의 구조와 함께 Test Data를 Input으로 넣었을 때, Output이 어떻게 나오는지를 확인하였습니다. (Output의 경우 <eos> 토큰이 나올때까지 반복적으로 예측을 합니다. ) 다행히도 Input과 output이 거의 동일하게 나오는 것을 확인할 수 있었습니다. 실제로 Test Data 셋 중 90% 이상의 경우 Input과 Output이 동일하게 나오는 것을 확인할 수 있었습니다. 지면 관계상, 다양한 경우를 보여 드리진 못하지만 대부분의 Test Data 셋에서 Context Vector가 입력 시퀀스를 다시 잘 생성해내는 것을 확인할 수 있다고 말씀드릴 수 있습니다. 



<p align="center">
<img src="/assets/works/transformer\image5.png" style="width:10in" />
    </p>


 

​    위의 두 그래프는 Test data를 모델에 넣었을 때, attention score 를 시각화한 결과입니다. x축은 test data의 sequence(130개)를 나타내고, y축은 test data로 encoding한 후 decoding한 문장 Sequence(131개 - <sos> 토큰까지) 결과입니다. (위의 번역 모델의 그래프와는 축이 반대입니다) 그리고 입출력간의 attention score를 위의 번역 모델처럼 그래프로 나타내 보았습니다. 위에서 설명했듯이, decoder layer 여러 개에 embedding vector를 넣었기 때문에 각각의 decoder layer마다 attention score가 나옴을 확인할 수 있습니다. 첫번째 그래프는 첫번째 decoder layer의 attention score, 두번째 그래프는 두번째 decoder layer의 attention score를 나타냅니다. 아무래도 decoder layer를 한번 더 거칠수록 attention score가 더욱 잘 나오는 것도 확인할 수 있었고 두 경우 모두 기대한대로 계단 모양(downward staircase)의 attention score를 보여주었습니다. 



  ## Downstream Task (Bad User Detection System)

   이와 같이 학습이 완료되었다면 Donwstream Task에 적용해볼 수 있을 것입니다. 이 중 NCSOFT에서 진행하는 '부정사용자탐지' 프로젝트에 모델을 적용시켜보려합니다. 부정사용자란 NCSOFT 게임에 존재하는 불법프로그램 사용자, 작업장 등 게임의 정책 및 경제에 악영향을 주는 유저들을 지칭합니다. 이는 게임 운영에 있어서 중요한 문제를 야기하는 요소들이며 이를 제재하고 탐지하기 위해서 다양한 방법들을 적용하고 있습니다. 물론, 부정사용자탐지는 앞선 'Snorkel을 이용한 Label 보정' 글에서도 알 수 있듯이 Weak Supervision 개념이나 여러 모델들의 앙상블, 다양한 데이터 전처리를 통해 진행하는 매우 복잡한 프로젝트이지만, 여기서는 임베딩 벡터를 추출한 결과가 어느 정도로 일반 사용자와 부정사용자를 구분해냈는지만을 확인해보고 이를 고도화한다면 프로젝트에 기여할 수 있을지 정도를 확인해보았습니다.  
  부정사용자도 다양한 행동을 하지만 특정 패턴들이 존재하는 경우가 많습니다. 여러 아이디에 있는 게임머니를 한 아이디로 몰아준다거나, 특정 Zone에서 특정 행동을 반복하는 것을 그 예로 들 수 있을 것 같습니다. 이러한 행동 패턴들은 일반사용자는 하지 않을 행동들이며 행동 로그 데이터에서 그 차이를 확인할 수 있습니다. 그렇기에 이런 행동 로그를 이용해 학습한 Transformer 모델은 부정사용자와 일반사용자간의 임베딩 벡터간 유사도가 적게 나타날 것입니다.  
  현재 Transformer - Autoencoder로 만든 모델에서 추출된 유저별(캐릭터별) 임베딩 벡터를 Input으로 사용하고 이진분류 딥러닝 모델을 이용하여 Task에 적용해보았습니다. (NCSOFT 운영정책상으로 실제 제재된 캐릭터들과 그렇지 않은 일반사용자를 대상으로 데이터를 추출하였습니다) 아래는 Baseline Model로 사용한 Seq2Seq(LSTM) Autoencoder 와 성능을 비교한 Confusion Matrix 입니다. Baseline Model과 학습데이터 및 Downstream Task Model 구조등은 동일하게 맞추었습니다. 아직 모델을 더 고도화하고 하이퍼파라미터를 조절하는 등의 연구가 진행되어야 하지만 Transformer 구조가 좋은 결과를 보여주는 것 같습니다.



#### Seq2Seq(LSTM) Autoencoder의 임베딩 벡터를 이용한 이진 분류 

   

|                     | 예측 부정사용자      | 예측 일반 사용자     |
| ------------------- | -------------------- | -------------------- |
| 실제 **부정사용자** | 2143 (True Positive) | 404 (False Negative) |
| 실제 **일반사용자** | 620 (False Positive) | 2957 (True Negative) |



  - f-1 score : 0.807
  - precision : 0.776
  - recall : 0.841



#### Transformer - Autoencoder의 임베딩 벡터를 이용한 이진 분류 

|                     | 예측 부정사용자      | 예측 일반 사용자     |
| ------------------- | -------------------- | -------------------- |
| 실제 **부정사용자** | 2320 (True Positive) | 227 (False Negative) |
| 실제 **일반사용자** | 156 (False Positive) | 3421 (True Negative) |

  - f-1 score : 0.924
  - precision : 0.937
  - recall : 0.911

  

  ## 마치며

  지금까지 Transformer를 이용한 대량의 로그 데이터 임베딩을 소개 해드렸습니다. 생각보다 학습에서 만족스러운 Attention Score나 학습 결과가 나왔지만 아직 고려해야할 점이 많이 있습니다.

   1.  게임 데이터의 특성상 업데이트가 진행되어 새로운 zone이나 새로운 로그들이 추가된다면 이를 OOV(Out-Of-Vocabulary)로 처리하기보다는 새로 재학습을 진행해야 모델이 계속해서 좋은 성능을 보여줄 것입니다.
   2.  현재는 도메인 지식에 기반하여 사용할 로그/사용하지 않을 로그들을 구분하였지만 더 나은 로그 데이터 처리 방식에 대한 고민이 이루어져야 할 것입니다. 
   3. Action Code / Context Code/ Zone Code 3가지만을 이용해서 유저의 행동 로그를 임베딩하였지만 유저는 정말 다양한 행동들을 합니다. 그렇기에 더 많은 Feature를 사용한다면 더 좋은 임베딩 결과가 나오겠지만 Feature를 많이 사용할수록 모델의 성능과 trade off 관계에 있기 때문에 이를 잘 조율해 볼 연구가 더 진행되어야 할 것입니다.

  GPU 분산 병렬 처리도 더 진행해야할 부분입니다. 대용량의 데이터를 처리하다보니 Training/Inference Time이 많이 소요되어 GPU 사용은 필수이고, 이를 어떻게 분산 처리를 잘! 할지가 참 중요한 부분입니다. 메인 GPU 메모리 이슈, Tensor를 어떻게 분배할지 등 고려할 요소는 정말 많은 듯 합니다. 

  


  ## 참고 자료

  - https://arxiv.org/abs/1706.03762
  - https://nlpinkorean.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/
  - [https://20chally.tistory.com/222](https://arxiv.org/abs/1703.00854)
  - [https://medium.com/platfarm/%EC%96%B4%ED%85%90%EC%85%98-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98%EA%B3%BC-transfomer-self-attention-842498fd3225](http://ai.stanford.edu/blog/weak-supervision/)
  - [https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html](https://github.com/snorkel-team/snorkel)