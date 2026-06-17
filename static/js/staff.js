AOS.init({
    duration:1200,
    once:false,
    offset:100,
    easing:'ease-in-out',
    mirror:true
});

/* Counter Animation */

const counters = document.querySelectorAll('.stat h3');

const animateCounter = (counter) => {

    const target = parseInt(counter.innerText) || 0;

    let count = 0;

    const increment = Math.ceil(target / 40);

    const update = () => {

        count += increment;

        if(count < target){
            counter.innerText = count;
            requestAnimationFrame(update);
        }else{
            counter.innerText = target;
        }
    };

    update();
};

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            animateCounter(entry.target);

            observer.unobserve(entry.target);
        }
    });

});

counters.forEach(counter => {
    observer.observe(counter);
});