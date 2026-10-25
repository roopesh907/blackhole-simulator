
import { Suspense, useMemo, useRef } from "react";
import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { Line, OrbitControls, Stars } from "@react-three/drei";

const DISK_VERTEX_SHADER = `
  varying vec2 vUv;
  varying vec3 vPosition;

  void main() {
    vUv = uv;
    vPosition = position;

    gl_Position = projectionMatrix
      * modelViewMatrix
      * vec4(position, 1.0);
  }
`;

const DISK_FRAGMENT_SHADER = `
  uniform float uTime;
  uniform float uMass;

  varying vec2 vUv;
  varying vec3 vPosition;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
  }

  float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    return mix(
      mix(a, b, f.x),
      mix(c, d, f.x),
      f.y
    );
  }

  void main() {
    float radius = length(vPosition.xy);
    float angle = atan(vPosition.y, vPosition.x);

    float innerBound = 2.1 * uMass;
    float outerBound = 7.8 * uMass;

    float innerEdge = smoothstep(
      innerBound - 0.1 * uMass,
      innerBound + 0.4 * uMass,
      radius
    );

    float outerEdge = 1.0 - smoothstep(
      outerBound - 1.0 * uMass,
      outerBound,
      radius
    );

    float edgeMask = innerEdge * outerEdge;

    float flow = angle * 4.5 - uTime * (0.7 / max(uMass, 0.2));

    vec2 uv1 = vec2(
      flow + radius * 0.6,
      radius * (3.0 / uMass) - uTime * 0.4
    );

    vec2 uv2 = vec2(
      angle * 12.0 + radius,
      radius * (5.5 / uMass) - uTime * 0.85
    );

    float turbulence = noise(uv1 * 3.0);
    turbulence += noise(uv2 * 2.0) * 0.5;
    turbulence = clamp(turbulence / 1.5, 0.0, 1.0);

    float filaments = 0.5 + 0.5 * sin(
      angle * 28.0
      - uTime * 2.0
      + (radius / uMass) * 4.0
      + turbulence * 5.0
    );

    float plasma = clamp(
      0.15 + turbulence * 0.7 + filaments * 0.3,
      0.0,
      1.0
    );

    vec3 deepRed = vec3(0.25, 0.008, 0.015);
    vec3 redOrange = vec3(1.2, 0.08, 0.02);
    vec3 orange = vec3(1.5, 0.42, 0.04);
    vec3 gold = vec3(1.8, 1.1, 0.35);
    vec3 hotWhite = vec3(2.0, 1.9, 1.6);

    float innerHeat = 1.0 - smoothstep(
      innerBound,
      innerBound * 2.2,
      radius
    );

    vec3 color = mix(deepRed, redOrange, plasma);
    color = mix(color, orange, smoothstep(0.2, 0.65, plasma));
    color = mix(color, gold, innerHeat * 0.8);
    color = mix(color, hotWhite, innerHeat * plasma * 0.6);

    float radialFalloff = 1.0
      - smoothstep(innerBound * 1.8, outerBound, radius) * 0.45;

    color *= radialFalloff * 1.8;

    float alpha = edgeMask * (0.35 + plasma * 0.65);

    gl_FragColor = vec4(color, alpha);
  }
`;

function AccretionDisk({ mass }) {
  const materialRef = useRef(null);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uMass: { value: mass },
    }),
    []
  );

  useFrame(({ clock }) => {
    if (materialRef.current) {
      materialRef.current.uniforms.uTime.value = clock.elapsedTime;
      materialRef.current.uniforms.uMass.value = mass;
    }
  });

  return (
    <mesh
      rotation={[-Math.PI / 2, 0, 0]}
      renderOrder={1}
      scale={[mass, mass, mass]}
    >
      <ringGeometry args={[2.1, 7.8, 320, 1]} />
      <shaderMaterial
        ref={materialRef}
        vertexShader={DISK_VERTEX_SHADER}
        fragmentShader={DISK_FRAGMENT_SHADER}
        uniforms={uniforms}
        transparent
        depthWrite={false}
        side={THREE.DoubleSide}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  );
}

function EventHorizon({ mass }) {
  return (
    <mesh renderOrder={2} scale={[mass, mass, mass]}>
      <sphereGeometry args={[2, 64, 64]} />
      <meshBasicMaterial color="#000000" toneMapped={false} />
    </mesh>
  );
}

function PhotonRing({ mass }) {
  const ringRef = useRef(null);

  useFrame(({ clock }) => {
    if (ringRef.current) {
      ringRef.current.rotation.y = clock.elapsedTime * 0.05;
    }
  });

  return (
    // IMPORTANT: rotate the torus from XY into the disk's XZ plane.
    <group
      rotation={[Math.PI / 2, 0, 0]}
      scale={[mass, mass, mass]}
    >
      <group ref={ringRef}>
        <mesh>
          <torusGeometry args={[2.92, 0.085, 16, 256]} />
          <meshBasicMaterial
            color="#ff8c2e"
            transparent
            opacity={0.4}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
            toneMapped={false}
          />
        </mesh>

        <mesh>
          <torusGeometry args={[2.92, 0.022, 16, 256]} />
          <meshBasicMaterial
            color="#ffffff"
            transparent
            opacity={1.0}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
            toneMapped={false}
          />
        </mesh>
      </group>
    </group>
  );
}

function PhotonTrajectory({ points = [] }) {
  const trajectory = useMemo(() => {
    if (!Array.isArray(points) || points.length < 2) {
      return [];
    }

    return points
      .filter(
        (point) =>
          Number.isFinite(point.x) &&
          Number.isFinite(point.y) &&
          Number.isFinite(point.z)
      )
      // Map the physics XY orbital plane into Three.js's XZ disk plane.
      .map((point) => new THREE.Vector3(point.x, point.z, point.y));
  }, [points]);

  if (trajectory.length < 2) {
    return null;
  }

  return (
    <Line
      points={trajectory}
      color="#70d6ff"
      lineWidth={2}
      transparent
      opacity={0.95}
    />
  );
}

function SceneContents({ points, mass }) {
  return (
    <>
      <color attach="background" args={["#000002"]} />

      <ambientLight intensity={0.2} />

      <Stars
        radius={100}
        depth={50}
        count={2500}
        factor={4}
        saturation={0.1}
        fade
        speed={0.15}
      />

      <Suspense fallback={null}>
        <AccretionDisk mass={mass} />
        <EventHorizon mass={mass} />
        <PhotonRing mass={mass} />
      </Suspense>

      <PhotonTrajectory points={points} />

      <OrbitControls
        makeDefault
        enableDamping
        dampingFactor={0.05}
        minDistance={6}
        maxDistance={35}
        maxPolarAngle={Math.PI * 0.82}
      />
    </>
  );
}

export default function BlackHoleScene({ points = [], mass = 1.0 }) {
  return (
    <Canvas
      camera={{
        position: [0, 6, 13],
        fov: 45,
        near: 0.1,
        far: 200,
      }}
      dpr={[1, 2]}
      gl={{
        antialias: true,
        powerPreference: "high-performance",
        alpha: false,
      }}
    >
      <SceneContents points={points} mass={mass} />
    </Canvas>
  );
}
