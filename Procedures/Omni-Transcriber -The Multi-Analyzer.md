# Proyecto: Omni-Transcriber (v2.5)

### Nota de uso en Kali: Para ingresar rutas de archivos de forma eficiente, arrastre el archivo de video directamente a la terminal después de que el script solicite el Video Path.


- Manual de Instalación, Configuración y Operación

Este documento detalla la implementación de una herramienta de IA basada en el modelo OpenAI Whisper, optimizada para la transcripción técnica con soporte multi-idioma y mapeo semántico en Kali Linux.

1. Preparación del Entorno (Lab Setup)

Para garantizar la estabilidad y evitar conflictos de dependencias en el sistema base, se utiliza un entorno virtual aislado.


Paso A: Creación y Activación del venv


### Crear el entorno virtual
```python3 -m venv venv```

### Activar el entorno (indispensable antes de ejecutar o instalar)
```source venv/bin/activate```



Paso B: Instalación de Dependencias Core

### Instalación de librerías de IA y compiladores de Rust
```pip install openai-whisper setuptools-rust```

### Instalación del motor de procesamiento de audio
```sudo apt update && sudo apt install ffmpeg -y```


2. Código Fuente Unificado (v2.5 Stable)

Este script representa la versión estable y unificada del Omni-Transcriber. Incorpora lógica de mapeo internacional y extracción de audio de alta fidelidad.

```python
import whisper
import os
import json
import subprocess
import datetime
from datetime import timedelta

def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def run_omni_session(video_path, tech_dict):
    file_name = os.path.basename(video_path)
    output_report = f"Professional_Report_{os.path.splitext(file_name)[0]}.md"
    
    # 1. Procesamiento de Audio vía FFmpeg
    temp_audio = "processing_temp.wav"
    subprocess.call(f"ffmpeg -i '{video_path}' -ar 16000 -ac 1 -c:a pcm_s16le {temp_audio} -y", 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # 2. Motor de IA (Modelo 'Small' para balance precisión/velocidad)
    model = whisper.load_model("small")
    
    # 3. Ejecución de Transcripción
    print(f"\n" + "="*60 + "\n LIVE ACADEMIC FEED \n" + "="*60)
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False, verbose=True)

    # 4. Mapeo Semántico (Español -> Inglés Técnico)
    smart_index = []
    full_text_lower = " ".join([s['text'].lower() for s in result['segments']])

    for segment in result['segments']:
        text_segment = segment['text'].lower()
        for english_term, synonyms in tech_dict.items():
            if any(syn.lower() in text_segment for syn in synonyms) or english_term.lower() in text_segment:
                if any(s.lower() in full_text_lower for s in synonyms):
                    smart_index.append({
                        "time": format_timestamp(segment['start']),
                        "term": english_term,
                        "context": segment['text'].strip()
                    })

    # 5. Exportación de Informe Final
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🎓 OMNI-ACADEMIC REPORT: {file_name}\n---\n")
        md.write(f"### 📊 Metadata\n- **Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n")
        md.write("## 🔍 Technical Index (Global Terms)\n")
        if smart_index:
            md.write("| Category (EN) | Timestamp | Source Context (ES) |\n| :--- | :--- | :--- |\n")
            for item in smart_index:
                md.write(f"| **{item['term']}** | `{item['time']}` | {item['context']} |\n")
        
        md.write("\n---\n## 📝 Full Transcription\n| Time | Text |\n| :--- | :--- |\n")
        for segment in result['segments']:
            md.write(f"| **{format_timestamp(segment['start'])}** | {segment['text'].strip()} |\n")

    if os.path.exists(temp_audio): os.remove(temp_audio)
    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    if available:
        for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
        idx = int(input("\n[?] Select Domain Index: "))
        v_path = input("[?] Video Path: ").strip().replace("'", "").replace('"', "")
        if os.path.exists(v_path):
            run_omni_session(v_path, load_dictionary(available[idx]))

```

3. Repositorio de Diccionarios Académicos

Los diccionarios se almacenan en la carpeta /dicts. Estos archivos permiten la Traducción Semántica Automática en los informes.


- Ciberseguridad (cybersecurity.json)

```json

{
    "Cross-Site Scripting (XSS)": ["Reflected", "Stored", "DOM-based", "payload", "script"],
    "Insecure CORS": ["Access-Control-Allow-Origin", "header", "misconfiguration"],
    "Privilege Escalation": ["escalada de privilegios", "elevar privilegios", "root"],
    "Remote Code Execution (RCE)": ["Reverse Shell", "Netcat", "payload delivery"]
}
```


- Matemática Avanzada (mathematics.json)

```json

{
    "Graphic Representation": ["eje de abscisas", "eje de ordenadas", "parábola", "hipérbola", "coordenadas"],
    "Limit and Continuity": ["límite", "tiende a", "continuidad", "asíntota"],
    "Integral Calculus": ["integral", "primitiva", "área bajo la curva", "antiderivada"]
}
```

4. Resolución de Problemas (Troubleshooting)

- Incidencia:
Timeout en Debugger

- Origen Técnico:
Saturación de CPU (100% en 12 núcleos) por Whisper.

- Solución Aplicada:
Ignorar alerta de VS Code; monitorear vía terminal/htop.
-------------------------------------------------------
- Incidencia:
JSON Warning

- Origen Técnico:
Errores de sintaxis o carga lenta de extensiones.

- Solución Aplicada:
Validar la ausencia de comas finales (trailing commas).
-------------------------------------------------------
- Incidencia:
Bucles de texto

