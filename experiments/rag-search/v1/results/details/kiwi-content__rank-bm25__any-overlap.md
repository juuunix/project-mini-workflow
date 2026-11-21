# kiwi-content__rank-bm25__any-overlap

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (7.81), policy-05-flextime (4.96), customer-03-faq (0.25) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (9.14), customer-04-terms (1.77), policy-05-flextime (1.76) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (14.62), policy-05-flextime (4.64), policy-02-remote (2.53) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | O | O | current: customer-02-refund (7.13), customer-03-faq (3.61), customer-01-plans (3.25) |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (6.35), customer-01-plans (2.86), customer-03-faq (2.69) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (6.35), customer-01-plans (2.86), customer-03-faq (2.69) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | O | O | current: policy-02-remote (5.00), policy-05-flextime (4.05), customer-04-terms (1.53) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | O | O | current: policy-02-remote (2.53), policy-05-flextime (2.49), customer-04-terms (1.77) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (9.78), policy-01-leave (3.00), policy-05-flextime (2.62) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (9.96), tech-03-incident (3.51), customer-02-refund (1.63) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (8.87), tech-03-incident (2.78), policy-05-flextime (0.76) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (9.21), tech-03-incident (2.78), policy-01-leave (0.82) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | O | current: customer-03-faq (4.35), tech-03-incident (1.45), tech-05-access (1.45) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (4.35), tech-03-incident (1.45), tech-05-access (1.45) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | O | current: tech-04-backup (1.50), tech-03-incident (1.45), tech-05-access (1.45) |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (4.98), tech-01-api-v2 (1.12), customer-01-plans (1.10) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (4.18), customer-05-support (0.75), customer-01-plans (0.73) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (4.98), tech-01-api-v2 (1.12), customer-01-plans (1.10) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (7.99), customer-02-refund (0.97), policy-01-leave (0.94) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (10.93), tech-01-api-v2 (2.11), policy-03-education (1.70) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (7.86), policy-01-leave (0.82), customer-02-refund (0.79) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (8.74), customer-03-faq (2.26), policy-05-flextime (0.80) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | O | O | current: tech-04-backup (4.51), customer-03-faq (2.36), customer-04-terms (0.78) |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (8.74), customer-03-faq (2.26), policy-05-flextime (0.80) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | O | O | current: tech-05-access (6.55), customer-03-faq (5.14), policy-02-remote (2.45) |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | O | O | current: tech-05-access (6.01), customer-03-faq (5.14), tech-01-api-v2 (3.39) |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (6.55), policy-02-remote (2.45), tech-04-backup (2.45) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | O | O | current: policy-05-flextime (7.91), customer-03-faq (5.62), policy-01-leave (2.79) |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (4.35) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (7.91), policy-01-leave (2.79), customer-01-plans (1.77) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (4.88), policy-01-leave (2.24), customer-04-terms (0.99) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (5.58), customer-02-refund (1.07), policy-03-education (1.07) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (2.24) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | X | X | current: customer-01-plans (2.99), customer-03-faq (2.31), tech-01-api-v2 (1.72) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | X | X | current: customer-03-faq (3.23), policy-04-expense (1.88), customer-01-plans (1.62) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | X | X | current: customer-01-plans (2.99), customer-03-faq (2.31), tech-01-api-v2 (1.72) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (2.59), tech-05-access (2.19), customer-04-terms (0.86) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (2.59), policy-02-remote (2.46), tech-05-access (2.19) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | X | X | current: customer-01-plans (3.24), policy-03-education (2.64), tech-01-api-v2 (2.28) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (3.96), policy-04-expense (2.29), policy-05-flextime (1.76) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (9.71) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (3.96), policy-04-expense (2.29), policy-05-flextime (1.76) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (6.45), customer-01-plans (2.44), tech-03-incident (2.37) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (5.71), tech-03-incident (2.37), customer-01-plans (2.07) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (6.45), customer-01-plans (2.44), tech-03-incident (2.37) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (10.47), tech-04-backup (2.15), tech-01-api-v2 (1.18) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (4.94), tech-02-deploy (3.49), tech-03-incident (2.78) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (10.47), tech-04-backup (2.15), tech-01-api-v2 (1.18) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | X | X | current: tech-01-api-v2 (2.11), customer-04-terms (1.77), customer-03-faq (1.26) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | X | X | current: policy-01-leave (4.34), tech-01-api-v2 (2.11) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | X | X | current: policy-01-leave (4.34), tech-01-api-v2 (2.11) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (6.57), tech-03-incident (1.65), customer-02-refund (0.92) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (5.62), customer-03-faq (0.92), customer-04-terms (0.86) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (6.57), tech-03-incident (1.65) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (5.17), policy-03-education (1.85), tech-02-deploy (1.31) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | X | X | current: policy-03-education (2.20), customer-02-refund (2.05), tech-02-deploy (1.93) |
| 19 | E | keywords | 사내 주차 지원 | 없음 | X | X | current: policy-03-education (1.16), customer-05-support (0.75), customer-01-plans (0.73) |
| 20 | E | polite | 안녕하세요 | 없음 | O | O | 없음 |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | X | X | current: policy-04-expense (0.73), policy-03-education (0.73), policy-01-leave (0.73) |
