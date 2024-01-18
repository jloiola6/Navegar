const modalList = document.querySelectorAll('[data-modal]')

if(modalList.length){
    modalList.forEach((modal) => {
        const id = modal.dataset.modal

        const modalTriggers = document.querySelectorAll(`[data-modal-open="${id}"]`)
        
        if(modalTriggers.length){
            modalTriggers.forEach((trigger) => {
                trigger.addEventListener('click', () => {
                    modal.showModal()
                })
            })
        }

        modal.addEventListener('click', (event) => {
            console.log(event.target)
        })
    })
}