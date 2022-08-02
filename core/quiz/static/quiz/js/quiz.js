const url = window.location.href

// Загрузка pk и перебор Блоков и Направлений
const data_ = {}
$.ajax({
    type: 'GET',
    url: `${url}block-data`,
    success: function(response) {
        const data = response.data
        data.forEach(el => {
            for (const[key, values] of Object.entries(el)) {
                data_[key] = values
            }
        })
    },
    error: function(error) {
        console.log(error)
    }
})

const direction = document.getElementById('direction-box')
const restDirection = document.getElementById('rest-direction')
const directionForm = document.getElementById('direction-form')

// перебор вопросов по направлениям и блокам...
let count = 0
let bCount = 0
let dCount = 0
restDirection.onclick = function () {
    if (count) {
        const setDCount = dCount - 1
        const setDirect = Object.keys(data_)[bCount] + '/' + Object.values(data_)[bCount][setDCount] + '/'
        const setUrl = url + setDirect
        setData(setUrl)
    }
    ++count
    cleanData()
    restDirection.innerHTML = `Далее`
    const direct = dCount < Object.values(data_)[bCount].length
    const block = bCount < Object.keys(data_)[bCount].length
    if (direct) {
        const direction = Object.keys(data_)[bCount] + '/' + Object.values(data_)[bCount][dCount] + '/'
        const loadUrl = url + direction
        loadData(loadUrl)
        ++dCount
    }
    else if (block) {
        dCount = 0
        ++bCount
        const direction = Object.keys(data_)[bCount] + '/' + Object.values(data_)[bCount][dCount] + '/'
        const loadUrl = url + direction
        loadData(loadUrl)
        ++dCount
   }
   else {
       directionForm.innerHTML = '<h3>Тестирование завершено. Результаты будут доступны после окончания вступительных испытаний.</h3>'
       console.log("Конец цикла!")
   }
}

// Получение вопросов и ответов по нажатию кнопки
function loadData(url) {
    $.ajax({
        type: 'GET',
        url: `${url}data`,
        success: function (response) {
            const data = response.data
            data.forEach(el => {
                for (const [question, answers] of Object.entries(el)) {
                    direction.innerHTML += `
                        <hr>
                        <div class="quest mb-2">
                            <b>${question}</b>
                        </div>
                    `
                    answers.forEach(answer => {
                        direction.innerHTML += `
                            <div>
                                <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}">${answer}</label>
                            </div>
                        `
                    })
                }
            })
        },
        error: function(error) {
            console.log(error)
        },
    })
}

const csrf = document.getElementsByName('csrfmiddlewaretoken')

// Функция оправки данных
const setData = (url) => {
    const elements = [...document.getElementsByClassName('ans')]
    const ansData = {}
    ansData['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el => {
        if (el.checked) {
            ansData[el.name] = el.value
        } else {
            if (!ansData[el.name]) {
                ansData[el.name] = null
            }
        }
    })
    console.log(ansData, url)
    $.ajax({
        type: 'POST',
        url: `${url}save`,
        data: ansData,
        success: function (response){
            //const Direction = response.co
        },
        error: function (error) {
            console.log(error)

        }
    })
}

function cleanData() {
    direction.innerHTML = ''
}

// directionForm.addEventListener('submit', e=> {
//     e.preventDefault()
// })

// Начало тестирования, нажимается один раз...
// const startQuiz = document.getElementById('start-quiz')
// startQuiz.onclick = function () {
//     cleanData()
//     const direction = Object.keys(data_)[0] + '/' + Object.values(data_)[0][0] + '/'
//     const url_ = url + direction
//     loadData(url_)
//     restDirection.innerHTML = `Отправить`
// }