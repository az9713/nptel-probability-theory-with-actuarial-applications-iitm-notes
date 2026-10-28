"""Offline Playwright checks of real rendered pages, controls, math and laboratory."""
import json
import math
import os
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
os.environ['TEMP']=str(ROOT/'work/tmp')
os.environ['TMP']=str(ROOT/'work/tmp')
os.environ['PLAYWRIGHT_BROWSERS_PATH']=str(ROOT/'.playwright')
from playwright.sync_api import sync_playwright


def main():
    plan=json.loads((ROOT/'book-plan.json').read_text(encoding='utf-8'))
    executable=Path('C:/Program Files/Google/Chrome/Application/chrome.exe')
    if not executable.exists():
        executable=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
    records=[];issues=[];console_errors=[]
    with sync_playwright() as p:
        context=p.chromium.launch_persistent_context(str(ROOT/'work/browser-profile'),
            executable_path=str(executable),headless=True,viewport={'width':1440,'height':1000},
            reduced_motion='reduce',offline=True)
        page=context.new_page()
        page.on('pageerror',lambda error:console_errors.append(str(error)))
        files=['index.html']+[c['file'] for c in plan['chapters']]+[
            'appendix-concentration.html','numerical-lab.html','source-map.html',
            'references.html','study-guide.html']
        for name in files:
            print('CHECK',name,flush=True)
            page.goto((ROOT/name).as_uri(),wait_until='load')
            page.wait_for_function("document.documentElement.dataset.mathReady === 'true'",timeout=30000)
            errors=page.locator('[data-mml-node="merror"],mjx-merror').count()
            math_count=page.locator('mjx-container').count()
            copy_count=page.locator('.copybtn').count()
            records.append({'page':name,'math_errors':errors,'rendered_math':math_count,
                            'copy_controls':copy_count})
            if errors:issues.append(name+': MathJax errors '+str(errors))
            if name.startswith('chapter-') and (math_count==0 or copy_count==0):
                issues.append(name+': missing rendered math/code controls')
            for width in [1440,390]:
                page.set_viewport_size({'width':width,'height':1000})
                overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth+2')
                if overflow:issues.append(name+': horizontal page overflow at '+str(width))
            page.set_viewport_size({'width':1440,'height':1000})
        page.goto((ROOT/plan['chapters'][0]['file']).as_uri(),wait_until='load')
        page.wait_for_function("document.documentElement.dataset.mathReady === 'true'")
        page.locator('#solutions').click()
        if page.locator('details.exercise:not([open])').count():issues.append('Show solutions failed')
        page.locator('#solutions').click()
        if page.locator('details.exercise[open]').count():issues.append('Hide solutions failed')
        before=page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--size')")
        page.locator('[data-font="1"]').click()
        after=page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--size')")
        if before==after:issues.append('Font size control failed')
        page.locator('[data-font="-1"]').click()
        theme=page.locator('html').get_attribute('data-theme');page.locator('#theme').click()
        if page.locator('html').get_attribute('data-theme')==theme:issues.append('Theme control failed')
        page.locator('#theme').click()
        page.locator('#search').fill('deductible')
        if page.locator('#search-results a').count()==0:issues.append('Offline full-text search failed')
        page.locator('#search').fill('')
        page.locator('.copybtn').first.click()
        page.wait_for_function("document.querySelector('.copybtn').textContent === 'Copied'",timeout=3000)
        if page.locator('.copybtn').first.inner_text()!='Copied':issues.append('Code copy control failed')
        page.emulate_media(media='print')
        page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
        if page.locator('details.exercise:not([open])').count():issues.append('Print solution expansion failed')
        page.emulate_media(media='screen');page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        page.goto((ROOT/'numerical-lab.html').as_uri(),wait_until='load')
        page.wait_for_function('window.LAB_READY===true')
        actual=float(page.locator('#layer-output').get_attribute('data-mean'))
        expected=2000*math.exp(-0.5)*(1-math.exp(-1.5))
        if not math.isclose(actual,expected,rel_tol=1e-12):issues.append('Layer lab mean mismatch')
        page.locator('#deductible').evaluate("e=>{e.value=2000;e.dispatchEvent(new Event('input'))}")
        changed=float(page.locator('#layer-output').get_attribute('data-mean'))
        if not changed<actual:issues.append('Layer deductible interaction failed')
        posterior=float(page.locator('#bayes-output').get_attribute('data-posterior'))
        if not math.isclose(posterior,0.009/(0.009+0.0495),rel_tol=1e-12):issues.append('Bayes lab mismatch')
        ratio=float(page.locator('#dependence-output').get_attribute('data-ratio'))
        if not math.isclose(ratio,0.109,rel_tol=1e-12):issues.append('Dependence lab mismatch')
        for value,expected in [('0',0.01),('1',1.0)]:
            page.locator('#correlation').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input"))}',value)
            actual=float(page.locator('#dependence-output').get_attribute('data-ratio'))
            if not math.isclose(actual,expected):issues.append('Dependence endpoint failed')
        page.goto((ROOT/'index.html').as_uri(),wait_until='load')
        page.wait_for_function("document.documentElement.dataset.mathReady === 'true'")
        page.screenshot(path=str(ROOT/'assets/site-preview.png'),full_page=False)
        page.set_viewport_size({'width':390,'height':844})
        page.reload(wait_until='load');page.wait_for_function("document.documentElement.dataset.mathReady === 'true'")
        page.screenshot(path=str(ROOT/'assets/site-preview-mobile.png'),full_page=False)
        context.close()
    issues.extend('JavaScript error: '+e for e in console_errors)
    report={'scope':'Offline Chrome rendering and reader/laboratory behavior; no mathematical or human accessibility certification',
        'page_count':len(records),'passed':not issues,'issues':issues,'records':records}
    (ROOT/'validation/reader-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'{len(records)} offline pages, {len(issues)} browser issues')
    for issue in issues:print(issue)
    return 0 if not issues else 1

if __name__=='__main__':sys.exit(main())
