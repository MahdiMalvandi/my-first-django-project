let imgsf = document.querySelectorAll(".swiper-slide")
let imgs = Array.from(imgsf)
let noneAll = () => {imgsf.forEach(i => i.style.display = "none")}
imgs.forEach(item => {
    item.addEventListener("click", () => {
        if (imgs.indexOf(item) === imgs.length -1 ){
            noneAll()
            imgs[0].style.display = "block"
        } else {
            noneAll()
            imgs[imgs.indexOf(item)+1].style.display = "block"
        }
    })
})