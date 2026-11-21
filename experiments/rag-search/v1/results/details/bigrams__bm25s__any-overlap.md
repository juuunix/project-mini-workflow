# bigrams__bm25s__any-overlap

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (7.82), policy-05-flextime (3.76), customer-03-faq (3.49) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (3.73), policy-05-flextime (1.00), policy-02-remote (0.25) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (7.93), policy-05-flextime (2.77), policy-02-remote (1.10) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | O | current: customer-03-faq (6.62), customer-02-refund (5.99), customer-01-plans (3.06) |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (5.37), customer-01-plans (2.45), customer-03-faq (2.34) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (5.19), customer-01-plans (2.22), customer-03-faq (2.06) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | O | current: policy-05-flextime (6.34), policy-02-remote (5.41), customer-03-faq (3.74) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | X | O | current: policy-05-flextime (1.67), policy-02-remote (1.67), customer-05-support (0.44) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (7.57), policy-05-flextime (4.48), policy-01-leave (1.76) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (4.05), customer-03-faq (1.82), tech-03-incident (1.30) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (5.77), tech-03-incident (1.14), customer-03-faq (0.76) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (3.94), tech-03-incident (1.17), policy-01-leave (0.20) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | O | current: customer-03-faq (5.59), tech-03-incident (2.44), tech-05-access (1.29) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (3.56), tech-03-incident (1.48), tech-05-access (1.29) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | O | O | current: tech-03-incident (1.48), tech-04-backup (1.35), tech-05-access (1.29) |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (4.85), customer-01-plans (1.55), tech-01-api-v2 (1.44) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (3.26), customer-01-plans (1.21), customer-02-refund (0.46) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (3.77), customer-01-plans (1.55), tech-01-api-v2 (0.82) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (4.81), customer-03-faq (3.81), policy-02-remote (1.66) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (6.13), policy-03-education (1.52), policy-02-remote (1.27) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (4.60), policy-02-remote (1.44), policy-03-education (0.76) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (3.67), customer-03-faq (1.73), policy-05-flextime (1.21) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | O | O | current: tech-04-backup (2.15), customer-04-terms (1.36), customer-03-faq (1.11) |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (3.67), customer-03-faq (0.84), policy-05-flextime (0.19) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | O | current: customer-03-faq (7.70), tech-05-access (5.38), tech-04-backup (2.48) |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | X | O | current: customer-03-faq (3.90), tech-05-access (3.23), tech-02-deploy (1.50) |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (3.82), tech-04-backup (1.70), policy-02-remote (1.46) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | O | O | current: policy-05-flextime (9.02), customer-03-faq (8.89), policy-01-leave (2.13) |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | O | current: customer-03-faq (4.14), policy-05-flextime (3.98), policy-02-remote (3.07) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (8.40), policy-01-leave (2.13), customer-01-plans (0.96) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (7.80), customer-01-plans (1.44), customer-04-terms (1.13) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (3.97), customer-02-refund (0.72), customer-01-plans (0.61) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (0.96) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | X | X | current: customer-01-plans (2.81), customer-03-faq (1.97), policy-03-education (1.18) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | X | X | current: customer-03-faq (2.00), tech-02-deploy (1.00), policy-04-expense (0.65) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | X | X | current: customer-01-plans (1.46), policy-03-education (1.18), customer-03-faq (1.08) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (3.74), customer-04-terms (0.03), policy-02-remote (0.02) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: tech-02-deploy (1.00), customer-03-faq (0.03), customer-04-terms (0.03) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | X | X | current: policy-03-education (1.28), customer-01-plans (1.05), tech-01-api-v2 (0.88) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (1.05), policy-04-expense (1.03), customer-03-faq (0.89) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (1.05), tech-04-backup (0.78) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (1.05), tech-04-backup (0.78) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (5.06), customer-01-plans (2.53), policy-03-education (1.84) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (3.90), customer-01-plans (2.18), customer-02-refund (1.42) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (4.44), customer-01-plans (2.53), customer-02-refund (1.61) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (3.75), tech-03-incident (1.50), customer-02-refund (0.86) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (3.56), tech-02-deploy (1.50), tech-03-incident (1.07) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (3.75), tech-03-incident (1.07) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | X | X | current: customer-03-faq (3.56), tech-01-api-v2 (2.51), policy-01-leave (1.83) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | X | X | current: policy-01-leave (1.83), tech-01-api-v2 (1.58) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | X | X | current: policy-01-leave (1.83), tech-01-api-v2 (1.58) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (4.07), tech-03-incident (1.98), policy-02-remote (1.28) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (3.02) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (4.07), tech-03-incident (1.98), policy-02-remote (1.28) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (5.75), policy-03-education (1.58), policy-02-remote (1.12) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | X | X | current: tech-02-deploy (1.25), customer-03-faq (1.21), tech-01-api-v2 (0.78) |
| 19 | E | keywords | 사내 주차 지원 | 없음 | X | X | current: policy-03-education (0.97), tech-02-deploy (0.56), policy-02-remote (0.50) |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (1.86) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | X | X | current: policy-04-expense (0.70), policy-03-education (0.70), policy-01-leave (0.70) |
