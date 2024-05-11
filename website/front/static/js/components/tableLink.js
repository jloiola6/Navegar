const rows = document.querySelectorAll('[data-link]')

if(rows)
    rows.forEach((row) => {
        const link = row.dataset.link

        row.addEventListener('click', () => {
            window.location.href = link
        })
    })