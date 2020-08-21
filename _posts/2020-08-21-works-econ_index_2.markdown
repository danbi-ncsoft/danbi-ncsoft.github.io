---
layout: post
title:  "R Markdown을 활용한 Interactive Report 만들기"
date:   2020-08-21 11:47:25
categories: Works
author : DANBI
cover:  "/assets/works/econ_index/title2.png"
---



## 작업의 배경

지난 포스팅 [게임 속 시장을 들여다보기 위한 단 하나의 지표]( https://danbi-ncsoft.github.io/works/2020/08/13/works-econ_index_1.html) 에서는 게임 내 거래의 활성화 정도를 살펴보는 거래 종합 지표의 개발 과정을 소개했다. 앞선 글에서 소개했던 종합 지표를 접하면 대부분의 사람들은 추가적인 정보에 대한 궁금증을 가질 것이다. 지난 기간 대비 지표가 얼마나 증감했는지, 세부적으로 어떤 활동의 변동이 전체 지수의 변동에 영향을 미쳤는지, AU 나 매출 등의 다른 지표와는 어떤 관계를 갖는지 등. 심지어 같은 자료를 보더라도 구체적으로 어떤 추가 정보를 알고 싶은지는 사람마다 차이가 있을 것이다. 예를 들어 지난 기간 대비 종합 지수가 감소했다면, 규모, 빈도 등 어떤 측면에서의 감소가 종합 지수의 감소로 이어졌는지 궁금한 사람이 있을 수도 있고, 전체적으로는 지수가 떨어졌음에도 불구하고 반대로 지수가 증가한 서버가 있는지, 혹은 유독 많이 떨어진 서버가 있는지를 궁금해할 수도 있을 것이다. 경우에 따라서는 특정 수치 기준 상위 n개 서버에 대한 정보가 필요하거나, 원 데이터를 제공받아 직접 분석을 원할 수도 있다. 이처럼 사용자들의 다양한 니즈를 모두 충족시킬 수 있도록 많은 정보를 깔끔하게 전달할 수는 없을까?

(대부분의 회사들이 비슷하겠지만) 우리 회사 데이터 조직에서는 웹 기반의 BI 서비스를 제공하고 있어서 이를 통해 수백 가지가 넘는 다양한 지표들을 조회할 수 있다. 하지만 모든 분석 결과를 BI 서비스를 통해 제공하는 것은 자칫 개발 및 유지 보수에 큰 부담을 줄 수 있다. 그래서 단기적으로 필요한 자료이거나 혹은 이번처럼 시범적인 지표들의 경우 분석가가 직접 보고서 형태로 만들어 제공한다. 그러나 일반적인 형태의 정적 보고서는 위에서 언급했던 다양한 사용자 요구를 충족시키기 어렵다. 그래서 이 글에서는 R markdown을 활용하여 웹 기반 BI 서비스 부럽지 않게 상호작용이 가능한 형태의 보고서를 만드는 과정을 소개해보고자 한다.



## R Markdown 시작하기

적절한 시각화는 데이터가 품고 있는 인사이트를 훨씬 수월하게 찾을 수 있도록 도와준다. 그리고 차트에 대한 필터링이나 정렬 등의 인터랙티브 기능은 사용자로 하여금 데이터 탐색을 훨씬 용이하게 한다. 사용자가 보고서를 동적으로 활용하면서 앞서 말한 궁금증을 직접 해결한다면 더욱 풍부한 인사이트가 도출되고 의사 결정에도 효과적일 것 것이다. 

R에서는 Markdown을 활용하여 HTML 형식의 보고서를 만들면 이것이 가능하다. Markdown이란 텍스트 기반의 마크업 언어로써 쉽고 간편하게 문서 작성을 할 수 있다는 것이 특징이다. R을 사용하는 경우 R Studio에서 Rmd 형식의 파일로 Markdown을 작성하면 HTML로 내보낼 수 있다. R Studio에서는 간단한 Markdown 예제 코드를 제공한다. File -> New File -> R Markdown에서 Document를 선택하고 Output Format을 HTML로 정하면 문서를 작성해 HTML로 내보낼 수 있도록 예제 코드가 쓰인 새로운 스크립트가 생성된다. 구성은 간단하다. 가장 위에는 문서의 제목이나 저자 등을 명시하는 부분이 있고, 코드는 **```** 로 구분이 되어 있다. 단락 제목은 #의 개수로 크기를 조절해서 쓰고, 설명은 그냥 입력하면 된다. 마지막으로 작성 후 HTML 파일로 내보낼 때에는 스크립트 상단의 knit를 클릭하기만 하면 된다. 전체적인 구성은 이것이 전부이다.

<p align="center">
<img src="/assets/works/econ_index/figure6.png"/>
[그림 1] R Markdown 시작하기
</p>



## Interactive Chart 그리기

동적인 차트를 통해 사용자는 원하는 데이터만 필터링하거나 마우스 오버 시 상세 수치를 보이게 하는 툴팁을 사용해 즉각적으로 정확한 데이터를 볼 수 있다. 그래프를 그리기 전에 먼저 살펴볼 것은 결과물인 그림만 보이고 코드는 숨기도록 하는 명령어이다. 이는 예제 코드에도 나와있는데, 보고서에 코드를 보이고 싶어하는 사람은 없을 테니 `echo=FALSE`를 활용해 코드를 숨기면 된다. 이때, 그래프를 그리는 과정에서 간혹 경고 메시지가 뜨는 경우가 있는데, 이러한 시스템 메시지들은 위 명령어를 활용해 코드를 숨겨도 보고서 상에서 보이기 때문에 `error=FALSE`와 `warning=FALSE`를 통해 이 메시지들을 없애는 것도 좋다. 

보고서에 차트만 표시하는 방법을 알았으니 본격적으로 그려볼 차례이다. 이 글에서는 보편적으로 사용되는 데이터 시각화 라이브러리인 'ggplot2'와 'plotly'를 활용하여 상호작용이 가능한 그래프를 그리는 과정을 다룰 것이다. 먼저 'plotly' 라이브러리에서 제공하는 함수인 `plot_ly()`를 통해 그리는 방법을 알아보자. 아래 [그림 2]는 각 서버별로 전체 거래 금액과 전체 중 고가 아이템의 거래 금액을 겹쳐 나타낸 것으로, 마우스 오버 시 [그림 2]처럼 해당하는 부분의 상세 수치를 볼 수 있다. 이와 같은 차트를 그리기 위한 코드는 다음과 같다.

<p align="center">
<img src="/assets/works/econ_index/figure7.png"/>
[그림 2] 서버별 전체 거래와 고가 아이템의 거래 금액
</p>

```R
p <- plot_ly(data, y = ~server, x = ~tot_value, type = 'bar', orientation = 'h', 
             name = '전체 거래', marker = list(color = '#6BA292'))
p <- p %>% add_bars(y = ~server, x=~value, name = '고가 아이템 거래',
                    marker = list(color = '#CC527A'))
p <- p %>% layout(barmode = 'overlay', hovermode = 'y unified',
                  xaxis = list(tickformat = ',.f', title= '거래 금액'), 
                  yaxis = list(title =''))
```

먼저 `plot_ly()`로 전체 거래 금액에 대한 막대 그래프를 그려주었다. 이때, `name`으로 범례와 툴팁에 표시될 이름을 명시하고, `marker` 옵션으로 막대의 색상을 변경했다. (색을 지정하지 않으면 default 색상으로 그려진다.) 그 다음 `add_bars()`로 고가 아이템 거래에 대한 막대를 추가해주었다. 여기까지의 코드로만 그림을 그려보면 서버 하나당 전체와 고가 아이템 거래에 대한 막대가 각각 하나씩 생기는데, [그림 2]처럼 동일한 서버의 데이터에 대하여 겹치도록 하려면 `layout()`에 `barmode='overlay'`를 추가해주면 된다. 그 뒤 `hovermode = 'y unified'`는 마우스가 오버된 데이터와 동일한 y축의 데이터를 모두 보여주는 옵션이다. 만약 아무것도 명시하지 않고 A서버의 전체 거래에 마우스를 갖다 대면 해당 수치만 보이고 고가 아이템 거래의 상세 수치는 보이지 않는다. `xaxis`와 `yaxis`는 축에 대한 옵션을 지정해주는 것으로, `title`은 축의 레이블을 나타내며  `tickformat=',.f'`는 숫자의 세자리마다 콤마를 표시해주기 위한 것이다. (tickformat을 지정하지 않으면 k(kilo), M(million) 등의 형식으로 나타난다.) 참고로 이 예제에서는 가로형 막대 그래프로 그렸는데, 세로형으로 그리고자 한다면 x와 y축을 바꾸고 `orientation='h'`를 없애면 된다.

앞선 방법은 처음부터 'plotly'를 사용해 동적인 그래프를 그리는 방법이었다면 이번에는 'ggplot'을 'plotly'로 변경하는 방법에 대해 알아보자. 평소 'ggplot'을 많이 사용했다면 이 방법이 훨씬 편리할 수도 있다. 예시로 그려볼 차트는 앞선 포스팅에도 있었던 아래 [그림 3]이다. 지표 개발 시 KOSPI에서 아이디어를 얻으면서 차트의 모양 또한 주가 그래프에서 착안했다. 보편적인 Boxplot을 그릴 때에는 `geom_boxplot()`을 사용하면 편리하지만, 이 그래프는 일반적인 Boxplot과 차이가 있기 때문에 빈 공간 위에 네모 박스를 그리고, 세로 선을 긋고, 시간에 따른 이동 선을 그리는 순서로 하나하나 커스터마이징이 필요했다.

<p align="center">
<img src="/assets/works/econ_index/figure8.png"/>
[그림 3] 시간에 따른 종합 지수 그래프
</p>

```R
g <- ggplot()+
	geom__rect(aes(ymin=q1, ymax=q3, xmax=id+0.45, xmin=id-0.45, fill=sign), data)+ 
	geom_linerange(aes(id, ymin=min, ymax=max, color=sign), data)+
	geom_line(aes(id, avg, group=’평균선’, color='평균선'), data, size=1)+
	theme_minimal()+
	theme(axis.text.x=element_text(angle=45, vjust=0.5), 
          legend.title = element_blank(), panel.grid.major.x = element_blank())+
	xlab('시간')+ylab('종합 지수')+
	scale_fill_manual(values=c('상승'='#FF4E50', '하락'='#3182BD'))+
	scale_color_manual(values=c('상승'='#FF4E50', '하락'='#3182BD','평균선'='#9DE0AD'))
```

코드를 자세히 살펴보자. `geom_rect()`로 각 시간 축에 따른 사각형을 그리고, `geom_linerange()`로 세로 선을 그어주었다. 그 다음 `geom_line()`로 연두색 평균선에 해당하는 선을 나타냈다. 이후로는 축이나 배경 등에 관한 것인데, `theme_minimal()`은 ggplot2에 내장된 테마 프리셋의 한 종류이다. 그리고 `theme()`은 세부 테마를 설정하기 위해 사용하였는데, `axis.text.x`는 x축 눈금에 대한 레이블에 대한 것이고, `legend.title`과 `panel.grid.major.x`는 각각 범례 제목과 그래프의 x축(세로) 눈금에 관한 것이다. `element_text()`로 텍스트의 각도나 위치에 대한 옵션을 주었고, 그래프 상에서 보이지 않게 하기 위한 방법으로는 `element_blank()`를 활용하였다. `xlab()`과 `ylab()`은 각 축의 레이블을 나타내며, `scale_fill_manual()`과 `scale_color_manual()`은 각각 fill과 color에 대하여 특정 색을 지정하기 위해 사용하였다.

이제 마우스 오버 시, 툴팁에서 해당 데이터에 대한 상세 수치를 나타낼 수 있도록 동적으로 바꾸어 보자. 방법은 간단하다. `gg <- plotly_build(g)`를 통해 plotly로 만들어 주기만 하면 된다. 그런데 지금 차트를 그려보면 툴팁이나 범례에 적힌 텍스트에 변수 이름이 그대로 뜨기 때문에 보기에 썩 좋지 못하다. 하지만 이 텍스트를 원하는 대로 변경할 수 있다. 현재 적용된 툴팁이나 범례의 텍스트는 `gg$x$data[[1]]$name`이나 `gg$x$data[[1]]$text`에서 볼 수 있는데, 이 곳의 내용을 변경하면 차트에 그대로 적용된다. 이때 인덱스 `[[1]]`은 앞서 ggplot을 그렸던 코드에 따라 길이가 다르게 구성되어 있으므로 원하는 대로 전부 변경해주면 된다.



## Interactive Table 만들기

그래프를 통해 자료를 한눈에 보는 것도 좋지만, 대개 보고서를 받아보는 담당자들은 데이터를 특정 기준으로 정렬하여 상위 수치를 확인하거나, 혹은 보고서에 사용된 상세한 자료를 직접 확인하고 탐색해 보기 위하여 원데이터를 다시 요청하는 경우가 종종 있다. 

이러한 니즈를 충족시키고자 그래프에 쓰인 원데이터나 연관시켜 관찰하면 좋을 데이터들을 보고서 상에서 제공할 방법을 고민했고, 그러다 상호작용이 가능한 테이블의 형태를 떠올렸다. 이러한 인터랙티브 테이블은 일반 표와 달리 검색이나 데이터 다운로드의 기능을 제공할 뿐만 아니라 색상이나 아이콘, 게이지 바 등을 통해 데이터와 함께 시각적 효과를 나타낼 수 있는 것이 특징이다. 이를 구현하고자 'formattable' 라이브러리를 사용하였으며, 다음 [그림 4]와 같은 테이블을 만들기 위한 코드는 아래와 같다.

<p align="center">
<img src="/assets/works/econ_index/figure9.png"/>
[그림 4] 서버별 각종 수치를 제공하는 인터랙티브 테이블
</p>

```R
mytable <- formattable(data, list(
    `수치(가)` = formatter("span", style = x ~ 
                        style(color = 'black', background = "#9DE0AD", 
                              padding.right = sprintf("%.0fpx", 100*normalize(x)+10),
                              padding.left = '4px', border.radius = '8px')),
    `수치(나)`= formatter("span", style = ~ 
                       style(color = ifelse(`수치(나)`>0, '#FF4E50', "#3182BD")),
                       ~ icontext(ifelse(`수치(나)`>0,"arrow-up", "arrow-down"), 
                                  `수치(나)`)),
    `수치(다)`= formatter("span", style = ~ 
                       style(color = ifelse(`수치(다)`>0, '#FF4E50', "#3182BD")),
                       ~ icontext(ifelse(`수치(다)`>0, "arrow-up", "arrow-down"), 
                                  `수치(다)`)),
    `서버` = formatter('span',style = x~style(color='black'))
))
as.datatable(mytable, rownames = FALSE, extensions = 'Buttons',
             options = list(dom = 'Bfrtip', buttons = 
                            list(list(extend = 'collection', text = '데이터 다운로드',
                                      buttons = list(list(extend='excel', 
                                                          fieldBoundary= '', 
                                                          filename = '파일명'),
                                                     list(extend='csv', 
                                                          fieldBoundary= '',
                                                          filename = '파일명'))
))))
```

`formattable()`함수를 사용하면 테이블의 각 컬럼마다 상세 옵션들을 정해줄 수 있다. 먼저 “수치(가)” 컬럼의 경우 `style()`을 통해 글자 및 게이지 바의 색상을 정해주었다. 이때, `100*normalize(x)+10` 부분은 게이지 바의 길이를 정해주는 부분으로, 기호에 따라 적절히 변경해 사용하면 된다. `border.radius`는 숫자를 크게 줄수록 게이지 바의 가장자리를 둥글게 만들 수 있는 옵션이다. 한편 "수치(나)"와 "수치 (다)"에 쓰인 `icontext()`를 통해 위 아래 화살표의 방향을 해당 수치의 부호에 따라 양수이면 "arrow-up"으로, 음수이면 "arrow-down"으로 정해주었다. 표에 대한 시각화를 마쳤다면 이제 `as.datatable()`을 통해 상호작용이 가능하도록 만들어주면 된다. 첫 부분의 `rownames=FALSE`는 데이터 앞에 붙는 행번호를 표에 보이지 않도록 하는 옵션이다. 

그 다음부터는 데이터 다운로드 기능을 추가하기 위한 것들인데, `text = '데이터 다운로드'` 부분의 글을 수정하면 [그림 4] 좌측 상단의 ‘데이터 다운로드’ 문구를 바꿀 수 있으며, `filename = '파일명`의 ‘파일명‘부분을 변경하면 데이터 다운로드 시 기본 파일명을 원하는 대로 지정할 수 있다. 또한 `extend = 'excel'`를 통해 Excel, csv 등 제공할 데이터의 포맷을 지정할 수 있다. 이때 주의할 점은 csv파일의 경우, 수치형 데이터가 **25,130**과 같은 형태로 세 자릿수마다 콤마(,)를 표시한 형식은 아닌지 잘 살펴보도록 하자. 만약 콤마가 포함된 수치 형식의 데이터를 csv로 저장하게 되면 **25,130**이 **25130**이 아닌 **25**와 **130**의 값을 갖는 각각의 열로 인식되므로 이점을 주의해야한다. 이렇게 보고서 자체에서 데이터를 다운로드 받을 수 있도록 하면 별도로 원데이터를 제공하는 번거로움도 피할 수 있을 뿐 아니라, 시간이 흐른 뒤, 예전 보고서와 관련된 데이터를 찾을 때에도 편리하다. 



## 문서 열람의 편의성 높이기

하나의 문서에 여러 정보를 제공할 때, 아래로 스크롤을 내리며 이어지는 내용을 보기에 적절한 항목이 있는 반면, 동등한 레벨을 갖는 자료의 경우, 탭을 사용하여 병렬적인 형태로 나타내는 것이 더욱 적절한 항목도 있다. 이러한 경우에 활용할 수 있도록 탭으로 섹션을 나누는 것도 좋은 방법이다. 사용법은 매우 간단하다. Markdown에서 소제목들을 구분할 때, 아래와 같이 한단계의 레벨 차이를 두고, 상위 소제목의 뒤에 `{.tabset}`을 입력하기만 하면 된다. 그러면 [그림 5]와 같은 모양으로 문서가 구성된다.

<p align="center">
<img src="/assets/works/econ_index/figure10.png"/>
[그림 5] 탭을 통해 보고서의 섹션을 나눈 모습
</p>

```html
## 제목 공간 {.tabset}
설명 공간 <br />
### 전체 거래
{r code 자리}
### XXXXXX
{r code 자리}
### YYYYYY
{r code 자리}
```

그런데 tabset으로 섹션을 나눈다고 해도, 내용이 많아지면 문서가 길어지기 마련이다. 이 경우 맨 위에 목차를 넣고 적절한 위치에 Top 버튼을 두거나, 스크롤에 따라서 움직이는 목차를 삽입한다면 사용자가 훨씬 편하게 문서를 열람할 수 있을 것이다. R Studio에서 File -> New File -> R Markdown을 통해 생성한 예제 파일에 문서를 작성하고 있었다면, 스크립트 최상단의 헤더에 `output: html_document`라 입력된 부분이 있을 것이다. 이를 다음과 같이 변경해주면 좌측에 스크롤과 관계없이 고정된 목차가 생기게 된다. 혹은 아래 코드에서 `toc_float: yes`를 제거하거나 `no`로 바꾸면 문서의 제목 바로 아래에 목차가 생긴다. 목차의 소제목을 클릭하면 해당 위치로 이동한다.

```markdown
output: 
  html_document:
    toc: yes
    toc_float: yes
```

원하는 곳에 Top 버튼을 추가하는 법은 매우 간단하다. 원하는 위치에 `<a href="#top" style='float: right'>Top</a>`를 추가하면 된다. 이때 `float: right`는 버튼을 오른쪽에 정렬한다는 뜻이므로 왼쪽 정렬 시 `float: left`로, 가운데 정렬 시 `float: left; position: relative; left: 50%`로 바꿔주면 된다. 또한 `Top`부분을 다른 글로 변경하면, 해당 문구가 버튼의 글귀가 된다. 

도움말 등 다른 내용과 분리해야 하는 설명이 필요할 때 사용하기 좋은 텍스트 박스도 있다. 아래 [그림 6]에서 다양한 텍스트 박스들을 볼 수 있는데, 특히 맨 아래 예시는 "도움말"이라는 문구를 클릭하면 ‘내용 입력”이 보이고 한 번 더 클릭하면 해당 내용이 다시 숨겨지는 형태이다. 코드는 아래와 같으며, 첫째줄의 `class=”well well-sm”`대신 각 텍스트 박스 안에 쓰인 코드를 입력하면 해당 테마로 바뀐다. `<button`으로 시작하는 코드부터는 [그림 6]의 가장 아래 열고 접기가 가능한 도움말을 위한 부분이다. 한가지 주의할 점은 button 절의 `data-target=’#myinfo’`와 가장 아래 `<div id=”myinfo”`에 있는 myinfo는 서로 동일하게 지정하되 다른 id와 겹치지 않도록 해주어야 한다는 것인데, 이는 id를 토대로 버튼 제목과 내용을 이어주기 때문이다. 참고로 `<br />`은 줄바꿈을 의미한다.

<p align="center">
<img src="/assets/works/econ_index/figure11.png"/>
[그림 6] 도움말을 삽입하는 여러 가지 방법
</p>

```html
<div class="well well-sm" style='font-size: 10pt;'>
<strong>도움말</strong><br />
내용 입력
</div>
<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#myinfo" style='font-size: 10pt'>도움말
</button><br/>
<div id="myinfo" class="collapse" style='font-size: 10pt;'>
내용 입력
</div>
```



## html 파일로 내보내기

내용을 모두 작성했다면 스크립트 상단의 Knit -> Knit To HTML을 클릭해 파일로 내보내도록 하자. 그러면 Rmd 스크립트와 동일한 경로에 html 형식으로 저장이 되며, 지금까지의 내용을 골고루 활용한 경우 아래 [그림 7]과 같은 모양의 문서를 볼 수 있다. 

<p align="center">
<img src="/assets/works/econ_index/figure12.png"/>
[그림 7] 예시 Interactive Report의 모습
</p>

지금까지 R Markdown으로 기본적인 틀 위에서 인터랙티브 보고서를 구현하는 방법을 소개해 보았다. 일반적인 문서에 비해 작성하는 과정은 다소 까다롭지만, 상황에 따라 이러한 노고를 뛰어넘는 효용을 가져오기도 하니 기회가 된다면 사용해보는 것을 추천한다. 평범한 정적 보고서와 달리 입력에 반응하는 보고서를 완성하면 뿌듯한 마음이 들기도 하고, 이런저런 기능을 추가해 더 발전시키고 싶은 마음도 든다. 인터넷을 검색해 보면 여기서 소개한 것보다 더 다양하고 많은 기능에 대한 예제들을 찾을 수 있다. 혹시 Markdown 예제 코드를 검색하다 이 포스팅을 보게 되었다면 조금이나마 도움이 되었기를 바라고, 그렇지 않더라도 언젠가 적당한 상황에서 '이런 게 있었지!'라고 떠올릴 수 있길 바라며 이 글을 마친다. 