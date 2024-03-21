const authTypeRadios = document.querySelectorAll('[data-radio-auth-type]')
const authTypeInputs = document.querySelectorAll('[data-input-auth-type]')

const showInput = () => {
    authTypeRadios.forEach((radio) => {
        if(radio.checked){
            const radioType = radio.getAttribute('data-radio-auth-type')

            authTypeInputs.forEach((input) => {
                const inputType = input.getAttribute('data-input-auth-type')

                if (radioType == inputType){
                    input.classList.remove('hidden')
                }else{
                    input.classList.add('hidden')
                    input.value = ''
                }
            })
        }
    })
}

authTypeRadios.forEach((radio) => {
    radio.addEventListener('click', showInput)
})

showInput()