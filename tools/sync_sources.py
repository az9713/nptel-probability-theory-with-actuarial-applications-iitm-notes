"""Produce public source metadata from private evidence without copying source text."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    path=ROOT/'source-manifest.json'
    manifest=json.loads(path.read_text(encoding='utf-8'))
    records=[]
    for video in manifest['recordings']:
        video_id=video['id']
        audio=ROOT/'work/sources'/f'{video_id}.m4a'
        transcript=ROOT/'work/sources'/f'{video_id}.transcript.json'
        record={'id':video_id,'title':video['title'],'chapters':video['chapters'],
                'identity':video['status'],'textual':'unavailable','visual':'not comprehensively reviewed'}
        if audio.exists():
            result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
                '-of','default=noprint_wrappers=1:nokey=1',str(audio)],capture_output=True,text=True,check=True)
            duration=float(result.stdout.strip())
            record.update({'audio_duration':duration,'audio_sha256':digest(audio),
                'audio_bytes':audio.stat().st_size,
                'duration_matches_metadata':abs(duration-(video['duration'] or duration))<2})
        if transcript.exists():
            text=json.loads(transcript.read_text(encoding='utf-8'))
            record.update({'textual':'machine transcript acquired',
                'transcription_method':text['method'],'transcript_sha256':digest(transcript),
                'segments':len(text['segments']),
                'first_segment_start':text['segments'][0]['start'] if text['segments'] else None,
                'last_segment_end':text['segments'][-1]['end'] if text['segments'] else None,
                'transcribed_audio_matches_current':text['source_audio_sha256']==record.get('audio_sha256')})
        video['source_evidence']={k:v for k,v in record.items() if k not in ['id','title','chapters']}
        records.append(record)
    path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    available=[r for r in records if r['identity']=='available']
    report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'listed_entries':len(records),'available_recordings':len(available),
        'available_lecture_uploads':sum(bool(r['chapters']) for r in available),
        'audio_files':sum('audio_sha256' in r for r in records),
        'machine_transcripts':sum(r['textual']=='machine transcript acquired' for r in records),
        'all_available_audio_duration_checks_pass':all(r.get('duration_matches_metadata',False) for r in available),
        'all_transcribed_audio_hashes_match':all(r.get('transcribed_audio_matches_current',False) for r in available),
        'caption_status':'Retrieval failed; publisher captions not used',
        'visual_scope':'No comprehensive audiovisual or slide transcription claimed',
        'records':records}
    (ROOT/'source-validation-summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print({k:v for k,v in report.items() if k!='records'})

if __name__=='__main__': main()
