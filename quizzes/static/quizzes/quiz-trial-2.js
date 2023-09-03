const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const quizAnswer = document.getElementById('quiz-answer')
const quizQuestion = document.getElementById('quiz-question')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const nextBtn = document.getElementById('next-button')
const quizSubmitBtn = document.getElementById('submit-button')
const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const explanationTab = document.getElementById('explanation-tab')
let quizAnswerBtn = null


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

            loadQuestions();
        }
    },
    error: function(error){
        console.log(error)
    }
})

const loadQuestions = () => {
    hideItems(quizSubmitBtn)
    hideItems(nextBtn)
    hideItems(explanationTab)
    
    let answer_set = null;
    let question_text = null;

    if (questionNo < question_set.length){
        answer_set = question_set[questionNo][1];
        question_text = question_set[questionNo][0];
        quizQuestion.innerHTML =`
                Q${questionNo + 1} : ${question_text}
        `

        answer_set.forEach(answer=>{
            quizAnswer.innerHTML += `
                <div class="col-7 col-sm-5 col-md-3 radio-btn-container">
                    <label class="custom-radio" for="${question_text}-${answer}">
                        <input type="radio" class="ans" id="${question_text}-${answer}" name="${question_text}" value="${answer}" />
                        <span class="radio-btn">
                            <i class="bi bi-check-lg bi-check-css"></i>
                            <i class="bi bi-x-lg"></i>
                            ${answer}
                        </span>
                    </label>
                </div>
            `
        })

    } else {
        quizBox.innerHTML =`
            <div class="d-flex justify-content-center mb-2">
                <h3>No more questions left!</h3>
            </div>
        `
        hideItems(nextBtn)
        showItems(quizSubmitBtn)
        
    } 

    quizAnswerBtn = [...document.getElementsByClassName('ans')]
    quizAnswerBtn.forEach((el) => {
        el.addEventListener('change', ()=>{
            saveQuiz()
        })
    })

    sendData()
}

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]

    //check which is clicked(question)
    elements.forEach(el=>{
        console.log("checking send data")
        console.log(el)
        console.log(el.checked)
        if (el.checked){
            data[el.name] = el.value
            checkedAns[`${el.name}-checked`] = el.value
        } else {
            if (!data[el.name]){
                data[el.name] = null
                checkedAns[`${el.name}-checked`] = null
            }
        }
    })
}

const endQuiz = () => {
    data['csrfmiddlewaretoken'] = csrf[0].value
    
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

                    // const initialClass = ['d-flex', 'justify-content-center']
                    // resDiv.classList.add(...initialClass)

                    resDiv.innerHTML += `
                        <h2>Question: ${question}</h2>
                        <br>
                    `
                    const cls = ['container','p-3','text-light','h3']
                    resDiv.classList.add(...cls)

                    if(resp == 'not answered'){
                        resDiv.innerHTML += 'Not Answered!'
                        resDiv.classList.add('bg-danger')
                    }
                    else{
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `Answered: ${answer}`
                        }else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `Answered: ${answer} <br>` 
                            resDiv.innerHTML += `Correct Answer: ${correct}`
                        }
                    }
                }
                
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
    endQuiz()
})

nextBtn.addEventListener('click', (event) => {
    event.preventDefault();
    sendData();
    questionNo++;
    quizAnswer.innerHTML = ''
    loadQuestions();
})


const saveQuiz = () => {
    sendData()
    showItems(nextBtn)
    showItems(explanationTab)
    quizQuestion.scrollIntoView()
    data['csrfmiddlewaretoken'] = csrf[0].value

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            const results = response.results
            // quizForm.classList.add('not-visible')
            
            results.forEach(res=>{
                const elements = [...document.getElementsByClassName('ans')]

                elements.forEach((el) => {
                    el.disabled = true
                    for (const [question, resp] of Object.entries(res)){
                        if (resp['answered'] === 'not answered'){
                            if (el.name === question) {
                                if (el.value === resp['correct_answer']) {
                                    el.nextElementSibling.classList.add('radio-btn-correct')
                                }
                            }
                        } else {
                            if (el.name === question) {
                                if (el.value === resp['correct_answer']) {
                                    el.nextElementSibling.classList.add('radio-btn-correct')
                                } else if (el.value === resp['answered']) {
                                    el.nextElementSibling.classList.add('radio-btn-incorrect')
                                    console.log(el.nextElementSibling)
                                }
                            }
                        }
                        
                    }
                })
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}

const hideItems = (element) => {
    element.style.display = "none";
}

const showItems = (element) => {
    element.style.display = "block";
}



