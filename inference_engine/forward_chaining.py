"""
Forward Chaining Inference Engine
Data-driven reasoning untuk sistem pakar smartphone
Berdasarkan Zhang et al. (2021) dan Kumar & Sharma (2022)
"""

import json
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class ForwardChaining:
    """
    Forward Chaining Inference Engine
    Melakukan reasoning dari fakta yang diketahui menuju kesimpulan
    """
    
    def __init__(self, rules_path: str = "knowledge_base/rules.json"):
        """
        Inisialisasi Forward Chaining Engine
        
        Args:
            rules_path: Path ke file rules JSON
        """
        # Try different path locations
        import os
        possible_paths = [
            rules_path,
            os.path.join(os.getcwd(), rules_path),
            os.path.join(os.path.dirname(__file__), "..", rules_path)
        ]
        
        loaded = False
        for path in possible_paths:
            if os.path.exists(path):
                self.rules = self._load_rules(path)
                loaded = True
                print(f"✓ Rules loaded from: {path}")
                break
        
        if not loaded:
            print(f"⚠ Warning: Could not load rules from any path")
            self.rules = {}
        
        self.working_memory = set()  # Fakta yang diketahui
        self.inferred_facts = set()  # Fakta hasil inferensi
        self.fired_rules = []  # Rules yang sudah dijalankan
        self.reasoning_trace = []  # Jejak reasoning untuk explanation
        self.diagnosis_scores = defaultdict(float)  # Skor untuk setiap diagnosis
        
        # Debug info
        print(f"✓ Total rules loaded: {len(self.rules)}")
        
    def _load_rules(self, rules_path: str) -> Dict:
        """Load rules dari file JSON"""
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('rules', {})
        except FileNotFoundError:
            print(f"Warning: Rules file not found at {rules_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
    
    def reset(self):
        """Reset working memory dan hasil inferensi"""
        self.working_memory.clear()
        self.inferred_facts.clear()
        self.fired_rules.clear()
        self.reasoning_trace.clear()
        self.diagnosis_scores.clear()
    
    def add_facts(self, facts: List[str]):
        """
        Tambahkan fakta ke working memory
        
        Args:
            facts: List of facts (symptoms) yang diamati
        """
        for fact in facts:
            self.working_memory.add(fact)
            self.reasoning_trace.append({
                'type': 'fact_added',
                'fact': fact,
                'timestamp': datetime.now().isoformat()
            })
    
    def can_fire_rule(self, rule: Dict) -> bool:
        """
        Cek apakah rule bisa di-fire
        
        Args:
            rule: Rule dictionary
            
        Returns:
            True jika semua kondisi IF terpenuhi
        """
        conditions = rule.get('IF', [])
        all_facts = self.working_memory.union(self.inferred_facts)
        return all(condition in all_facts for condition in conditions)
    
    def fire_rule(self, rule_id: str, rule: Dict) -> Optional[str]:
        """
        Fire/execute sebuah rule
        
        Args:
            rule_id: ID rule
            rule: Rule dictionary
            
        Returns:
            Conclusion yang dihasilkan atau None
        """
        if rule_id in self.fired_rules:
            return None
        
        conclusion = rule.get('THEN')
        cf = rule.get('CF', 1.0)
        
        # Tambahkan conclusion ke inferred facts
        self.inferred_facts.add(conclusion)
        self.fired_rules.append(rule_id)
        
        # Update diagnosis score dengan CF
        self.diagnosis_scores[conclusion] += cf
        
        # Catat dalam reasoning trace
        self.reasoning_trace.append({
            'type': 'rule_fired',
            'rule_id': rule_id,
            'conditions': rule.get('IF', []),
            'conclusion': conclusion,
            'cf': cf,
            'description': rule.get('description', ''),
            'timestamp': datetime.now().isoformat()
        })
        
        return conclusion
    
    def forward_chain(self, max_iterations: int = 50) -> Dict:
        """
        Jalankan forward chaining
        
        Args:
            max_iterations: Maksimal iterasi untuk mencegah infinite loop
            
        Returns:
            Dictionary berisi hasil inferensi
        """
        iteration = 0
        new_facts_added = True
        
        while new_facts_added and iteration < max_iterations:
            new_facts_added = False
            iteration += 1
            
            # Iterasi semua rules
            for rule_id, rule in self.rules.items():
                # Skip jika rule sudah pernah fired
                if rule_id in self.fired_rules:
                    continue
                
                # Cek apakah rule bisa di-fire
                if self.can_fire_rule(rule):
                    conclusion = self.fire_rule(rule_id, rule)
                    if conclusion:
                        new_facts_added = True
        
        # Compile hasil
        results = {
            'iterations': iteration,
            'initial_facts': list(self.working_memory),
            'inferred_facts': list(self.inferred_facts),
            'fired_rules': self.fired_rules,
            'diagnosis_scores': dict(self.diagnosis_scores),
            'reasoning_trace': self.reasoning_trace,
            'final_diagnoses': self._get_final_diagnoses()
        }
        
        return results
    
    def _get_final_diagnoses(self) -> List[Dict]:
        """
        Dapatkan diagnosis final dengan ranking berdasarkan CF
        
        Returns:
            List of diagnoses dengan score terurut
        """
        # Filter hanya diagnosis yang merupakan kesimpulan akhir
        final_diagnosis_keywords = [
            'kerusakan', 'masalah', 'degradasi', 'rusak', 
            'aplikasi', 'malware', 'storage', 'tindakan'
        ]
        
        diagnoses = []
        for diagnosis, score in self.diagnosis_scores.items():
            # Cek apakah ini diagnosis final (bukan intermediate)
            is_final = any(keyword in diagnosis.lower() 
                          for keyword in final_diagnosis_keywords)
            
            if is_final:
                diagnoses.append({
                    'diagnosis': diagnosis,
                    'confidence': min(score, 1.0),  # Normalize ke 0-1
                    'percentage': min(score * 100, 100)  # Dalam persen
                })
        
        # Sort berdasarkan confidence
        diagnoses.sort(key=lambda x: x['confidence'], reverse=True)
        
        return diagnoses
    
    def explain_reasoning(self, diagnosis: str) -> List[Dict]:
        """
        Jelaskan bagaimana sistem sampai pada diagnosis tertentu
        
        Args:
            diagnosis: Diagnosis yang ingin dijelaskan
            
        Returns:
            List of reasoning steps yang mengarah ke diagnosis
        """
        explanation = []
        
        # Cari semua rules yang mengarah ke diagnosis
        for trace in self.reasoning_trace:
            if trace['type'] == 'rule_fired' and trace['conclusion'] == diagnosis:
                explanation.append({
                    'rule_id': trace['rule_id'],
                    'conditions': trace['conditions'],
                    'conclusion': trace['conclusion'],
                    'cf': trace['cf'],
                    'description': trace['description']
                })
        
        return explanation
    
    def get_reasoning_chain(self, diagnosis: str) -> List[str]:
        """
        Dapatkan rantai reasoning lengkap untuk diagnosis
        
        Args:
            diagnosis: Target diagnosis
            
        Returns:
            List of rules dalam urutan firing
        """
        chain = []
        
        for trace in self.reasoning_trace:
            if trace['type'] == 'rule_fired':
                if diagnosis in trace['conclusion'] or trace['conclusion'] == diagnosis:
                    chain.append(trace['rule_id'])
        
        return chain
    
    def why_question(self, question: str) -> str:
        """
        Jawab pertanyaan WHY - mengapa sistem menanyakan sesuatu
        
        Args:
            question: Gejala yang ditanyakan
            
        Returns:
            Penjelasan mengapa gejala tersebut penting
        """
        # Cari rules yang menggunakan gejala ini
        relevant_rules = []
        for rule_id, rule in self.rules.items():
            if question in rule.get('IF', []):
                relevant_rules.append({
                    'rule_id': rule_id,
                    'conclusion': rule.get('THEN'),
                    'description': rule.get('description', '')
                })
        
        if not relevant_rules:
            return f"Gejala '{question}' digunakan untuk membantu diagnosis."
        
        explanation = f"Sistem menanyakan '{question}' karena:\n\n"
        for i, rule in enumerate(relevant_rules[:3], 1):  # Max 3 rules
            explanation += f"{i}. {rule['description']}\n"
            explanation += f"   → Dapat mengarah ke: {rule['conclusion']}\n\n"
        
        return explanation
    
    def how_question(self, diagnosis: str) -> str:
        """
        Jawab pertanyaan HOW - bagaimana sistem sampai pada kesimpulan
        
        Args:
            diagnosis: Diagnosis yang ditanyakan
            
        Returns:
            Penjelasan step-by-step reasoning
        """
        explanation_steps = self.explain_reasoning(diagnosis)
        
        if not explanation_steps:
            return f"Tidak ditemukan reasoning path untuk diagnosis '{diagnosis}'"
        
        explanation = f"Sistem sampai pada diagnosis '{diagnosis}' melalui langkah:\n\n"
        
        for i, step in enumerate(explanation_steps, 1):
            explanation += f"Langkah {i} - {step['rule_id']}:\n"
            explanation += f"  Jika: {', '.join(step['conditions'])}\n"
            explanation += f"  Maka: {step['conclusion']}\n"
            explanation += f"  Kepercayaan: {step['cf']*100:.0f}%\n"
            explanation += f"  Penjelasan: {step['description']}\n\n"
        
        return explanation
    
    def get_confidence_explanation(self, diagnosis: str) -> Dict:
        """
        Dapatkan penjelasan detail tentang confidence score
        
        Args:
            diagnosis: Diagnosis yang ditanyakan
            
        Returns:
            Dictionary berisi breakdown confidence
        """
        rules_contributing = []
        total_cf = 0
        
        for trace in self.reasoning_trace:
            if trace['type'] == 'rule_fired' and trace['conclusion'] == diagnosis:
                rules_contributing.append({
                    'rule_id': trace['rule_id'],
                    'cf': trace['cf'],
                    'conditions': trace['conditions']
                })
                total_cf += trace['cf']
        
        return {
            'diagnosis': diagnosis,
            'total_confidence': min(total_cf, 1.0),
            'contributing_rules': rules_contributing,
            'explanation': f"Diagnosis ini didukung oleh {len(rules_contributing)} rule(s)"
        }


# Utility functions
def combine_certainty_factors(cf1: float, cf2: float) -> float:
    """
    Kombinasi CF untuk multiple evidence
    Formula: CF(H,E1∧E2) = CF(H,E1) + CF(H,E2) × [1 - CF(H,E1)]
    
    Args:
        cf1: Certainty Factor pertama
        cf2: Certainty Factor kedua
        
    Returns:
        Combined certainty factor
    """
    if cf1 > 0 and cf2 > 0:
        return cf1 + cf2 * (1 - cf1)
    elif cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    else:
        return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))


