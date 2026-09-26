import json
import os

from http.server import BaseHTTPRequestHandler
from openai import OpenAI


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            # 1. 브라우저에서 보낸 데이터 읽기
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body)

            grade = data.get("grade", "")
            interest = data.get("interest", "")
            project_type = data.get("type", "")


            # 2. 필수 입력값 확인
            if not interest:
                self.send_json(
                    400,
                    {"error": "관심사를 입력해주세요."}
                )
                return


            # 3. 환경 변수에서 API Key 가져오기
            api_key = os.environ.get("OPENAI_API_KEY")

            if not api_key:
                self.send_json(
                    500,
                    {"error": "AI API 설정이 완료되지 않았습니다."}
                )
                return


            client = OpenAI(api_key=api_key)


            # 4. AI에게 전달할 프롬프트
            prompt = f"""
너는 초등학생을 위한 창의적인 디지털 창작 교육 전문가야.

다음 학생에게 혼자 또는 교사의 간단한 도움을 받아
도전할 수 있는 디지털 창작 프로젝트를 하나 제안해줘.

학생 정보:
- 학년: {grade}
- 관심사: {interest}
- 만들고 싶은 것: {project_type}

다음 형식으로 한국어로 답변해줘.

프로젝트 제목: 짧고 재미있는 제목

오늘의 미션:
2~3문장으로 프로젝트 목표 설명

만들어보기:
1. 첫 번째 단계
2. 두 번째 단계
3. 세 번째 단계
4. 네 번째 단계

한 단계 더 도전하기:
프로젝트를 완성한 뒤 추가할 수 있는 도전 과제 1개

조건:
- 해당 학년 학생이 이해할 수 있는 쉬운 표현을 사용해.
- 결과는 너무 길지 않게 작성해.
- 아이가 직접 만들고 싶어지는 방식으로 설명해.
"""


            # 5. OpenAI 호출
            response = client.responses.create(
                model="gpt-5-mini",
                input=prompt
            )


            ai_text = response.output_text


            # 6. 브라우저로 결과 반환
            self.send_json(
                200,
                {"result": ai_text}
            )


        except Exception as e:

            print("ERROR:", str(e))

            self.send_json(
                500,
                {"error": "AI 프로젝트 생성 중 오류가 발생했습니다."}
            )


    def send_json(self, status_code, data):

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(
                data,
                ensure_ascii=False
            ).encode("utf-8")
        )