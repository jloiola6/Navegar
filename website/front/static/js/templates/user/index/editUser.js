const typeRadios = document.querySelectorAll('[data-radio-type]')

if(typeRadios)
    typeRadios.forEach((radio) => {
        const id = radio.getAttribute('data-radio-type')
        const issuanceGroup = document.querySelector(`[data-issuance-group="${id}"]`)

        if (radio.value == 'F')
            if(radio.checked)
                issuanceGroup.classList.remove('hidden')
            else
                issuanceGroup.classList.add('hidden')

        radio.addEventListener('click', () => {
            if (radio.value == 'F' && radio.checked)
                issuanceGroup.classList.remove('hidden')
            else
                issuanceGroup.classList.add('hidden')
        })
    })