const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const questionIndex = document.getElementById('question-index')
const questionIndexBtn = []
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timeTitle = document.getElementById('time-title')
const timerBox = document.getElementById('timer-box')
const nextBtn = document.getElementById('next-button')
const prevBtn = document.getElementById('prev-button')
const quizSubmitBtn = document.getElementById('submit-button')
const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const data = {}
const checkedAns = {}

let timer = null
let hour = null
let minutes = null
let seconds = null

let question_set = [];
let questionNo = 0;

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        if (response.data!=null){
            const question_data = response.data
            
            if (question_set.length == 0){
                question_data.forEach(el => {
                    for (const [question, answers] of Object.entries(el)){
                        question_set.push([question, answers])
                    }
                });
            }

            for (let i = 0; i < question_set.length; i++) {
                console.log(question_set.length)
                let question_text = question_set[i][0];
                data[question_text] = null;

                questionIndex.innerHTML += `
                    <button class="btn btn-outline-dark col-1 question-index-button-css disabled" id="question-index-button-${i}">${i}</button>
                `
                if (i === 0) {
                    document.getElementById(`question-index-button-${i}`).classList.remove("disabled")
                }

                // questionIndexBtn[`question-index-button-${i}`] = document.getElementById(`question-index-button-${i}`)
                // console.log("index button")
                // console.log(document.getElementById(`question-index-button-${i}`))
                // console.log(questionIndexBtn[`question-index-button-${i}`].classList.contains("active"))
            }
            
            // for (let [key, value] of Object.entries(questionIndexBtn)) {
            //     if (questionIndexBtn.hasOwnProperty(key)) {
            //         // console.log(key, questionIndexBtn[key]);
            //         // console.log(value.id)
            //         value.addEventListener('click', (event) => {
            //             event.preventDefault()
            //             console.log(value)
            //             console.log(value.classList.contains("btn"))
            //         })
            //      }
            // }
            for (let i = 0, element; i < question_set.length; i++) {
                element = document.getElementById(`question-index-button-${i}`)
                element.addEventListener('click', (event) => {
                    event.preventDefault()
                    sendData()
                    questionNo = i
                    loadQuestions()
                    
                })
            }

            activateTimer(response.time)
            loadQuestions();
        }
    },
    error: function(error){
        console.log(error)
    }
})

const activateTimer = (time) => {
    hour = Math.floor(time/60)
    minutes = time - (hour*60)
    seconds = 0

    if (hour < 10) {
        timerBox.innerHTML = `<b>${time < 10 ? `0${hour}:0${time}:00` : `0${hour}:${time}:00`}</b>`
    } else {
        timerBox.innerHTML = `<b>${time < 10 ? `${hour}:0${time}:00` : `${hour}:${time}:00`}</b>`
    }

    timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --

            if (minutes < 0) {
                minutes = 59
                hour --

                if (hour < 0) {
                    stopTimer()
                    timerBox.innerHTML = `<b>00:00:00</b>`
                    setTimeout(()=>{ 
                        timerBox.innerHTML = `<b>00:00:00</b>`
                        alert('Time over')
                    }, 500)
                    return;
                }
            }
        }
        
        
        let h = hour < 10 ? '0' + hour : hour;
        let m = minutes < 10 ? '0' + minutes : minutes;
        let s = seconds < 10 ? '0' + seconds : seconds;
        timerBox.innerHTML = `
            <b>${h}:${m}:${s}</b>
        `
    }, 1000)


}

const stopTimer = () => {
    let h = hour < 10 ? '0' + hour : hour;
    let m = minutes < 10 ? '0' + minutes : minutes;
    let s = seconds < 10 ? '0' + seconds : seconds;

    timeTitle.innerText = "Time Left:"
    timerBox.innerHTML = `
        <b>${h}:${m}:${s}</b>
    `
    clearInterval(timer)

    sendData()
    endQuiz()
}

