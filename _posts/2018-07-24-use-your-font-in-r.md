--- 
layout: post  
title: "너의 폰트를 써라! (R에서도)"
date: 2018-07-24 11:59:59
categories: ETC 
author : DANBI  
cover: "/assets/statistics.jpg"  
---

# 알파벳이 아닌 그런 경우 

R을 쓸 때 폰트 문제는 쉬운 듯 어려운 문제다. 그냥 OS에서 폰트 깔아서 쓰듯 쓸 수 있으면 좋으련만 ‘그렇게’ 쉽게 쓸 수는 없다. R에서 그래프를 그려본 사람이라면, 어 “왜 (그래프에서) 폰트가 네모박스로 나와”하는 상황을 한번은 마주쳐 봤을 것이다. 이는 R과 RStudio가 OS에서 끌어다 쓰는 부분이 제한적이기 때문에 생기는 일이다. 그렇다고 못생긴 굴림체와 계속 살 수는 없는 노릇이니 방법을 찾긴 해야 한다.

# extrafont? showtext? 

이럴 때 누구나 하는 구글 검색을 해보면 extrafont 패키지가 주로 검색된다. 이 패키지는 로컬 머신(내 컴퓨터)에 설치된 폰트를 끌어다가 그림에 심는 것을 구현한다. 다만 이 경우 여러 개의 로컬 머신을 오가며 작업할 경우 일관되게 폰트를 쓰기에 곤란할 수 있다. 아울러 패키지가 트루타입(ttf)만 지원하기 때문에 폰트 이용 자체에도 다소 한계가 있다.

Yixuan Qiu가 개발한 showtext 패키지는 보다 일관된 폰트 사용을 목표로 한다. 우선 이 패키지를 쓰면 폰트를 꼭 시스템에 미리 설치해 둘 필요가 없다. 설치되지 않은 폰트도 파일의 경로만 지정해주면 그래프 등의 시각 결과물에서 해당 폰트를 잘 구현해준다. 아울러 TrueType, OpenType, Type 1, web font 등 다양한 포맷을 지원한다. 구글에서 제공하는 폰트의 경우에는 파일 경로로 필요 없다. 이름만 지정해주면 온라인에서 다운로드 받아서 알아서 구현한다. 원래 한글이 없었는데, 나눔고딕을 포함해 한글 폰드가 대거 포함되어, 로컬 머신에 폰트가 깔려 있지 않은 경우에도 한글 구현이 용이해졌다. 

