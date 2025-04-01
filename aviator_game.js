import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

let scene, camera, renderer, airplane;
let betAmount = 0, multiplier = 1, gameRunning = false;

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 5, 10);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10).normalize();
    scene.add(light);

    const loader = new GLTFLoader();
    loader.load('path/to/airplane_model.glb', (gltf) => {
        airplane = gltf.scene;
        airplane.scale.set(1, 1, 1);
        airplane.position.set(0, 0, 0);
        scene.add(airplane);
    });

    document.getElementById('betButton').addEventListener('click', placeBet);
    document.getElementById('cashoutButton').addEventListener('click', cashout);

    window.addEventListener('resize', onWindowResize, false);
    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function placeBet() {
    if (!gameRunning) {
        betAmount = parseFloat(document.getElementById('betAmount').value);
        if (betAmount > 0) {
            multiplier = 1;
            gameRunning = true;
            airplane.position.set(0, 0, 0);
            animateGame();
        }
    }
}

function cashout() {
    if (gameRunning) {
        let winnings = betAmount * multiplier;
        alert(`You cashed out at x${multiplier}! You won $${winnings.toFixed(2)}`);
        gameRunning = false;
    }
}

function animateGame() {
    if (gameRunning) {
        requestAnimationFrame(animateGame);
        airplane.position.z -= 0.1;
        multiplier += 0.01;
        document.getElementById('multiplierDisplay').innerText = `Multiplier: x${multiplier.toFixed(2)}`;
    }
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

init();