const loadQuestions = () => {
    hideItems(quizSubmitBtn)
    
    let answer_set = null;
    let question_text = null;
    console.log(question_text)
    if (questionNo < question_set.length){
        answer_set = question_set[questionNo][1];
        question_text = question_set[questionNo][0];
        quizBox.innerHTML =`
            <div class="d-flex justify-content-center mb-2">
                <h3>Q${questionNo + 1} : ${question_text}</h3>
            </div>
            <hr>
        `

        answer_set.forEach(answer=>{
            quizBox.innerHTML += `
                <div class="d-flex justify-content-center">
                    <input type="radio" class="ans" id ="${question_text}-${answer}" name="${question_text}" value="${answer}">
                    <label for="${question_text}-${answer}">${answer}</label>
                </div>
                </br>
            `
        })

        showItems(nextBtn)
    } else {
        quizBox.innerHTML =`
            <p>
                No more questions left!
            </p>
        `
        hideItems(nextBtn)
        showItems(quizSubmitBtn)
        
    } 
    
    console.log(checkedAns[`${question_text}-checked`])
    if (checkedAns[`${question_text}-checked`]) {
        const elements = [...document.getElementsByClassName('ans')]
        elements.forEach(el => {
            if (checkedAns[`${el.name}-checked`] === el.value) {
                el.checked = true
            } 
        })
    }

    //index button active/disabled view
    for (let i = 0, element; i < question_set.length; i++) {
        element = document.getElementById(`question-index-button-${i}`)
        if (i === questionNo) {
            element.classList.add("active")
        }
         else if (element.classList.contains("active")) {
            element.classList.remove("active")
        }
    }

    //index

    // if (questionNo == (question_set.length - 1)) {
    //     hideItems(nextBtn)
    //     showItems(quizSubmitBtn)
    // } 

    if (questionNo == 0) {
        hideItems(prevBtn)
    } else {
        showItems(prevBtn)
    }

    sendData()
}

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]

    //check which is clicked(question)
    elements.forEach(el=>{
        if (el.checked){
            data[el.name] = el.value
            checkedAns[`${el.name}-checked`] = el.value
            console.log(el.name)
            console.log(checkedAns[`${el.name}-checked`])
            console.log(!checkedAns[`${el.name}-checked`])
        } else {
            if (!data[el.name]){
                data[el.name] = null
                checkedAns[`${el.name}-checked`] = null
            }
        }
    })
}

const endQuiz = () => {
    questionIndex.innerHTML = ""
    data['csrfmiddlewaretoken'] = csrf[0].value
    console.log(data)
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            console.log(response)
            const results = response.results
            console.log(results)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML = `
                <h3>
                    ${response.passed ? 'Congratulations! ': 'Oops ... :( '}Your result is ${response.score.toFixed(2)}%
                </h3>
            `

            results.forEach(res=>{
                console.log("check for res")
                console.log(res)
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){
                    console.log(question)
                    console.log(resp)
                    console.log('********')

                    resDiv.innerHTML += question
                    const cls =['container','p-3','text-light','h3']
                    resDiv.classList.add(...cls)

                    if(resp == 'not answered'){
                        resDiv.innerHTML += ' Not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else{
                        console.log(`answered = ${resp['answered']}`)
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        }else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += `| answered: ${answer}` 
                        }
                    }
                }
                //const body = document.getElementsByTagName('BODY')[0]
                resultBox.append(resDiv)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}

quizSubmitBtn.addEventListener('click', (event) =>{
    event.preventDefault()
    stopTimer()
})

nextBtn.addEventListener('click', (event) => {
    event.preventDefault();
    sendData();
    questionNo++;
    loadQuestions();
    if (questionNo <= question_set.length && document.getElementById(`question-index-button-${questionNo}`).classList.contains("disabled")){
        document.getElementById(`question-index-button-${questionNo}`).classList.remove("disabled")
    }
})

prevBtn.addEventListener('click', (event) => {
    event.preventDefault();
    sendData();
    questionNo--;
    loadQuestions();
})

const hideItems = (element) => {
    element.style.display = "none";
}

const showItems = (element) => {
    element.style.display = "block";
}




