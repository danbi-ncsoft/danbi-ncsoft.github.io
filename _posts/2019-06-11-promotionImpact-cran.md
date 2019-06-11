---
layout: post
title: "promotionImpact R 패키지 CRAN 등록기"
date: 2019-06-11 13:50:23
categories: Works
author : DANBI
cover: "/assets/pie_cover.png"
---



### **피땀 흘려 만든 R 패키지... CRAN에 등록해볼까?**

이전 포스팅에서 설명했듯이, 집계된 지표를 토대로 여러 가지 프로모션들의 효과를 추정하는 데 필요한 데이터 전처리 및 회귀 분석 과정을 도와주는 R 패키지 'promotionImpact'를 만들었다. (<https://danbi-ncsoft.github.io/works/2019/01/08/works-promotionImpact.html>)

그리고 이왕 R 패키지를 만든 김에, R의 공식 Repository, CRAN에 등록해보고자 어쩌면 험난할지도 모르는 여정을 시작했다.

 

<img src="/assets/pie.png" style="width:6in" />

​    

### **그런데 뭐부터 시작해야 하지?**

찾아본 사람은 알겠지만 R 패키지를 만드는 방법에 대한 한글로 된 문서는 꽤 있으나, CRAN 등록에 관해서는 잘 없다. 사실 리서치를 해보면 CRAN 등록을 준비할 때 참고하면 좋을 만한 사이트들은 더러 있는데, 한글로 쓰여진 건 없다. (적어도 나는 못 찾았다.) 그래서 우리말로 몇 가지 팁을 담은 후기를 써보려 한다. 

먼저 피땀 흘려 만든 패키지를 `devtools::build()`를 통해 tar.gz파일로 잘 묶는다. 이때, 숨김 폴더나 .Rhistory, .gitignore 파일 등은 패키징 될 필요가 없으므로 .Rbuildignore 파일에 적어주면 여기에 적힌 파일은 빌드 시 제외된다. 그 다음, `devtools::check()` 혹은, 터미널에서 `R CMD check` 명령어를 실행하면 이 패키지에 흔히 발생 가능한 문제가 있는지, 있다면 어떠한 것들인지 자동으로 체크할 수 있다. 체킹이 끝나고 나면 에러, 경고, 노트가 몇 개나 있는지 뜨게 되는데, 에러가 있다면 CRAN에 제출하는 것이 아니더라도 꼭 수정해야 한다. 경고가 있다면 CRAN에 제출을 목표로 하는 경우 고쳐야 하는 문제이고, (물론 CRAN이 목표가 아니더라도 고쳐서 없애면 좋다.) NOTE의 경우 CRAN에 제출할 것이 아니라면 크게 신경 쓰지 않아도 되지만, 그렇지 않다면 최대한 없애는 것이 좋다. 이것들을 하나하나 없애는 데에 시간이 조금 걸리긴 하지만, 늘 그렇듯이 구글링을 하면 세계 곳곳에 나와 같은 문제를 가진 사람들이 존재하므로 웬만한 문제는 해결할 수 있다. 그 중에서 'promotionImpact'를 체크하면서 맞닥뜨렸던 문제들을 몇 가지만 소개해보도록 하겠다.

​    

#### Case 1) no visible binding for global variable [variable name]

이런 문제가 발생했을 때, 혹시 [variable name] 자리의 변수명이 ggplot의 `aes()`에 쓰인 변수는 아닌지 살펴보라. 이에 대해 구글링을 하면 가장 간단한 해결법으로 `aes()`대신 `aes_string()`을 쓰면 된다고 나와있는데, promotionImpact의 경우에는 `aes_string()`을 사용하여도 여전히 동일한 NOTE가 발생했었다. 다른 해결법으로는 `with()`를 사용하는 것이라고 나오는데, 아래와 같이 코드를 변경하니 NOTE가 사라졌다.

 ```R
전) ggplot(data, aes(xvariable, yvariable)) + geom_point()

후) ggplot() + with(data, geom_point(aes(xvariable, yvariable)))
 ```

​    

#### Case 2) no visible global function definition for [function name]

혹시 [function name] 자리의 함수에 오타가 없는데도 불구하고 이러한 문구가 뜬다면 import나 importFrom을 사용해 해당 함수가 포함된 패키지를 불러오는 것을 잊지는 않았는지 의심해보도록 하자. 만약 NAMESPACE 파일에 `import([package name])` 혹은 `importFrom([package name],[function name])` 이 없는 경우 .R파일에서 import 혹은 importFrom을 통해 패키지를 불러온 다음 `devtools::document()`로 NAMESPACE 파일을 갱신하자. 혹시 [function name] 자리의 함수가 `head()`, `tail()`, `median()`과 같은 매우 기본적인 함수라면 한가지 간과하고 있었던 사실을 상기해 보아야 한다. 늘 `library()`없이 써서 잊고 있었겠지만 `head()`, `tail()`은 'utils'라는 패키지에, `median()`은 'stats'라는 패키지에 있는 함수이다. 따라서 이들 함수를 사용한 경우에도 import를 명시해주어야 한다.

  

#### 그 외에도…

\* pdf manual이 생성되지 않았다는 메시지가 뜰 때에는 MiKTeX이나 LaTeX와 같은 프로그램이 설치가 되어있는지 확인해보고 그렇지 않다면 설치를 하면 된다.

\* 코드에 한글로 쓰여진 주석이 있다면 모두 제거하는 편이 좋다.

\* 코딩 시 편의상 TRUE, FALSE를 T, F로만 쓰는 경우가 종종 있는데 이를 TRUE, FALSE라고 전부 써주어야만 한다. 

\* Example이 있는 경우 Example의 실행 시간이 너무 길다면 NOTE가 발생하는데, 개발자의 PC에서는 실행 시간이 그리 길지 않았다 하더라도 제출 시 자동 체크되는 환경에서는 오랜 시간이 걸릴 수 있기 때문에 이점을 유의하여 Example을 만들어야 한다.

\* Description 파일에 imports나 depends 등에 패키지 이름과 버전을 쓸 때, [패키지이름] (>= 버전)의 형식으로 패키지 이름 뒤 한 칸, 부등호 뒤 한 칸의 공백을 주어야 한다.

​     

### CRAN은 그렇게 호락호락하지 않다

하나하나 노트를 지워나가며 셀 수도 없을 만큼 체크를 했고 그 결과는 아름다웠다. 0 Errors, 0 Warnings, 0 NOTEs. 하지만 기뻐하기엔 아직 이르다. 동일한 체크를 적어도 2개의 OS에서 실행하여 다른 환경에서도 여전히 문제가 없는지 확인해 보아야 한다. 'promotionImpact'의 경우, windows에서 개발되었기 때문에 윈도우에서 먼저 체크한 다음, linux에서 동일한 테스트를 진행하였으며 다행히도 결과는 윈도우에서와 동일했다. 하지만 여기서 끝이 아니다. 대부분 현재 공식 release 버전이나 크게 오래되지 않은 이전 release버전에서 작업을 마쳤을 텐데, 이 체크는 현재 개발 버전인 R-devel에서도 무사히 통과되어야 한다. 이쯤에서 ‘아니, 이렇게까지 해서 CRAN에 패키지를 등록해야 하나.’ 라는 생각이 들 수도 있겠지만, CRAN에 등록하면 무려 `devtools::install_github()`이 아니라 `install.packages()`로 설치가 가능하다.(!) 그러니 조금만 더 힘을 내보도록 하자. 하나의 사이트를 추천하자면 <https://win-builder.r-project.org/upload.aspx>라는 곳인데, 이 곳에 패키지 파일을 업로드 하면 패키지 체크 후 결과가 Maintainer의 메일로 온다. 실제 CRAN에 패키지를 제출하면 자동으로 패키지를 체크하고 그 결과를 Maintainer에게 메일로 알려주는데, 그때 발송자의 메일 주소와 위 사이트의 메일 발송자가 동일하다.

여러 플랫폼에서, 여러 버전에서 패키지가 테스트 되었다면 이제 정말로 제출할 차례다. 최종적으로 build된 파일을 <https://cran.r-project.org/submit.html>에 업로드하면 Maintainer에게 이를 확인하라는 메일이 오며, 정책 등을 마지막으로 잘 읽고 확인을 하면 정상 제출이 된다. 그리고 몇 시간 후, 제출한 패키지가 체크되어 로그파일과 함께 Maintainer에게 메일이 오는데, 이 관문을 통과하지 못했다면 고치라는 메일이, 통과했다면 며칠 이내로 CRAN 직원에게서 답장이 올 것이라는 메일이 오게 된다. 참고로 이후 CRAN 직원에게 받는 메일은 생각보다 빨리 온다. (지구 반대편에서 열일 중이신 듯하다.)

자동 체크가 무사 통과되고 CRAN 직원으로부터 답장이 와 두근거리는 마음으로 열어보았더니 Description을 중심으로 조금 수정한 뒤 다시 제출하라는 내용이었다. 그런데, 수정해야 하는 사항들 중에는 다소 형식적인 것들도 꽤 있었는데 정리해보면 다음과 같다.

\* 패키지에 대한 설명 중 variable(e.g. daily sales)라는 구절이 있었는데 variable (e.g. daily sales)와 같이 괄호 앞에는 한 칸의 공백을 두어야 한다. 

\* 인용은 저자 (년도) &lt;doi:…&gt;의 형식이어야 하며 이때 콜론 뒤에는 띄어쓰기를 하면 안 된다.

\* 저자는 Author뿐 아니라 Authors@R 항목에도 정해진 형식인 `person()`을 사용하여 이름과 함께 이메일과 역할도 쓰여져야 한다. (이때, 저작권자도 함께 쓰여져야 한다.) 참고로 Author에는 여러 사람을 쓸 수 있지만 Maintainer에는 단 한 명의 이름과 이메일만 써야 하며, 회사 이름이나 팀 이름 등이 아니라 실제 사람 이름을 적어야 한다. 

\* 데이터 전처리 등을 위해 정의하여 굳이 export하지 않은 함수들이라도 각각의 함수에 대한 Rd파일이 man폴더에 있어야 한다. 

\* 전체 check 시간은 10분 안쪽이어야 한다. promotionImpact의 경우 함수의 실행 시간 자체가 길어 Example을 check하는 과정에서 오랜 시간이 걸려 처음엔 10분을 넘었다. 이러한 경우에는 아주 간단한 예제를 `\dontshow{}`로 감싸 간단한 예제만 check 되도록 하고, 실제 매뉴얼에 넣고자 하는 예제는 `\donttest{}`로 묶어 test는 되지 않도록 하여 이 문제를 해결할 수 있다.

이처럼 CRAN에 등록하려면 세세한 것 하나하나까지 신경 써야 했고, 아무리 작은 수정사항들일지라도 고쳐서 제출하는 과정을 반복해야 하기 때문에 이에 대한 시간이 꽤 걸렸다. 그러니 패키지 CRAN 등록을 준비하면서 이 글을 보는 사람들은 이점을 유의하여 사소한 수정에 굳이 시간을 쓰지 않기를 바란다. 다른 패키지들의 CRAN 페이지에서 tar.gz파일을 직접 받아 나의 파일과 비교해보며 참고하는 것도 아주 좋은 방법이 될 것이다.

​    

### Thanks, on its way to CRAN.

사실 위에 작성한 수정 사항들을 한번에 알려준 것이 아니라 하나 고쳐서 내면 다른 하나를, 그것을 고쳐서 내면 또 다른 하나를 수정하라고 오는 방식이었다. (도대체 왜 한번에 알려주지 않은 건가요..ㅠㅠ) 그렇게 서서히 지쳐가고 있을 때쯤, 이번에는 또 뭘 고치라고 답장이 왔으려나 하는 자포자기의 심정으로 메일을 열었다. 메일의 내용은 단 한 문장이 전부였는데, 그 메시지는 바로 Thanks, on its way to CRAN. 이 메일을 받은 순간만큼은 그간 고생한 나날들을 떠올리며 감격에 겨워도 좋다. 그 후, 약간의 시간이 지나면 `install.packages()`를 사용해 설치할 수 있으며 CRAN에 아래와 같이 url도 생기고, 바이너리 파일들이 순차적으로 생성된다.

(<https://cran.r-project.org/web/packages/promotionImpact/index.html>)

등록 절차는 이로써 끝이지만, 유지 및 보수라는 지속적인 작업들이 기다리고 있을 것이다. 유지 보수는 끝이 없는 여정이지만 보람과 뿌듯함으로 패키지를 관리하길 바라며 이 글을 마친다.

PS. promotionImpact 많은 관심 부탁 드립니다. (_ _)

