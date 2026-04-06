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
        md.write(f"#  OMNI-ANALYZER v3.7 (Contextual Explorer): {file_name}\n")
        md.write(f"**Report Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n---\n")

        # SECCIÓN 1: RESUMEN CONTEXTUAL
        md.write("##  Executive Contextual Summary\n")
        md.write("Principales bloques de pensamiento detectados (Context Window):\n\n")
        md.write(generate_contextual_summary(data) + "\n\n")

        # SECCIÓN 2: TOPIC INTENSITY (Solo en modo estudio)
        if not is_raw:
            md.write("--- \n##  Topic Intensity Analysis\n")
            if term_stats:
                md.write("| Categoría | Menciones | Nivel |\n| :--- | :--- | :--- |\n")
                for term, count in term_stats.most_common():
                    level = " Critical" if count > 15 else " Relevant"
                    md.write(f"| **{term.upper()}** | {count} | {level} |\n")
            
            # CONCEPT MAPPING (Relaciones)
            if len(term_stats) >= 2:
                top = term_stats.most_common(2)
                md.write(f"\n** Concept Link:** Se detectó una fuerte correlación entre **{top[0][0]}** y **{top[1][0]}**.\n")

        # SECCIÓN 3: ACTIVE RECALL (Top 5 Questions)
        md.write("\n--- \n##  Active Recall (Self-Evaluation)\n")
        md.write("Intenta responder sin mirar la transcripción para reforzar tu memoria a largo plazo:\n\n")
        for q in generate_qa(all_words.most_common(5)):
            md.write(f"- [ ] {q}\n")

        # SECCIÓN 4: INTELLIGENCE DISCOVERY (Top 20 Keywords)
        md.write("\n--- \n## Intelligence Discovery (Top 20 Keywords)\n")
        discovery = [f"`{word}` ({count})" for word, count in all_words.most_common(20)]
        md.write(" | ".join(discovery) + "\n")

        # SECCIÓN 5: DATA BUNKER (Transcripción)
        md.write("\n---\n##  Data Bunker (Full Transcript)\n")
        md.write("<details>\n<summary>🔓 Expandir Transcripción Completa</summary>\n\n")
        md.write("| Loc | Content |\n| :--- | :--- |\n")
        for entry in data:
            md.write(f"| `{entry['pos']}` | {entry['text']} |\n")
        md.write("\n</details>\n")

    return output_report

if __name__ == "__main__":
    if not os.path.exists('dicts'): os.makedirs('dicts')
    available = [f.replace('.json', '') for f in os.listdir('dicts') if f.endswith('.json')]
    
    print("---  OMNI-ANALYZER v3.7 PRO ---")
    print("[-1]  RAW MODE (Deep Analysis)")
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