---
layout: post
title: "회귀분석에서 로그변환 시 계수 해석"
date: 2018-08-07 15:00:00
categories: Study
author : DANBI
cover: "/assets/statistics.jpg"
---

# 들어가며

회귀분석을 하다보면 여러가지 이유로 변환(transformation)을 하게 된다. 가장 흔하게 하는 변형은 log 변형이다. 회귀분석의 좌변(종속변수)와 우변(독립변수)를 각기 log로 변환한다고 하면, 변환 유무에 따라서 네 가지 조합이 가능하다. 

|  |level  | log |
|--|--|--|
|__level__|$$y_i = \alpha + \beta x_i + \varepsilon_i$$|$$y_i = \alpha + \beta \log x_i + \varepsilon_i$$|
|__log__|$$\log y_i = \alpha + \beta x_i + \varepsilon_i$$|$$\log y_i = \alpha + \beta \log x_i + \varepsilon_i$$|

level-level의 조합에서 $$\beta$$는 $$x$$의 한 단위 변화에 대한 $$y$$의 변화 단위를 측정한다. 이하에서는 오해의 소지가 없는 이상 $$i$$ 인덱스 와 $$\varepsilon_i$$은 생략하도록 하자. 

# log-level model 

살짝 복잡하지만 log-level 모형부터 시작해보자. 계산 과정을 이해하는 데 도움이 된다. 

$$\log y = \alpha + \beta x$$

* $$y$$에 붙은 로그를 제거한다. $$y = e^{\alpha + \beta x}$$ 
* $$x$$가 $$\Delta x$$ 만큼 변하면 그에 상응하여 $$y$$가 $$\Delta y$$ 만큼 변한다고 하자. 
   $$y + \Delta y = e^{\alpha + \beta (x + \Delta x)} = e^{\alpha + \beta x} e^{\beta \Delta x}= y (e^{\beta \Delta x})$$
*  양변을 $$y$$로 나눈다. $$\frac{y + \Delta y}{y} =  1 + \frac{\Delta y}{y} = e^{\beta \Delta x}$$
 * 종속변수에 log를 취했다면 $$x$$의 $$\Delta x$$ 증가에 대한 $$y$$의 % 변화율은 위와 같이 측정할 수 있다. 
   $$100 \times \frac{\Delta y}{y} = (e^{\beta \Delta x} -1) \times 100$$

* 근사치로 해석해보자. $$\beta \Delta x$$ 값이 크지 않다면 (대략 0.1이하), $$e^{\beta \Delta x} \approx 1 + \beta \Delta x$$에 따라서 대략 $$(\beta \Delta x \times 100)$$ % 변화로 간주해도 무방하다. 

* 같은 취지로 식의 양변을 편미분해서 동일한 결과를 도출할 수 있다.  
$$\dfrac{d{\,}y / d{\,}x }{y} = \dfrac{d{\,}y / y }{d{\,}x} = \beta$$
*  $$\dfrac{d{\,}y / y }{d{\,}x}$$는 $$x$$가 몹시 미세하게(infinitesimal) 변화할 때 $$d{\,}y / y$$의 '순간'(instantaneous) 변화비율을 나타낸다. 만일 이를 %로 표시하고 싶다면, $$\beta \times 100$$이 된다. 

# level-log model 

$$y = \alpha + \beta \log x$$

* 앞서와 마찬가지로 $$\Delta x$$, $$\Delta y$$를 적어보자.  
  $$y + \Delta y = \alpha + \beta \log (x + \Delta x)$$ $$\Delta y = \beta \log (1+\frac{\Delta x}{x})$$
* 정확한 $$\beta$$ 값은 위와 같이 구할 수 있다. 
* 만일 $$\frac{\Delta x}{x}$$의 값이 작다면, $$\log(1+\frac{\Delta x}{x}) \approx \frac{\Delta x}{x}$$를 사용할 수 있다. $$\frac{\Delta x}{x}$$를 %로 표현하고 싶다면 100을 곱하면 된다. 이렇게 되면, 
$$\Delta y \approx \frac{\beta}{100} (100 \times \Delta x / x)$$
* 같은 결과를 편미분을 통해 도출할 수 있다. 양변을 $$x$$에 대해서 미분하면 
 $$dy = \beta \dfrac{dx}{x}$$ 

# log-log model 

$$\log y = \alpha + \beta \log x$$

정확한 변화를 계산하는 것은 위의 두 과정을 합친 것과 비슷하니 각자 연습해보기 바란다! 혹시 어렵다면 아래 부록을 참고하기 바란다. 이 문제도 역시 편미분으로 접근하면 조금 이해가 쉽다. 모델에서 $$\beta$$는 $$\log y$$를 $$\log x$$에 대해서 편미분한 값과 같다. 즉,  
$$\beta = \dfrac{d{\,}{\log y}}{d{\,}\log x}  = \dfrac{(dy / y) \times 100}{(dx / x) \times 100}$$

