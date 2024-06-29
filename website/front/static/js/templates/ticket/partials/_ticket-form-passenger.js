// Dynamic table for multiple passengers form

const nameField = document.getElementById('name-field')
const birthField = document.getElementById('birth-date-field')

const documentTypeCpfRadio = document.getElementById('temp-document-type-cpf')
const documentField = document.getElementById('document-field')

const addPassengerButton = document.querySelector('[data-add-passenger]')

const passengerTable = document.querySelector('[data-passenger-table]')

// const submitButton = document.querySelector('button[type="submit"]')

const PassengerRow = (name, birthDate, passengerDocument) => {
    const row = document.createElement('tr')

    const html = `
        <td>
            <input type="text" name="client_${ passengerCount }" value="${ name }" readonly>
        </td>

        <td>
            <input type="date" name="birth_date_${ passengerCount }" value="${ birthDate }" id="" readonly>
        </td>

        <td>
            <input type="hidden" name="document_type_${ passengerCount }" value="${ documentTypeCpfRadio.checked ? 'cpf' : 'rg' }" readonly>
            <input type="text" name="document_${ passengerCount }" value="${ passengerDocument }" readonly>
        </td>

        <td>
            <button data-remove-passenger type="button" class="action delete"></button>
        </td>
    `

    row.innerHTML = html

    return row
}

const clear = () => {
    nameField.value = ''
    nameField.classList.remove('touched')

    birthField.value = ''
    documentField.value = ''
}

const removePassenger = (event) => {
    const parent = event.target.parentElement.parentElement
    parent.remove()
    // validSubmit() 
}

const initRemovePassenger = () => {
    const removeButtons = document.querySelectorAll('[data-remove-passenger]')

    removeButtons.forEach((button) => {
        button.addEventListener('click', removePassenger)
    })
}

let passengerCount = 1

const addPassenger = () => {
    const name = nameField.value
    const birthDate = birthField.value.split('/').reverse().join('-')
    const passengerDocument = documentField.value

    if(name.length && !new Date(birthDate).toString().includes('Invalid')){
        passengerTable.appendChild(PassengerRow(name, birthDate, passengerDocument))
        initRemovePassenger()
        passengerCount++
        // validSubmit()
        clear()
    }
}

addPassengerButton.addEventListener('click', addPassenger)

const handleEnterKeyDown = (event) => {
    if(event.key == 'Enter'){
        event.preventDefault()
        addPassenger()
    }
}

nameField.addEventListener('keydown', handleEnterKeyDown)
birthField.addEventListener('keydown', handleEnterKeyDown)
documentField.addEventListener('keydown', handleEnterKeyDown)

// const validSubmit = () => {
//     const valid = passengerTable.querySelectorAll('tr').length > 0

//     submitButton.disabled = !valid
// }

// validSubmit()