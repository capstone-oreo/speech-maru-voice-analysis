#! /bin/bash

ORGANIZATION=$1
REPOSITORY=$2
DOCKER_COMPOSE_FILE=$3

# flask 컨테이너가 실행 중이면 종료한다
if [ "$(docker ps -aqf name="^flask")" ];
then
  echo "> flask container 제거"
  docker stop flask && docker rm flask
else
  echo "> 구동 중인 flask container가 없으므로 종료하지 않습니다."
fi

if [[ "$(docker images -q ghcr.io/"$ORGANIZATION"/"$REPOSITORY":latest 2> /dev/null)" != "" ]]; then
  echo "> latest image tag를 old로 변경"
  docker rmi ghcr.io/"$ORGANIZATION"/"$REPOSITORY":old
  docker tag ghcr.io/"$ORGANIZATION"/"$REPOSITORY":latest ghcr.io/"$ORGANIZATION"/"$REPOSITORY":old
  docker rmi ghcr.io/"$ORGANIZATION"/"$REPOSITORY":latest
fi

echo "> docker compose"
docker compose -f "$DOCKER_COMPOSE_FILE" up -d --build

sleep 10

# 실행 중인 flask container 확인
for RETRY_COUNT in $(seq 1 10)
do
  RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/test)

  if [ "$RESPONSE_CODE" -ge 400 ]
  then
    echo "> 응답 실패, Response code : $RESPONSE_CODE"
    sleep 0.5
  else
    echo "> 응답 성공"
    break
  fi

  if [ "$RETRY_COUNT" -eq 10 ]
  then
    echo "> 배포 실패"
    echo "> 배포에 실패한 container 삭제"
    docker stop flask && docker rm flask

    echo "> old image tag를 latest로 변경"
    docker rmi ghcr.io/"$ORGANIZATION"/"$REPOSITORY":latest
    docker tag ghcr.io/"$ORGANIZATION"/"$REPOSITORY":old ghcr.io/"$ORGANIZATION"/"$REPOSITORY":latest

    echo "> 이전 image 실행"
    docker compose -f "$DOCKER_COMPOSE_FILE" up -d --build
  fi
done