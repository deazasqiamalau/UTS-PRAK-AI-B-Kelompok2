"""
Backward Chaining Inference Engine
Goal-driven reasoning untuk sistem pakar smartphone
Berdasarkan Kumar & Sharma (2022) dan Lee et al. (2023)
"""

import json
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict
from datetime import datetime


class BackwardChaining:
    """
    Backward Chaining Inference Engine
    Melakukan reasoning dari goal/hipotesis mundur ke fakta
    """
    
    def __init__(self, rules_path: str = "knowledge_base/rules.json"):
        """
        Inisialisasi Backward Chaining Engine
        
        Args:
            rules_path: Path ke file rules JSON
        """
        self.rules = self._load_rules(rules_path)
        self.working_memory = set()  # Fakta yang diketahui
        self.asked_questions = set()  # Pertanyaan yang sudah ditanyakan
        self.proved_goals = set()  # Goal yang sudah terbukti
        self.failed_goals = set()  # Goal yang gagal dibuktikan
        self.reasoning_trace = []  # Jejak reasoning
        self.question_callback = None  # Callback untuk menanyakan user
        
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
        """Reset state engine"""
        self.working_memory.clear()
        self.asked_questions.clear()
        self.proved_goals.clear()
        self.failed_goals.clear()
        self.reasoning_trace.clear()
    
    def set_question_callback(self, callback):
        """
        Set callback function untuk menanyakan user
        
        Args:
            callback: Function yang return True/False untuk question
        """
        self.question_callback = callback
    
    def add_facts(self, facts: List[str]):
        """
        Tambahkan fakta yang sudah diketahui
        
        Args:
            facts: List of known facts
        """
        for fact in facts:
            self.working_memory.add(fact)
            self.reasoning_trace.append({
                'type': 'fact_added',
                'fact': fact,
                'timestamp': datetime.now().isoformat()
            })
    
    def find_rules_for_goal(self, goal: str) -> List[Tuple[str, Dict]]:
        """
        Cari rules yang conclusion-nya adalah goal
        
        Args:
            goal: Goal yang ingin dibuktikan
            
        Returns:
            List of (rule_id, rule) tuples
        """
        matching_rules = []
        for rule_id, rule in self.rules.items():
            if rule.get('THEN') == goal:
                matching_rules.append((rule_id, rule))
        return matching_rules
    
    def prove_goal(self, goal: str, depth: int = 0, max_depth: int = 10) -> bool:
        """
        Coba buktikan sebuah goal secara rekursif
        
        Args:
            goal: Goal yang ingin dibuktikan
            depth: Kedalaman rekursi saat ini
            max_depth: Maksimal kedalaman rekursi
            
        Returns:
            True jika goal terbukti
        """
        # Check depth limit
        if depth > max_depth:
            self.reasoning_trace.append({
                'type': 'max_depth_reached',
                'goal': goal,
                'depth': depth
            })
            return False
        
        # Jika goal sudah terbukti sebelumnya
        if goal in self.proved_goals:
            return True
        
        # Jika goal sudah gagal dibuktikan
        if goal in self.failed_goals:
            return False
        
        # Jika goal adalah fakta yang diketahui
        if goal in self.working_memory:
            self.proved_goals.add(goal)
            self.reasoning_trace.append({
                'type': 'goal_proved_by_fact',
                'goal': goal,
                'depth': depth
            })
            return True
        
        # Cari rules yang bisa membuktikan goal
        matching_rules = self.find_rules_for_goal(goal)
        
        if not matching_rules:
            # Tidak ada rule, tanya user
            if self._ask_user(goal):
                self.working_memory.add(goal)
                self.proved_goals.add(goal)
                self.reasoning_trace.append({
                    'type': 'goal_proved_by_user',
                    'goal': goal,
                    'depth': depth
                })
                return True
            else:
                self.failed_goals.add(goal)
                return False
        
        # Coba buktikan dengan setiap rule
        for rule_id, rule in matching_rules:
            conditions = rule.get('IF', [])
            all_conditions_met = True
            
            self.reasoning_trace.append({
                'type': 'trying_rule',
                'rule_id': rule_id,
                'goal': goal,
                'conditions': conditions,
                'depth': depth
            })
            
            # Coba buktikan semua kondisi
            for condition in conditions:
                if not self.prove_goal(condition, depth + 1, max_depth):
                    all_conditions_met = False
                    break
            
            if all_conditions_met:
                # Semua kondisi terbukti, goal terbukti!
                self.proved_goals.add(goal)
                self.reasoning_trace.append({
                    'type': 'goal_proved_by_rule',
                    'rule_id': rule_id,
                    'goal': goal,
                    'cf': rule.get('CF', 1.0),
                    'depth': depth
                })
                return True
        
        # Tidak ada rule yang berhasil
        self.failed_goals.add(goal)
        return False
    
    def _ask_user(self, question: str) -> bool:
        """
        Tanyakan user tentang sebuah fakta
        
        Args:
            question: Pertanyaan tentang fakta
            
        Returns:
            True jika user confirm
        """
        if question in self.asked_questions:
            return False
        
        self.asked_questions.add(question)
        
        if self.question_callback:
            answer = self.question_callback(question)
            self.reasoning_trace.append({
                'type': 'user_questioned',
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat()
            })
            return answer
        
        return False
    
    def backward_chain(self, goals: List[str]) -> Dict:
        """
        Jalankan backward chaining untuk membuktikan goals
        
        Args:
            goals: List of goals yang ingin dibuktikan
            
        Returns:
            Dictionary berisi hasil reasoning
        """
        results = {
            'goals': goals,
            'proved_goals': [],
            'failed_goals': [],
            'reasoning_trace': [],
            'questions_asked': list(self.asked_questions)
        }
        
        for goal in goals:
            if self.prove_goal(goal):
                results['proved_goals'].append({
                    'goal': goal,
                    'status': 'proved',
                    'confidence': self._calculate_goal_confidence(goal)
                })
            else:
                results['failed_goals'].append({
                    'goal': goal,
                    'status': 'failed'
                })
        
        results['reasoning_trace'] = self.reasoning_trace
        
        return results
    
    def _calculate_goal_confidence(self, goal: str) -> float:
        """
        Hitung confidence untuk goal yang terbukti
        
        Args:
            goal: Goal yang sudah terbukti
            
        Returns:
            Confidence value (0-1)
        """
        # Cari rules yang membuktikan goal
        confidence = 1.0
        
        for trace in self.reasoning_trace:
            if (trace.get('type') == 'goal_proved_by_rule' and 
                trace.get('goal') == goal):
                confidence = min(confidence, trace.get('cf', 1.0))
        
        return confidence
    
    def get_proof_chain(self, goal: str) -> List[Dict]:
        """
        Dapatkan chain of reasoning untuk goal
        
        Args:
            goal: Goal yang ingin dilihat reasoning-nya
            
        Returns:
            List of reasoning steps
        """
        chain = []
        
        for trace in self.reasoning_trace:
            if trace.get('goal') == goal or goal in str(trace.get('conditions', [])):
                chain.append(trace)
        
        return chain
    
    def explain_goal(self, goal: str) -> str:
        """
        Jelaskan bagaimana goal terbukti atau gagal
        
        Args:
            goal: Goal yang ingin dijelaskan
            
        Returns:
            Penjelasan dalam string
        """
        if goal in self.proved_goals:
            explanation = f"Goal '{goal}' TERBUKTI melalui:\n\n"
            
            proof_chain = self.get_proof_chain(goal)
            
            for i, step in enumerate(proof_chain, 1):
                step_type = step.get('type')
                
                if step_type == 'goal_proved_by_fact':
                    explanation += f"{i}. Fakta yang diketahui: {step.get('goal')}\n"
                
                elif step_type == 'goal_proved_by_rule':
                    explanation += f"{i}. Rule {step.get('rule_id')} fired:\n"
                    explanation += f"   Conclusion: {step.get('goal')}\n"
                    explanation += f"   Confidence: {step.get('cf', 1.0)*100:.0f}%\n"
                
                elif step_type == 'goal_proved_by_user':
                    explanation += f"{i}. Dikonfirmasi oleh user: {step.get('goal')}\n"
            
            return explanation
        
        elif goal in self.failed_goals:
            return f"Goal '{goal}' GAGAL dibuktikan. Tidak ada rule atau fakta yang mendukung."
        
        else:
            return f"Goal '{goal}' belum dicoba dibuktikan."
    
    def get_statistics(self) -> Dict:
        """
        Dapatkan statistik reasoning
        
        Returns:
            Dictionary berisi statistik
        """
        return {
            'total_goals_attempted': len(self.proved_goals) + len(self.failed_goals),
            'proved_goals': len(self.proved_goals),
            'failed_goals': len(self.failed_goals),
            'questions_asked': len(self.asked_questions),
            'reasoning_steps': len(self.reasoning_trace),
            'success_rate': (len(self.proved_goals) / 
                           max(len(self.proved_goals) + len(self.failed_goals), 1) * 100)
        }


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("BACKWARD CHAINING ENGINE - TEST")
    print("=" * 70)
    
    # Initialize engine
    engine = BackwardChaining()
    
    # Define question callback
    def simple_callback(question: str) -> bool:
        """Simple callback untuk testing"""
        # Simulasi user answer
        user_answers = {
            'touchscreen_tidak_respons': True,
            'layar_tampil_normal': True,
            'tombol_fisik_berfungsi': True,
            'baterai_cepat_habis': False
        }
        return user_answers.get(question, False)
    
    engine.set_question_callback(simple_callback)
    
    # Test case: Coba buktikan kerusakan digitizer
    print("\nTest Case: Membuktikan 'kerusakan_touchscreen_digitizer'")
    print("-" * 70)
    
    # Add some initial facts
    initial_facts = ['layar_tampil_normal', 'tombol_fisik_berfungsi']
    engine.add_facts(initial_facts)
    
    # Try to prove goal
    goal = 'kerusakan_touchscreen_digitizer'
    
    if engine.prove_goal(goal):
        print(f"✅ Goal '{goal}' TERBUKTI!")
        print(f"\nConfidence: {engine._calculate_goal_confidence(goal)*100:.0f}%")
    else:
        print(f"❌ Goal '{goal}' GAGAL dibuktikan")
    
    # Show explanation
    print("\n" + "=" * 70)
    print("PENJELASAN REASONING:")
    print("=" * 70)
    print(engine.explain_goal(goal))
    
    # Show statistics
    print("\n" + "=" * 70)
    print("STATISTIK:")
    print("=" * 70)
    stats = engine.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 70)