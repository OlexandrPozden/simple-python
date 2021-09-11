/*let card = document.getElementsByClassName("parallax")[0];

card.addEventListener('mousemove', (e)=>{
    console.log("invokes eventlistener");
    var rect = card.getBoundingClientRect();
    console.log(rect.top, rect.right, rect.bottom, rect.left);
    console.log(e.pageX,e.pageY);
    console.log(this);
    arr = card.getElementsByClassName("layer");
    console.log(arr);
    var array = Array.prototype.slice.call( arr )
    array.forEach(element => {
        element.style.color = "green";
        console.log(element.getAttribute("data-speed"));
        speed = element.getAttribute("data-speed");
        console.log(card.clientWidth);
        innerX = e.pageX - rect.left;
        innerY = e.pageY - rect.top;
        const x = (card.clientWidth - innerX * speed) / 100;
        const y = (card.clientHeight - innerY * speed) / 100;
        console.log(x,y);
        
        element.style.transform = `translateX(${x}px) translateY(${y}px)`;

    });
});
*/
