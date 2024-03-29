---
layout: post
title:  "데이터 분석을 이용한 게임 고객 모델링 #3"
date:   2018-06-28 12:00:00
categories: Works
author : DANBI
cover:  "/assets/works/game_user_segmentation/user_segmentation.png"
---

2편에서 예고했듯이 이번 편에서는 ‘사회 연결망 분석(Social network analysis)’을 통해 고객의 특성을 파악하는 방법에 대해 소개해 드리겠습니다.

사회 연결망 분석을 위해선 먼저 게임 고객 간의 관계를 ‘연결망(보통 네트워크라는 말을 더 많이 사용)’이라고 부르는 구조로 만들어야 합니다. 연결망(혹은 네트워크)은 말 그대로 여러 개의 개체(보통 ‘노드’라고 함)들을 연결한 것을 말하는데요, 예를 들어 인터넷 네트워크는 여러 기기들이 인터넷을 통해 연결된 구조를 의미합니다. 마찬가지로 사회 연결망(혹은 소셜 네트워크)은 사람들이 사회적 관계를 통해 연결된 구조이죠.

온라인 게임에서 게임 고객들은 다양한 사회적 관계를 갖게 됩니다. 친구가 되거나 같은 혈맹에 소속되는 것처럼 현실과 유사한 사회적 관계를 맺기도 하고, 같이 파티를 맺고 인던을 돌거나 혹은 서로 아이템을 주고 받는 것과 같은 다양한 상호 작용을 하기도 합니다. 그래서 이런 관계나 게임 활동을 이용하면 게임 고객 네트워크를만들 수 있습니다.

보통 네트워크 분석을 할 때는 네트워크 구조를 우리가 수학 시간에 배우는 ‘행렬’로 표현합니다. 가령 네 명의 사람이 아래와 같이 연결되어 있다면 이들을 행과 열에 놓고 두 사람 사이가 연결되어 있으면 1, 아니면 0으로 표시하는 것이죠.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_1.png" style="width:5in" />
네트워크 구조를 행렬로 표현한 예
</p>


얼핏 생각하기엔 그냥 그림으로 그리면 될 것을 왜 이렇게 머리 아프게 행렬로 표시하나 싶지만 여러 가지 복잡한 계산을 하거나 혹은 분석에 필요한 계산을 컴퓨터가 자동으로 처리하도록 프로그래밍할 때는 이렇게 행렬을 이용하는 것이 편하답니다.

