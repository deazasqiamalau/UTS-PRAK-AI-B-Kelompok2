"""
Export Module
Export hasil diagnosis ke berbagai format (PDF, JSON, CSV)
"""

from fpdf import FPDF
import json
import csv
from datetime import datetime
from typing import Dict, List
import os


class DiagnosisPDFExporter(FPDF):
    """Custom PDF class untuk laporan diagnosis"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Header untuk setiap halaman"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Laporan Diagnosis Smartphone', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Sistem Pakar Identifikasi Kerusakan', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Footer untuk setiap halaman"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title: str):
        """Judul chapter"""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(3)
        
    def chapter_body(self, body: str):
        """Body chapter"""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(2)


class DiagnosisExporter:
    """Main exporter class"""
    
    def __init__(self, export_dir: str = 'exports'):
        """
        Initialize exporter
        
        Args:
            export_dir: Directory untuk menyimpan exports
        """
        self.export_dir = export_dir
        self._ensure_export_dir()
        
    def _ensure_export_dir(self):
        """Pastikan directory export ada"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_to_pdf(self, 
                     diagnosis_data: Dict,
                     symptoms: List[str],
                     reasoning_trace: List[Dict],
                     output_filename: str = None) -> str:
        """
        Export hasil diagnosis ke PDF
        
        Args:
            diagnosis_data: Data diagnosis
            symptoms: List gejala yang dipilih
            reasoning_trace: Trace reasoning
            output_filename: Nama file output (optional)
            
        Returns:
            Path file PDF yang dibuat
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'diagnosis_{timestamp}.pdf'
        
        output_path = os.path.join(self.export_dir, output_filename)
        
        # Create PDF
        pdf = DiagnosisPDFExporter()
        pdf.add_page()
        
        # Informasi Umum
        pdf.chapter_title('INFORMASI DIAGNOSIS')
        info_text = f"""
Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}
Session ID: {diagnosis_data.get('session_id', 'N/A')}
Total Gejala: {len(symptoms)}
        """
        pdf.chapter_body(info_text.strip())
        
        # Gejala yang Dipilih
        pdf.chapter_title('GEJALA YANG DIALAMI')
        symptoms_text = '\n'.join([f"- {symptom}" for symptom in symptoms])
        pdf.chapter_body(symptoms_text)
        
        # Hasil Diagnosis
        pdf.chapter_title('HASIL DIAGNOSIS')
        
        diagnoses = diagnosis_data.get('diagnoses', [])
        
        for i, diag in enumerate(diagnoses[:3], 1):
            diagnosis_text = f"""
#{i} - {diag.get('name', 'Unknown')}

Tipe: {diag.get('type', 'Unknown').upper()}
Tingkat Kepercayaan: {diag.get('confidence', 0)*100:.1f}%
Kategori: {diag.get('confidence_category', 'Unknown')}

Deskripsi:
{diag.get('description', 'Tidak ada deskripsi')}

Penyebab Kemungkinan:
{self._format_list(diag.get('causes', []))}

Solusi Perbaikan:
{self._format_solutions(diag.get('solutions', []))}

Estimasi Biaya: Rp {diag.get('estimated_cost', '0')}
Tingkat Kesulitan: {diag.get('repair_difficulty', 'Unknown')}

Pencegahan:
{self._format_list(diag.get('prevention', []))}
            """
            pdf.chapter_body(diagnosis_text.strip())
            pdf.ln(3)
        
        # Reasoning Explanation
        if reasoning_trace:
            pdf.add_page()
            pdf.chapter_title('PENJELASAN REASONING')
            
            reasoning_text = "Sistem sampai pada kesimpulan melalui langkah-langkah berikut:\n\n"
            
            for i, trace in enumerate(reasoning_trace[:10], 1):
                if trace.get('type') == 'rule_fired':
                    reasoning_text += f"{i}. Rule {trace.get('rule_id')}:\n"
                    reasoning_text += f"   IF: {', '.join(trace.get('conditions', []))}\n"
                    reasoning_text += f"   THEN: {trace.get('conclusion')}\n"
                    reasoning_text += f"   CF: {trace.get('cf', 0)*100:.0f}%\n\n"
            
            pdf.chapter_body(reasoning_text)
        
        # Rekomendasi
        pdf.add_page()
        pdf.chapter_title('REKOMENDASI')
        
        recommendation_text = """
