//---

let metaballCount = 25;
let metaballs = [];

let w = 1024;
let h = 512;

let fullscreenMode = false;
let pictureFrameMode = true;

// const center = { x: w / 2, y: h / 2 };
const border = {x: 0, y: 0, w: w, h: h};

//---

let mouseActive = false;
let mouseDown = false;
let mousePos = {x: 0, y: 0};

//---

let animationFrame = null;

//---

let canvas = null;
let gl = null;

let vertexShaderCode = null;
let fragmentShaderCode = null;

let shaderProgram = null;
let metaballsHandle = null;

//---

function init() {

    document.querySelector('.button-fullscreen').addEventListener('click', clickFullscreenHandler, false);
    // document.querySelector( '.button-pictureframe' ).addEventListener( 'click', clickPictureFrameHandler, false );

    canvas = document.querySelector('canvas');
    canvas.addEventListener('mousedown', mouseDownHandler, false);
    canvas.addEventListener('mouseup', mouseUpHandler, false);
    canvas.addEventListener('mousemove', mouseMoveHandler, false);
    canvas.addEventListener('mouseenter', mouseEnterHandler, false);
    canvas.addEventListener('mouseleave', mouseLeaveHandler, false);

    gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

    window.addEventListener('resize', onResize, false);

    restart();

}

function onResize(event) {

    restart();

}

function restart() {

    if (fullscreenMode === true) {

        w = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        h = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

        canvas.style.position = 'fixed';
        canvas.style.left = '0';
        canvas.style.top = '0';

    } else {

        const canvasWrapper = document.querySelector('.canvas');

        w = canvasWrapper.clientWidth;
        h = canvasWrapper.clientHeight;

        canvas.style.position = 'initial';

    }

    if (pictureFrameMode === true) {

        gl.clearColor(16 / 255, 53 / 255, 82 / 255, 1.0);

        border.x = 0;
        border.y = 0;
        border.w = w;
        border.h = h;

    } else {

        gl.clearColor(0, 0, 0, 0.0);

        border.x = 200;
        border.y = 200;
        border.w = w - 200;
        border.h = h - 200;

    }

    canvas.width = w;
    canvas.height = h;

    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;

    // center.x = w / 2;
    // center.y = h / 2;

    //---

    addMetaballs();

    vertexShaderCode = createShader(gl, getVertexShaderCode(), gl.VERTEX_SHADER);
    fragmentShaderCode = createShader(gl, getFragmentShaderCode(metaballCount), gl.FRAGMENT_SHADER);

    shaderProgram = createShaderProgram(gl, vertexShaderCode, fragmentShaderCode);

    gl.viewport(0, 0, w, h);

    // gl.clearColor( 16 / 255, 53 / 255, 82 / 255, 1.0 );
    // gl.clearColor( 0, 0, 0, 0.0 );
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    gl.useProgram(shaderProgram);

    //---

    const vertexData = new Float32Array([

        -1.0, 1.0, // top left
        -1.0, -1.0, // bottom left
        1.0, 1.0, // top right
        1.0, -1.0, // bottom right

    ]);

    const vertexBuffer = createBuffer(gl, gl.ARRAY_BUFFER, vertexData, gl.STATIC_DRAW);

    //---

    const positionHandle = getAttribLocation(shaderProgram, 'position');

    gl.enableVertexAttribArray(positionHandle);
    gl.vertexAttribPointer(positionHandle, 2, gl.FLOAT, gl.FALSE, 2 * 4, 0);

    //---

    metaballsHandle = getUniformLocation(shaderProgram, 'metaballs');

    //---

    if (animationFrame != null) {

        cancelAnimFrame(animationFrame);

    }

    render();

}

//---

function getVertexShaderCode() {

    return `
    attribute vec2 position;

    void main(void) {

      gl_Position = vec4(position, 0.0, 1.0);

    }
  `

}

