"use strict";

const body = document.querySelector("body");
const album = document.querySelector(".album");
let loaded = false;
const albumDetails = {
    dark: {
        album: "Grouper - Grid of Points",
        song: "The Races",
        art: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/36124/grouper-grid-of-points.jpg",
        position: "01 of 07",
        start: "0:27",
        end: "0:50",
        highlight: "#fdfdfd",
        accent: "#f70040",
        background: "#1d1d1d"
    },
    light: {
        album: "Frontierer - Orange Mathematics",
        song: "The Collapse",
        art: "https://s3-us-west-2.amazonaws.com/s.cdpn.io/36124/frontierer-orange-mathematics.jpg",
        accent: "#f78900",
        highlight: "#1d1d1d",
        background: "#fdfdfd",
        position: "03 of 16",
        start: "1:00",
        end: "2:08"
    }
};
album.classList.add("album--loaded");
setTimeout(() => {
    album.classList.add("album--parallax");
}, 1200);

function toggleThemes(theme) {
    const album = albumDetails[theme];
    const albumArt = document.querySelector(".album__art");
    const albumTitle = document.querySelector(".album__song__album marquee");
    const albumSong = document.querySelector(".album__song__title");
    const albumPosition = document.querySelector(".album__song__position");
    const albumCurrentTime = document.querySelector(".album__song__current-time");
    const albumFullTime = document.querySelector(".album__song__full-length");
    albumArt.style.background = `url(${album.art}) 50% 50% no-repeat`;
    albumTitle.innerText = album.album;
    albumSong.innerText = album.song;
    albumPosition.innerText = album.position;
    albumCurrentTime.innerText = album.start;
    albumFullTime.innerText = album.end;
    document.documentElement.style.setProperty("--highlight", album.highlight);
    document.documentElement.style.setProperty("--background", album.background);
    document.documentElement.style.setProperty("--accent", album.accent);
}

const buttons = document.querySelectorAll(".toggles button");
buttons.forEach(function (el) {
    el.addEventListener("click", () => {
        let theme = "";
        if (el.innerText === "Dark Theme") {
            theme = "dark";
        } else {
            theme = "light";
        }
        toggleThemes(theme);
    });
});

// https://css-tricks.com/animated-intro-rxjs/

function smoothParallax() {
    const body = document.querySelector("body");
    const clientHeight = window.innerHeight;
    const bodyDims = {
        w: body.getBoundingClientRect().width,
        h: body.getBoundingClientRect().height
    };
    const limit = {
        x: 25,
        y: 25
    };
    console.clear();

    function lerp(start, end) {
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        return {
            x: start.x + dx * 0.1,
            y: start.y + dy * 0.1
        };
    }

    const docEl = document.documentElement;
    const mouseMove$ = Rx.Observable.fromEvent(docEl, "mousemove").map(event => ({
        x: event.clientX,
        y: event.clientY
    }));
    const touchMove$ = Rx.Observable.fromEvent(docEl, "touchmove").map(event => ({
        x: event.touches[0].clientX,
        y: event.touches[0].clientY
    }));
    const animationFrame$ = Rx.Observable.interval(10, Rx.Scheduler.animationFrame);
    const move$ = Rx.Observable.merge(mouseMove$, touchMove$);
    const smoothMove$ = animationFrame$.withLatestFrom(move$, (frame, move) => move).scan(lerp);
    console.log(smoothMove$);
    smoothMove$.subscribe(pos => {
        const clamped = {
            x: pos.x / bodyDims.w * limit.x - limit.x / 2,
            y: pos.y / bodyDims.h * limit.y - limit.y / 2
        };
        document.documentElement.style.setProperty("--move-y", `${clamped.y}deg`);
        document.documentElement.style.setProperty("--move-x", `${clamped.x}deg`);
    });
}

smoothParallax();