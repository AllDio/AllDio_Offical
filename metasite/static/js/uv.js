var container, stats;
var camera, controls, scene, renderer;
var info;
var cube;
var sphereTab = [];
var objects = [];
var parent2;
var sun;
var sun2;
var sun3;
var currentcolor;
var cubeNul;
var earthPivot;
var earthPivot3;
var mesh;
var planetViewed = 0;
init();
animate();
$(window).on('load', function () {
    TweenMax.to($('#welcome'), 1, {
        css: {
            opacity: 1
        },
        ease: Quad.easeInOut,
    });
    TweenMax.to($('#social'), 0.5, {
        css: {
            bottom: '20px'
        }, delay: 0.5,
        ease: Quad.easeInOut,
    });
    TweenMax.to($('#border'), 0.5, {
        css: {
            height: '200px',
        },
        delay: 0.5,
        ease: Quad.easeInOut,
    });

});

function hideWelcome() {
    TweenMax.to($('#welcome'), 0.5, {
        css: {
            opacity: 0
        },
        ease: Quad.easeInOut
    });
    TweenMax.to($('#welcome'), 0.5, {
        css: {
            display: 'none'
        },
        delay: 1,
        ease: Quad.easeInOut
    });
}


function init() {
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.z = 68;
    controls = new THREE.OrbitControls(camera);
    controls.maxDistance = 300;
    controls.minDistance = 30;
    scene = new THREE.Scene();
    var geoSphere = new THREE.SphereGeometry(Math.random() * 1, 20, 20);
    for (var i = 0; i < 500; i++) {
        // randRadius = Math.random()*30+10;
        lumiereS = new THREE.MeshPhongMaterial({
            emissive: '#fff'
        });
        sphereTab.push(new THREE.Mesh(new THREE.SphereGeometry(Math.random() * 1, 20, 20), lumiereS));
    }
    var posX = -3000;
    var posY = -3000;
    for (var i = 0; i < sphereTab.length; i++) {
        sphereTab[i].position.set(Math.random() * 600 - 300, Math.random() * 600 - 300, Math.random() * 600 - 300);
        scene.add(sphereTab[i]);
    }
    //////Sun////////
    var pinkMat = new THREE.MeshPhongMaterial({
        color: 0xF66120,
        emissive: 0xF66120,
        specular: 0xFFED22,
        shininess: 10,
        shading: THREE.FlatShading,
        transparent: 1,
        opacity: 1
    });
    var pinkMat2 = new THREE.MeshPhongMaterial({
        color: 0xF66120,
        emissive: 0xF66120,
        specular: 0xFFED22,
        shininess: 10,
        shading: THREE.FlatShading,
        transparent: 1,
        opacity: 1
    });


    var geometry = new THREE.IcosahedronGeometry(3, 1);
    var geometry2 = new THREE.IcosahedronGeometry(2.5, 1);
    var geometry4 = new THREE.IcosahedronGeometry(3, 1);
    // material
    var material = new THREE.MeshPhongMaterial({
        color: 0xffc12d,
        emissive: 0xffc12d,
        shading: THREE.FlatShading
    });
    var material2 = new THREE.MeshPhongMaterial({
        color: 0x26D7E7,
        emissive: 0x26D7E7,
        shading: THREE.FlatShading
    });
    var material4 = new THREE.MeshPhongMaterial({
        color: 0xacacac,
        emissive: 0xacacac,
        shading: THREE.FlatShading
    });

    sun = new THREE.Mesh(new THREE.IcosahedronGeometry(10, 1), pinkMat);
    scene.add(sun);
    objects.push(sun);
    sun2 = new THREE.Mesh(new THREE.IcosahedronGeometry(10, 1), pinkMat2);
    sun2.rotation.x = 1;
    scene.add(sun2);
    objects.push(sun2);
    sun3 = new THREE.Mesh(new THREE.IcosahedronGeometry(10, 1), pinkMat2);
    sun3.rotation.x = 1;
    scene.add(sun2);
    objects.push(sun3);

    earthPivot3 = new THREE.Object3D();
    sun.add(earthPivot3);

    var radius = 16;
    var tubeRadius = 0.03;
    var radialSegments = 8 * 10;
    var tubularSegments = 6 * 15;
    var arc = Math.PI * 3;
    var geometry3 = new THREE.TorusGeometry(radius, tubeRadius, radialSegments, tubularSegments, arc);
    var material3 = new THREE.MeshLambertMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        shading: THREE.FlatShading,
    });
    mesh = new THREE.Mesh(geometry3, material3);
    earthPivot3.add(mesh);
    /// planet blue ///
    earthPivot = new THREE.Object3D();
    sun.add(earthPivot);
    var earth = new THREE.Mesh(geometry, material);
    earth.position.x = 15;
    earthPivot.add(earth);
    objects.push(earth);
    ///// planet green ////
    earthPivot2 = new THREE.Object3D();
    sun.add(earthPivot2);
    var earth2 = new THREE.Mesh(geometry2, material2);
    earth2.position.x = 20;
    earthPivot2.add(earth2);
    objects.push(earth2);
    ////planet violet ///
    earthPivot4 = new THREE.Object3D();
    sun.add(earthPivot4);
    var earth3 = new THREE.Mesh(geometry4, material4);
    earth3.position.x = 26;
    earthPivot4.add(earth3);
    objects.push(earth3);

    // lights
    light = new THREE.DirectionalLight(0x4f4f4f);
    light.position.set(4, 4, 4);
    scene.add(light);
    light = new THREE.DirectionalLight(0x4f4f4f);
    light.position.set(-4, -4, -4);
    scene.add(light);
    //render
    renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    renderer.sortObjects = false;
    renderer.setClearColor(0x131A3D, 1);
    renderer.setSize(window.innerWidth, window.innerHeight);
    stats = new Stats();
    container = document.getElementById('container');
    container.appendChild(renderer.domElement);
    window.addEventListener('resize', onWindowResize, false);
    info = document.getElementById('contentTitle');
    subtitle = document.getElementById('subtitle');
    description = document.getElementById('description')
    var univers = document.getElementById('univers');
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