function getFragmentShaderCode(count) {

    return `
    precision highp float;
    
    uniform vec3 metaballs[ ${count} ];

    void main(void) {

      float x = gl_FragCoord.x;
      float y = gl_FragCoord.y;
      float v = 0.0;
      
      for ( int i = 0; i < ${count}; i++ ) {
      	
        vec3 mb = metaballs[ i ];
        
        float dx = mb.x - x;
        float dy = mb.y - y;
        
        float radius = mb.z;
        
        v += radius * radius / ( dx * dx + dy * dy );
      
      }

      if ( v > 0.4 && v < 0.5 ) {
      		
        gl_FragColor = vec4( 0.068, 0.208, 0.322, 1.0 );

      } else if ( v > 0.5 && v < 0.6 ) {
      		
        gl_FragColor = vec4( 0.094, 0.306, 0.467, 1.0 );

      } else if ( v > 0.6 && v < 0.7 ) {
      
      	gl_FragColor = vec4( 0.118, 0.376, 0.569, 1.0 );
      
      } else if ( v > 0.7 && v < 0.8 ) {
      
      	gl_FragColor = vec4( 0.102, 0.459, 0.624, 1.0 );
      
      } else if ( v > 0.8 && v < 0.9 ) {
      
      	gl_FragColor = vec4( 0.086, 0.541, 0.678, 1.0 );
      
      } else if ( v > 0.9 && v < 1.0 ) {
      
      	gl_FragColor = vec4( 0.204, 0.627, 0.643, 1.0 );
      
      } else if ( v > 1.0 && v < 1.1 ) {
      
      	gl_FragColor = vec4( 0.322, 0.714, 0.604, 1.0 );
      
      } else if ( v > 1.1 && v < 1.2 ) {
      
      	gl_FragColor = vec4( 0.463, 0.784, 0.576, 1.0 );
      
      } else if ( v > 1.2 && v < 1.3 ) {
      
      	gl_FragColor = vec4( 0.600, 0.851, 0.549, 1.0 );
      
      } else if ( v > 1.3 && v < 1.4 ) {
      
      	gl_FragColor = vec4( 0.709, 0.894, 0.549, 1.0 );
      
      } else if ( v > 1.4 ) {
      
      	gl_FragColor = vec4( 0.851, 0.929, 0.573, 1.0 );
      
      }

    }
  `

}

//---

function getAttribLocation(program, name) {

    const attributeLocation = gl.getAttribLocation(program, name);

    if (attributeLocation === -1) {

        console.log('Can not find attribute ' + name + '.');

    }

    return attributeLocation;

}

function getUniformLocation(program, name) {

    const uniformLocation = gl.getUniformLocation(program, name);

    if (uniformLocation === -1) {

        console.log('Can not find uniform ' + name + '.');

    }

    return uniformLocation;

}

//---

function createBuffer(gl, target, bufferArray, usage) {

    const buffer = gl.createBuffer();

    gl.bindBuffer(target, buffer);
    gl.bufferData(target, bufferArray, usage);

    return buffer;

}

function createShader(gl, shaderCode, type) {

    const shader = gl.createShader(type);

    gl.shaderSource(shader, shaderCode);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {

        console.log('Could not compile WebGL program. \n\n' + gl.getShaderInfoLog(shader));

    }

    return shader;

}

function createShaderProgram(gl, vertexShader, fragmentShader) {

    const shaderProgram = gl.createProgram();

    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);

    gl.linkProgram(shaderProgram);

    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {

        console.log('Could not compile WebGL program. \n\n' + gl.getProgramInfoLog(shaderProgram));

    }

    return shaderProgram;

}

//---

function mouseDownHandler(event) {

    mouseDown = true;

}

function mouseUpHandler(event) {

    mouseDown = false;

}

function mouseEnterHandler(event) {

    mouseActive = true;

}

function mouseLeaveHandler(event) {

    mouseActive = false;

    mouseDown = false;

}

function mouseMoveHandler(event) {

    mousePos = getMousePos(canvas, event);

}

function getMousePos(canvas, event) {

    const rect = canvas.getBoundingClientRect();

    //return { x: event.clientX - rect.left, y: event.clientY - rect.top };

    return {x: event.clientX - rect.left, y: h - (event.clientY - rect.top)};

}

