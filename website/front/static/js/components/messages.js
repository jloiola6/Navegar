const messagesList = document.querySelector('[data-messages]')

if(messagesList)
    messagesList.addEventListener('animationend', () => {
        messagesList.classList.add('hidden')
    })