# 전남대학교 학사공지
[![Discord](https://img.shields.io/badge/참여하기-전남대학교%20학사공지-7289DA?logo=discord&logoColor=white)](https://jnu.ho9.me)

`rss-check-bot__jnu`는 전남대학교 각 학과사이트의 RSS 피드를 파싱하여 특정 디스코드 채널로 결과를 전송하는 챗봇입니다. RSS 피드를 읽어들여 실행 시각으로부터 24시간 전에 게시된 게시물을 가져옵니다.  

이 챗봇은 Github Actions를 통해 24시간에 한번씩 자동으로 작동합니다. 자세한 내용은 [run_automatic.yml](./.github/workflows/run_automatic.yml)을 참조하세요.

## 시작하기
### 의존성 패키지 설치
```sh
pip install -r requirements.txt
```

### `config.json` 설정
이 저장소는 실제 디스코드 서버와 연동되어 있어 파싱 대상 학과가 이미 지정되어 있습니다. `config.json`을 참조하세요.  

```json
{
  "KEY": "봇 인증키 (공란으로 두면 `discord_key` 환경 변수를 가져옵니다.)",
  "get_notice_limit": "(정수형) 읽어들일 게시물 개수",
  "targets": {
    "학과 서브도메인": {
      "name": "학과명",
      "host": "학과 도메인",
      "rss": "RSS 피드",
      "format": "이후 하위호환성 지원용 ('default', ...)",
      "discord": "(정수형) 디스코드 채널 ID"
    },
    ...
  }
}
```

#### 디스코드 설정
[디스코드 개발자 포털](https://discord.com/developers)에서 애플리케이션을 생성하고 봇을 서버에 추가하세요. `config.json`은 이미 봇이 대상 서버에 추가되었다는 전제 하에 처리됩니다.  

* 디스코드 채널 ID는 `설정 > 고급 > 개발자 모드`를 활성화하면 채널을 우클릭하여 복사할 수 있습니다.