function clickFullscreenHandler(event) {

    const status = event.target.innerText.toLowerCase() !== 'off';

    const info = document.querySelector('.info');

    if (status === true) {

        event.target.innerHTML = '<strong>Off</strong>';

        fullscreenMode = false;

        info.style.position = 'absolute';
        info.style.right = '0';
        info.style.bottom = '-50px';

    } else {

        event.target.innerHTML = '<strong>On</strong>';

        fullscreenMode = true;

        info.style.position = 'fixed';
        info.style.right = '10px';
        info.style.bottom = '10px';

    }

    restart();

}

function clickPictureFrameHandler(event) {

    const status = event.target.innerText.toLowerCase() !== 'off';

    const c = document.querySelector('.canvas');

    if (status === true) {

        event.target.innerHTML = '<strong>Off</strong>';

        pictureFrameMode = false;

        c.classList.remove('border-image');

    } else {

        event.target.innerHTML = '<strong>On</strong>';

        pictureFrameMode = true;

        c.classList.add('border-image');

    }

    restart();

}

//---

function randomBetween(min, max) {

    return Math.floor(Math.random() * (max - min + 1) + min);

}

//---

function addMetaballs() {

    metaballs = [];

    //---

    let radiusValue = 0;

    if (w > h) {

        radiusValue = Math.floor(h / 10);

    } else {

        radiusValue = Math.floor(w / 14);

    }

    //---

    const maxRadius = radiusValue;

    for (let i = 0, l = metaballCount; i < l; i++) {

        const radius = Math.round(Math.random() * (maxRadius - maxRadius / 2)) + maxRadius / 2;

        const metaball = {

            x: randomBetween(border.x + radius, border.w - radius),
            y: randomBetween(border.y + radius, border.h - radius),
            vx: Math.random() * 1 - 0.5,
            vy: Math.random() * 1 - 0.5,
            radius: radius,
            mouseFollow: false

        };

        if (i === 0) {

            metaball.radius = Math.round(maxRadius + maxRadius / 2);
            metaball.mouseFollow = true;

        }

        metaballs.push(metaball);

    }

}

function moveMetaballs() {

    for (let i = 0, l = metaballs.length; i < l; i++) {

        const metaball = metaballs[i];

        if (mouseActive === true && metaball.mouseFollow === true) {

            metaball.x += (mousePos.x - metaball.x) / 8;
            metaball.y += (mousePos.y - metaball.y) / 8;

        } else {

            if (mouseDown === false) {

                metaball.x += metaball.vx;
                metaball.y += metaball.vy;

            }

        }

        if (metaball.x > border.w - metaball.radius) {

            metaball.x = border.w - metaball.radius;
            metaball.vx *= -1;

        } else if (metaball.x < border.x + metaball.radius) {

            metaball.x = border.x + metaball.radius;
            metaball.vx *= -1;

        }

        if (metaball.y > border.h - metaball.radius) {

            metaball.y = border.h - metaball.radius;
            metaball.vy *= -1;

        } else if (metaball.y < border.y + metaball.radius) {

            metaball.y = border.y + metaball.radius;
            metaball.vy *= -1;

        }

    }

}

//---

function render(timestamp) {

    gl.clear(gl.COLOR_BUFFER_BIT);

    const dataToSendToGPU = new Float32Array(3 * metaballCount);

    for (let i = 0; i < metaballCount; i++) {

        const baseIndex = 3 * i;
        const metaball = metaballs[i];

        dataToSendToGPU[baseIndex + 0] = metaball.x;
        dataToSendToGPU[baseIndex + 1] = metaball.y;
        dataToSendToGPU[baseIndex + 2] = metaball.radius;

    }

    gl.uniform3fv(metaballsHandle, dataToSendToGPU);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

    //---
    //---
    moveMetaballs();

    //---

    animationFrame = requestAnimFrame(render);

}

window.requestAnimFrame = (function () {

    return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.msRequestAnimationFrame

})();

window.cancelAnimFrame = (function () {

    return window.cancelAnimationFrame ||
        window.mozCancelAnimationFrame;

})();

//---

document.addEventListener('DOMContentLoaded', () => {

    init();

});

//---