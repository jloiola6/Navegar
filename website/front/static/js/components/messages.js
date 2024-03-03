const messagesList = document.querySelector('[data-messages]')

console.log(messagesList)

if(messagesList)
    messagesList.addEventListener('animationend', () => {
        messagesList.classList.add('hidden')
    })