function inform() {
    let person = document.querySelectorAll(".person");
    console.log(person);
    for (let pers of person) {
        animateLine(pers);

        let infoFullNode = pers.lastElementChild;
        pers.addEventListener("click", function() {
            setTimeout(function() {
                if (!infoFullNode.classList.contains("active")) {
                    infoFullNode.classList.add("active");
                    setTimeout(function() {
                        infoFullNode.classList.add("animate-line-full");
                    }, 500);
                    let infoNode = infoFullNode.previousElementSibling;
                    if (infoNode.lastElementChild.classList.contains("online") || infoNode.parentElement.getAttribute('id')) {
                        statLight(infoFullNode, true);
                    }
                } else {
                    infoFullNode.classList.remove("active");
                    infoFullNode.classList.remove("animate-line-full");
                    statLight(infoFullNode, false);
                }
            }, 0);
        });
    }
}

function animateLine(person) {
    let info = person.firstElementChild;
    person.addEventListener("mouseenter", function() {
        if (info.classList.contains("animate-line-info-after")) {
            info.classList.remove("animate-line-info-after");
        }
        info.classList.add("animate-line-info");

        person.addEventListener("mouseleave", function() {
            info.classList.remove("animate-line-info");
            info.classList.add("animate-line-info-after");
        });
    });
}

function lightLiTag(value, color, shadow, time) {
    let timer = 350;
    for(let liTag of value.children) {
        setTimeout(function() {
            liTag.style.color = color;
            liTag.style.textShadow = shadow;
        }, timer);
        timer += time;
    }
}

function statLight(element, bull) {
    let infoValue = element.lastElementChild;
    let infoElements = infoValue.previousElementSibling;
    if(bull) {
        lightLiTag(infoValue, "white", "0 0 10px rgba(255, 255, 255, 0.61)", 150);
        lightLiTag(infoElements, "white", "0 0 10px rgba(255, 255, 255, 0.61)", 150);
    } else {
        lightLiTag(infoValue, "#e0e0e085", "none", -30);
        lightLiTag(infoElements, "#e0e0e085", "none", -30);
    }
}

function minuteToString(minute) {
    let min = minute % 60;
    let hours = parseInt((minute - min) / 60) % 24;
    let days = parseInt(parseInt((minute - min) / 60) / 24);
    return `${days} д. ${hours} ч. ${min} мин.`;
}

async function curse(currency) {
    const requestURL = 'https://api.binance.com/api/v3/ticker/price?symbol=ETH' + currency;

    let response = await fetch(requestURL);
    if (response.ok) {
        let json = await response.json();
        return json.price
    } else {
        return 1;
    }
}

async function updateList() {
    const requestURL = '/api/stats';
    const xhr = new XMLHttpRequest();
    let textStatus, classStatus;
    let rubCurse = await curse('RUB'), usdCurse = await curse('USDT');
    xhr.open('GET', requestURL, false);
    xhr.onreadystatechange = function () {
        if (xhr.readyState !== 4 || xhr.status !== 200) {
            return;
        }
        const response = JSON.parse(xhr.responseText);
        const listElement = document.getElementsByClassName('main__person')[0];
        let html = [];

        console.log(rubCurse);
        response.miners.forEach(element => {
            if (element.is_online == true) {
                textStatus = "Online";
                classStatus = "online";
            } else {
                textStatus = "Offline";
                classStatus = "offline";
            }
            html.unshift('<li class="person">' +
            '<div class="info">' +
            '<span></span><span></span>' +
            '<div class="info-name">' + element.name + '</div>' +
                '<div class="info-name">' + Math.round(response.balance * element.share * rubCurse) + ' RUB</div>' +
                '<div class="info-status ' + classStatus + '">' + textStatus + '</div>' +
                '</div>' +
            '<div class="full-info">' +
            '<span></span><span></span><span></span><span></span>' +
                '<ul class="full-info-elements">' +
                    '<li>Средний хешрейт: </li>' +
                    '<li>Хешрейт в работе: </li>' +
                    '<li>Доля, %: </li>' +
                    '<li>ETH: </li>' +
                    '<li>USD: </li>' +
                    '<li>Время работы: </li>' +
                '</ul>' +
                '<ul class="full-info-value">' +
                    '<li>' + element.general_hr + '</li>' +
                    '<li>' + element.hr + '</li>' +
                    '<li>' + (element.share * 100).toFixed(2) + '</li>' +
                    '<li>' + (response.balance * element.share).toFixed(8) + '</li>' +
                    '<li>' + (response.balance * element.share * usdCurse).toFixed(2) + '</li>' +
                    '<li>' + minuteToString(element.working_time) + '</li>' +
                '</ul>' +
            '</div>' +
            '</li>');
        }); 
        html.push('<li class="person" id="sum">' +
        '<div class="info">' +
            '<span></span><span></span>' +
            '<div class="info-name">Сумма</div>' +
        '</div>' +
        '<div class="full-info">' +
            '<span></span><span></span><span></span><span></span>' +
            '<ul class="full-info-elements">' +
                '<li>ETH</li>' +
                '<li>USD</li>' +
                '<li>RUB</li>' +
                '<li>Время работы</li>' +
            '</ul>' +
            '<ul class="full-info-value">' +
                '<li>' + response.balance + '</li>' +
                '<li>' + (response.balance * usdCurse).toFixed(2) + '</li>' +
                '<li>' + Math.round(response.balance * rubCurse) + '</li>' +
                '<li>' + minuteToString(response.time) + '</li>' +
            '</ul>' +
        '</div>' +
    '</li>');
        listElement.innerHTML = html.join('');
    }
    xhr.send();


}
// после готовности DOM
document.addEventListener('DOMContentLoaded', async function () {
    await updateList();
    inform();
//setTimeout(inform, 5000);
});

function updateTitle() {
    const url = "https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT";

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myObj = JSON.parse(this.responseText);
            //document.getElementById("demo").innerHTML = myObj.name;
            console.log(myObj);
            document.title = myObj["lastPrice"]/1 + " (" + myObj["priceChangePercent"] + " %)";
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

updateTitle();
setInterval(updateTitle, 5000);