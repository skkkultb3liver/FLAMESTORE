$(document).ready(function(){
    $('.mainscreen__slider').slick({
        dots:true
    });
})

const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("The rating is set"))
        .catch(error => alert("Error"))
});