/********** ZDOG - Minimal Lighthouse Animation */
let illo = new Zdog.Illustration({
    element: ".canvas",
    //dragRotate: true,
    rotate: {x: -0.15},
    zoom: 0.85
});

/********** wave form shape */
function Shape(stroke, base, vertices_quantity, width, value, x, y, z, color) {
    this.stroke = stroke;
    this.base = base;
    this.vertices_quantity = vertices_quantity;
    this.width = width;
    this.value = value;

    this.wave_limits = this.base / 2;
    this.vertices_gap = this.width / this.vertices_quantity;

    this.shapePaths = this.createShapePath();

    this.obj = new Zdog.Shape({
        addTo: illo,
        path: this.shapePaths,
        stroke: this.stroke,
        closed: false,
        color: color,
        translate: {x: x, y: y, z: z},
        fill: true
    });
}

Shape.prototype.createShapePath = function() {
    let shapePaths = [];

    for (let i = 0; i < this.vertices_quantity; i++) {
        let val = this.value * i;
        shapePaths.push({
            x: this.vertices_gap * (i - this.vertices_quantity / 2),
            y: this.base + Math.sin(val) * this.base / 1.2,
            val: val
        });
    }

    shapePaths.push({
        x: shapePaths[shapePaths.length - 1].x,
        y: this.base * 2 + this.wave_limits
    });

    shapePaths.push({
        x: shapePaths[0].x,
        y: this.base * 2 + this.wave_limits
    });

    shapePaths.push({
        x: shapePaths[0].x,
        y: shapePaths[0].y
    });

    return shapePaths;
}

Shape.prototype.update = function(value) {
    for (let i = 0; i < this.shapePaths.length - 3; i++) {
        this.shapePaths[i].val += value;
        this.shapePaths[i].y = this.base + Math.sin(this.shapePaths[i].val * 1.5) * this.wave_limits;
    }

    this.shapePaths[this.shapePaths.length - 3].x = this.shapePaths[this.shapePaths.length - 4].x;
    this.shapePaths[this.shapePaths.length - 2].x = this.shapePaths[0].x;
    this.shapePaths[this.shapePaths.length - 1].x = this.shapePaths[0].x;
    this.shapePaths[this.shapePaths.length - 1].y = this.shapePaths[0].y;

    this.obj.path = this.shapePaths;
    this.obj.updatePath();
}

/********** tower body */
let tower_body = new Zdog.Cylinder({
    addTo: illo,
    diameter: 50,
    length: 120,
    stroke: false,
    color: '#464D55',
    backface: '#7D8288',
    rotate: {x: Math.PI / 2},
    translate: {x: -30, y: 50, z: -175}
  });

/********** tower windows */
let tower_window = new Zdog.Ellipse({
    addTo: tower_body,
    diameter: 5,
    stroke: 10,
    color: '#D4D4D4',
    rotate: {x: -Math.PI / 2},
    translate: {x: 0, y: 25, z: 30}
});

tower_window.copy({
    translate: {x: 0, y: 25, z: 0}
});

tower_window.copy({
    translate: {x: 0, y: 25, z: -30}
});

/********** light and fake light to rotate the light effect */
let light = tower_body.copy({
    diameter: 25,
    length: 20,
    translate: {x: -30, z: -177, y: -20},
    color: "#F4F4F4",
    backface: "#FFFFFF"
});

let f_light = light.copy({
    visible: false
});

/********** light effect */
new Zdog.Cone({
    addTo: f_light,
    diameter: 70,
    length: 250,
    stroke: false,
    color: 'rgba(255, 255, 255, 0.5)',
    backface: 'rgba(255, 255, 255, 0.75)',
    rotate: {x: -Math.PI / 2 - 0.4, y: -Math.PI},
    translate: {y: 240, z: -90}
});

/********** dome of the tower */
new Zdog.Hemisphere({
    addTo: tower_body,
    diameter: 60,
    // fill enabled by default
    // disable stroke for crisp edge
    stroke: false,
    color: '#343C44',
    backface: '#7D8288',
    translate: {x: 0, y: 0, z: 80}
  });

/********** ground of the tower's dome */
tower_body.copy({
    diameter: 60,
    length: 15,
    translate: {x: -30, z: -177, y: -2},
    color: '#343C44',
    backface: '#7D8288',
});

/********** initialization of wave form shapes */
let A = new Shape(5, 45, 40, 600, 0.20, 0, 40, 0, "#1CACF4");
let B = new Shape(5, 60, 65, 600, 0.05, 0, 2, -50, "#1A9DDE");
let C = new Shape(5, 65, 50, 600, 0.08, 0, -10, -100, "#178DC8");
let D = new Shape(5, 60, 40, 600, 0.12, 0, 0, -240, "#157EB2");

let tick = 0;

function animate() {
    A.update(0.012);
    B.update(0.016);
    C.update(0.020);
    D.update(0.010);


    illo.rotate.y = -Math.sin(tick) * 0.2;
    f_light.rotate.z = -Math.sin(tick * 1.5) * 0.8;
    f_light.rotate.y = -Math.sin(tick * 1.2) * 0.4;
    tick += 0.006;

    illo.updateRenderGraph();
    requestAnimationFrame(animate);
}

animate();