이때  $$\beta$$는 $$x$$의 미세한 % 변화율에 대한 $$y$$의 % 변화율을 측정한다. 둘 다 % 변화로 표현되었기 때문에 단위에서 자유롭다. 경제학에서 흔히 "순간 탄력성"이라고 부르는 값이다. 즉, 가격 미세한 $$x$$ % 변화에 대한 수요의 변화율을 측정한다. 경제학에서 log-log 변환이 유달리 많이 사용되는 이유는 이렇듯 경제적인 해석이 쉽기 때문이다.

# 주의 사항 

변환을 이용하면 비선형적인 함수 관계를 선형으로 바꿔 다룰 수 있다. 그 대신 계수 해석에서는 몹시 조심해야 한다. 우선, %로 간편하게 근사치로 해석을 하려면 각 변화량이 크면 안된다. 근사치의 오차가 너무 큰 상황에서 근사치를 쓰면 안되는 것이다. 특히 주의해야 할 것이 더미변수다. 만일 설명 변수에 더미 변수가 들어 있고, 종속 변수가 로그 변환되어 있다면, 계수 값을 그대로 log-level 모델에 따라서 $$100 \times \beta$$로 해석하면 곤란하다. 더미 변수는 질적 변수이고, 변수의 차이는 측정할 수 없다. 이 경우는 $$e^{\beta} -1$$을 변화율로 따져야 한다. 

## 사례 

### log-level 모형에서 더미 변수 해석 

$$\log(\text{write}) = \beta_0 + \beta_1 * \text{female} + \beta_2 * \text{read} + \beta_3 * \text{math} $$

![](/assets/study/logwithlevel/reg_0.PNG)

이 회귀분석은 분석 대상이 된 표본 학생들의 쓰기 점수를 성별, 읽기 점수 그리고 수학 점수로 회귀한 결과이다. female 계수(1이면 여성, 0이면 남성)는 어떻게 해석해야 할까? 앞서 보았듯 더미 변수는 질적인 변수다. 따라서 계수에 100을 곱해 여자 성별이 11.4% 더 높은 점수를 준다고 해석해서는 곤란하다. $$e^{0.114718} = 1.12$$의 결과에 따라서 약 12% 정도 더 높은 점수를 준다고 보는 것이 맞다. 다른 계수들은 어떨까? 다른 변수은 모두 연속 함수이고 계수 값들이 크지 않음을 알 수 있다. 따라서 근사 값로 해석하는 것이 가능하다. 즉, 읽기 점수가 1% 증가하면 글쓰기 점수는 약 0.66% 정도 증가한다. 

### level-log  모형에서 변수 해석 

$$\text{write} = \beta_0 + \beta_1 * \text{female} + \beta_2 * \log \text{read} + \beta_3 * \log \text{math} $$

![](/assets/study/logwithlevel/reg_1.PNG)

$$\log \text{read}$$의 계수는 어떻게 해석해야 할까? read 값은 연속 값이므로 1%의 작은 값을 취하는 것이 가능하다. 따라서 근사 값으로 해석해도 무방하다. 앞서 보았 듯 read 값의 1% 증가는 $$\beta * 0.01$$ %의 효과를 종속 변수에 준다. 즉, 약 0.17% 증가를 초래한다. 물론 정확하게 계산하면 0.161%가 나올 테지만, 소수점 자리를 생각할 때 오차는 무시할 만 하다. 

### log-log  모형에서 변수 해석 

$$\log \text{write} = \beta_0 + \beta_1 * \text{female} + \beta_2 * \log \text{math} +\beta_3 *\text{read} $$

![](/assets/study/logwithlevel/reg_2.PNG)

$$\beta_2$$는 어떻게 해석해야 할까? 근사 값로 해석하면 된다. 수학 점수 1% 상승은 쓰기 점수 0,4% 상승을 가져온다. 

## (부록) log-log 계산 

$$
\begin{aligned}
y + \Delta y & = e^{\alpha + \beta (\log x + \Delta x)} \\
1 + \frac{\Delta y}{y} & = e^{\beta (1 + \frac{\Delta x}{x})}
\end{aligned}
$$

양변에 로그를 취하면, 

$$\log (1+\frac{\Delta y}{y} ) = \beta \log (1+\frac{\Delta x}{x})$$

만일 $$\frac{\Delta y}{y}$$, $$\frac{\Delta x}{x}$$가 충분히 작다면, 
$$\frac{\Delta y}{y}  \approx \beta \frac{\Delta x}{x}$$

# Reference 

* [http://kenbenoit.net/assets/courses/ME104/logmodels2.pdf](http://kenbenoit.net/assets/courses/ME104/logmodels2.pdf)
* [UCLA 대학 통계센터](https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faqhow-do-i-interpret-a-regression-model-when-some-variables-are-log-transformed)