function setFromCamera(raycaster, coords, origin) {
    raycaster.ray.origin.copy(camera.position);
    raycaster.ray.direction.set(coords.x, coords.y, 0.5).unproject(camera).sub(camera.position).normalize();
}

function onMouseDown(event) {
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    mouse.x = (event.clientX / renderer.domElement.width) * 2 - 1;
    mouse.y = -(event.clientY / renderer.domElement.height) * 2 + 1;
    setFromCamera(raycaster, mouse, camera);
    var intersects = raycaster.intersectObjects(objects);
    currentcolor = intersects[0].object.material.color.getHex();
    if (intersects.length > 0) {
        console.log(currentcolor);
        switch (intersects[0].object.geometry.type) {
            case 'IcosahedronGeometry':
                if (currentcolor == 0xF66120) {
                    if (planetViewed == 0) {
                        hideWelcome();
                        planetViewed = 1;
                        TweenMax.from($('#content'), 0.5, {
                            css: {
                                left: '-500px'
                            },
                            delay: 0.5,
                            ease: Quad.easeInOut
                        });

                        TweenMax.from($('#border'), 0.5, {
                            css: {
                                height: '0px'
                            },
                            delay: 1,
                            ease: Quad.easeInOut,
                        });

                        info.innerHTML = " <span>Sunny</span> Icosahedron,";

                        description.innerHTML = "Alive for <span>204895</span> years<br/><br/><div>Click on the other planets to learn more ...<div>";
                    }
                    if (planetViewed == 2 || planetViewed == 3 || planetViewed == 4) {
                        planetViewed = 1;
                        TweenMax.from($('#content'), 0.5, {
                            css: {
                                left: '-500px'
                            },
                            ease: Quad.easeInOut
                        });
                        TweenMax.to($('#border'), 0.2, {
                            css: {
                                height: '200px'
                            }, delay: 1,
                            ease: Quad.easeInOut,
                        });
                        TweenMax.from($('#border'), 0.5, {
                            css: {
                                height: '0px'
                            },
                            delay: 0.5,
                            ease: Quad.easeInOut,
                        });

                        info.innerHTML = " <span>Sunny</span> Icosahedron,";

                        description.innerHTML = "Alive for <span>204895</span> years<br/><br/><div>Click on the other planets to learn more ...<div>";
                    }
                }
                if (currentcolor == 0x26D7E7) {
                    if (planetViewed == 1 || planetViewed == 3 || planetViewed == 4) {
                        planetViewed = 2;
                        info.innerHTML = " <span id='couleur'>Blue</span> Icosahedron,";

                        document.getElementById('couleur').style.color = "#26d7e7";

                        description.innerHTML = "<br/><br/><div>Click on the other planets to learn more ...<div>";

                        TweenMax.from($('#content'), 0.5, {
                            css: {
                                left: '-500px'
                            },
                            ease: Quad.easeInOut
                        });
                        TweenMax.to($('#border'), 0.2, {
                            css: {
                                height: '200px'
                            }, delay: 1,
                            ease: Quad.easeInOut,
                        });

                        TweenMax.from($('#border'), 0.5, {
                            css: {
                                height: '0px'
                            },
                            delay: 0.5,
                            ease: Quad.easeInOut,
                        });
                    }
                }
                if (currentcolor == 0xffc12d) {
                    if (planetViewed == 1 || planetViewed == 2 || planetViewed == 4) {
                        planetViewed = 3;
                        info.innerHTML = '<span id="couleur">Yellow</span> Icosahedron';


                        description.innerHTML = "<br/><br/><div>Click on the other planets to learn more ...<div>";
                        document.getElementById('couleur').style.color = "#ffc12d";

                        TweenMax.from($('#content'), 0.5, {
                            css: {
                                left: '-500px'
                            },
                            ease: Quad.easeInOut
                        });

                        TweenMax.to($('#border'), 0.2, {
                            css: {
                                height: '200px'
                            }, delay: 1,
                            ease: Quad.easeInOut,
                        });
                        TweenMax.from($('#border'), 0.5, {
                            css: {
                                height: '0px'
                            },
                            delay: 0.5,
                            ease: Quad.easeInOut,
                        });
                    }
                }
                if (currentcolor == 0xacacac) {
                    if (planetViewed == 1 || planetViewed == 2 || planetViewed == 3) {
                        planetViewed = 4;
                        info.innerHTML = '<span id="couleur">Grey</span> Icosahedron';
                        document.getElementById('couleur').style.color = "#acacac";

                        description.innerHTML = "<br/><br/><div>Click on the other planets to learn more ...<div>";

                        TweenMax.from($('#content'), 0.5, {
                            css: {
                                left: '-500px'
                            },
                            ease: Quad.easeInOut
                        });

                        TweenMax.to($('#border'), 0.1, {
                            css: {
                                height: '200px'
                            }, delay: 1,
                            ease: Quad.easeInOut,
                        });
                        TweenMax.from($('#border'), 0.5, {
                            css: {
                                height: '0px'
                            },
                            delay: 0.5,
                            ease: Quad.easeInOut,
                        });
                    }
                }
                break;
        }
    }
    console.log('Down');
}

document.addEventListener('mousedown', onMouseDown, false);

function animate() {
    ;
    var timer = 0.00001 * Date.now();
    for (var i = 0, il = sphereTab.length; i < il; i++) {
        var sfere = sphereTab[i];
        sfere.position.x = 400 * Math.sin(timer + i);
        // sfere.position.z= 500 * Math.sin( timer + i * 1.1 );
        sfere.position.z = 400 * Math.sin(timer + i * 1.1);
    }
    sun.rotation.x += 0.008;
    sun2.rotation.y += 0.008;
    sun3.rotation.z += 0.008;
    earthPivot.rotation.z += 0.006;
    earthPivot2.rotation.z += 0.01;
    earthPivot3.rotation.y += 0.007;
    earthPivot4.rotation.z += 0.008;
    requestAnimationFrame(animate);
    controls.update();
    render();
}

function render() {
    // }
    renderer.render(scene, camera)
}