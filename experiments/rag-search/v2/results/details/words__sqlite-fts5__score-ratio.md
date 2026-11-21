# words__sqlite-fts5__score-ratio

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (3.36), customer-03-faq (2.42), customer-01-plans (0.17) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (5.92) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (9.12), policy-02-remote (1.73) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | O | current: customer-03-faq (5.16), customer-02-refund (3.53), customer-01-plans (1.57) |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (4.32), policy-03-education (2.76), customer-01-plans (2.31) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (5.58), customer-01-plans (3.18), customer-03-faq (2.68) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | O | current: customer-03-faq (3.86), policy-02-remote (1.31), tech-02-deploy (1.27) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (2.30) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (8.23), policy-01-leave (2.55), policy-05-flextime (2.48) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (7.59), tech-03-incident (2.31), customer-03-faq (1.70) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (4.54) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (7.78), tech-03-incident (2.31), policy-01-leave (0.21) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | X | archive: tech-12-incident-2021 (5.09), customer-15-friends-reward (2.36), customer-11-refund-2023 (1.65) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (4.04), tech-05-access (2.72), tech-03-incident (2.51) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | X | archive: tech-12-incident-2021 (6.55), customer-15-friends-reward (3.12), customer-11-refund-2023 (1.65) |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (7.05), tech-01-api-v2 (2.76), tech-02-deploy (1.27) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (2.28) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (6.73), tech-01-api-v2 (3.28), customer-01-plans (1.72) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (6.75), policy-05-flextime (0.00), tech-05-access (0.00) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (9.99), policy-03-education (1.70) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (6.95), policy-01-leave (0.21), tech-02-deploy (0.20) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (8.21), policy-05-flextime (1.72), customer-02-refund (1.67) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | O | O | current: tech-04-backup (4.61) |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (8.21), policy-05-flextime (0.00), policy-02-remote (0.00) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | O | O | current: tech-05-access (9.09), customer-03-faq (4.04), tech-04-backup (3.23) |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | O | O | current: tech-05-access (7.47), customer-03-faq (4.04), tech-01-api-v2 (2.61) |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (8.16), tech-01-api-v2 (2.71), tech-04-backup (2.47) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | O | O | current: policy-05-flextime (6.20), customer-03-faq (4.04) |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (4.04) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (7.28), tech-05-access (0.22), tech-04-backup (0.21) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (4.04), policy-01-leave (2.32) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (4.69), customer-02-refund (1.01), customer-01-plans (0.87) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (2.32) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (13.66), policy-15-refresh-sabbatical (2.32) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | X | X | current: customer-03-faq (2.29), customer-04-terms (0.00), policy-02-remote (0.00) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (14.30), policy-15-refresh-sabbatical (2.65) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (3.86), customer-04-terms (0.00), policy-02-remote (0.00) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (5.44), tech-14-atlas-deploy-tool (2.23), policy-14-wellness-points (0.91) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | X | X | current: tech-01-api-v2 (2.97), policy-01-leave (0.68), customer-02-refund (0.64) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (9.12) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (7.35), policy-15-refresh-sabbatical (1.69) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (11.71), policy-15-refresh-sabbatical (1.69) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (6.70), policy-03-education (2.33), customer-01-plans (1.97) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (5.12), customer-01-plans (1.97), tech-03-incident (1.68) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (7.21), customer-01-plans (3.69), policy-03-education (2.01) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (4.73) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (4.04), tech-02-deploy (2.85), tech-03-incident (2.31) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (7.59), tech-03-incident (2.31) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (9.15) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | X | X | current: policy-01-leave (3.60) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | X | X | current: policy-01-leave (3.60) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | O | O | archive: tech-15-orion-monitoring-console (13.29) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (3.12) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (4.81), tech-03-incident (1.68) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (4.04), policy-03-education (0.22), tech-05-access (0.13) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | O | O | 없음 |
| 19 | E | keywords | 사내 주차 지원 | 없음 | X | X | current: policy-03-education (2.66), tech-02-deploy (1.40), tech-01-api-v2 (1.19) |
| 20 | E | polite | 안녕하세요 | 없음 | O | O | 없음 |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | X | X | archive: policy-15-refresh-sabbatical (2.27) |
