import logging

# 로그를 설정하지 않은 프로그램에서는 mini_agent의 기록을 아무 데도 내보내지 않는다.
# 처리기가 하나도 없으면 logging이 WARNING 이상을 화면(stderr)에 대신 출력하기 때문이다.
logging.getLogger(__name__).addHandler(logging.NullHandler())
