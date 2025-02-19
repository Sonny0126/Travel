document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");
    const startBtn = document.getElementById("startBtn");

    // 5개의 질문을 위한 데이터
    const questions = [
        { 
            text: "1. 누구와 떠나시나요?", 
            options: [
                { text: "나홀로", icon: "🧳" },
                { text: "연인과", icon: "👫" },
                { text: "친구와", icon: "👬" },
                { text: "가족과", icon: "👨‍👩‍👧" },
                { text: "효도", icon: "👴" },
                { text: "자녀와", icon: "👶" },
                { text: "반려동물과", icon: "🐱" }
            ]
        },
        { 
            text: "2. 어떻게 이동하시나요?", 
            options: [
                { text: "기차", icon: "🚄" },
                { text: "자동차", icon: "🚗" },
                { text: "버스", icon: "🚌" },
                { text: "자전거", icon: "🚲" },
            ]
        },
        { 
            text: "3. 어떤 여행을 원하시나요?", 
            options: [
                { text: "여유있는 일정", icon: "🦗" },
                { text: "알찬 일정", icon: "🐜" },
            ]
        },
        { 
            text: "4. 어떤 여행 스타일을 원하시나요?(중복 선택 가능)", 
            options: [
                { text: "힐링 여행", icon: "🌿" },
                { text: "액티비티", icon: "🏄" },
                { text: "문화 탐방", icon: "🏛️" },
                { text: "맛집 여행", icon: "🍽️" },
                { text: "자연 속 여행", icon: "🏕️" },
            ]
        },
        { 
            text: "5. 어디로 가고 싶으신가요?", 
            options: [
                { text: "바다", icon: "🌊" },
                { text: "산", icon: "⛰️" },
                { text: "드라이브", icon: "🚗" },
                { text: "산책", icon: "🚶" },
                { text: "쇼핑", icon: "🛍️" },
                { text: "실내 여행지", icon: "🏠" },
                { text: "시티투어", icon: "🏙️" }
            ]
        },

    ];

    let currentQuestionIndex = 0; // 현재 질문 인덱스

    // 질문 컨테이너 생성
    const questionContainer = document.createElement("div");
    questionContainer.id = "questionContainer";
    questionContainer.style.display = "none"; // 처음에는 숨김
    questionContainer.style.textAlign = "center";
    questionContainer.style.position = "absolute";
    questionContainer.style.top = "50%";
    questionContainer.style.left = "50%";
    questionContainer.style.transform = "translate(-50%, -50%)";
    questionContainer.style.backgroundColor = "white";
    questionContainer.style.padding = "20px";
    questionContainer.style.borderRadius = "15px";
    questionContainer.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";
    document.body.appendChild(questionContainer);

    // 질문과 옵션을 표시하는 함수
    function showQuestion(index) {
        if (index >= questions.length) {
            // 마지막 질문이 끝난 후 탐색 메시지 표시
            questionContainer.innerHTML = `<h2 style="color: #F79C34;">Loading...</h2>`;
            
            // 2초 후 loading.html로 이동
            setTimeout(() => {
                window.location.href = "loading.html";
            });
            return;
        }

        const questionData = questions[index];
        questionContainer.innerHTML = ""; // 이전 질문 제거

        // 질문 추가
        const questionText = document.createElement("h2");
        questionText.innerText = questionData.text;
        questionText.style.color = "#F79C34";
        questionContainer.appendChild(questionText);

        // 버튼 컨테이너 생성
        const buttonContainer = document.createElement("div");
        buttonContainer.style.display = "flex";
        buttonContainer.style.flexWrap = "wrap";
        buttonContainer.style.justifyContent = "center";
        buttonContainer.style.gap = "10px";

        // 옵션 버튼 추가
        questionData.options.forEach(option => {
            const button = document.createElement("button");
            button.innerHTML = `${option.text} ${option.icon}`;
            button.style.padding = "10px 20px";
            button.style.border = "none";
            button.style.borderRadius = "10px";
            button.style.fontSize = "16px";
            button.style.cursor = "pointer";
            button.style.backgroundColor = "#f1f1f1";
            button.style.transition = "0.3s";

            // 버튼 클릭 시 다음 질문으로 이동
            button.addEventListener("click", () => {
                document.querySelectorAll("#questionContainer button").forEach(btn => btn.style.backgroundColor = "#f1f1f1");
                button.style.backgroundColor = "#D4F4BE"; // 선택된 버튼 색 변경
                setTimeout(() => {
                    showQuestion(index + 1); // 다음 질문 표시
                }, 500);
            });

            buttonContainer.appendChild(button);
        });

        questionContainer.appendChild(buttonContainer);
    }

    // Start 버튼 클릭 시 첫 번째 질문 표시
    startBtn.addEventListener("click", function () {
        startBtn.style.display = "none"; // Start 버튼 숨기기
        questionContainer.style.display = "block"; // 질문 표시
        showQuestion(0); // 첫 번째 질문부터 시작
    });
});
