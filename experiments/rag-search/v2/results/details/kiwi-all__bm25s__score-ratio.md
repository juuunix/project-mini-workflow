# kiwi-all__bm25s__score-ratio

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | X | X | 없음 |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (3.72), policy-05-flextime (1.03), customer-03-faq (0.29) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (6.33), policy-05-flextime (2.01), policy-02-remote (1.10) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | X | 없음 |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | X | X | 없음 |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | X | X | 없음 |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (2.14), customer-14-freepass (0.25), policy-15-refresh-sabbatical (0.25) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (2.20), customer-14-freepass (0.20), tech-15-orion-monitoring-console (0.19) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (4.44), policy-01-leave (1.73), policy-05-flextime (1.39) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (3.98), tech-03-incident (1.33), customer-03-faq (0.84) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (3.81), tech-03-incident (1.25), customer-03-faq (0.89) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (3.80), tech-03-incident (1.16), policy-01-leave (0.20) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | X | 없음 |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | X | 없음 |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | X | 없음 |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (2.55), tech-01-api-v2 (0.93), customer-01-plans (0.71) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (2.02), customer-01-plans (0.52), customer-02-refund (0.50) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (2.49), tech-01-api-v2 (0.88), customer-01-plans (0.66) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | X | X | 없음 |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (4.79), policy-03-education (0.93), customer-03-faq (0.24) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (3.11), policy-01-leave (0.20), customer-02-refund (0.19) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (3.69), customer-03-faq (0.88), policy-05-flextime (0.25) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | X | X | 없음 |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (3.64), customer-03-faq (0.84), policy-05-flextime (0.19) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | X | 없음 |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | X | 없음 |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | X | X | 없음 |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (2.38), customer-04-terms (0.42), tech-05-access (0.34) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (4.26), policy-01-leave (1.50), customer-01-plans (1.33) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | O | O | archive: customer-14-freepass (11.27), policy-13-onboarding-buddy (1.60), customer-15-friends-reward (1.36) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | O | O | archive: customer-14-freepass (6.88), policy-13-onboarding-buddy (1.34), customer-15-friends-reward (0.70) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (0.93) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.63), customer-15-friends-reward (2.36), policy-15-refresh-sabbatical (1.35) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (5.84), customer-15-friends-reward (1.32), customer-12-terms-2022 (0.28) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.57), customer-15-friends-reward (1.68), policy-15-refresh-sabbatical (1.29) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (5.10), customer-14-freepass (0.83), policy-14-wellness-points (0.78) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (2.35), customer-14-freepass (0.85), policy-14-wellness-points (0.81) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (5.51), customer-13-edu-plan (1.03), customer-15-friends-reward (0.85) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (2.68), tech-04-backup (0.84), policy-05-flextime (0.82) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (4.07), customer-14-freepass (0.03), policy-14-wellness-points (0.03) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (2.62), tech-04-backup (0.78), policy-05-flextime (0.76) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.26), customer-12-terms-2022 (1.31), tech-12-incident-2021 (0.84) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (6.62), customer-14-freepass (0.92), customer-15-friends-reward (0.91) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.20), customer-12-terms-2022 (1.25), tech-12-incident-2021 (0.79) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (4.63), tech-04-backup (1.15), tech-01-api-v2 (0.70) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | 없음 |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (4.53), tech-04-backup (1.04), tech-01-api-v2 (0.59) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (4.17), tech-13-hermes-api (1.21), customer-14-freepass (0.22) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.35), policy-11-leave-2021 (1.34), tech-13-hermes-api (1.16) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.19), policy-11-leave-2021 (1.25), tech-13-hermes-api (0.99) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.87), tech-03-incident (0.79), customer-02-refund (0.67) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.09), customer-03-faq (0.06), policy-02-remote (0.05) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.82), tech-03-incident (0.74) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (4.72), policy-03-education (1.27), tech-03-incident (0.97) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | O | O | 없음 |
| 19 | E | keywords | 사내 주차 지원 | 없음 | O | O | 없음 |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (1.89), customer-04-terms (0.03), tech-05-access (0.03) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | O | O | 없음 |
