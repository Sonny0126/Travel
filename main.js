document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");
    const startBtn = document.getElementById("startBtn");

    // 여행 선택 화면 생성
    const selectionContainer = document.createElement("div");
    selectionContainer.id = "selectionContainer";
    selectionContainer.style.display = "none"; // 처음에는 숨김
    selectionContainer.style.textAlign = "center";
    selectionContainer.style.position = "absolute";
    selectionContainer.style.top = "50%";
    selectionContainer.style.left = "50%";
    selectionContainer.style.transform = "translate(-50%, -50%)";
    selectionContainer.style.backgroundColor = "white";
    selectionContainer.style.padding = "20px";
    selectionContainer.style.borderRadius = "15px";
    selectionContainer.style.boxShadow = "0 4px 8px rgba(0,0,0,0.2)";

    // 질문 추가
    const question = document.createElement("h2");
    question.innerText = "1. 누구와 떠나시나요?";
    question.style.color = "#F79C34"; // 주황색
    selectionContainer.appendChild(question);

    // 선택 버튼 추가
    const options = [
        { text: "나홀로", icon: "🧳" },
        { text: "연인과", icon: "👫" },
        { text: "친구와", icon: "👬" },
        { text: "가족과", icon: "👨‍👩‍👧" },
        { text: "효도", icon: "👴" },
        { text: "자녀와", icon: "👶" },
        { text: "반려동물과", icon: "🐱" }
    ];

    const buttonContainer = document.createElement("div");
    buttonContainer.style.display = "flex";
    buttonContainer.style.flexWrap = "wrap";
    buttonContainer.style.justifyContent = "center";
    buttonContainer.style.gap = "10px";
    
    options.forEach(option => {
        const button = document.createElement("button");
        button.innerHTML = `${option.text} ${option.icon}`;
        button.style.padding = "10px 20px";
        button.style.border = "none";
        button.style.borderRadius = "10px";
        button.style.fontSize = "16px";
        button.style.cursor = "pointer";
        button.style.backgroundColor = "#f1f1f1";
        button.style.transition = "0.3s";

        button.addEventListener("click", () => {
            document.querySelectorAll("#selectionContainer button").forEach(btn => btn.style.backgroundColor = "#f1f1f1");
            button.style.backgroundColor = "#D4F4BE"; // 선택된 버튼 색 변경 (초록)
        });

        buttonContainer.appendChild(button);
    });

    selectionContainer.appendChild(buttonContainer);
    document.body.appendChild(selectionContainer);

    // Start 버튼 클릭 시 동작
    startBtn.addEventListener("click", function () {
        startBtn.style.display = "none"; // Start 버튼 숨기기
        selectionContainer.style.display = "block"; // 선택 화면 표시
    });
});