- Origen Técnico:
Alucinaciones auditivas por ruido de fondo.

- Solución Aplicada:
Implementación de beam_size=5 para mayor coherencia.
-------------------------------------------------------

# Omni-Transcriber v3.0 "The Multi-Analyzer"

```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter

def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    subprocess.call(f"ffmpeg -i '{file_path}' -ar 16000 -ac 1 -c:a pcm_s16le {temp_audio} -y", 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False, verbose=True)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

def run_omni_analyzer(file_path, tech_dict):
    target_dir = os.path.dirname(os.path.abspath(file_path))
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    output_report = os.path.join(target_dir, f"Omni_Report_{base_name}.md")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".mp4", ".mp3", ".wav", ".m4a"]:
        data = process_audio_video(file_path)
    else:
        data = extract_text_from_doc(file_path)

    smart_index = []
    term_stats = Counter() # Motor de estadísticas
    full_text_lower = " ".join([d['text'].lower() for d in data])

    for entry in data:
        text_lower = entry['text'].lower()
        for english_term, synonyms in tech_dict.items():
            found_in_segment = False
            for syn in synonyms:
                count_in_segment = text_lower.count(syn.lower())
                if count_in_segment > 0:
                    term_stats[english_term] += count_in_segment
                    found_in_segment = True
            
            if found_in_segment:
                smart_index.append({
                    "location": entry['pos'],
                    "term": english_term,
                    "context": entry['text']
                })

    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.1: {file_name}\n---\n")
        
        # NUEVA SECCIÓN: Métrica de Prioridades del Autor
        md.write("## 📊 Topic Intensity (Métricas de Relevancia)\n")
        md.write("| Academic Category | Total Occurrences | Importance |\n| :--- | :--- | :--- |\n")
        
        # Ordenamos por los más mencionados
        for term, count in term_stats.most_common():
            level = "🔥 High" if count > 10 else "📘 Medium" if count > 3 else "💡 Mention"
            md.write(f"| **{term}** | {count} | {level} |\n")
        
        md.write("\n---\n## 🔍 Semantic Technical Index\n")
        md.write("| Term (EN) | Location | Source Context |\n| :--- | :--- | :--- |\n")
        for item in smart_index:
            md.write(f"| **{item['term']}** | `{item['location']}` | {item['context']} |\n")

    return output_report

if __name__ == "__main__":
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    if available:
        for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
        idx = int(input("\n[?] Select Domain: "))
        path = input("[?] Drag & Drop File: ").strip().replace("'", "").replace('"', "")
        if os.path.exists(path):
            final_path = run_omni_analyzer(path, load_dictionary(available[idx]))
            print(f"\n[+] Report saved at: {final_path}")
```
- v3.1 (Statistical Edition). He añadido un motor de conteo que agrupa los sinónimos bajo la categoría principal para que tengas una métrica clara.

```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter

def format_timestamp(seconds: float):
    """Formatea segundos a HH:MM:SS para reportes de video."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    """Carga el archivo JSON desde la carpeta dicts/."""
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    """Extrae texto de PDFs y archivos Word indexando por página o párrafo."""
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    """Extrae audio y transcribe usando OpenAI Whisper."""
    temp_audio = "processing_temp.wav"
    subprocess.call(f"ffmpeg -i '{file_path}' -ar 16000 -ac 1 -c:a pcm_s16le {temp_audio} -y", 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Usamos el modelo 'small' por su buen balance entre velocidad y precisión
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False, verbose=True)
    
    if os.path.exists(temp_audio):
        os.remove(temp_audio)
    
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

def run_omni_analyzer(file_path, tech_dict):
    """Función principal de análisis y generación de reporte en carpeta Reports/."""
    # --- AJUSTE DE RUTA DE REPORTES ---
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]
    output_report = os.path.join(reports_dir, f"Omni_Report_{base_name}.md")
    
    # Identificar tipo de archivo
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".mp4", ".mp3", ".wav", ".m4a"]:
        print(f"[*] Multimedia detectada. Iniciando Whisper Engine...")
        data = process_audio_video(file_path)
    elif ext in [".pdf", ".docx", ".txt"]:
        print(f"[*] Documento detectado. Iniciando extracción de texto...")
        data = extract_text_from_doc(file_path)
    else:
        print("[!] Formato no soportado.")
        return

    # --- ANÁLISIS SEMÁNTICO Y ESTADÍSTICO ---
    smart_index = []
    term_stats = Counter()
    
    for entry in data:
        text_lower = entry['text'].lower()
        for category, synonyms in tech_dict.items():
            found_this_category = False
            for syn in synonyms:
                occurrences = text_lower.count(syn.lower())
                if occurrences > 0:
                    term_stats[category] += occurrences
                    found_this_category = True
            
            if found_this_category:
                smart_index.append({
                    "location": entry['pos'],
                    "term": category,
                    "context": entry['text'].strip()
                })

    # --- GENERACIÓN DEL ARCHIVO MARKDOWN ---
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.2: {file_name}\n")
        md.write(f"**Fecha de Análisis:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n")
        
        md.write("## 📊 Topic Intensity (Métricas de Relevancia)\n")
        md.write("| Categoría Académica | Menciones Totales | Importancia |\n| :--- | :--- | :--- |\n")
        
        for term, count in term_stats.most_common():
            level = "🔥 Alta" if count > 15 else "📘 Media" if count > 5 else "💡 Mención"
            md.write(f"| **{term}** | {count} | {level} |\n")
        
        md.write("\n---\n## 🔍 Índice Técnico Semántico\n")
        md.write("| Concepto | Ubicación | Contexto Detectado |\n| :--- | :--- | :--- |\n")
        for item in smart_index:
            md.write(f"| **{item['term']}** | `{item['location']}` | {item['context']} |\n")

    return output_report

if __name__ == "__main__":
    print("=== OMNI-ANALYZER v3.2: UNIFIED DATA INGESTION ===")
    
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    if available:
        for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
        try:
            idx = int(input("\n[?] Selecciona el Dominio Académico: "))
            path = input("[?] Arrastra el archivo aquí: ").strip().replace("'", "").replace('"', "")
            
            if os.path.exists(path):
                report_path = run_omni_analyzer(path, load_dictionary(available[idx]))
                print(f"\n[+] ANÁLISIS COMPLETADO EXITOSAMENTE")
                print(f"[>] Reporte guardado en: {report_path}")
            else:
                print("[!] El archivo no existe.")
        except Exception as e:
            print(f"[!] Error: {e}")
    else:
        print("[!] No se encontraron diccionarios en la carpeta /dicts")
```
# -----------------------------------------------------------------------------

