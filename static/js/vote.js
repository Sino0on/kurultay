const form = document.querySelector('.voteForm')
const rezalts = document.querySelector('.rezalts')
form.onsubmit = (e) => {
    e.preventDefault()
    e.target.style.display = 'none';
    rezalts.classList.toggle('rezaltsHide')
}