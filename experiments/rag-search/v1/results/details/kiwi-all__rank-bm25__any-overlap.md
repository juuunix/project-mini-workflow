# kiwi-all__rank-bm25__any-overlap

| # | 유형 | 말투 | 질문 | 정답 | Hit@1 | Hit@3 | 결과 (상위 3건) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | polite | 연차휴가 이월은 최대 며칠까지 가능한가요? | current: policy-01-leave | O | O | current: policy-01-leave (11.71), policy-05-flextime (8.58), policy-02-remote (4.03) |
| 1 | A | casual | 연차 이월 며칠까지 돼? | current: policy-01-leave | O | O | current: policy-01-leave (9.65), policy-05-flextime (3.20), customer-03-faq (2.18) |
| 1 | A | keywords | 연차휴가 이월 일수 | current: policy-01-leave | O | O | current: policy-01-leave (14.60), policy-05-flextime (4.57), policy-02-remote (2.49) |
| 2 | A | polite | 연간 결제를 환불하면 위약금이 있나요? | current: customer-02-refund | X | O | current: customer-03-faq (11.56), customer-02-refund (9.98), customer-01-plans (6.33) |
| 2 | A | casual | 연간 결제 환불하면 위약금 내? | current: customer-02-refund | O | O | current: customer-02-refund (7.65), customer-01-plans (4.43), customer-03-faq (4.30) |
| 2 | A | keywords | 연간 결제 환불 위약금 | current: customer-02-refund | O | O | current: customer-02-refund (6.38), customer-01-plans (2.88), customer-03-faq (2.61) |
| 3 | A | polite | 재택근무는 일주일에 며칠 할 수 있나요? | current: policy-02-remote | X | O | current: customer-03-faq (9.12), policy-02-remote (7.67), policy-05-flextime (6.45) |
| 3 | A | casual | 재택 일주일에 며칠 돼? | current: policy-02-remote | O | O | current: policy-02-remote (4.40), policy-05-flextime (4.15), customer-03-faq (2.49) |
| 3 | A | keywords | 재택근무 주간 최대 일수 | current: policy-02-remote | O | O | current: policy-02-remote (9.67), policy-01-leave (2.99), policy-05-flextime (2.57) |
| 4 | A | polite | 배포 후 롤백 기준은 무엇인가요? | current: tech-02-deploy | O | O | current: tech-02-deploy (11.43), tech-03-incident (4.94), customer-03-faq (3.72) |
| 4 | A | casual | 배포하고 롤백은 언제 해? | current: tech-02-deploy | O | O | current: tech-02-deploy (12.46), tech-03-incident (6.47), customer-03-faq (5.67) |
| 4 | A | keywords | 배포 롤백 기준 | current: tech-02-deploy | O | O | current: tech-02-deploy (9.20), tech-03-incident (2.78), policy-01-leave (0.75) |
| 5 | A | polite | 장애 등급은 어떻게 나뉘나요? | current: tech-03-incident | X | O | current: customer-03-faq (10.13), tech-05-access (2.44), tech-03-incident (2.34) |
| 5 | A | casual | 장애 등급 어떻게 나눠? | current: tech-03-incident | X | O | current: customer-03-faq (5.32), tech-03-incident (2.34), tech-05-access (2.32) |
| 5 | A | keywords | 장애 등급 구분 | current: tech-03-incident | X | O | current: tech-04-backup (1.55), tech-03-incident (1.46), tech-05-access (1.45) |
| 6 | B | polite | 교육비 지원 한도는 얼마인가요? | current: policy-03-education | O | O | current: policy-03-education (6.56), tech-01-api-v2 (2.79), customer-01-plans (2.66) |
| 6 | B | casual | 교육비 얼마까지 지원돼? | current: policy-03-education | O | O | current: policy-03-education (5.95), customer-03-faq (2.53), customer-01-plans (2.53) |
| 6 | B | keywords | 교육비 지원 한도 | current: policy-03-education | O | O | current: policy-03-education (4.88), tech-01-api-v2 (1.12), customer-01-plans (1.05) |
| 7 | B | polite | 해외 출장비 기준을 알려주세요. | current: policy-04-expense | O | O | current: policy-04-expense (9.49), customer-03-faq (7.19), policy-02-remote (2.86) |
| 7 | B | casual | 해외 출장 가면 출장비 얼마 나와? | current: policy-04-expense | O | O | current: policy-04-expense (12.62), policy-03-education (3.54), customer-03-faq (2.32) |
| 7 | B | keywords | 해외 출장비 기준 | current: policy-04-expense | O | O | current: policy-04-expense (7.72), policy-01-leave (0.75), customer-02-refund (0.72) |
| 8 | B | polite | 백업 보존 기간은 얼마인가요? | current: tech-04-backup | O | O | current: tech-04-backup (10.38), customer-03-faq (3.57), policy-05-flextime (2.44) |
| 8 | B | casual | 백업 얼마나 보관해? | current: tech-04-backup | O | O | current: tech-04-backup (6.08), customer-03-faq (3.92), customer-05-support (2.17) |
| 8 | B | keywords | 백업 보존 기간 | current: tech-04-backup | O | O | current: tech-04-backup (8.76), customer-03-faq (2.10), policy-05-flextime (0.73) |
| 9 | B | polite | 운영 환경 임시 권한은 어떻게 신청하나요? | current: tech-05-access | X | O | current: customer-03-faq (11.73), tech-05-access (8.31), tech-04-backup (4.22) |
| 9 | B | casual | 운영 서버 임시 권한 어떻게 받아? | current: tech-05-access | O | O | current: tech-05-access (6.81), customer-03-faq (6.03), tech-01-api-v2 (4.05) |
| 9 | B | keywords | 운영 환경 임시 권한 신청 | current: tech-05-access | O | O | current: tech-05-access (6.41), tech-04-backup (2.41), policy-02-remote (2.29) |
| 10 | B | polite | 선택적 근로시간제는 어떻게 운영되나요? | current: policy-05-flextime | X | O | current: customer-03-faq (13.05), policy-05-flextime (10.11), policy-01-leave (5.09) |
| 10 | B | casual | 선택근무제 어떻게 돌아가? | current: policy-05-flextime | X | X | current: customer-03-faq (5.32), policy-04-expense (0.90), tech-03-incident (0.88) |
| 10 | B | keywords | 선택적 근로시간제 운영 | current: policy-05-flextime | O | O | current: policy-05-flextime (8.73), policy-01-leave (3.70), customer-01-plans (3.17) |
| 11 | C | polite | 프리패스 이용권 잔여 쿠폰은 어떻게 관리하나요? | archive: customer-14-freepass | X | X | current: customer-03-faq (11.49), policy-04-expense (5.29), policy-01-leave (3.93) |
| 11 | C | casual | 프리패스 쿠폰 남은 거 어떻게 해? | archive: customer-14-freepass | X | X | current: customer-03-faq (7.59), policy-04-expense (4.91), customer-02-refund (3.52) |
| 11 | C | keywords | 프리패스 잔여 쿠폰 | archive: customer-14-freepass | X | X | current: policy-01-leave (2.23) |
| 12 | C | polite | 에듀 플랜 가입 자격은 무엇인가요? | archive: customer-13-edu-plan | X | X | current: customer-01-plans (5.81), customer-03-faq (4.92), tech-01-api-v2 (4.60) |
| 12 | C | casual | 에듀 플랜 누가 가입할 수 있어? | archive: customer-13-edu-plan | X | X | current: customer-03-faq (6.34), policy-02-remote (6.06), policy-04-expense (4.78) |
| 12 | C | keywords | 에듀 플랜 가입 자격 | archive: customer-13-edu-plan | X | X | current: customer-01-plans (3.03), customer-03-faq (2.25), tech-01-api-v2 (1.78) |
| 13 | C | polite | 리프레시 안식월은 누가 쓸 수 있나요? | archive: policy-15-refresh-sabbatical | X | X | current: customer-03-faq (9.58), policy-02-remote (5.27), tech-05-access (3.41) |
| 13 | C | casual | 안식월 누가 쓸 수 있어? | archive: policy-15-refresh-sabbatical | X | X | current: policy-02-remote (5.89), customer-03-faq (4.78), customer-02-refund (3.45) |
| 13 | C | keywords | 리프레시 안식월 사용 자격 | archive: policy-15-refresh-sabbatical | X | X | current: customer-01-plans (2.93), tech-01-api-v2 (2.30), policy-03-education (2.28) |
| 14 | C | polite | 온보딩 버디 활동비는 얼마인가요? | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (7.42), policy-05-flextime (3.44), tech-04-backup (3.40) |
| 14 | C | casual | 버디 활동비 얼마 나와? | archive: policy-13-onboarding-buddy | X | X | current: customer-03-faq (0.83), policy-03-education (0.79), policy-04-expense (0.77) |
| 14 | C | keywords | 온보딩 버디 활동비 | archive: policy-13-onboarding-buddy | X | X | current: customer-01-plans (5.80), tech-04-backup (1.77), policy-05-flextime (1.72) |
| 15 | D | polite | 헤르메스 API 호출 한도는 얼마인가요? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (8.23), customer-01-plans (4.08), tech-03-incident (3.99) |
| 15 | D | casual | 헤르메스 API 호출 몇 번까지 돼? | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (7.64), customer-01-plans (5.19), tech-03-incident (4.81) |
| 15 | D | keywords | 헤르메스 API 호출 한도 | archive: tech-13-hermes-api | X | X | current: tech-01-api-v2 (6.55), customer-01-plans (2.46), tech-03-incident (2.41) |
| 16 | D | polite | 아틀라스 배포 도구로 롤백하는 방법은? | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (13.45), tech-04-backup (5.35), tech-01-api-v2 (4.52) |
| 16 | D | casual | 아틀라스로 롤백 어떻게 해? | archive: tech-14-atlas-deploy-tool | X | X | current: customer-03-faq (7.00), tech-02-deploy (5.14), tech-03-incident (4.94) |
| 16 | D | keywords | 아틀라스 배포 도구 롤백 | archive: tech-14-atlas-deploy-tool | X | X | current: tech-02-deploy (10.58), tech-04-backup (2.18), tech-01-api-v2 (1.23) |
| 17 | D | polite | 웰니스 포인트는 이월되나요? | archive: policy-14-wellness-points | X | X | current: customer-03-faq (7.28), tech-01-api-v2 (4.67), customer-01-plans (3.05) |
| 17 | D | casual | 웰니스 포인트 이월 돼? | archive: policy-14-wellness-points | X | X | current: policy-01-leave (5.40), tech-01-api-v2 (3.67), customer-03-faq (1.66) |
| 17 | D | keywords | 웰니스 포인트 이월 | archive: policy-14-wellness-points | X | X | current: policy-01-leave (4.34), tech-01-api-v2 (2.20) |
| 18 | D | polite | 오리온 모니터링 콘솔의 경보 단계는? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (8.24), tech-03-incident (3.23), customer-02-refund (2.55) |
| 18 | D | casual | 오리온 경보 단계 뭐 있어? | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (6.33), customer-03-faq (1.66), policy-02-remote (1.50) |
| 18 | D | keywords | 오리온 모니터링 경보 단계 | archive: tech-15-orion-monitoring-console | X | X | current: tech-02-deploy (6.65), tech-03-incident (1.69) |
| 19 | E | polite | 사내 주차 지원은 어떻게 받나요? | 없음 | X | X | current: customer-03-faq (10.83), policy-03-education (2.57), customer-02-refund (2.03) |
| 19 | E | casual | 주차 지원 받을 수 있어? | 없음 | X | X | current: policy-03-education (4.18), customer-02-refund (4.18), customer-03-faq (4.02) |
| 19 | E | keywords | 사내 주차 지원 | 없음 | X | X | current: policy-03-education (1.08), customer-05-support (0.69), tech-02-deploy (0.68) |
| 20 | E | polite | 안녕하세요 | 없음 | X | X | current: customer-03-faq (5.34), customer-04-terms (0.91), tech-05-access (0.91) |
| 20 | E | casual | 안녕 | 없음 | O | O | 없음 |
| 20 | E | keywords | 인사 | 없음 | X | X | current: policy-03-education (0.73), policy-04-expense (0.73), policy-01-leave (0.73) |
