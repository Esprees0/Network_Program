function taskOne() {
  setTimeout(function () {
    console.log("this is task 1");
  }, 500);
} 
function taskTwo() {
  console.log("this is task 2");
}
function taskThree() {
  setTimeout(function() {
    console.log("this is task 3");
  },  1000)
}
 
taskOne();
taskTwo();
taskThree();

