const typeRadios = document.querySelectorAll('[data-radio-type]')
const issuanceGroup = document.querySelector('[data-issuance-group]')

const showIssuanceGroup = (show) => {
    if (show)
        issuanceGroup.classList.remove('hidden')
    else
        issuanceGroup.classList.add('hidden')
}

typeRadios.forEach((radio) => {
    if(radio.value == 'F')
        showIssuanceGroup(radio.checked)

    radio.addEventListener('click', () => {
        showIssuanceGroup(radio.value == 'F')
    })
})