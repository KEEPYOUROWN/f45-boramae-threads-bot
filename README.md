# F45 보라매 Threads 자동 발행 봇

해외 피트니스 트렌드를 참고해 F45 보라매 톤으로 재구성한 **오리지널** 한국어 콘텐츠를
Threads에 정기적으로 발행하는 자동화입니다.

> 원문을 그대로 번역해 올리지 않습니다 (저작권 문제). 트렌드/주제만 참고하고
> 문구는 항상 새로 작성합니다.

## 구조

1. Claude 클라우드 루틴(예약 실행)이 트렌드를 리서치하고 한국어 원고를 작성해
   `queue/YYYY-MM-DD.txt`로 커밋 & 푸시합니다.
2. GitHub Actions(`.github/workflows/publish.yml`)가 해당 push를 감지해
   `scripts/publish_threads.py`로 실제 Threads 발행을 수행합니다.
3. 발행이 끝나면 파일을 `queue/published/`로 이동시켜 기록을 남깁니다.

Threads 액세스 토큰은 **GitHub Actions Secrets에만** 존재하며, Claude 루틴에는
절대 전달되지 않습니다.

## 설정 방법

### 1. Meta Threads API 앱 만들기

1. https://developers.facebook.com 에서 새 앱 생성 (유형: Business)
2. 앱에 **Threads API** 제품 추가
3. F45 보라매 Threads 계정을 테스터로 초대 후 수락
4. OAuth로 `threads_content_publish` 스코프 포함해 인증 → 액세스 토큰 발급
   (단기 토큰은 장기 토큰으로 교환)
5. Threads 사용자 ID 확인 (`GET /v1.0/me?access_token=...`)

### 2. GitHub Secrets 등록

레포 Settings → Secrets and variables → Actions 에서 추가:

- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`

### 3. 로컬 테스트

```bash
pip install -r requirements.txt
export THREADS_ACCESS_TOKEN=xxx
export THREADS_USER_ID=xxx
echo "테스트 게시물입니다" > /tmp/test.txt
python scripts/publish_threads.py /tmp/test.txt
```

## 장기 토큰 갱신

Threads 장기 토큰은 60일마다 만료됩니다. 만료 전 갱신이 필요하며, 별도
갱신 자동화(또는 캘린더 리마인더)를 권장합니다.
