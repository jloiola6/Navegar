const inputs = document.querySelectorAll(':is(input, select)')

console.log(inputs)

const initialize = (input) => {
    input.addEventListener('blur', () => {
        input.classList.add('touched')
    })
}

if(inputs){
    inputs.forEach(initialize)
}