하지만 역시 저같은 일반인들에게는 숫자보다는 그림이 더 보기 좋고 직관적이기 때문에 보통 네트워크는 그림으로 많이 표현됩니다. 예를 들어 아래 그림은 인터넷 네트워크를 시각화한 것입니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_2.png" style="width:6in" />
인터넷 네트워크 (이미지 출처:https://en.wikipedia.org/wiki/Internet_backbone)
</p>

뭔지 모르지만 아무튼 멋지죠? 그런데 이와 비슷하게 온라인 게임에서도 게임 고객간의 네트워크를 시각화할 수 있습니다. 아래 그림은 저희 회사 모 게임에서 고객 간에 서로 아이템을 주고 받는 관계를 네트워크로 시각화한 것입니다. 비록 그리는 방식에 약간의 차이는 있지만 자세히 보면 이 둘은 구조 상 매우 유사하답니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_3.png" style="width:6in" />
게임 유저 네트워크 시각화 예
</p>

한편 보통 네트워크는 여러 개의 작은 집단으로 나눌 수 있습니다. 가령 위 그림에서는 각기 다른 색깔로 구분된 수백 개의 소집단으로 구분될 수 있죠. 이런 소집단들은 같은 집단에 속한 노드 간의 연결선이 외부 노드와의 연결선에 비해 상대적으로 밀도가 높게 구성되는데 이런 여러 개의 소집단들이 모여서 전체 네트워크를 이루게 되죠. 이런 소규모 집단들을 ‘커뮤니티’라고 부릅니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_4.png" style="width:6in" />
이 네트워크의 경우 세 개의 커뮤니티로 나눌 수 있죠
</p>

각각의 ‘커뮤니티’들은 저마다 다양한 네트워크 구조를 갖고 있습니다. 예를 들어 우리 회사 게임 고객 네트워크를 보면 아래와 같은 다양한 커뮤니티 구조를 발견할 수 있습니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_5.png" style="width:6in" />
다양한 구조의 게임 유저 커뮤니티
</p>


따라서 유저들을 유사한 행동 패턴끼리 군집화하듯이 커뮤니티 역시 비슷한 네트워크 구조를 갖는 커뮤니티끼리 군집화할 수 있습니다.

이 때 군집화를 위해 커뮤니티 구조 간의 유사도를 측정하려면 우선 각 커뮤니티 구조를 나타내는 적절한 값을 구해야 합니다. 이를 위해 사용하는 여러 가지 네트워크 지표가 있는데 일일이 다 설명하기에는 지면이 부족하니 대표적인 것 몇 가지만 소개하면 다음과 같습니다.

### **Degree**

Degree는 네트워크 상의 어떤 노드가 몇 개의 노드와 연결되어 있는지를 나타내는 값입니다. 즉, 노드에 연결된 선의 개수죠. 이 때 개별 노드의 degree를 구하고 난 후 커뮤니티 별로 노드들의 degree 평균이나 표준 편차를 구하면 각 커뮤니티 구조의 차이를 아는데 도움이 됩니다.

또한 서로 비슷한 degree를 갖는 노드끼리 연결되었느냐 차이가 큰 노드끼리 연결되었느냐를 측정하는 지표로 degree assortativity(동질성)라는 것이 있습니다. 아래 그림에서 왼쪽 커뮤니티는 비슷한 degree를 갖는 개체끼리만 연결되었기 때문에 이 수치가 높은 반면, 오른쪽 커뮤니티는 반대로 매우 낮은 값을 갖습니다. 그래서 이 지표 역시 네트워크 구조를 파악하는데 도움이 되는 정보입니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_6.png" style="width:6in" />
Degree assortativity가 큰 커뮤니티(왼쪽)와 작은 커뮤니티(오른쪽)의 예
</p>


### **Radius**

우리말로 하면 반경인데요, 쉽게 말해 커뮤니티 내에서 가장 멀리 떨어진 개체 사이의 거리를 의미합니다. 이것 역시 네트워크 구조를 파악하는데 많이 사용하는 지표입니다.


<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_7.png" style="width:6in" />
Radius가 큰 커뮤니티(왼쪽)와 작은 커뮤니티(오른쪽)의 예
</p>


각 커뮤니티마다 이런 다양한 지표를 구한 후 커뮤니티에 대한 군집화를 수행하면 마치 탄소 분자간의 얽힘 구조를 보고 다이아몬드와 석탄을 구분하듯이 전체 네트워크에서 비슷한 구조를 갖는 커뮤니티끼리 분류할 수 있습니다. 아래 그림은 다양한 네트워크 지표를 기반으로 군집화 알고리즘을 사용해 게임 고객 네트워크를 다섯 가지 유형의 커뮤니티로 분류한 것입니다.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_8.png" style="width:6in" />
네트워크 구조를 기준으로 커뮤니티들을 다섯 가지 유형으로 군집화한 예
</p>


이렇게 분류를 하면 설령 행동 패턴만 볼 때는 동일한 유형의 게임 고객처럼 보이더라도 어떤 커뮤니티 유형에 속해 있는지에 따라 다르게 관리할 수도 있고 혹은 고객 관리 자체를 커뮤니티 단위로 할 수도 있겠죠.

더 나아가 네트워크 구조를 잘 파악하면 개체의 특성만 보고는 알 수 없는 독특한 패턴을 발견할 수 있습니다. 가령 범죄자들은 자신의 정체를 숨기기 위해 일반인 코스프레를 하기 때문에 개체의 특성만 분석해서는 정체를 파악하기 쉽지 않은 반면, 네트워크 구조는 여러 노드를 제어해야 하기 때문에 일반인들의 자연스런 관계 구조를 흉내내기가 상대적으로 어렵죠. 따라서 보험 사기나 주식 작전 세력, 악성코드에 감염된 좀비 PC 등을 탐지할 때 이런 네트워크 분석 기법을 많이 활용하고 있습니다.

저희 회사도 악성 유저를 탐지할 때 이런 기법을 활용하곤 합니다. 예를 들어 아래 커뮤니티의 경우 각 캐릭터들의 게임 활동만 보면 일반 고객과 큰 차이점이 없지만 캐릭터 간의 관계 구조를 시각화하면 이렇게 매우 규칙적이고 인위적인 구조가 나타납니다. 그래서 이런 정보가 큰 도움이 되죠.

<p align="center">
<img src="/assets/works/game_user_segmentation/image_3_9.png" style="width:6in" />
이것은 사람이 아니므니다...
</p>


비록 여기서는 고객 커뮤니티를 군집화하기 위해 네트워크 구조를 파악하는 방법만을 살펴 봤지만 실제로는 이 외에도 매우 다양한 네트워크 분석 기법이 있으며 여러 분야에서 폭넓게 활용되고 있답니다.

지금까지 세 편에 걸쳐 게임 고객을 모델링하기 위해 사용하는 데이터 분석 기법들을 소개해 드렸는데 잘 따라오셨나요? 그럼 마지막으로 다음 편에서는 앞서 설명한 세 가지 기법을 실전에서 어떻게 적용할 수 있는지 소개하면서 그 동안 정신 없이 달려오느라 미처 다루지 못했던 내용들을 FAQ 형식으로 정리하는 시간을 갖겠습니다.