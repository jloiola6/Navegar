const userAvatar = document.querySelector('[data-user-avatar]')
const userMenu = document.querySelector('[data-user-menu]')

if(userAvatar && userMenu){
    userAvatar.addEventListener('click', () => {
        userMenu.classList.toggle('visible')
    })

    window.addEventListener('click', (event) => {
        if(event.target.getAttribute('data-user-avatar') === null)
            userMenu.classList.remove('visible')
    })
}