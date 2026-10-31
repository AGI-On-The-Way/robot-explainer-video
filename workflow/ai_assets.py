"""Local AI footage for the presenter cut: stills from Z-Image-Turbo (Apache-2.0), motion from Wan 2.2 TI2V-5B (Apache-2.0).

  .venv-mlx/bin/python -I workflow/ai_assets.py stills [id ...]
  .venv-wan/bin/python -I workflow/ai_assets.py clips [id ...]
Everything runs on this machine. Robots are generic with no brand marks, and every clip is labelled as an AI illustration on screen.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, 'work')
WAN = os.path.join(ROOT, 'vendor', 'Wan2.2-TI2V-5B-MLX')
SIZE = (704, 1280)
ROBOT = 'a full body bipedal humanoid robot standing on two legs with two arms and a head, matte graphite and white panels, realistic adult human proportions, plain sensor visor instead of a face'
LOOK = 'photorealistic cinematic film still, shallow depth of field, soft volumetric light, high detail, no text, no logos, no people'

# id → (scene prompt, motion prompt)
SHOTS = {
    'factory': (f'{ROBOT} carrying a metal car door along a modern automotive assembly line, car bodies and robot arms behind, cool blue light',
                'the robot walks forward steadily carrying the part, conveyor moves behind, slow camera dolly'),
    'warehouse': (f'{ROBOT} sorting parcels from a conveyor belt in a large logistics warehouse, tall shelving in the background, warm overhead light',
                  'the robot picks up a parcel and places it into a bin, conveyor moves, slow camera push in'),
    'patrol': (f'{ROBOT} walking toward the camera on a clear concrete path in an outdoor industrial park at dusk, whole body visible with nothing in front of it, large pipes along the far side of the path, orange sky, steel structures',
               'the robot walks slowly forward along the path and turns its head toward the pipes, slow tracking camera'),
    'grasp': ('close up of a humanoid robot hand with articulated metal fingers picking up a small machined gear from a workbench in a factory, cool light',
              'the robot fingers close around the gear and lift it slowly, very slow camera push in'),
    'lab': (f'{ROBOT} standing on a test platform in a university robotics laboratory, cables, monitors and workbenches around it, clean white light',
            'the robot lifts one arm slowly and shifts its weight, monitors flicker, slow camera pan'),
    'expo': (f'{ROBOT} on a stage at a technology exhibition, dramatic spotlights, dark hall, blurred booths in the background',
             'the robot waves one hand slowly under moving spotlights, slow camera arc'),
    'w_hook': ('a vast dark hall with rows of inactive humanoid robots in deep blue light, haze, symmetrical composition, seen from far away',
               'light slowly sweeps across the hall, haze drifts, very slow camera push in'),
    'w_perf': ('a dim research workshop full of robot arms and test rigs in deep indigo light, glowing status lamps, haze, seen from a distance',
               'status lamps pulse, robot arms move slightly, haze drifts, very slow camera drift'),
    'w_val': ('a city financial district at night seen through a tall glass window, deep burgundy and amber light, rain on the glass, blurred skyline',
              'rain runs slowly down the glass, city lights shimmer, very slow camera drift'),
    'w_mkt': ('aerial view of a huge modern factory complex with automated logistics yards at blue hour, teal light, long straight roads',
              'small vehicles move along the roads, clouds drift, very slow aerial camera move'),
    'w_end': ('sunrise over a wide industrial park and distant mountains, purple and gold sky, long shadows, calm atmosphere',
              'clouds drift, sunlight slowly grows, very slow camera push in'),
}


def stills(ids):
    os.makedirs(os.path.join(W, 'img'), exist_ok=True)
    tool = os.path.join(ROOT, '.venv-mlx', 'bin', 'mflux-generate-z-image-turbo')
    for k in ids:
        out = os.path.join(W, 'img', f'{k}.png')
        if not os.path.exists(out):
            subprocess.run([tool, '--prompt', f'{SHOTS[k][0]}, {LOOK}', '--width', str(SIZE[0]), '--height', str(SIZE[1]), '--steps', '9', '--seed', '11', '--quantize', '8', '--output', out], check=True, capture_output=True)
        print('still', k, flush=True)


def clips(ids):
    os.makedirs(os.path.join(W, 'clip'), exist_ok=True)
    for k in ids:
        out = os.path.join(W, 'clip', f'{k}.mp4')
        if not os.path.exists(out):
            subprocess.run([sys.executable, '-m', 'mlx_video.models.wan_2.generate', '--model-dir', WAN, '--image', os.path.join(W, 'img', f'{k}.png'), '--prompt', f'{SHOTS[k][1]}, photorealistic, stable, natural motion',
                            '--negative-prompt', 'text, logo, watermark, distorted limbs, flicker, jitter', '--width', str(SIZE[0]), '--height', str(SIZE[1]), '--num-frames', '81', '--steps', '30', '--seed', '11', '--output-path', out], check=True)
        print('clip', k, flush=True)


if __name__ == '__main__':
    what, ids = sys.argv[1], sys.argv[2:] or list(SHOTS)
    {'stills': stills, 'clips': clips}[what](ids)
