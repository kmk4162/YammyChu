let observer = new IntersectionObserver((e) => {
  e.forEach((box)=>{
    if (box.isIntersecting){
      box.target.opacity = 1;
    }
    else {
      box.target.opacity = 0;
    }
  })
})


let h2 = document.querySelectorAll("h2")
for (let d of h2){
  observer.observer(d)
}