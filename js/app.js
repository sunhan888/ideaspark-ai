const form = document.getElementById("projectForm");
const gradeInput = document.getElementById("grade");
const interestInput = document.getElementById("interest");
const typeInput = document.getElementById("type");

const message = document.getElementById("message");
const result = document.getElementById("result");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const grade = gradeInput.value;
    const interest = interestInput.value.trim();
    const type = typeInput.value;

    // 1. 빈 입력 확인
    if (!interest) {
        message.textContent = "⚠️ 관심사를 하나 입력해주세요.";
        return;
    }

    message.textContent = "✨ AI가 프로젝트를 만들고 있어요...";

    const button = form.querySelector(".generate-button");
    button.disabled = true;

    result.innerHTML = `
        <div class="result-placeholder">
            <div class="placeholder-icon">🤖</div>
            <h3>CREATING...</h3>
            <p>AI가 아이에게 맞는 프로젝트를 생각하고 있어요.</p>
        </div>
    `;

    try {

        // 2. Python 백엔드로 요청
        const response = await fetch("/api/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                grade: grade,
                interest: interest,
                type: type
            })
        });


        // 3. Python이 보내준 JSON 읽기
        const data = await response.json();


        // 4. API 오류 처리
        if (!response.ok) {
            throw new Error(
                data.error || "AI 요청에 실패했습니다."
            );
        }


        // 5. AI 결과 화면에 표시
        result.innerHTML = `
            <div class="ai-result">

                <p class="result-label">
                    YOUR AI PROJECT
                </p>

                <h3>
                    ${interest} × ${type}
                </h3>

                <p style="white-space: pre-line;">
                    ${escapeHtml(data.result)}
                </p>

            </div>
        `;

        message.textContent = "✅ 프로젝트가 완성되었습니다!";

    }

    catch (error) {

        console.error(error);

        message.textContent =
            "😢 프로젝트를 만들지 못했어요. 잠시 후 다시 시도해주세요.";

        result.innerHTML = `
            <div class="result-placeholder">
                <div class="placeholder-icon">😢</div>

                <h3>ERROR</h3>

                <p>
                    AI 프로젝트 생성 중 문제가 발생했습니다.<br>
                    잠시 후 다시 시도해주세요.
                </p>
            </div>
        `;
    }

    finally {

        // 성공/실패 관계없이 버튼 다시 활성화
        button.disabled = false;
    }

});


// AI 응답을 HTML에 안전하게 표시
function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}