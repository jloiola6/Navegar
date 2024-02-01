const inputs = document.querySelectorAll(':is(input, select)')

const initialize = (input) => {
    input.addEventListener('blur', () => {
        input.classList.add('touched')
    })
}

if(inputs){
    inputs.forEach(initialize)
}