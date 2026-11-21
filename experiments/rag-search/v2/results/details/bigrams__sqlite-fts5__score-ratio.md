# bigrams__sqlite-fts5__score-ratio

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | X | X | 없음 |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (7.28), policy-05-flextime (1.72), policy-02-remote (0.00) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (16.66), policy-05-flextime (6.11), policy-02-remote (2.40) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | X | 없음 |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (9.24), policy-03-education (2.79), customer-01-plans (2.72) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (9.24), customer-01-plans (2.72), customer-03-faq (2.49) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (14.18), policy-13-onboarding-buddy (1.88), policy-15-refresh-sabbatical (1.86) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (4.63), customer-14-freepass (0.00), customer-13-edu-plan (0.00) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (16.38), policy-11-leave-2021 (4.25), tech-11-deploy-2022 (1.73) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | X | X | 없음 |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (12.59), tech-03-incident (2.34), customer-03-faq (1.60) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (7.92), tech-03-incident (2.34), policy-01-leave (0.00) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | O | current: customer-03-faq (12.31), tech-03-incident (3.65), tech-05-access (1.35) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (7.90), tech-03-incident (1.36), tech-05-access (1.35) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | X | 없음 |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (8.92), customer-01-plans (2.19), customer-03-faq (2.15) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (5.84), customer-01-plans (1.67), customer-02-refund (0.00) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (6.57), customer-01-plans (2.19), tech-01-api-v2 (0.66) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | X | X | 없음 |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (12.95), policy-03-education (3.44), policy-02-remote (2.72) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (9.46), policy-02-remote (2.72), policy-03-education (1.72) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | X | X | 없음 |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | X | X | 없음 |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (7.41), customer-03-faq (1.60), policy-05-flextime (0.00) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | X | 없음 |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | X | 없음 |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (4.57), tech-03-incident (1.71), tech-04-backup (1.53) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (16.49), policy-01-leave (4.38), customer-01-plans (1.74) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (15.90), customer-01-plans (2.37), policy-01-leave (2.30) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (8.52), customer-02-refund (1.03), customer-01-plans (0.88) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (2.30) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (15.76), policy-15-refresh-sabbatical (4.16), customer-15-friends-reward (3.60) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (14.28), customer-15-friends-reward (2.32), policy-12-remote-2023 (1.71) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (14.00), customer-15-friends-reward (3.60), policy-15-refresh-sabbatical (2.45) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (8.17), customer-04-terms (0.00), policy-02-remote (0.00) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: tech-02-deploy (2.34), customer-03-faq (0.00), customer-04-terms (0.00) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (25.76), customer-13-edu-plan (2.00), customer-15-friends-reward (1.28) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (19.31), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (10.55), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (19.31), policy-15-refresh-sabbatical (2.86), policy-14-wellness-points (1.26) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (28.93), policy-13-onboarding-buddy (3.07), customer-12-terms-2022 (2.69) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (26.25), tech-12-incident-2021 (1.77), policy-15-refresh-sabbatical (0.00) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (28.93), customer-12-terms-2022 (2.69), tech-12-incident-2021 (1.77) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | O | O | archive: tech-14-atlas-deploy-tool (25.02), tech-11-deploy-2022 (5.25), tech-15-orion-monitoring-console (3.65) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | O | O | archive: tech-14-atlas-deploy-tool (16.88), tech-11-deploy-2022 (3.25), policy-14-wellness-points (3.10) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (7.92), tech-03-incident (2.34) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (22.44), tech-13-hermes-api (4.21), tech-11-deploy-2022 (2.69) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (19.13), tech-13-hermes-api (4.21), policy-11-leave-2021 (2.68) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (19.13), tech-13-hermes-api (4.21), policy-11-leave-2021 (2.68) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (28.31), policy-12-remote-2023 (4.69), tech-12-incident-2021 (2.78) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (6.77) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (25.79), policy-12-remote-2023 (4.69), policy-13-onboarding-buddy (0.76) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (12.31), policy-03-education (0.83), policy-02-remote (0.74) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | O | O | 없음 |
| 19 | E | keywords | 사내 주차 지원 | 없음 | O | O | 없음 |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (4.09) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | O | O | 없음 |
