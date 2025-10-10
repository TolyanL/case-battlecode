const slider = document.getElementById('rating-slider');
const finalRatings = document.querySelectorAll(".final-rating");

const valueClass = "final-rating";
const newClass = " text-sm text-white";
let oldItem = finalRatings[2];

slider.oninput = () => {
    oldItem.className = valueClass;
    oldItem = finalRatings[slider.value-1];
    oldItem.className += newClass;
};