#!/usr/bin/env python3
"""Threads Graph API로 텍스트 게시물을 발행한다.

사용법:
    python publish_threads.py <text_file_path>

필요한 환경변수:
    THREADS_ACCESS_TOKEN  - Threads 장기 액세스 토큰
    THREADS_USER_ID       - Threads 사용자(계정) ID
"""
import os
import sys
import time
import requests

GRAPH_BASE = "https://graph.threads.net/v1.0"


def publish(text: str) -> str:
    token = os.environ["THREADS_ACCESS_TOKEN"]
    user_id = os.environ["THREADS_USER_ID"]

    # 1) 컨테이너 생성
    create_resp = requests.post(
        f"{GRAPH_BASE}/{user_id}/threads",
        data={
            "media_type": "TEXT",
            "text": text,
            "access_token": token,
        },
        timeout=30,
    )
    create_resp.raise_for_status()
    creation_id = create_resp.json()["id"]

    # Meta 권장: 컨테이너 생성 후 발행 전 잠시 대기
    time.sleep(20)

    # 2) 발행
    publish_resp = requests.post(
        f"{GRAPH_BASE}/{user_id}/threads_publish",
        data={
            "creation_id": creation_id,
            "access_token": token,
        },
        timeout=30,
    )
    publish_resp.raise_for_status()
    return publish_resp.json()["id"]


def main() -> None:
    if len(sys.argv) != 2:
        print("사용법: python publish_threads.py <text_file_path>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"'{path}' 파일이 비어 있습니다.", file=sys.stderr)
        sys.exit(1)

    if len(text) > 500:
        print(f"경고: 본문이 {len(text)}자로 Threads 제한(500자)을 초과할 수 있습니다.", file=sys.stderr)

    post_id = publish(text)
    print(f"발행 완료: post_id={post_id}")


if __name__ == "__main__":
    main()