LANGKAH SELANJUTNYA:

1. Backup Data Penting
   Sebelum melakukan perbaikan apapun, pastikan untuk melakukan backup
   semua data penting (foto, kontak, dokumen, dll).

2. Konsultasi Profesional
   Jika Anda tidak yakin, sebaiknya konsultasikan dengan teknisi
   profesional untuk menghindari kerusakan lebih lanjut.

3. Garansi
   Cek apakah smartphone masih dalam masa garansi. Perbaikan resmi
   melalui service center dapat mencegah void garansi.

4. Preventive Maintenance
   Lakukan perawatan rutin setiap 6 bulan untuk mencegah kerusakan.

PERINGATAN:
- Jangan coba perbaikan sendiri jika tidak berpengalaman
- Matikan smartphone jika terjadi overheating atau baterai kembung
- Jangan gunakan charger tidak resmi
- Hindari tempat lembab dan suhu ekstrem
        """
        pdf.chapter_body(recommendation_text.strip())
        
        # Footer info
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 9)
        footer_text = """
---
Laporan ini dihasilkan oleh Sistem Pakar Identifikasi Kerusakan Smartphone
Kelompok 2 - INF313 Kecerdasan Artifisial
Disclaimer: Hasil diagnosis bersifat rekomendasi. Konsultasi dengan profesional
untuk diagnosis definitif.
        """
        pdf.multi_cell(0, 5, footer_text.strip())
        
        # Save PDF
        pdf.output(output_path)
        
        return output_path
    
    def _format_list(self, items: List[str]) -> str:
        """Format list menjadi string dengan bullet"""
        if not items:
            return "- Tidak ada informasi"
        return '\n'.join([f"- {item}" for item in items])
    
    def _format_solutions(self, solutions: List[Dict]) -> str:
        """Format solutions menjadi string terstruktur"""
        if not solutions:
            return "- Tidak ada solusi tersedia"
        
        formatted = []
        for sol in solutions:
            step = sol.get('step', '?')
            action = sol.get('action', 'Unknown')
            detail = sol.get('detail', '')
            formatted.append(f"Langkah {step}: {action}\n   {detail}")
        
        return '\n\n'.join(formatted)
    
    def export_to_json(self, 
                      diagnosis_data: Dict,
                      output_filename: str = None) -> str:
        """
        Export hasil diagnosis ke JSON
        
        Args:
            diagnosis_data: Data diagnosis
            output_filename: Nama file output
            
        Returns:
            Path file JSON yang dibuat
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'diagnosis_{timestamp}.json'
        
        output_path = os.path.join(self.export_dir, output_filename)
        
        # Add metadata
        export_data = {
            'export_date': datetime.now().isoformat(),
            'export_format': 'json',
            'version': '1.0',
            'data': diagnosis_data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def export_to_csv(self,
                     diagnosis_data: Dict,
                     output_filename: str = None) -> str:
        """
        Export hasil diagnosis ke CSV
        
        Args:
            diagnosis_data: Data diagnosis
            output_filename: Nama file output
            
        Returns:
            Path file CSV yang dibuat
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'diagnosis_{timestamp}.csv'
        
        output_path = os.path.join(self.export_dir, output_filename)
        
        diagnoses = diagnosis_data.get('diagnoses', [])
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if not diagnoses:
                return output_path
            
            # Get all possible fields
            fieldnames = ['rank', 'diagnosis', 'type', 'confidence', 
                         'description', 'estimated_cost', 'repair_difficulty']
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, diag in enumerate(diagnoses, 1):
                writer.writerow({
                    'rank': i,
                    'diagnosis': diag.get('name', 'Unknown'),
                    'type': diag.get('type', 'Unknown'),
                    'confidence': f"{diag.get('confidence', 0)*100:.1f}%",
                    'description': diag.get('description', '')[:100] + '...',
                    'estimated_cost': diag.get('estimated_cost', '0'),
                    'repair_difficulty': diag.get('repair_difficulty', 'Unknown')
                })
        
        return output_path
    
    def export_history(self,
                      history: List[Dict],
                      format: str = 'json',
                      output_filename: str = None) -> str:
        """
        Export riwayat diagnosis
        
        Args:
            history: List riwayat diagnosis
            format: Format output (json, csv)
            output_filename: Nama file output
            
        Returns:
            Path file yang dibuat
        """
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'history_{timestamp}.{format}'
        
        output_path = os.path.join(self.export_dir, output_filename)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_date': datetime.now().isoformat(),
                    'total_entries': len(history),
                    'history': history
                }, f, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if not history:
                    return output_path
                
                fieldnames = ['timestamp', 'symptoms_count', 'top_diagnosis', 'confidence']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in history:
                    diagnoses = entry.get('diagnoses', [])
                    top_diag = diagnoses[0] if diagnoses else {}
                    
                    writer.writerow({
                        'timestamp': entry.get('timestamp', 'Unknown'),
                        'symptoms_count': len(entry.get('symptoms', [])),
                        'top_diagnosis': top_diag.get('diagnosis', 'Unknown'),
                        'confidence': f"{top_diag.get('cf', 0)*100:.1f}%" if top_diag else 'N/A'
                    })
        
        return output_path


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("EXPORT MODULE TEST")
    print("=" * 70)
    
    # Sample diagnosis data
    sample_diagnosis = {
        'session_id': 'TEST_20250101_120000',
        'diagnoses': [
            {
                'name': 'Kerusakan Touchscreen Digitizer',
                'type': 'hardware',
                'confidence': 0.88,
                'confidence_category': 'Yakin',
                'description': 'Touchscreen tidak berfungsi sementara tampilan normal',
                'causes': [
                    'Kerusakan komponen digitizer',
                    'Konektor digitizer longgar'
                ],
                'solutions': [
                    {
                        'step': 1,
                        'action': 'Restart smartphone',
                        'detail': 'Kadang masalah bisa teratasi dengan restart'
                    },
                    {
                        'step': 2,
                        'action': 'Ganti digitizer',
                        'detail': 'Bawa ke service center untuk penggantian'
                    }
                ],
                'estimated_cost': '200000-500000',
                'repair_difficulty': 'medium',
                'prevention': [
                    'Pasang screen protector',
                    'Hindari tekanan berlebihan'
                ]
            }
        ]
    }
    
    sample_symptoms = [
        'touchscreen_tidak_respons',
        'layar_tampil_normal',
        'tombol_fisik_berfungsi'
    ]
    
    sample_reasoning = [
        {
            'type': 'rule_fired',
            'rule_id': 'R6',
            'conditions': ['touchscreen_tidak_respons', 'layar_tampil_normal'],
            'conclusion': 'kerusakan_touchscreen_digitizer',
            'cf': 0.88
        }
    ]
    
    # Create exporter
    exporter = DiagnosisExporter()
    
    # Export to PDF
    print("\n1. Exporting to PDF...")
    pdf_path = exporter.export_to_pdf(
        sample_diagnosis,
        sample_symptoms,
        sample_reasoning
    )
    print(f"   ✅ PDF exported to: {pdf_path}")
    
    # Export to JSON
    print("\n2. Exporting to JSON...")
    json_path = exporter.export_to_json(sample_diagnosis)
    print(f"   ✅ JSON exported to: {json_path}")
    
    # Export to CSV
    print("\n3. Exporting to CSV...")
    csv_path = exporter.export_to_csv(sample_diagnosis)
    print(f"   ✅ CSV exported to: {csv_path}")
    
    print("\n" + "=" * 70)
    print("Export completed successfully!")
    print("=" * 70)