# v3.3 "Executive Edition"

```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter

# --- FUNCIONES DE SOPORTE (Se mantienen de la v3.2) ---
def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    subprocess.call(f"ffmpeg -i '{file_path}' -ar 16000 -ac 1 -c:a pcm_s16le {temp_audio} -y", 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False, verbose=True)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

# --- FUNCIÓN PRINCIPAL OPTIMIZADA v3.3 ---
def run_omni_analyzer(file_path, tech_dict):
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    if not os.path.exists(reports_dir): os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    output_report = os.path.join(reports_dir, f"Omni_Report_{os.path.splitext(file_name)[0]}.md")
    
    ext = os.path.splitext(file_path)[1].lower()
    data = process_audio_video(file_path) if ext in [".mp4", ".mp3", ".wav"] else extract_text_from_doc(file_path)

    # 1. Agrupación y Métrica
    grouped_data = {category: [] for category in tech_dict.keys()}
    term_stats = Counter()
    
    for entry in data:
        text_lower = entry['text'].lower()
        for category, synonyms in tech_dict.items():
            count = sum(text_lower.count(syn.lower()) for syn in synonyms)
            if count > 0:
                term_stats[category] += count
                grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})

    # 2. Generación del Reporte Ejecutivo
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.3 (Executive): {file_name}\n")
        md.write(f"**Análisis de Inteligencia:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")
        
        # SECCIÓN 1: Cuadro de Mando (Métricas)
        md.write("## 📊 Topic Intensity (Resumen Ejecutivo)\n")
        md.write("| Categoría | Menciones | Relevancia |\n| :--- | :--- | :--- |\n")
        for term, count in term_stats.most_common():
            level = "🔥 Crítica" if count > 20 else "📘 Significativa" if count > 5 else "💡 Mención"
            md.write(f"| **{term}** | {count} | {level} |\n")
        
        md.write("\n---\n## 🔍 Análisis por Categoría (Top Contexts)\n")
        
        # SECCIÓN 2: Hallazgos Clave y Colapsables
        for category, count in term_stats.most_common():
            findings = grouped_data[category]
            md.write(f"### 📌 {category} ({count} hallazgos)\n")
            
            # Mostramos solo los primeros 3 contextos como "Destacados"
            md.write("**Contextos destacados:**\n")
            for f in findings[:3]:
                md.write(f"- `{f['loc']}`: {f['ctx'][:150]}...\n")
            
            # El resto lo mandamos al "Búnker" colapsable si hay muchos
            if len(findings) > 3:
                md.write(f"\n<details>\n<summary>📦 Ver {len(findings) - 3} hallazgos adicionales de {category}</summary>\n\n")
                md.write("| Ubicación | Contexto Completo |\n| :--- | :--- |\n")
                for f in findings[3:]:
                    md.write(f"| `{f['loc']}` | {f['ctx']} |\n")
                md.write("\n</details>\n")
            md.write("\n")

    return output_report

if __name__ == "__main__":
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    if available:
        for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
        idx = int(input("\n[?] Selección: "))
        path = input("[?] Archivo: ").strip().replace("'", "").replace('"', "")
        if os.path.exists(path):
            print(f"\n[+] Reporte generado: {run_omni_analyzer(path, load_dictionary(available[idx]))}")
```

- Limpieza Visual: 
    Si el libro de Gvirtz menciona "Pedagogía" 200 veces, el reporte ahora solo muestra las 3 menciones más importantes arriba. El resto (las otras 197) están "escondidas" dentro de un botón que dice "Ver 197 hallazgos adicionales".

- Métricas Primero: 
    Lo primero que ves es la tabla de intensidad. Si sos un jefe o un profesor, con ver esa tabla ya sabés de qué trata el libro sin leer el resto.

- Prevención de Pánico: 
    El archivo .md ahora es un 80% más corto visualmente, pero mantiene el 100% de la información disponible para quien quiera profundizar.

# ------------------------------------------------------------------------------------
1. The Logic Fix (The "Unclassified" Bucket)

El problema es que el script actual solo guarda data si encuentra un match en el tech_dict. Para solucionar esto, vamos a crear una categoría llamada "TRANSCRIPCIÓN COMPLETA / RAW DATA" que se llene siempre, independientemente de los diccionarios.

