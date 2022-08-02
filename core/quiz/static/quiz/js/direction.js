const url = window.location.href

const directionBox = document.getElementById('direction-box')
const restDirect = document.getElementById('restDirect')

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)) {
                directionBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer => {
                    directionBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div> 
                    `
                })
            }
        });

    },
    error: function(error) {
        console.log(error)
    },
})

const directionForm = document.getElementById('direction-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    console.log(elements)
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    // elements.forEach(el=>{
    //     if (el.checked) {
    //         data[el.name] = el.value
    //     } else {
    //         if (!data[el.name]) {
    //             data[el.name] = null
    //         }
    //     }
    // })

    // let count = 0
    // $.ajax({
    //     type: 'POST',
    //     url: `${url}save`,
    //     data: data,
    //     success: function (response){
    //         const Direction = response.co
    //     },
    //     error: function (error) {
    //         console.log(error)
    //
    //     }
    // })
}

directionForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()
})