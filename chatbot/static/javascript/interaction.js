document.addEventListener('click', function(event) {
    const targetElement = event.target;
    if (targetElement.id || targetElement.className) {
        const data = {
            eventType: 'click',
            elementId: targetElement.id,
            elementClass: targetElement.className, // 클래스 이름
            elementType: targetElement.tagName, // 타입(예: BUTTON, A 등)
            elementName: targetElement.name, // name 속성
            timestamp: new Date().toISOString(),
        };
        sendLogData(data);
    }
});

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // 폼의 기본 제출 동작을 방지
    const targetElement = event.target;
    const formData = new FormData(event.target);
    const data = {
        eventType: 'formSubmit',
        elementId: targetElement.id,
        // elementName: targetElement.name, // name 속성
        formData: Object.fromEntries(formData.entries()), // 폼 데이터를 객체로 변환
        timestamp: new Date().toISOString(),
    };
    sendLogData(data);
});

window.addEventListener('load', function(event) {
    const targetElement = event.target;
    const data = {
        eventType: 'pageView',
        elementId: targetElement.id,
        url: window.location.href, // 현재 페이지 URL
        timestamp: new Date().toISOString(),
    };
    sendLogData(data);
});

window.addEventListener('scroll', function(event) {
    const targetElement = event.target;
    const scrollPosition = window.scrollY; // 수직 스크롤 위치
    const data = {
        eventType: 'scroll',
        elementId: targetElement.id,
        scrollPosition: scrollPosition,
        timestamp: new Date().toISOString(),
    };
    sendLogData(data);
});

window.addEventListener('error', function(event) {
    const targetElement = event.target;
    const data = {
        eventType: 'error',
        elementId: targetElement.id,
        message: event.message, // 오류 메시지
        filename: event.filename, // 오류가 발생한 파일
        lineno: event.lineno, // 오류가 발생한 줄 번호
        timestamp: new Date().toISOString(),
    };
    sendLogData(data);
});

// 쿠키 수집 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 로그데이터 전송 함수
function sendLogData(data) {
    fetch('/log_interaction/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
    }).then(response => {
        if(response.ok) {
            console.log('Log data sent successfully');
        } else {
            console.error('Failed to send log data');
        }
    }).catch(error => console.error('Error sending log data:', error));
}