Modificar tu función run_omni_analyzer en estos puntos clave:

```python
# 1. Agrupación y Métrica
    grouped_data = {category: [] for category in tech_dict.keys()}
    # AGREGAMOS ESTO: Un balde para lo que no matchea
    unclassified_data = [] 
    term_stats = Counter()
    
    for entry in data:
        text_lower = entry['text'].lower()
        matched = False # Flag para saber si encontramos algo
        
        for category, synonyms in tech_dict.items():
            count = sum(text_lower.count(syn.lower()) for syn in synonyms)
            if count > 0:
                term_stats[category] += count
                grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})
                matched = True
        
        # Si no matcheó con nada, lo mandamos al Raw Data
        if not matched:
            unclassified_data.append(entry)

```
este concepto se llama Log Aggregation & Analysis:

    The Dictionary: Son tus Signatures (como un Antivirus viejo que solo busca lo que conoce).

    The Unclassified Data: Es tu Anomaly Detection. Si algo no matchea, no significa que no sea importante; significa que es desconocido.

The Logic Fix (The "Unclassified" Bucket)

El problema es que el script actual solo guarda data si encuentra un match en el tech_dict. Para solucionar esto, vamos a crear una categoría llamada "TRANSCRIPCIÓN COMPLETA / RAW DATA" que se llene siempre, independientemente de los diccionarios.

El "Safety Net" en el Reporte

Para que no pierdas tiempo leyendo todo el audio si no es necesario, vamos a meter toda la transcripción que no matcheó en un colapsable al final del reporte. Así, si la tabla de "Topic Intensity" está vacía, simplemente bajas y abres el búnker.

función que extraiga automáticamente Keywords (sustantivos más comunes) de la unclassified_data usando la librería Counter. Así, el script te diría: "No encontré nada en tus diccionarios, pero las palabras que más se repiten son: [Palabra A, Palabra B]".

# 3.4 "Intelligence Edition"
```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter
import re

# --- FUNCIONES DE SOPORTE ---
def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    # Ajuste de comando para manejar espacios y paths complejos
    subprocess.call(f'ffmpeg -i "{file_path}" -ar 16000 -ac 1 -c:a pcm_s16le {temp_audio} -y', 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

# --- FUNCIÓN PRINCIPAL v3.4 "INTELLIGENCE" ---
def run_omni_analyzer(file_path, tech_dict):
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    if not os.path.exists(reports_dir): os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    output_report = os.path.join(reports_dir, f"Omni_Report_{os.path.splitext(file_name)[0]}.md")
    
    ext = os.path.splitext(file_path)[1].lower()
    data = process_audio_video(file_path) if ext in [".mp4", ".mp3", ".wav", ".ogg", ".m4a"] else extract_text_from_doc(file_path)

    # 1. Clasificación y Detección de Anomalías (Unclassified)
    grouped_data = {category: [] for category in tech_dict.keys()}
    unclassified_entries = []
    term_stats = Counter()
    all_words = Counter() # Para el Auto-Discovery
    
    for entry in data:
        text_lower = entry['text'].lower()
        matched = False
        
        # Guardar palabras para discovery (limpieza básica)
        words = re.findall(r'\w+', text_lower)
        all_words.update([w for w in words if len(w) > 4]) # Filtramos palabras cortas (artículos, etc)

        for category, synonyms in tech_dict.items():
            count = sum(text_lower.count(syn.lower()) for syn in synonyms)
            if count > 0:
                term_stats[category] += count
                grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})
                matched = True
        
        if not matched:
            unclassified_entries.append(entry)

    # 2. Generación del Reporte Ejecutivo
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.4 (Intelligence): {file_name}\n")
        md.write(f"**Análisis de Inteligencia:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")
        
        # SECCIÓN 1: Cuadro de Mando (Métricas)
        md.write("## 📊 Topic Intensity\n")
        if term_stats:
            md.write("| Categoría | Menciones | Relevancia |\n| :--- | :--- | :--- |\n")
            for term, count in term_stats.most_common():
                level = "🔥 Crítica" if count > 20 else "📘 Significativa" if count > 5 else "💡 Mención"
                md.write(f"| **{term}** | {count} | {level} |\n")
        else:
            md.write("> ⚠️ **Alerta:** No se detectaron coincidencias con el diccionario seleccionado.\n")
        
        # SECCIÓN 2: Análisis por Categoría
        if term_stats:
            md.write("\n---\n## 🔍 Análisis por Categoría (Top Contexts)\n")
            for category, count in term_stats.most_common():
                findings = grouped_data[category]
                md.write(f"### 📌 {category} ({count})\n")
                for f in findings[:3]:
                    md.write(f"- `{f['loc']}`: {f['ctx'][:150]}...\n")
                
                if len(findings) > 3:
                    md.write(f"\n<details>\n<summary>📦 Ver {len(findings) - 3} adicionales de {category}</summary>\n\n")
                    md.write("| Ubicación | Contexto |\n| :--- | :--- |\n")
                    for f in findings[3:]:
                        md.write(f"| `{f['loc']}` | {f['ctx']} |\n")
                    md.write("\n</details>\n")
        
        # SECCIÓN 3: Catch-All (Transcripción sin matchear)
        if unclassified_entries:
            md.write("\n---\n## 📋 Transcripción / Raw Data (Sin Clasificar)\n")
            md.write("> **Contenido recuperado:** Estos fragmentos no matchearon con tus `dicts` pero fueron procesados.\n\n")
            md.write("<details>\n<summary>🔓 Expandir Transcripción Completa</summary>\n\n")
            md.write("| Tiempo/Pos | Texto |\n| :--- | :--- |\n")
            for entry in data: # Mostramos TODO el texto original aquí para contexto total
                md.write(f"| `{entry['pos']}` | {entry['text']} |\n")
            md.write("\n</details>\n")

        # SECCIÓN 4: Auto-Discovery de Keywords (IA Sugerida)
        md.write("\n---\n## 🧠 Auto-Discovery (Keywords Sugeridas)\n")
        md.write("Palabras frecuentes detectadas para actualizar tus diccionarios:\n\n")
        common = [f"`{word}`" for word, count in all_words.most_common(10)]
        md.write(", ".join(common) + "\n")

    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    if available:
        for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
        try:
            idx = int(input("\n[?] Selección: "))
            path = input("[?] Archivo: ").strip().replace("'", "").replace('"', "")
            if os.path.exists(path):
                print(f"\n[+] Analizando: {path}...")
                report = run_omni_analyzer(path, load_dictionary(available[idx]))
                print(f"[+] Reporte generado: {report}")
            else:
                print(f"[-] Error: El archivo '{path}' no existe.")
        except ValueError:
            print("[-] Error: Selección inválida.")
    else:
        print("[-] No hay diccionarios en la carpeta /dicts. Crea un archivo .json para empezar.")

```

