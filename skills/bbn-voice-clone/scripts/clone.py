"""Create Thai speech with the saved BoomBigNose profile."""
import argparse
import json
import os
from pathlib import Path
from uuid import uuid4

from voice_engine import synthesize, validate_settings


def load_kit(kit=None, profile=None):
    """Kit folder (argument, installed assets/kit-location.json, or three levels above scripts/) and its profile."""
    locator=Path(__file__).resolve().parents[1]/'assets/kit-location.json'
    if kit is None:
        kit=Path(json.loads(locator.read_text())['kit']) if locator.exists() else Path(__file__).resolve().parents[3]
    kit=kit.resolve()
    return kit,json.loads((profile or kit/'voice/profile.json').read_text())


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit',type=Path)
    parser.add_argument('--profile',type=Path)
    parser.add_argument('--text-file',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--pitch',type=float,help='Pitch in semitones; default -0.5')
    parser.add_argument('--pace',type=float,help='Duration factor; default 0.85, higher speaks slower')
    parser.add_argument('--pause-scale',type=float,help='Scale pauses; default 1.0')
    parser.add_argument('--seed',type=int,help='Retake with another seed (profile default 42); same text + seed = same take')
    parser.add_argument('--no-breath-cleanup',action='store_true',help='Keep audible inhales (default: muted)')
    parser.add_argument('--keep-lead',action='store_true',help='Keep a sound+inhale at a phrase start (default: dropped as เอ่อ)')
    args=parser.parse_args()
    kit,profile=load_kit(args.kit,args.profile)
    settings=dict(profile['settings'])
    for option,key in ((args.pitch,'pitch_semitones'),(args.pace,'pace_factor'),(args.pause_scale,'pause_scale'),(args.seed,'seed')):
        if option is not None: settings[key]=option
    validate_settings(settings)
    output=args.output or kit/'generated'/f'thai-{uuid4().hex[:12]}.wav'
    if output.exists():
        parser.error('Output exists; choose a new filename to preserve it')
    output.parent.mkdir(parents=True,exist_ok=True)
    os.environ['HF_HUB_OFFLINE']='1'
    synthesize(str(kit/profile['reference']),profile['reference_text'],args.text_file.read_text().strip(),str(output),kit/profile['model']['path'],settings,
               breath_cleanup=not args.no_breath_cleanup,drop_lead_filler=not args.keep_lead)
    quality=json.loads(output.with_suffix('.json').read_text())['quality']
    if quality['status']=='needs_review':
        print('ต้องฟังทวน: '+'; '.join(quality['flags']))
    else:
        print('ตรวจอัตโนมัติผ่าน: ตัดคำแทรก คำซ้ำ เดดแอร์ และเสียงหายใจแล้ว')
    print(output.resolve())


if __name__=='__main__': main()
