
gsap.set('svg', {
    visibility: 'visible'
})
gsap.set('.dot', {
    transformOrigin: '50% 50%',
    attr: {
        cx: 'random(350, 450)',
        cy: 440,
        r: 'random(4, 20)'
    }
})
gsap.set('.outsideDot', {
    transformOrigin: '50% 50%',
    attr: {
        cx: 'random(370, 420)',
        cy: 420,
        r: 'random(3, 19)'
    }
})
let tl1 = gsap.timeline();
tl1.to('.dots1 .dot', {
    duration: 'random(2,8)',
    attr: {
        cy: 'random(-220, -320)'
    },
    stagger: {
        each: 0.16,
        repeat: -1,
        repeatRefresh: false
    },
    ease: 'linear'
}).seek(100)

let tl2 = gsap.timeline();
tl2.to('.dots2 .dot', {
    duration: 'random(2,5)',
    attr: {
        cy: 'random(-220, -320)'
    },
    stagger: {
        each: 0.16,
        repeat: -1,
        repeatRefresh: false
    },
    ease: 'sine.in'
}).seek(100)

let tl3 = gsap.timeline();
tl3.to('.dots3 .dot', {
    duration: 'random(6,12)',
    attr: {
        cy: 'random(-220, -320)'
    },
    stagger: {
        each: 0.16,
        repeat: -1,
        repeatRefresh: false
    },
    ease: 'sine.in'
}).seek(100)

let tl4 = gsap.timeline();
tl4.to('.dots4 .dot', {
    duration: 'random(3,9)',
    attr: {
        cy: 'random(-220, -320)'
    },
    stagger: {
        each: 0.16,
        repeat: -1,
        repeatRefresh: false
    },
    ease: 'sine.in'
}).seek(100)

let tl5 = gsap.timeline();
tl5.to('.dots5 .outsideDot', {
    duration: 'random(3,9)',
    attr: {
        cy: 'random(-220, -320)',
        r: 0
    },
    stagger: {
        each: 0.16,
        repeat: -1,
        repeatRefresh: false
    },
    ease: 'power2.in'
}).seek(100)

gsap.to('.outline', {
    duration: gsap.utils.wrap([7, 6.1, 5.2]),
    svgOrigin: '400 300',
    rotation: gsap.utils.wrap([-360, -360]),
    ease: 'linear',
    stagger: {
        each: 1,
        repeat: -1
    }
}).seek(200)
//ScrubGSAPTimeline(tl)
//gsap.globalTimeline.timeScale(0.25)