const about = document.getElementsByClassName("about")[0]
console.log(about)
const about_text = document.getElementsByClassName("about_text")[0]
console.log(about_text)
about.addEventListener('click', () => {
    about_text.classList.toggle('active')
})