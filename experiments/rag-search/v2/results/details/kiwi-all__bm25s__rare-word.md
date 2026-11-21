# kiwi-all__bm25s__rare-word

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (4.87), policy-05-flextime (3.40) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (3.72) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (6.33) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | X | current: customer-03-faq (4.29) |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (3.86) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (3.79) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | X | current: customer-03-faq (2.18) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | O | O | current: policy-02-remote (1.16), policy-05-flextime (1.13) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (4.44), policy-05-flextime (1.39) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (3.98), tech-03-incident (1.33) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | X | X | current: customer-03-faq (0.89), customer-04-terms (0.83) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (3.80), tech-03-incident (1.16) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | X | current: customer-03-faq (4.41) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | X | current: customer-03-faq (2.38) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | O | O | current: tech-03-incident (1.48), tech-04-backup (1.35), tech-05-access (1.28) |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (2.55) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (2.02) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (2.49) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (3.47), customer-03-faq (2.41) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (4.79) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (3.11) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (3.69) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | O | O | current: tech-04-backup (2.18), customer-03-faq (1.17) |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (3.64) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | X | current: customer-03-faq (5.01) |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | X | current: customer-03-faq (2.88) |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (3.78), tech-03-incident (1.04) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | X | current: customer-03-faq (5.36) |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (2.38) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (4.26), policy-01-leave (1.50) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (4.92) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (2.84), policy-04-expense (1.33) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | O | O | archive: customer-14-freepass (8.49) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.63) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | X | X | current: policy-02-remote (1.20) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.57) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (2.94), policy-02-remote (1.17) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: policy-02-remote (1.57) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (5.51) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (9.54) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (4.07) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (9.49) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.26) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (6.62) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.20) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | O | O | archive: tech-14-atlas-deploy-tool (7.08) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (2.43) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | O | O | archive: tech-14-atlas-deploy-tool (6.97) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | X | X | current: customer-03-faq (2.11) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.35) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.19) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (8.28) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (4.71) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (6.90) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (4.72) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | X | X | current: policy-03-education (0.75), customer-02-refund (0.62), tech-02-deploy (0.59) |
| 19 | E | keywords | 사내 주차 지원 | 없음 | X | X | current: policy-03-education (0.96), tech-02-deploy (0.56), policy-02-remote (0.49) |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (1.89) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | X | X | current: policy-03-education (0.69), policy-04-expense (0.69), policy-01-leave (0.69) |
