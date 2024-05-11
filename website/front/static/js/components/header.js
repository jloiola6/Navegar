const current_path = window.location.pathname.split('/')
const links = document.querySelectorAll('[data-header-link]')

if(links)
    if (current_path.length == 2)
        document.querySelectorAll(('[data-header-link="/"]')).forEach((link) => {
            link.classList.add('active')
        })
    else
        links.forEach((link) => {
            const paths = link.getAttribute('data-header-link').split(' ')

            paths.forEach((path) => {
                if (current_path.includes(path))
                    link.classList.add('active')
            })
        })