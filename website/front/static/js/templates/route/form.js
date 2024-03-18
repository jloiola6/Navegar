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


$(document).ready(function() {
    $('#add-route-weekday').click(function() {
        var formsetContainer = $('#formset-container');
        var totalForms = $('#id_routeweekday_set-TOTAL_FORMS').val();
        var newFormIndex = parseInt(totalForms); // Obter o índice do próximo formulário

        // Clonar o último formulário e atualizar seus campos
        var lastForm = formsetContainer.find('.route-weekday-form:last');
        var newForm = lastForm.clone(true);
        newForm.find(':input').each(function() {
            var name = $(this).attr('name').replace('-' + (newFormIndex - 1) + '-', '-' + newFormIndex + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newForm.insertAfter(lastForm).removeClass('has_original');

        // Atualizar o TOTAL_FORMS
        $('#id_routeweekday_set-TOTAL_FORMS').val(newFormIndex + 1);
    });
});

// const formsetContainer = document.querySelector('[data-formset-container]')

// const totalFormsInput = document.getElementById('id_routeweekday_set-TOTAL_FORMS')
// let totalForms = 0

// const addFormButton = document.querySelector('[data-add-form-button]')


// // console.log(formsetContainer, totalForms, totalForms, addFormButton)

// const updateTotalFormsInput = () => {
//     totalFormsInput.value = totalFormsInput.querySelectorAll('[data-weekday-form]')
// }

// const addForm = () => {
//     const lastForm = formsetContainer.querySelector('[data-weekday-form]:last-child')
//     const newForm = lastForm.cloneNode(true)

//     const formSelects = newForm.querySelectorAll('select')
    
//     formSelects.forEach((select) => {
//         console.log(select, select.name, select.id)

//         select.name = select.name.replace(/\D/, tot)
//     })

//     console.log(newForm, formSelects)
// }

// addFormButton.addEventListener('click', addForm)