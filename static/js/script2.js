let items = document.querySelectorAll('.cartItem-js');
let count = 0;

for (item of items) {
    ++count
}

if (count === 1) {
    document.getElementById('cart-js').style.height= "230px"
} else if (count === 0) {
    document.getElementById('cart-js').style.height= "200px"
}