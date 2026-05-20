import re
import subprocess
import tempfile
import os

MMDC = r"C:\nvm4w\nodejs\mmdc.cmd"

def on_page_content(html, page, config, **kwargs):
    #print(f"\n🔍 Hook ejecutándose en página: {page.title}")
    #print(f"   ¿Contiene 'mermaid'?: {'mermaid' in html}")
    
    if 'mermaid' in html:
        idx = html.find('mermaid')
        #print(f"   Contexto: ...{html[max(0,idx-50):idx+100]}...")

    pattern = re.compile(r'<pre class="mermaid"><code>(.*?)</code></pre>', re.DOTALL)
    
    def render_mermaid(match):
        code = match.group(1).strip()
        code = code.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        
        #print(f"   🎨 Renderizando: {code[:50]}...")
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
                f.write(code)
                tmp_input = f.name
            
            tmp_output = tmp_input.replace('.mmd', '.svg')
            
            result = subprocess.run(
                [MMDC, '-i', tmp_input, '-o', tmp_output, '-b', 'transparent'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(tmp_output):
                with open(tmp_output, 'r', encoding='utf-8') as f:
                    svg = f.read()
                svg = re.sub(r'<\?xml[^?]*\?>', '', svg).strip()
                #print(f"   ✅ SVG generado correctamente")
                return f'<div class="mermaid-svg">{svg}</div>'
            else:
                print(f"   ❌ stdout: {result.stdout}")
                print(f"   ❌ stderr: {result.stderr}")
                return match.group(0)
                
        except Exception as e:
            #print(f"   ❌ Excepción: {e}")
            return match.group(0)
        finally:
            for tmp in [tmp_input, tmp_output]:
                try: os.unlink(tmp)
                except: pass
    
    return pattern.sub(render_mermaid, html)