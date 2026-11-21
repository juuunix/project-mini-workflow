# bigrams__rank-bm25__score-ratio

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (16.56), customer-03-faq (7.25), policy-05-flextime (7.21) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (8.78), policy-05-flextime (2.34), policy-02-remote (0.63) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (18.23), policy-05-flextime (6.28), policy-02-remote (2.50) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | X | 없음 |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (10.18), customer-01-plans (3.51), customer-03-faq (3.30) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (9.74), customer-01-plans (2.90), customer-03-faq (2.61) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (16.84), policy-15-refresh-sabbatical (2.75), policy-13-onboarding-buddy (2.48) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (5.79), customer-14-freepass (0.79), customer-13-edu-plan (0.62) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (17.96), policy-11-leave-2021 (4.46), tech-11-deploy-2022 (1.74) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | X | X | 없음 |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (14.21), tech-03-incident (3.15), customer-03-faq (2.18) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (9.59), tech-03-incident (2.86), policy-01-leave (0.86) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | O | current: customer-03-faq (13.40), tech-03-incident (3.77), tech-05-access (1.46) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (8.53), tech-03-incident (1.47), tech-05-access (1.46) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | X | 없음 |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (10.36), customer-01-plans (2.98), customer-03-faq (2.55) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (7.73), customer-01-plans (2.86), customer-02-refund (1.16) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (7.91), customer-01-plans (2.98), customer-02-refund (1.11) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | X | X | 없음 |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (14.11), policy-03-education (3.45), policy-02-remote (2.90) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (11.04), policy-02-remote (3.63), policy-03-education (1.72) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | X | X | 없음 |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | X | X | 없음 |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (8.92), customer-03-faq (2.18), policy-05-flextime (0.83) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | X | 없음 |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | X | 없음 |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (6.69), tech-04-backup (2.52), policy-02-remote (2.49) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (19.84), policy-01-leave (5.33), customer-01-plans (2.41) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (17.99), customer-01-plans (2.79), policy-01-leave (2.31) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (9.15), customer-02-refund (1.09), customer-01-plans (0.92) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (2.31) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (17.19), policy-15-refresh-sabbatical (4.48), customer-15-friends-reward (3.69) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (16.38), customer-15-friends-reward (3.20), policy-12-remote-2023 (2.51) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (15.36), customer-15-friends-reward (3.69), policy-15-refresh-sabbatical (2.70) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (9.83), customer-04-terms (0.93), policy-02-remote (0.84) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: tech-02-deploy (3.07), customer-03-faq (0.94), customer-04-terms (0.93) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (29.76), customer-13-edu-plan (2.56), customer-15-friends-reward (1.71) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (21.42), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (11.76), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (21.42), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (32.07), policy-13-onboarding-buddy (3.18), customer-12-terms-2022 (2.86) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (29.77), tech-12-incident-2021 (1.78), policy-15-refresh-sabbatical (0.82) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (32.07), customer-12-terms-2022 (2.86), tech-12-incident-2021 (1.78) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (8.81), tech-03-incident (3.09), customer-02-refund (1.38) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (8.53), tech-02-deploy (3.41), tech-03-incident (2.43) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (8.81), tech-03-incident (2.43) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (24.95), tech-13-hermes-api (4.32), tech-11-deploy-2022 (2.86) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (21.30), tech-13-hermes-api (4.32), policy-11-leave-2021 (2.85) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (21.30), tech-13-hermes-api (4.32), policy-11-leave-2021 (2.85) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (31.51), policy-12-remote-2023 (4.88), tech-12-incident-2021 (2.79) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (7.24) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (28.71), policy-12-remote-2023 (4.88), policy-13-onboarding-buddy (0.85) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (13.81), policy-03-education (1.86), customer-05-support (1.48) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | O | O | 없음 |
| 19 | E | keywords | 사내 주차 지원 | 없음 | O | O | 없음 |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (4.45) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | O | O | 없음 |
