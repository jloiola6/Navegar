// Monetary value fields

const valueField = document.getElementById('id_value')
const discountedValueField = document.getElementById('id_discounted_value')

valueField.addEventListener('input', () => {
    discountedValueField.value = Number.parseFloat(valueField.value) - Number.parseFloat(valueField.value) * 0.025
})

const costValueField = document.getElementById('id_cost')
const discountedCostField = document.getElementById('id_discounted_cost')

costValueField.addEventListener('input', () => {
    discountedCostField.value = Number.parseFloat(costValueField.value) - 20.0
})

// Boat selections

const weekdaysInputs = document.querySelectorAll('[data-weekday]')
const weekdays = [...weekdaysInputs].map((weekday) => {
    return {
        'en': weekday.getAttribute('data-weekday'),
        'pt': weekday.value
    }
})

const boatsInputs = document.querySelectorAll('[data-boat]')
const boats = [...boatsInputs].map((boat) => {
    return {
        'id': boat.getAttribute('data-boat'),
        'name': boat.value
    }
})

const form = document.querySelector('#route_form')
const addSelectionButton = form.querySelector('[data-add-selection-button]')
const buttonContainer = form.querySelector('.button-container')

const BoatSelection = () => {
    const div = document.createElement('div')
    div.classList.add('boat-selection')

    const boatOptions = boats.map((boat) => {
        return `
            <option value="${ boat.id }">${ boat.name }</option>
        `
    })

    const weekdayCheckboxes = weekdays.map((weekday, index) => {
        const name = `new-boat-${ selectionCount }-new-weekday-${ index }`

        return `
            <input id="${ name }" name="${ name }" value="${ weekday.en }" type="checkbox" />
            <label for="${ name }">${ weekday.pt }</label>
        `
    })

    const html = `
        <div class="flex justify-content-between">
            <div class="radio-control">
                ${
                    weekdayCheckboxes.map((checkbox) => {
                        return checkbox
                    }).join("")
                }
            </div>

            <button class="action delete lg" title="Remover embarcação" type="button" data-remove-selection></button>
        </div>

        <select name="new-boat-${ selectionCount }" id="new-boat-${ selectionCount }" required>
            <option value="" disabled selected>Selecione uma embarcação</option>

            ${
                boatOptions.map((option) => {
                    return option
                }).join("")
            }
        </select>
    `

    div.innerHTML = html

    return div
}

const removeSelection = (event) => {
    const parent = event.target.parentElement.parentElement
    parent.remove()
}

const initRemoveButtons = () => {
    const removeButtons = document.querySelectorAll('[data-remove-selection]')

    if(removeButtons)
        removeButtons.forEach((button) => {
            button.addEventListener('click', removeSelection)
        })
}

initRemoveButtons()

let selectionCount = 0

const addSelection = () => {
    form.insertBefore(BoatSelection(), buttonContainer)
    selectionCount++
    initRemoveButtons()
}

if(addSelectionButton)
    addSelectionButton.addEventListener('click', addSelection)