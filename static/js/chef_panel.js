const select1 = document.getElementById("order-status");
const select2 = document.getElementById("order-time");
const inputElement = document.getElementById("Update-status");

select1.addEventListener("change", (event) => {
  const selectedValue1 = event.target.value;
  updateInputValue();
});

select2.addEventListener("change", (event) => {
  const selectedValue2 = event.target.value;
  updateInputValue();
});

function updateInputValue() {
  const combinedValue = `${order-status.value} - ${order-time.value}`;  
  inputElement.value = combinedValue;
}