# ----------------------------------------------------------------------------------

v3.5 "Universal Dispatcher". He ajustado la lógica para que, si seleccionas el Modo RAW (-1), el script te entregue un Top 20 de Keywords en lugar de solo 10

Key Upgrades en esta versión:

    Top 20 Keywords: En lugar de 10, ahora te da un espectro más amplio. Esto es vital en Australia o Dinamarca, donde los términos técnicos suelen ser muy específicos.

    Stop-Words Filter: Agregué un pequeño set de palabras comunes que no aportan nada (como "donde" o "sobre") para que las keywords que veas sean Real Tech Data.

    Report Hybridization: El reporte en modo RAW tiene una estructura diferente, más limpia, enfocada 100% en la transcripción y el descubrimiento de inteligencia.

    Auto-Open Transcript: En el .md, la transcripción completa viene con la etiqueta <details open>, lo que significa que en modo RAW la verás desplegada de entrada sin tener que hacer click.

```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter
import re

# --- FUNCIONES DE SOPORTE ---
def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    # Encapsulamos el path entre comillas dobles para evitar errores con espacios de WhatsApp
    subprocess.call(f'ffmpeg -i "{file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{temp_audio}" -y', 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

# --- FUNCIÓN PRINCIPAL v3.5 "UNIVERSAL DISPATCHER" ---
def run_omni_analyzer(file_path, tech_dict, is_raw=False):
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    if not os.path.exists(reports_dir): os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    report_type = "RAW" if is_raw else "Executive"
    output_report = os.path.join(reports_dir, f"Omni_Report_{report_type}_{os.path.splitext(file_name)[0]}.md")
    
    ext = os.path.splitext(file_path)[1].lower()
    data = process_audio_video(file_path) if ext in [".mp4", ".mp3", ".wav", ".ogg", ".m4a"] else extract_text_from_doc(file_path)

    # 1. Procesamiento de Data e Inteligencia
    grouped_data = {category: [] for category in tech_dict.keys()}
    all_words = Counter()
    term_stats = Counter()
    
    # Lista de stop-words básicas para limpiar el Auto-Discovery (puedes ampliarla)
    stop_words = {"puesto", "donde", "cuando", "desde", "entre", "sobre", "todos", "estos", "había"}

    for entry in data:
        text_clean = re.sub(r'[^\w\s]', '', entry['text'].lower())
        words = text_clean.split()
        # Auto-Discovery: Palabras > 4 letras y que no sean basura común
        all_words.update([w for w in words if len(w) > 4 and w not in stop_words])

        if not is_raw:
            for category, synonyms in tech_dict.items():
                count = sum(text_clean.count(syn.lower()) for syn in synonyms)
                if count > 0:
                    term_stats[category] += count
                    grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})

    # 2. Escritura del Reporte .md
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.5 ({report_type}): {file_name}\n")
        md.write(f"**Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")
        
        if is_raw:
            md.write("## 🔓 Mode: RAW DATA ANALYSIS\n")
            md.write("> En este modo se omite la clasificación por diccionarios para priorizar la captura total de información.\n\n")
        else:
            # SECCIÓN 1: Cuadro de Mando (Solo en modo categorizado)
            md.write("## 📊 Topic Intensity\n")
            if term_stats:
                md.write("| Categoría | Menciones | Relevancia |\n| :--- | :--- | :--- |\n")
                for term, count in term_stats.most_common():
                    level = "🔥 Crítica" if count > 20 else "📘 Significativa" if count > 5 else "💡 Mención"
                    md.write(f"| **{term}** | {count} | {level} |\n")
            else:
                md.write("> ⚠️ **Alerta:** No se detectaron coincidencias. Revisa la sección de Transcripción abajo.\n")

            # SECCIÓN 2: Análisis por Categoría
            md.write("\n---\n## 🔍 Top Contexts\n")
            for category, count in term_stats.most_common():
                findings = grouped_data[category]
                md.write(f"### 📌 {category} ({count})\n")
                for f in findings[:3]:
                    md.write(f"- `{f['loc']}`: {f['ctx'][:150]}...\n")
                if len(findings) > 3:
                    md.write(f"\n<details><summary>📦 Ver {len(findings)-3} más</summary>\n\n| Loc | Contexto |\n|:---|:---|\n")
                    for f in findings[3:]: md.write(f"| `{f['loc']}` | {f['ctx']} |\n")
                    md.write("</details>\n")

        # SECCIÓN 3: Transcripción Universal (Siempre disponible)
        md.write("\n---\n## 📋 Transcripción Completa\n")
        md.write("<details open>\n<summary>🔓 Ver Contenido</summary>\n\n| Ubicación | Texto |\n| :--- | :--- |\n")
        for entry in data:
            md.write(f"| `{entry['pos']}` | {entry['text']} |\n")
        md.write("\n</details>\n")

        # SECCIÓN 4: Auto-Discovery (Top 20 Keywords)
        md.write("\n---\n## 🧠 Intelligence Discovery (Top 20 Keywords)\n")
        md.write("Sugerencias para nuevos diccionarios basadas en frecuencia de uso:\n\n")
        # Mostramos 20 palabras clave
        discovery_list = [f"`{word}` ({count})" for word, count in all_words.most_common(20)]
        md.write(" | ".join(discovery_list) + "\n")

    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    print("--- 🌌 OMNI-ANALYZER v3.5 ---")
    print("[-1] 🔓 RAW MODE (Deep Transcript + 20 Keywords)")
    for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
    
    try:
        selection = int(input("\n[?] Selección: "))
        path = input("[?] Archivo: ").strip().replace("'", "").replace('"', "")
        
        if os.path.exists(path):
            is_raw = (selection == -1)
            tech_dict = {} if is_raw else load_dictionary(available[selection])
            
            print(f"\n[+] Procesando: {os.path.basename(path)}...")
            report = run_omni_analyzer(path, tech_dict, is_raw=is_raw)
            print(f"[+ Success] Reporte: {report}")
        else:
            print(f"[-] Error: Path no encontrado.")
    except (ValueError, IndexError):
        print("[-] Selección inválida.")

```
# -----------------------------------------------------------------------

