#!/usr/bin/env python3
"""Build an offline Casorama HTML report from a UTF-8 JSON manifest."""
import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / 'assets' / 'report-template.html'
def esc(value):
    return html.escape(str(value), quote=True)
def image_url(path, base):
    p = Path(path)
    if not p.is_absolute(): p = base / p
    if not p.is_file(): raise ValueError(f'Image not found: {p}')
    mime = mimetypes.guess_type(p.name)[0]
    if mime not in ('image/png','image/jpeg','image/webp','image/gif'):
        raise ValueError(f'Unsupported image type: {p}')
    return 'data:' + mime + ';base64,' + base64.b64encode(p.read_bytes()).decode('ascii')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest',type=Path)
    ap.add_argument('output',type=Path)
    ap.add_argument('--overwrite',action='store_true')
    args=ap.parse_args()
    if args.output.exists() and not args.overwrite: ap.error('Output already exists; choose a new name or explicitly use --overwrite')
    data=json.loads(args.manifest.read_text(encoding='utf-8'))
    items=data.get('comparisons',[])
    attempts=data.get('unverified_attempts',[])
    if not items and not attempts: ap.error('Manifest must contain comparisons or unverified_attempts')
    sections=[]
    for i,item in enumerate(items,1):
        original=image_url(item['original'],args.manifest.parent); concept=image_url(item['concept'],args.manifest.parent)
        room=esc(item['room']); title=esc(item.get('title',item['room'])); subtitle=esc(item.get('subtitle','Ideia com IA')); description=esc(item['description']); note=esc(item.get('note',''))
        origlabel=esc(item.get('original_label','Original')); idealabel=esc(item.get('concept_label','Ideia com IA'))
        oa=esc(item.get('original_alt',f'Fotografia de origem: {item["room"]}')); ca=esc(item.get('concept_alt',f'Ideia gerada por IA: {item["room"]}'))
        fallback=f'<div class="fallback"><figure><img src="{original}" alt="{oa}"><figcaption>{origlabel}</figcaption></figure><figure><img src="{concept}" alt="{ca}"><figcaption>{idealabel}</figcaption></figure></div>'
        side_first = item.get('side_by_side', False)
        comparison_hidden = ' hidden' if side_first else ''
        alternate_hidden = '' if side_first else ' hidden'
        pressed = 'true' if side_first else 'false'
        button_label = 'Ver comparação deslizante' if side_first else 'Ver lado a lado'
        compare=f'''<div class="comparison-group"><noscript><style>.comparison,.view-switch,.alternate-view{{display:none!important}}</style>{fallback}</noscript><div class="comparison"{comparison_hidden}><img src="{concept}" alt="{ca}"><div class="before"><img src="{original}" alt="{oa}"></div><span class="label left">{origlabel}</span><span class="label right">{idealabel}</span><span class="divider" aria-hidden="true"><i>↔</i></span><input type="range" min="0" max="100" value="50" aria-label="{esc('Comparar original e ideia com IA — '+item['room'])}"></div><div class="alternate-view"{alternate_hidden}>{fallback}</div><button class="view-switch" type="button" aria-pressed="{pressed}">{button_label}</button></div>'''
        hint='<p class="hint">Arrasta ou usa as teclas de direção para comparar.</p>'
        extra=f'<p class="notice">{note}</p>' if note else ''
        sections.append(f'''<section class="room"><div class="room-head"><div><span class="number">{i:02d} / {room}</span><h2>{title}</h2></div><span class="caption">COMPARA AS IMAGENS ↔</span></div>{compare}{hint}<div class="room-copy"><h3>{subtitle}</h3><div><p>{description}</p>{extra}</div></div></section>''')
    attempt_sections=[]
    if attempts:
        cards=[]
        for item in attempts:
            image=image_url(item['image'],args.manifest.parent)
            room=esc(item['room']); description=esc(item['description'])
            alt=esc(item.get('alt',f'Tentativa de geração não verificada: {item["room"]}'))
            cards.append(f'<article class="attempt-card"><h3>{room} · Tentativa não verificada</h3><img src="{image}" alt="{alt}"><p>{description}</p></article>')
        attempt_sections.append(f'<section class="attempts"><h2>Tentativas de geração não verificadas</h2><p class="attempts-intro">Estas imagens mostram resultados gerados que não puderam ser confirmados como transformações fiéis de uma divisão. Não são comparações antes/depois.</p><div class="attempt-grid">{"".join(cards)}</div></section>')
    values={'LANG':esc(data.get('lang','pt-PT')),'TITLE':esc(data.get('title','Casorama — Relatório')),'HEADER_LABEL':esc(data.get('header_label','Relatório do imóvel')),'INTRO':f'<p class="report-note">{esc(data.get("intro",""))}</p>' if data.get('intro') else '', 'SECTIONS':'\n'.join(sections),'ATTEMPTS':'\n'.join(attempt_sections),'CLOSING_TITLE':esc(data.get('closing_title','Uma ideia para começar.')),'DISCLAIMER':esc(data.get('disclaimer','Estas imagens são ilustrative e podem alterar detalhes do espaço. Não são medições, projetos de arquitetura ou uma garantia de viabilidade de obras.'))}
    result=TEMPLATE.read_text(encoding='utf-8')
    for k,v in values.items(): result=result.replace('{{'+k+'}}',v)
    args.output.write_text(result,encoding='utf-8')
    print(f'Created {args.output} with {len(items)} comparisons')
if __name__=='__main__': main()
