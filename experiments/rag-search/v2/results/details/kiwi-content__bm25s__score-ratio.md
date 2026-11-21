# kiwi-content__bm25s__score-ratio

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | X | X | 없음 |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (3.97), customer-04-terms (0.85), policy-05-flextime (0.78) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (6.34), policy-05-flextime (2.04), policy-02-remote (1.11) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | X | 없음 |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | X | X | 없음 |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | X | X | 없음 |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (2.23), tech-11-deploy-2022 (0.34), policy-13-onboarding-buddy (0.33) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | X | archive: policy-12-remote-2023 (2.05), customer-12-terms-2022 (0.63), tech-14-atlas-deploy-tool (0.60) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (4.49), policy-01-leave (1.73), policy-05-flextime (1.41) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (3.90), tech-03-incident (1.26), customer-02-refund (0.33) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (3.77), tech-03-incident (1.21), policy-05-flextime (0.31) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (3.78), tech-03-incident (1.14), policy-01-leave (0.20) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | X | 없음 |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | X | 없음 |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | X | 없음 |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (2.50), tech-01-api-v2 (0.86), customer-01-plans (0.65) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (1.74), customer-05-support (0.31), customer-01-plans (0.30) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (2.50), tech-01-api-v2 (0.86), customer-01-plans (0.65) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (3.45), customer-02-refund (0.62), policy-01-leave (0.50) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (4.65), tech-01-api-v2 (0.88), policy-03-education (0.75) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (3.14), policy-01-leave (0.20), customer-02-refund (0.19) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (3.60), customer-03-faq (0.88), policy-05-flextime (0.19) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | X | X | 없음 |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (3.60), customer-03-faq (0.88), policy-05-flextime (0.19) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | X | 없음 |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | X | 없음 |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | X | X | 없음 |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | X | 없음 |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (1.82) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (3.61), policy-01-leave (1.22), customer-01-plans (0.84) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | O | O | archive: customer-14-freepass (9.93), customer-12-terms-2022 (1.15), customer-11-refund-2023 (1.13) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (2.48), customer-02-refund (0.71), policy-03-education (0.60) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (0.94) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.60), customer-15-friends-reward (1.71), policy-15-refresh-sabbatical (1.30) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (5.66), customer-15-friends-reward (1.14), policy-15-refresh-sabbatical (0.08) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | O | O | archive: customer-13-edu-plan (6.60), customer-15-friends-reward (1.71), policy-15-refresh-sabbatical (1.30) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (5.01), customer-14-freepass (0.67), policy-14-wellness-points (0.62) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (2.76), policy-14-wellness-points (0.99), policy-13-onboarding-buddy (0.84) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | O | O | archive: policy-15-refresh-sabbatical (6.05), customer-13-edu-plan (1.01), customer-11-refund-2023 (0.98) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (5.64), policy-15-refresh-sabbatical (1.94), customer-12-terms-2022 (0.63) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (4.05) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | O | O | archive: policy-13-onboarding-buddy (5.64), policy-15-refresh-sabbatical (1.94), customer-12-terms-2022 (0.63) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.17), customer-12-terms-2022 (1.26), tech-12-incident-2021 (0.75) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (5.89), tech-12-incident-2021 (0.75), customer-12-terms-2022 (0.63) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | O | O | archive: tech-13-hermes-api (7.17), customer-12-terms-2022 (1.26), tech-12-incident-2021 (0.75) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (4.48), tech-04-backup (1.02), tech-01-api-v2 (0.56) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | 없음 |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (4.48), tech-04-backup (1.02), tech-01-api-v2 (0.56) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (3.96), tech-13-hermes-api (0.98), customer-12-terms-2022 (0.63) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.20), policy-11-leave-2021 (1.25), tech-13-hermes-api (0.98) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | O | O | archive: policy-14-wellness-points (5.20), policy-11-leave-2021 (1.25), tech-13-hermes-api (0.98) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.78), tech-03-incident (0.73), customer-02-refund (0.61) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.06), customer-03-faq (0.03), customer-04-terms (0.03) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (2.78), tech-03-incident (0.73) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | O | O | 없음 |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | O | O | 없음 |
| 19 | E | keywords | 사내 주차 지원 | 없음 | O | O | 없음 |
| 20 | E | polite | 안녕하세요 | 없음 | O | O | 없음 |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | O | O | 없음 |