def calculate_mb_md(mb: float, md: float) -> float:
    """
    Hitung CF dari Measure of Belief dan Measure of Disbelief
    Formula: CF(H,E) = MB(H,E) - MD(H,E)
    
    Args:
        mb: Measure of Belief (0 to 1)
        md: Measure of Disbelief (0 to 1)
        
    Returns:
        Certainty Factor (-1 to 1)
    """
    return mb - md


# Example usage and testing
if __name__ == "__main__":
    # Initialize engine
    engine = ForwardChaining()
    
    # Test case: Layar tidak merespons
    print("=" * 60)
    print("TEST CASE: Touchscreen tidak merespons")
    print("=" * 60)
    
    # Add symptoms
    symptoms = [
        'touchscreen_tidak_respons',
        'layar_tampil_normal',
        'tombol_fisik_berfungsi'
    ]
    
    engine.add_facts(symptoms)
    
    # Run inference
    results = engine.forward_chain()
    
    # Display results
    print(f"\nIterasi: {results['iterations']}")
    print(f"Fakta awal: {len(results['initial_facts'])}")
    print(f"Fakta terinferensi: {len(results['inferred_facts'])}")
    print(f"Rules yang fired: {len(results['fired_rules'])}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSIS:")
    print("=" * 60)
    
    for i, diag in enumerate(results['final_diagnoses'], 1):
        print(f"\n{i}. {diag['diagnosis']}")
        print(f"   Tingkat Kepercayaan: {diag['percentage']:.1f}%")
    
    # Test WHY question
    print("\n" + "=" * 60)
    print("WHY Question:")
    print("=" * 60)
    print(engine.why_question('touchscreen_tidak_respons'))
    
    # Test HOW question
    if results['final_diagnoses']:
        top_diagnosis = results['final_diagnoses'][0]['diagnosis']
        print("\n" + "=" * 60)
        print("HOW Question:")
        print("=" * 60)
        print(engine.how_question(top_diagnosis))