이용 가능한 폰트 목록은 [fonts.google.com](https://fonts.google.com/)를 참고하자. 

# 구현 

```{r} 
#### Start of testing code 
library(tidyverse) 
library(showtext)
```

구글에 등록된 폰트는 showtext에서 제공하는 `font_add_google` 명령을 통해 쉽게 불러올 수 있다. 

```{r}
font_add_google("Gochi Hand", "gochi") 
font_add_google("Schoolbell", "bell")
```

한번 시험을 해보자. 

```{r}
showtext_auto() 

#windows() # if your local os is Windows 
# x11() # if your local os is Macos 
set.seed(123) 
hist(rnorm(1000), breaks = 30, col = "steelblue", border = "white", main = "", xlab = "", ylab = "") 
title("Histogram of Normal Random Numbers", family = "bell", cex.main = 2) 
title(ylab = "Frequency", family = "gochi", cex.lab = 2) 
text(2, 70, "N = 1000", family = "bell", cex = 2.5)
```

![](/assets/etc/use-your-font-in-r/fig_1.png&s=150)

이제 같은 내용을 한글로도 구현해보자! 

```{r}
#### Start of testing code 
library(tidyverse)
library(showtext)

font_add_google("Nanum Gothic", "nanumgothic")
font_add_google("Poor Story", "poorstory")

showtext_auto()

windows() # if your local os is Windows 
# x11() # if your local os is Macos 

set.seed(123)
hist(rnorm(1000), breaks = 30, col = "steelblue", border = "white",
     main = "", xlab = "", ylab = "")
title("무작위 생성 숫자의 히스토그램", family = "nanumgothic", cex.main = 2)
title(ylab = "빈도", family = "poorstory", cex.lab = 1)
text(2, 70, "생성 샘플 수: 1000", family = "poorstory", cex = 1.5)
```

![](/assets/etc/use-your-font-in-r/fig_2.png&s=150)

참고 삼아서 `windows()`에서 별도 창으로 출력한 결과를 그대로 붙여 보았다. 

`showtext_auto()`는 showtext  패키지에게 필요한 상황이 되면 폰트 출력 모드를 켜고 끄는 것을 알아서 하라는 지시다. 수동으로 켜고 끌 수도 있다. 안타깝지만 RStudio의 기본 그래픽 장치는 showtext와 호환되지 않는다. 즉, RStudio IDE 화면 우측 하단에는 폰트가 위의 그림처럼 표현되지 않는다. 당황하지 말자. 그냥 명령어로 별도의 그래픽 장치를 호출하면 된다. Windows라면 `windows()`를, Macos라면 `x11()`을 적절한 위치에 넣어주자. 아울러 rmarkdown에서도 폰트가 제대로 표현되지 않는다. 이때 코드 옵션에 `fig.showtext=TRUE`를 추가하면 위의 그림처럼 잘 나온다. 즉, 마크다운 코드 옵션의 윗단을 아래와 같이 적절하게 처리해주면 되겠다.

```{r}
{R message=FALSE, warning=FALSE, fig.showtext=TRUE}
```

# 어쨌든 나의 폰트를 쓰고 싶다! 

구글에서 편리하게 제공하는 폰트로 만족을 못할 수도 있다. 이때는 내 폰트를 파일 채 들고 와서 심어주면 그만이다. 

```{r}
font_add(family = "hwhitecat", regular = "./fonts/HoonWhitecatR.ttf")
```
위의 코드는 현재 작업 디렉토리(폴더)의 하위에 위치한 `./fonts/HoonWhitecatR.ttf` 폰트를 “hwitecat”이라는 패밀리의 레귤러로 심어준다. 레귤러, 이탤릭, 볼드 등을 아래 명령과 같이 별도로 지정할 수도 있다.

```{r}
showtext_auto() 
p = ggplot(NULL, aes(x = 1, y = 1)) + 
ylim(0.8, 1.2) + 
theme(axis.title = element_blank(), axis.ticks = element_blank(), axis.text = element_blank()) + 
annotate("text", 1, 1.1, family = "hwhitecat", size = 17, label = "안녕, 세상아! 나는 흰고양체야.") + 
annotate("text", 1, 1, family = "heiti", size = 15, label = "\u4F60\u597D\uFF0C\u4E16\u754C") + 
annotate("text", 1, 0.9, label = 'Chinese for "Hello, world!"', family = "constan", fontface = "italic", size = 12) 
print(p)
```

![](/assets/etc/use-your-font-in-r/fig_3.png)

# 어디까지나 기우 

언제나 그렇지만 너무 많은 서체를 쓰는 것은 (단연코!) 보기 좋지 않다. 한마디로 없어보인다. 디자이너들의 일치된 의견이다! 단정하게 그냥 나눔고딕 혹은 Noto Sans CJK KR 정도로 만족하면 어떨까? 

# One More Thing 

혹시나 하는 마음에서 부록 하나 덧붙여 본다. R도 그렇지만 대개의 오픈소스 소프트웨어들은 그림을 만들 때 “장치”를 사용해서 만든다. 그래픽을 생성해 출력하는 장치라고 보면 되고, 스크린, pdf, png 등등 여러가지 형태를 지닌다. 일반적으로 OS 상에서 화면에 있는 그림을 캡쳐해서 포맷에 맞게 저장하는 식으로 생각하지 말고, 필요한 그림은 장치를 통해 생성한다고 이해하면 쉽다.

바로 위에 예를 RStudio에 그대로 복붙했다면, 앞선 예의 출력물 `p`에서 폰트를 제대로 볼 수 없었을 것이다. 앞서도 말했지만, RStudio의 기본 화면 장치는 showtext를 아직 지원하지 않는다. 아래 처럼 해야 제대로 출력된다.

```{r}
# windows() # if your local os is Windows 
# x11() # if your local os is Macos 
print(p)
```

여기까지 실행하면 화면에 팝업으로 출력물이 뜨게 된다. PDF로 저장하기 위해서는 PDF 장치를 부르면 된다. 이때 `dev.off()`를 지정해줘야 pdf 저장이 완료된다는 점 명심하자. 화면 팝업은 수동으로 창을 끄면 `dev.off()`가 되지만 파일은 그렇지 않다. 반드시 `dev.off()`를 넣어줘야 파일을 쓰게 된다.

```{r}
pdf("YOUR_FILENAME.pdf", width = 7, height = 4) 
print(p) 
dev.off()
```
이게 귀찮다면 ggplot2 패키지를 쓰자. ggplot2는 장치를 포맷 별로 편리하게 기록할 수 있는 통일적인 방법을 제공한다. `ggsave` 명령어를 쓰면 `dev.off()`없이 대부분의 포맷으로 아래와 같이 편리하게 저장할 수 있다.

```{r}
ggsave("YOUR_FILENAME.pdf", p, width = 7, height = 4) ggsave("YOUR_FILENAME.png", p, width = 7, height = 4, dpi = 96)
``

폰트를 PDF에 심는 문제는 문제가 될 수도 있고 아닐 수도 있다. 문제가 될 것 같으면 그냥 확실히 해두면 되겠다. 아래 같이 하면 pdf에 폰트를 함께 확실하게 심을 수 있다. 

```{r}
library(Cairo)
# ggsave(filename="./foo.pdf", q, device=cairo_pdf) #
```

# 참고 자료 

* [showtext: Using Fonts More Easily in R Graphs](https://cran.rstudio.com/web/packages/showtext/vignettes/introduction.html)
