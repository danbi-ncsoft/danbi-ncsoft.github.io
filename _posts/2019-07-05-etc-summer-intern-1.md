---
layout: post
title: "인턴 생활기 시즌2 #1"
date: 2019-07-05 18:00:00
categories: ETC
author: DANBI
cover: "/assets/start2.jpg"
---

7월 1일부터 7주간 분석모델링팀에서 2명의 사원이 인턴의 업무를 수행하게 되었습니다. 인턴
생활 동안 저희가 배우고 느낀 바를 간략하게나마 전달해 드리고자 합니다. 매주 성장해나가는 모습 지켜 봐주시면 감사하겠습니다.

A - 안녕하세요. 저는 컴퓨터 공학과 통계학을 전공하였으며 데이터 분석과 머신 러닝 관련 공부를 하고 있습니다. 지금까지 진행했던 프로젝트들로는 Expedia 데이터 관련 패키지를 사는 사람들을 분류, zebrafish가 돌연변이인지에 대한 분류 등이 있습니다. 

B - 안녕하세요. 저는 통계학을 전공하고 머신러닝/딥러닝 모델링에 흥미가 있습니다. 데이터 분석과 관련하여 다양한 공모전 참여, 동아리 활동을 통해 이 분야를 공부해왔습니다.

### 오리엔테이션

입사 첫날, 저희가 찾은 곳은 R&D센터의 NC University였습니다. 이곳은 사내 직원들을 위한 다양한 교육, 행사들이 열리는 곳으로 쾌적한 환경이 조성되어 있었습니다. 모든 직무의 인턴사원들이 이곳에 모여 Ice Breaking 시간을 가졌고 첫 교육으로는 회사의 사업에 대한 소개, 사내 제도와 각종 복지에 대한 안내를 받을 수 있었습니다. 이어서 보안에 대한 교육을 받았는데, 아무래도 데이터를 직접 다루는 직무이다 보니 사내 보안 사항에 대해 더 귀를 기울여 들었던 것 같습니다. 회사에서 진행되고 있는 많은 일들은 보안이 유지되어야 하기 때문에 회사에서 하는 어떠한 일들이 보안 규정에 어긋나는 일인지, 사용하고 있는 여러 보안 프로그램들은 왜 설치해야 하는 지 등에 대해 교육을 받았습니다. 이를 통해 철저한 보안 유지가 매우 중요하다는 것을 알 수 있었습니다. 

엔씨소프트의 인턴십 과정은 해당 직무의 멘토님과 함께하는 제도로 이루어져 있습니다. 일대일로 회사 적응을 위한 안내와 더불어 업무 중에 생기는 질문에 친절히 답변해주시는 등 인턴 사원을 배려해주는 좋은 제도라고 생각했습니다. 그렇게 저희는 각 부서의 멘토 분들의 인솔하에 각자의 팀으로 이동했습니다.

### 데이터플랫폼실 설명회 참석

엔씨소프트 Data Center에는 분석모델링팀 외에도 많은 데이터 관련 팀이 존재합니다. 그 중 데이터플랫폼실은 분석가가 데이터를 쉽게 접근하고 분석할 수 있도록 다양한 데이터 관련 서비스를 개발하고 운영하는 조직입니다. 따라서 이 조직에서 어떤 일을 하고 어떤 서비스를 운영하는 지 알아두는 것은 저희처럼 회사에 첫 입사한 분석가들에게 꼭 필요한 일입니다. 

마침 이번 주에 데이터플랫폼실에서 주요 업무 설명회를 열어주셨는데요. 구체적으로 어떤 일을 하는지에 대해 들을 수 있어서 좋았습니다. 신규 입사자를 포함한 데이터플랫폼실의 업무에 관심이 있는 직원을 대상으로 한 세미나였기 때문에 다양한 업무들을 쉽게 파악할 수 있었습니다. 주제로는 게임 로그 데이터의 구축과 활용, 모바일 데이터 분석에 사용되는 MAP, 유저들 관련 데이터 수집, Hive DB의 전체적인 구조 등이 있었습니다. 이용자로서는 전혀 알지 못했던 것들이기에 정말 흥미롭고 많이 배울 수 있는 시간이었습니다. 이렇게 타 팀 간에도 지식을 공유할 수 있는 장이 마련되어 있어, 사내 데이터 구축과 분석 시스템의 흐름을 이해하는 데 도움을 주는 설명회였습니다. 

<p align="center">
<img src="/assets/etc/summer_intern/excited.jpg" style="width:3in" />  


</p>

### 앞으로의 여정

그렇다면 I&I 실의 분석 모델링 팀에서는 어떤 업무를 수행하고 있을까요? 이 부분에서 궁금증이 많으실 것 같습니다. 다양한 분석 업무가 수행되고 있지만 저희가 수행할 두가지 분석을 안내해 드리겠습니다.

먼저, 악성 유저(이하 봇) 탐지가 있습니다. 작업장이라고 불리는 봇을 올바르게 제재하는 것은 게임 운영에 있어 아주 중요한 일입니다. 봇은 노력을 들이지 않고도 24시간 내내 캐릭터를 육성하는 편법으로써 일반 유저에게 상대적 박탈감을 느끼게 하고, 재화를 비이상적으로 취득하여 게임 내 경제에 악영향을 끼칩니다. 이러한 봇들은 일반 유저들과는 게임 플레이 패턴이 상이할 것이므로 유저들의 게임 로그 데이터를 분석하면 이 유저가 봇인지 아닌지 탐지할 수 있을 것입니다. 따라서 분석모델링팀에서는 머신러닝 기법을 이용하여 봇을 탐지하여 운영 팀에서 봇들을 효과적으로 제재할 수 있도록 돕고 있습니다.

둘째, 모바일 마케팅 데이터 분석입니다. 현재 진행중인 분석은 광고 효과에 대한 것으로 리니지M에 유입된 유저들 중, 광고 매체로 유입된 유저와 그렇지 않은 유저들의 차이를 비교하는 것입니다. 두 그룹이 매출, 전투 유형, 잔존율, 컨텐츠 이용 등에서 어떠한 차이가 있는지 분석하고, 이를 마케팅 전략에 반영하는 것이 목적입니다. 사용되는 게임 로그 데이터는 매일 수 TB가 생성된다고 하는데, 이렇게 큰 데이터가 담고 있는 정보를 모형에 반영시킬 수 있다는 것이 놀라웠습니다.

인턴 생활을 한지 한 주 밖에 되지 않았기 때문에 아직 본격적인 업무를 시작하지는 않았지만 데이터 마이닝과 관련하여 배웠던 것들이나, 참여했던 프로젝트들과의 연관성을 찾아볼 수 있어서 흥미로웠습니다. 아직 배워야 할 것도 많고 직접 해봐야 할 것도 많기 때문에 앞으로의 인턴 생활이 많이 기대가 됩니다!