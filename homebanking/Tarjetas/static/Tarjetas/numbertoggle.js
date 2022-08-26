const showbtn = document.getElementsByClassName('toggler');
const nums = document.getElementsByClassName('number');
const numh = document.getElementsByClassName('numberh');
const cvvs = document.getElementsByClassName('cvv');
const cvvh = document.getElementsByClassName('cvvh');

Array.from(showbtn).forEach(function (element, index) {
element.addEventListener('click', () => {
    nums[index].classList.toggle('hide');
    numh[index].classList.toggle('hide');
    cvvs[index].classList.toggle('hide');
    cvvh[index].classList.toggle('hide');
})});