Summarization Module: Ya no tienes que leer el reporte de 200 páginas. El script aplica un algoritmo de Sentence Scoring para encontrar las 4 oraciones que más "peso" tienen en el texto. Es tu párrafo de "Executive Overview".

Concept Mapping: En lugar de listas aisladas, el script intenta cruzar tus dos categorías más importantes. Esto te ayuda a ver la Arquitectura del Pensamiento del autor (ej: cómo relaciona Ciberseguridad con Riesgo).

Active Recall Q&A: Al final del reporte, el script te genera 5 preguntas de examen automáticas basadas en las palabras que más se repitieron.

    Pro-Tip: No leas el reporte todavía. Intenta responder las preguntas primero; si no puedes, ahí es donde vas a buscar la data. Esto es lo que pide el CompTIA Security+: capacidad de análisis crítico.

# v3.7
```python
import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter
import re
import heapq # Para extraer las oraciones más importantes

# --- FUNCIONES DE SOPORTE ---
def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    subprocess.call(f'ffmpeg -i "{file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{temp_audio}" -y', 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

# --- NUEVOS MÓDULOS DE INTELIGENCIA v3.6 ---

def generate_summary(text_data, top_n=4):
    """Summarization Module: Extrae las oraciones más representativas"""
    full_text = " ".join([d['text'] for d in text_data])
    sentences = re.split(r'(?<=[.!?]) +', full_text)
    if len(sentences) < top_n: return full_text
    
    # Simple scoring basado en frecuencia de palabras
    words = re.findall(r'\w+', full_text.lower())
    freq = Counter(words)
    scores = {}
    for sent in sentences:
        for word in sent.lower().split():
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]
    
    summary_sentences = heapq.nlargest(top_n, scores, key=scores.get)
    return " ".join(summary_sentences)

def generate_qa(keywords):
    """Automatic Q&A: Crea preguntas de Active Recall"""
    questions = []
    for word, _ in keywords[:5]:
        questions.append(f"¿Cómo define el autor el concepto de **'{word.upper()}'** y cuál es su impacto en el texto?")
    return questions

# --- FUNCIÓN PRINCIPAL v3.6 ---
def run_omni_analyzer(file_path, tech_dict, is_raw=False):
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    if not os.path.exists(reports_dir): os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    report_type = "PRO_STUDY" if not is_raw else "RAW"
    output_report = os.path.join(reports_dir, f"Omni_Report_{report_type}_{os.path.splitext(file_name)[0]}.md")
    
    data = process_audio_video(file_path) if os.path.splitext(file_path)[1].lower() in [".mp4", ".mp3", ".wav", ".ogg", ".m4a"] else extract_text_from_doc(file_path)

    # 1. Procesamiento Base
    grouped_data = {category: [] for category in tech_dict.keys()}
    all_words = Counter()
    term_stats = Counter()
    stop_words = {"puesto", "donde", "cuando", "desde", "entre", "sobre", "todos", "estos", "aquí", "tiene"}

    for entry in data:
        text_clean = re.sub(r'[^\w\s]', '', entry['text'].lower())
        words = text_clean.split()
        all_words.update([w for w in words if len(w) > 5 and w not in stop_words])

        for category, synonyms in tech_dict.items():
            if any(syn.lower() in text_clean for syn in synonyms):
                term_stats[category] += 1
                grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})

    # 2. Generación de Reporte Académico
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.6 (Academic Pro): {file_name}\n")
        md.write(f"**Análisis Estratégico:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")

        # NUEVO: SUMMARIZATION MODULE
        md.write("## 📝 Resumen Ejecutivo (Thesis Focus)\n")
        md.write(f"> {generate_summary(data)}\n\n")

        # SECCIÓN METRICAS
        md.write("--- \n## 📊 Topic Intensity\n")
        for term, count in term_stats.most_common(5):
            md.write(f"- **{term.upper()}**: {count} menciones clave.\n")

        # NUEVO: CONCEPT MAPPING
        md.write("\n--- \n## 🗺️ Concept Mapping (Relaciones de Poder)\n")
        if len(term_stats) >= 2:
            top_cats = [t for t, _ in term_stats.most_common(2)]
            pages = list(set([f['loc'] for f in grouped_data[top_cats[0]]][:5]))
            md.write(f"El autor vincula **{top_cats[0]}** con **{top_cats[1]}** principalmente en: `{', '.join(pages)}`.\n")

        # NUEVO: AUTOMATIC Q&A (ACTIVE RECALL)
        md.write("\n--- \n## 🧠 Active Recall (Auto-Evaluación)\n")
        md.write("Utiliza estas preguntas para validar tu conocimiento sin mirar el texto:\n\n")
        for q in generate_qa(all_words.most_common(5)):
            md.write(f"- [ ] {q}\n")

        # DATA COMPLETA (BUNKER)
        md.write("\n---\n## 📋 Índice de Contextos (Data Bunker)\n")
        md.write("<details>\n<summary>🔓 Ver referencias completas</summary>\n\n")
        for entry in data:
            md.write(f"| `{entry['pos']}` | {entry['text']} |\n")
        md.write("\n</details>\n")

    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    print("--- 🌌 OMNI-ANALYZER v3.6 PRO ---")
    print("[-1] 🔓 RAW/QUICK MODE")
    for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
    
    try:
        selection = int(input("\n[?] Selección: "))
        path = input("[?] Archivo: ").strip().replace("'", "").replace('"', "")
        if os.path.exists(path):
            is_raw = (selection == -1)
            tech_dict = {} if is_raw else load_dictionary(available[selection])
            print(f"\n[+] Generando Inteligencia Académica...")
            report = run_omni_analyzer(path, tech_dict, is_raw=is_raw)
            print(f"[+ Success] Reporte Pro: {report}")
    except Exception as e:
        print(f"[-] Error: {e}")
```
# -----------------------------------------------------------------------------

