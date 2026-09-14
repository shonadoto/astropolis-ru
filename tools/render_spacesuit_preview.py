#!/usr/bin/env python3
"""Build an interactive in-conversation preview of the current spacesuit."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path
from zipfile import ZipFile

from customize_spacesuit import OUTPUT as LAYER_1_PATH
from customize_spacesuit import find_cosmopolis_jar


LAYER_2_MEMBER = "assets/cosmopolis/textures/models/armor/space_suit_layer_2.png"


def png_data_uri(data: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def build_fragment(layer_1: str, layer_2: str) -> str:
    fragment = r'''
<div id="astropolis-armor-preview">
  <h2>Скафандр — текущий вариант</h2>
  <div class="viz-controls" aria-label="Ракурс">
    <button class="btn" type="button" data-view="front" aria-pressed="false">Спереди</button>
    <button class="btn btn-primary" type="button" data-view="three" aria-pressed="true">Под углом</button>
    <button class="btn" type="button" data-view="back" aria-pressed="false">Сзади</button>
  </div>
  <div class="armor-stage" role="img" aria-label="Интерактивный трёхмерный манекен в текущей броне Astropolis. Манекен можно вращать мышью.">
    <canvas></canvas>
    <div class="armor-loading text-muted" aria-live="polite">Загрузка текстур…</div>
  </div>
  <div class="text-small text-muted">Потащи модель мышью, чтобы рассмотреть бока. Скин под бронёй показан условно.</div>
</div>

<style>
  #astropolis-armor-preview { width: 100%; color: var(--foreground); }
  #astropolis-armor-preview h2 { margin: 0 0 12px; }
  #astropolis-armor-preview .viz-controls { margin-bottom: 8px; }
  #astropolis-armor-preview .armor-stage {
    position: relative;
    width: 100%;
    height: 540px;
    min-height: 420px;
    overflow: hidden;
    background: radial-gradient(circle at 50% 44%, color-mix(in srgb, var(--muted) 55%, transparent), transparent 68%);
  }
  #astropolis-armor-preview canvas {
    display: block;
    width: 100%;
    height: 100%;
    cursor: grab;
    image-rendering: pixelated;
    touch-action: none;
  }
  #astropolis-armor-preview canvas:active { cursor: grabbing; }
  #astropolis-armor-preview .armor-loading {
    position: absolute;
    inset: 50% auto auto 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
  }
  @media (max-width: 480px) {
    #astropolis-armor-preview .armor-stage { height: 460px; min-height: 380px; }
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
<script>
(() => {
  const root = document.getElementById('astropolis-armor-preview');
  if (!root || root.dataset.ready) return;
  root.dataset.ready = '1';

  const canvas = root.querySelector('canvas');
  const loading = root.querySelector('.armor-loading');
  const layer1Url = '__LAYER1__';
  const layer2Url = '__LAYER2__';
  const views = { front: 0, three: -0.58, back: Math.PI };

  if (typeof THREE === 'undefined') {
    loading.textContent = 'Не удалось загрузить модуль 3D-просмотра.';
    loading.classList.add('text-destructive');
    return;
  }

  const loadImage = src => new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = reject;
    image.src = src;
  });

  Promise.all([loadImage(layer1Url), loadImage(layer2Url)]).then(([layer1, layer2]) => {
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 200);
    camera.position.set(0, 19, 72);
    camera.lookAt(0, 16, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x34404c, 2.1));
    const key = new THREE.DirectionalLight(0xffffff, 2.2);
    key.position.set(12, 30, 28);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0x8bb8ff, 1.0);
    rim.position.set(-22, 16, -18);
    scene.add(rim);

    const character = new THREE.Group();
    character.rotation.y = views.three;
    scene.add(character);

    function cropTexture(image, x, y, width, height) {
      const source = document.createElement('canvas');
      source.width = width;
      source.height = height;
      const context = source.getContext('2d');
      context.imageSmoothingEnabled = false;
      context.drawImage(image, x, y, width, height, 0, 0, width, height);
      const texture = new THREE.CanvasTexture(source);
      texture.magFilter = THREE.NearestFilter;
      texture.minFilter = THREE.NearestFilter;
      texture.generateMipmaps = false;
      texture.colorSpace = THREE.SRGBColorSpace;
      return texture;
    }

    function faceMaterial(image, rect, shade = 0xffffff) {
      return new THREE.MeshLambertMaterial({
        map: cropTexture(image, ...rect),
        color: shade,
        transparent: true,
        alphaTest: 0.02,
        side: THREE.DoubleSide
      });
    }

    function boxMaterials(image, uv) {
      return [
        faceMaterial(image, uv.right, 0xd9e1e7),
        faceMaterial(image, uv.left, 0xc9d2d9),
        faceMaterial(image, uv.top, 0xffffff),
        faceMaterial(image, uv.bottom, 0xaab5bd),
        faceMaterial(image, uv.front, 0xf2f6f8),
        faceMaterial(image, uv.back, 0xbdc8d0)
      ];
    }

    const UV = {
      head: {
        right: [0, 8, 8, 8], left: [16, 8, 8, 8], top: [8, 0, 8, 8],
        bottom: [16, 0, 8, 8], front: [8, 8, 8, 8], back: [24, 8, 8, 8]
      },
      torso: {
        right: [16, 20, 4, 12], left: [28, 20, 4, 12], top: [20, 16, 8, 4],
        bottom: [28, 16, 8, 4], front: [20, 20, 8, 12], back: [32, 20, 8, 12]
      },
      arm: {
        right: [40, 20, 4, 12], left: [48, 20, 4, 12], top: [44, 16, 4, 4],
        bottom: [48, 16, 4, 4], front: [44, 20, 4, 12], back: [52, 20, 4, 12]
      },
      leg: {
        right: [0, 20, 4, 12], left: [8, 20, 4, 12], top: [4, 16, 4, 4],
        bottom: [8, 16, 4, 4], front: [4, 20, 4, 12], back: [12, 20, 4, 12]
      }
    };

    function solidMaterials(color) {
      return Array.from({ length: 6 }, () => new THREE.MeshLambertMaterial({ color }));
    }

    function addBox(parent, size, position, materials, order = 0) {
      const geometry = new THREE.BoxGeometry(...size);
      const mesh = new THREE.Mesh(geometry, materials);
      mesh.position.set(...position);
      mesh.renderOrder = order;
      parent.add(mesh);
      return mesh;
    }

    // Neutral mannequin underneath transparent armor pixels.
    addBox(character, [8, 8, 8], [0, 28, 0], solidMaterials(0xb98263));
    addBox(character, [8, 12, 4], [0, 18, 0], solidMaterials(0x263746));
    addBox(character, [4, 12, 4], [-6, 18, 0], solidMaterials(0xb98263));
    addBox(character, [4, 12, 4], [6, 18, 0], solidMaterials(0xb98263));
    addBox(character, [4, 12, 4], [-2.05, 6, 0], solidMaterials(0x202c38));
    addBox(character, [4, 12, 4], [2.05, 6, 0], solidMaterials(0x202c38));

    // Armor passes follow Minecraft's layer-1 / layer-2 atlases.
    addBox(character, [8.6, 8.6, 8.6], [0, 28, 0], boxMaterials(layer1, UV.head), 3);
    addBox(character, [8.45, 12.45, 4.45], [0, 18, 0], boxMaterials(layer1, UV.torso), 3);
    addBox(character, [4.45, 12.45, 4.45], [-6, 18, 0], boxMaterials(layer1, UV.arm), 3);
    addBox(character, [4.45, 12.45, 4.45], [6, 18, 0], boxMaterials(layer1, UV.arm), 3);
    addBox(character, [4.28, 12.28, 4.28], [-2.05, 6, 0], boxMaterials(layer2, UV.leg), 2);
    addBox(character, [4.28, 12.28, 4.28], [2.05, 6, 0], boxMaterials(layer2, UV.leg), 2);
    addBox(character, [4.48, 12.48, 4.48], [-2.05, 6, 0], boxMaterials(layer1, UV.leg), 3);
    addBox(character, [4.48, 12.48, 4.48], [2.05, 6, 0], boxMaterials(layer1, UV.leg), 3);

    // Small ground shadow helps the silhouette read without framing the canvas.
    const shadow = new THREE.Mesh(
      new THREE.CircleGeometry(8.5, 48),
      new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.16, depthWrite: false })
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = -0.35;
    scene.add(shadow);

    let targetYaw = views.three;
    let dragging = false;
    let lastX = 0;

    function selectView(name) {
      targetYaw = views[name];
      root.querySelectorAll('[data-view]').forEach(button => {
        const selected = button.dataset.view === name;
        button.setAttribute('aria-pressed', String(selected));
        button.classList.toggle('btn-primary', selected);
      });
    }

    root.querySelectorAll('[data-view]').forEach(button => {
      button.addEventListener('click', () => selectView(button.dataset.view));
    });
    canvas.addEventListener('pointerdown', event => {
      dragging = true;
      lastX = event.clientX;
      canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener('pointermove', event => {
      if (!dragging) return;
      const delta = event.clientX - lastX;
      lastX = event.clientX;
      targetYaw += delta * 0.012;
      root.querySelectorAll('[data-view]').forEach(button => {
        button.setAttribute('aria-pressed', 'false');
        button.classList.remove('btn-primary');
      });
    });
    canvas.addEventListener('pointerup', event => {
      dragging = false;
      canvas.releasePointerCapture(event.pointerId);
    });
    canvas.addEventListener('pointercancel', () => { dragging = false; });

    function resize() {
      const width = Math.max(1, canvas.clientWidth);
      const height = Math.max(1, canvas.clientHeight);
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    }
    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    resize();
    loading.remove();

    function animate() {
      character.rotation.y += (targetYaw - character.rotation.y) * 0.13;
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }
    animate();
  }).catch(() => {
    loading.textContent = 'Не удалось прочитать текстуры брони.';
    loading.classList.add('text-destructive');
  });
})();
</script>
'''
    return fragment.replace("__LAYER1__", layer_1).replace("__LAYER2__", layer_2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="Destination HTML fragment")
    args = parser.parse_args()

    layer_1 = png_data_uri(LAYER_1_PATH.read_bytes())
    with ZipFile(find_cosmopolis_jar()) as archive:
        layer_2 = png_data_uri(archive.read(LAYER_2_MEMBER))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_fragment(layer_1, layer_2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