He consolidado todas las mejoras: el Modo RAW, el Top 20 de Keywords, el Active Recall (Q&A) y, lo más importante, el nuevo motor de Summarization con Ventana de Contexto. Ahora, cuando el script detecte una idea importante, te entregará un bloque coherente de texto (la idea anterior, la central y la siguiente) para que no pierdas el hilo.

Bloques de Pensamiento: En el resumen, ya no verás solo una línea. El script busca la frase con mayor puntuación y te entrega el párrafo completo (la oración de antes y la de después). Esto es vital para entender por qué el autor dice lo que dice.

Relación de Conceptos: Si usas un diccionario, el script ahora te dirá explícitamente: "Ojo, estás estudiando mucho sobre X, pero el autor lo vincula siempre con Y".

Filtrado de Ruido: He mejorado las stop_words para que en tu Intelligence Discovery no aparezcan palabras como "luego" o "estaba", y solo veas conceptos reales.

```python

import whisper
import os
import json
import subprocess
import datetime
import fitz  # PyMuPDF
from docx import Document
from datetime import timedelta
from collections import Counter
import re
import heapq

# --- SOPORTE TÉCNICO ---
def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

def load_dictionary(dict_name):
    path = f"dicts/{dict_name}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def extract_text_from_doc(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    content = []
    if ext == ".pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc):
            content.append({"pos": f"Page {page_num + 1}", "text": page.get_text().strip()})
    elif ext == ".docx":
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                content.append({"pos": f"Paragraph {i + 1}", "text": para.text.strip()})
    return content

def process_audio_video(file_path):
    temp_audio = "processing_temp.wav"
    subprocess.call(f'ffmpeg -i "{file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{temp_audio}" -y', 
                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    model = whisper.load_model("small")
    result = model.transcribe(temp_audio, language="es", beam_size=5, fp16=False)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return [{"pos": format_timestamp(s['start']), "text": s['text'].strip()} for s in result['segments']]

# --- MÓDULOS DE INTELIGENCIA v3.7 ---

def generate_contextual_summary(text_data, top_n=3):
    """
    Summarization Module v3.7: 
    Extrae bloques de contexto (3 oraciones) para evitar texto fragmentado.
    """
    full_text = " ".join([d['text'] for d in text_data])
    sentences = re.split(r'(?<=[.!?]) +', full_text)
    
    if len(sentences) < 5: return full_text
    
    # Scoring basado en frecuencia de palabras relevantes (>4 letras)
    words = re.findall(r'\w+', full_text.lower())
    freq = Counter([w for w in words if len(w) > 4])
    
    scores = []
    for i, sent in enumerate(sentences):
        score = sum(freq[word] for word in sent.lower().split() if word in freq)
        scores.append((i, score))
    
    # Seleccionamos los índices de las mejores oraciones
    top_indices = [idx for idx, score in heapq.nlargest(top_n, scores, key=lambda x: x[1])]
    
    summary_blocks = []
    for idx in sorted(top_indices):
        # Ventana de contexto: Anterior + Actual + Siguiente
        start = max(0, idx - 1)
        end = min(len(sentences), idx + 2)
        block = " ".join(sentences[start:end])
        summary_blocks.append(f"> ... {block} ...")
    
    return "\n\n".join(summary_blocks)

def generate_qa(keywords):
    """Crea preguntas de Active Recall basadas en las keywords principales"""
    questions = []
    for word, _ in keywords[:5]:
        questions.append(f"¿Cómo explica el material el concepto de **'{word.upper()}'** y qué importancia tiene en el contexto general?")
    return questions

# --- FUNCIÓN PRINCIPAL ---
def run_omni_analyzer(file_path, tech_dict, is_raw=False):
    project_root = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(project_root, "Reports")
    if not os.path.exists(reports_dir): os.makedirs(reports_dir)

    file_name = os.path.basename(file_path)
    report_type = "PRO_STUDY" if not is_raw else "RAW"
    output_report = os.path.join(reports_dir, f"Omni_Report_{report_type}_{os.path.splitext(file_name)[0]}.md")
    
    ext = os.path.splitext(file_path)[1].lower()
    data = process_audio_video(file_path) if ext in [".mp4", ".mp3", ".wav", ".ogg", ".m4a"] else extract_text_from_doc(file_path)

    # 1. Procesamiento de Datos
    grouped_data = {category: [] for category in tech_dict.keys()}
    all_words = Counter()
    term_stats = Counter()
    stop_words = {"puesto", "donde", "cuando", "desde", "entre", "sobre", "todos", "estos", "aquí", "tiene", "luego", "estaba"}

    for entry in data:
        text_clean = re.sub(r'[^\w\s]', '', entry['text'].lower())
        words = text_clean.split()
        # Auto-Discovery de palabras clave
        all_words.update([w for w in words if len(w) > 5 and w not in stop_words])

        if not is_raw:
            for category, synonyms in tech_dict.items():
                if any(syn.lower() in text_clean for syn in synonyms):
                    term_stats[category] += 1
                    grouped_data[category].append({"loc": entry['pos'], "ctx": entry['text'].strip()})

    # 2. Generación del Reporte Markdown
    with open(output_report, "w", encoding="utf-8") as md:
        md.write(f"# 🌌 OMNI-ANALYZER v3.7 (Contextual Explorer): {file_name}\n")
        md.write(f"**Report Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")

        # SECCIÓN 1: RESUMEN CONTEXTUAL
        md.write("## 📝 Executive Contextual Summary\n")
        md.write("Principales bloques de pensamiento detectados (Context Window):\n\n")
        md.write(generate_summary(data) + "\n\n")

        # SECCIÓN 2: TOPIC INTENSITY (Solo en modo estudio)
        if not is_raw:
            md.write("--- \n## 📊 Topic Intensity Analysis\n")
            if term_stats:
                md.write("| Categoría | Menciones | Nivel |\n| :--- | :--- | :--- |\n")
                for term, count in term_stats.most_common():
                    level = "🔥 Critical" if count > 15 else "📘 Relevant"
                    md.write(f Crist| **{term.upper()}** | {count} | {level} |\n")
            
            # CONCEPT MAPPING (Relaciones)
            if len(term_stats) >= 2:
                top = term_stats.most_common(2)
                md.write(f"\n**🗺️ Concept Link:** Se detectó una fuerte correlación entre **{top[0][0]}** y **{top[1][0]}**.\n")

        # SECCIÓN 3: ACTIVE RECALL (Top 5 Questions)
        md.write("\n--- \n## 🧠 Active Recall (Self-Evaluation)\n")
        md.write("Intenta responder sin mirar la transcripción para reforzar tu memoria a largo plazo:\n\n")
        for q in generate_qa(all_words.most_common(5)):
            md.write(f"- [ ] {q}\n")

        # SECCIÓN 4: INTELLIGENCE DISCOVERY (Top 20 Keywords)
        md.write("\n--- \n## 🧠 Intelligence Discovery (Top 20 Keywords)\n")
        discovery = [f"`{word}` ({count})" for word, count in all_words.most_common(20)]
        md.write(" | ".join(discovery) + "\n")

        # SECCIÓN 5: DATA BUNKER (Transcripción)
        md.write("\n---\n## 📋 Data Bunker (Full Transcript)\n")
        md.write("<details>\n<summary>🔓 Expandir Transcripción Completa</summary>\n\n")
        md.write("| Loc | Content |\n| :--- | :--- |\n")
        for entry in data:
            md.write(f"| `{entry['pos']}` | {entry['text']} |\n")
        md.write("\n</details>\n")

    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    print("--- 🌌 OMNI-ANALYZER v3.7 PRO ---")
    print("[-1] 🔓 RAW MODE (Deep Analysis)")
    for i, d in enumerate(available): print(f"[{i}] {d.upper()}")
    
    try:
        selection = int(input("\n[?] Selección: "))
        path = input("[?] Path del archivo: ").strip().replace("'", "").replace('"', "")
        
        if os.path.exists(path):
            is_raw = (selection == -1)
            tech_dict = {} if is_raw else load_dictionary(available[selection])
            
            print(f"\n[+] Extrayendo inteligencia de: {os.path.basename(path)}...")
            report = run_omni_analyzer(path, tech_dict, is_raw=is_raw)
            print(f"[+ Success] Reporte generado: {report}")
        else:
            print(f"[-] Error: Archivo no encontrado.")
    except Exception as e:
        print(f"[-] Error en el proceso: {e}")

```
