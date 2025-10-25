"""
Certainty Factor Module
Implementasi CF untuk menangani ketidakpastian dalam diagnosis
Berdasarkan Shortliffe-Buchanan (1975) dan Zhang et al. (2021)
"""

from typing import Dict, List, Tuple
import math


class CertaintyFactor:
    """
    Certainty Factor Calculator untuk Expert System
    CF Range: -1.0 (pasti salah) hingga +1.0 (pasti benar)
    """
    
    def __init__(self):
        """Initialize CF calculator"""
        self.cf_rules = {}  # CF untuk setiap rule
        self.cf_user = {}   # CF dari user input
        self.cf_combined = {}  # CF hasil kombinasi
    
    @staticmethod
    def calculate_cf(mb: float, md: float) -> float:
        """
        Hitung CF dari Measure of Belief dan Measure of Disbelief
        Formula: CF(H,E) = MB(H,E) - MD(H,E)
        
        Args:
            mb: Measure of Belief (0 to 1)
            md: Measure of Disbelief (0 to 1)
            
        Returns:
            CF value (-1 to 1)
        """
        return mb - md
    
    @staticmethod
    def combine_sequential_cf(cf1: float, cf2: float) -> float:
        """
        Kombinasi CF untuk evidence sequential (E1 dan E2)
        
        Formula:
        - Jika CF1 > 0 dan CF2 > 0: CF = CF1 + CF2 * (1 - CF1)
        - Jika CF1 < 0 dan CF2 < 0: CF = CF1 + CF2 * (1 + CF1)
        - Jika CF1 dan CF2 berbeda tanda: CF = (CF1 + CF2) / (1 - min(|CF1|, |CF2|))
        
        Args:
            cf1: Certainty Factor pertama
            cf2: Certainty Factor kedua
            
        Returns:
            Combined CF
        """
        # Both positive
        if cf1 > 0 and cf2 > 0:
            return cf1 + cf2 * (1 - cf1)
        
        # Both negative
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        
        # Different signs
        else:
            denominator = 1 - min(abs(cf1), abs(cf2))
            if denominator == 0:
                return 0
            return (cf1 + cf2) / denominator
    
    @staticmethod
    def combine_parallel_cf(cf_list: List[float]) -> float:
        """
        Kombinasi CF untuk multiple evidence parallel
        Digunakan saat ada beberapa rule yang mengarah ke conclusion yang sama
        
        Args:
            cf_list: List of CF values
            
        Returns:
            Combined CF
        """
        if not cf_list:
            return 0.0
        
        result = cf_list[0]
        for cf in cf_list[1:]:
            result = CertaintyFactor.combine_sequential_cf(result, cf)
        
        return result
    
    @staticmethod
    def cf_with_user_certainty(cf_rule: float, cf_user: float) -> float:
        """
        Kombinasi CF rule dengan CF dari user
        CF(H,E) = CF(E) * CF(Rule)
        
        Args:
            cf_rule: CF dari rule/pakar
            cf_user: CF dari user (tingkat keyakinan user terhadap gejala)
            
        Returns:
            Combined CF
        """
        return cf_rule * cf_user
    
    @staticmethod
    def interpret_cf(cf: float) -> Tuple[str, str]:
        """
        Interpretasi nilai CF menjadi bahasa natural
        
        Args:
            cf: Certainty Factor value
            
        Returns:
            Tuple (kategori, deskripsi)
        """
        cf = abs(cf)  # Gunakan absolute untuk interpretasi
        
        if cf >= 0.9:
            return ("Sangat Yakin", "Diagnosis ini sangat mungkin benar")
        elif cf >= 0.7:
            return ("Yakin", "Diagnosis ini kemungkinan besar benar")
        elif cf >= 0.5:
            return ("Cukup Yakin", "Diagnosis ini cukup mungkin benar")
        elif cf >= 0.3:
            return ("Kurang Yakin", "Diagnosis ini mungkin benar")
        elif cf >= 0.1:
            return ("Tidak Yakin", "Diagnosis ini kurang mungkin benar")
        else:
            return ("Sangat Tidak Yakin", "Diagnosis ini sangat kecil kemungkinannya")
    
    @staticmethod
    def get_confidence_percentage(cf: float) -> float:
        """
        Konversi CF ke persentase kepercayaan
        
        Args:
            cf: Certainty Factor value
            
        Returns:
            Percentage (0-100)
        """
        # Normalisasi dari [-1, 1] ke [0, 100]
        return ((cf + 1) / 2) * 100
    
    def add_rule_cf(self, rule_id: str, cf: float):
        """
        Tambahkan CF untuk sebuah rule
        
        Args:
            rule_id: ID rule
            cf: Certainty factor value
        """
        self.cf_rules[rule_id] = cf
    
    def add_user_cf(self, symptom: str, cf: float):
        """
        Tambahkan CF dari user untuk sebuah gejala
        
        Args:
            symptom: Symptom ID
            cf: User certainty (0-1, bisa juga 1-5 scale yang dinormalisasi)
        """
        self.cf_user[symptom] = cf
    
    def calculate_hypothesis_cf(self, 
                                rule_cfs: List[float], 
                                user_cfs: List[float]) -> float:
        """
        Hitung CF untuk sebuah hipotesis dengan multiple evidence
        
        Args:
            rule_cfs: List of CF dari rules
            user_cfs: List of CF dari user
            
        Returns:
            Final combined CF
        """
        if len(rule_cfs) != len(user_cfs):
            raise ValueError("Rule CFs and User CFs must have same length")
        
        # Hitung CF untuk setiap evidence
        evidence_cfs = []
        for rule_cf, user_cf in zip(rule_cfs, user_cfs):
            evidence_cf = self.cf_with_user_certainty(rule_cf, user_cf)
            evidence_cfs.append(evidence_cf)
        
        # Kombinasikan semua CF
        return self.combine_parallel_cf(evidence_cfs)
    
    @staticmethod
    def normalize_user_input(value: int, scale: int = 5) -> float:
        """
        Normalisasi input user dari skala tertentu ke [0, 1]
        
        Args:
            value: Nilai input user (misal 1-5)
            scale: Skala maksimum (default 5)
            
        Returns:
            Normalized CF (0-1)
        """
        return value / scale
    
    @staticmethod
    def likert_to_cf(likert: str) -> float:
        """
        Konversi Likert scale ke CF value
        
        Args:
            likert: String Likert (Sangat Tidak Yakin, Tidak Yakin, dst)
            
        Returns:
            CF value
        """
        mapping = {
            "sangat_tidak_yakin": 0.0,
            "tidak_yakin": 0.2,
            "ragu_ragu": 0.4,
            "yakin": 0.6,
            "cukup_yakin": 0.8,
            "sangat_yakin": 1.0
        }
        return mapping.get(likert.lower(), 0.5)


class CFCalculator:
    """
    Advanced CF Calculator dengan tracking dan history
    """
    
    def __init__(self):
        """Initialize calculator"""
        self.calculations = []
        self.hypothesis_cfs = {}
    
    def calculate_and_track(self, 
                           hypothesis: str,
                           evidences: List[Dict]) -> Dict:
        """
        Calculate CF dengan tracking detail
        
        Args:
            hypothesis: Hypothesis/diagnosis name
            evidences: List of evidence dicts dengan 'rule_cf' dan 'user_cf'
            
        Returns:
            Dictionary berisi hasil dan detail kalkulasi
        """
        cf = CertaintyFactor()
        
        rule_cfs = [e['rule_cf'] for e in evidences]
        user_cfs = [e.get('user_cf', 1.0) for e in evidences]
        
        # Calculate individual evidence CFs
        evidence_results = []
        for i, (rule_cf, user_cf) in enumerate(zip(rule_cfs, user_cfs)):
            evidence_cf = cf.cf_with_user_certainty(rule_cf, user_cf)
            evidence_results.append({
                'evidence_id': evidences[i].get('id', f'E{i+1}'),
                'rule_cf': rule_cf,
                'user_cf': user_cf,
                'combined_cf': evidence_cf
            })
        
        # Calculate final CF
        final_cf = cf.calculate_hypothesis_cf(rule_cfs, user_cfs)
        
        # Interpretation
        category, description = cf.interpret_cf(final_cf)
        percentage = cf.get_confidence_percentage(final_cf)
        
        result = {
            'hypothesis': hypothesis,
            'final_cf': final_cf,
            'percentage': percentage,
            'category': category,
            'description': description,
            'evidence_details': evidence_results,
            'calculation_steps': self._generate_calculation_steps(evidence_results, final_cf)
        }
        
        # Store calculation
        self.calculations.append(result)
        self.hypothesis_cfs[hypothesis] = final_cf
        
        return result
    
    def _generate_calculation_steps(self, 
                                   evidences: List[Dict], 
                                   final_cf: float) -> List[str]:
        """
        Generate penjelasan step-by-step kalkulasi
        
        Args:
            evidences: List of evidence results
            final_cf: Final CF value
            
        Returns:
            List of calculation steps
        """
        steps = []
        
        steps.append("Langkah 1: Hitung CF untuk setiap evidence")
        for i, ev in enumerate(evidences, 1):
            steps.append(
                f"  E{i}: CF(Rule) × CF(User) = {ev['rule_cf']:.2f} × {ev['user_cf']:.2f} "
                f"= {ev['combined_cf']:.2f}"
            )
        
        steps.append("\nLangkah 2: Kombinasikan semua CF")
        if len(evidences) > 1:
            steps.append(f"  CF kombinasi = {final_cf:.2f}")
            steps.append(f"  Formula: CF1 + CF2 × (1 - CF1) untuk CF positif")
        else:
            steps.append(f"  CF final = {final_cf:.2f}")
        
        steps.append(f"\nLangkah 3: Interpretasi")
        steps.append(f"  Tingkat Kepercayaan: {((final_cf + 1) / 2 * 100):.1f}%")
        
        return steps
    
    def get_top_hypotheses(self, n: int = 3) -> List[Tuple[str, float]]:
        """
        Dapatkan top N hypotheses berdasarkan CF
        
        Args:
            n: Jumlah top hypotheses
            
        Returns:
            List of (hypothesis, cf) tuples
        """
        sorted_hyp = sorted(
            self.hypothesis_cfs.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_hyp[:n]
    
    def compare_hypotheses(self, hyp1: str, hyp2: str) -> Dict:
        """
        Bandingkan dua hypotheses
        
        Args:
            hyp1: Hypothesis 1
            hyp2: Hypothesis 2
            
        Returns:
            Comparison result
        """
        cf1 = self.hypothesis_cfs.get(hyp1, 0)
        cf2 = self.hypothesis_cfs.get(hyp2, 0)
        
        return {
            'hypothesis_1': {'name': hyp1, 'cf': cf1, 'percentage': CertaintyFactor.get_confidence_percentage(cf1)},
            'hypothesis_2': {'name': hyp2, 'cf': cf2, 'percentage': CertaintyFactor.get_confidence_percentage(cf2)},
            'difference': abs(cf1 - cf2),
            'more_likely': hyp1 if cf1 > cf2 else hyp2
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("CERTAINTY FACTOR CALCULATOR - TEST")
    print("=" * 70)
    
    # Test 1: Basic CF calculation
    print("\nTest 1: Basic CF Calculation")
    print("-" * 70)
    
    cf = CertaintyFactor()
    
    # Contoh: Rule mengatakan CF=0.8, user yakin 100% (CF=1.0)
    rule_cf = 0.8
    user_cf = 1.0
    combined = cf.cf_with_user_certainty(rule_cf, user_cf)
    
    print(f"CF Rule: {rule_cf}")
    print(f"CF User: {user_cf}")
    print(f"CF Combined: {combined}")
    print(f"Persentase: {cf.get_confidence_percentage(combined):.1f}%")
    category, desc = cf.interpret_cf(combined)
    print(f"Interpretasi: {category} - {desc}")
    
    # Test 2: Multiple evidence combination
    print("\n\nTest 2: Multiple Evidence Combination")
    print("-" * 70)
    
    calculator = CFCalculator()
    
    # Simulasi diagnosis dengan 3 evidence
    evidences = [
        {'id': 'E1', 'rule_cf': 0.7, 'user_cf': 1.0, 'name': 'Layar tidak merespons'},
        {'id': 'E2', 'rule_cf': 0.8, 'user_cf': 0.9, 'name': 'Layar tampil normal'},
        {'id': 'E3', 'rule_cf': 0.9, 'user_cf': 1.0, 'name': 'Tombol fisik berfungsi'}
    ]
    
    result = calculator.calculate_and_track('Kerusakan Digitizer', evidences)
    
    print(f"Diagnosis: {result['hypothesis']}")
    print(f"CF Final: {result['final_cf']:.3f}")
    print(f"Persentase Kepercayaan: {result['percentage']:.1f}%")
    print(f"Kategori: {result['category']}")
    print(f"Deskripsi: {result['description']}")
    
    print("\nDetail Evidence:")
    for ev in result['evidence_details']:
        print(f"  {ev['evidence_id']}: CF_rule={ev['rule_cf']:.2f}, "
              f"CF_user={ev['user_cf']:.2f}, CF_combined={ev['combined_cf']:.3f}")
    
    print("\nLangkah Kalkulasi:")
    for step in result['calculation_steps']:
        print(step)
    
    # Test 3: Sequential CF combination
    print("\n\nTest 3: Sequential CF Combination")
    print("-" * 70)
    
    cf_values = [0.6, 0.7, 0.5]
    combined_cf = CertaintyFactor.combine_parallel_cf(cf_values)
    
    print(f"CF Values: {cf_values}")
    print(f"Combined CF: {combined_cf:.3f}")
    print(f"Persentase: {CertaintyFactor.get_confidence_percentage(combined_cf):.1f}%")
    
    # Test 4: Likert scale conversion
    print("\n\nTest 4: Likert Scale to CF")
    print("-" * 70)
    
    likert_scales = [
        "sangat_tidak_yakin",
        "tidak_yakin", 
        "ragu_ragu",
        "yakin",
        "cukup_yakin",
        "sangat_yakin"
    ]
    
    print("Konversi Likert Scale:")
    for likert in likert_scales:
        cf_val = CertaintyFactor.likert_to_cf(likert)
        print(f"  {likert:20s} -> CF: {cf_val:.1f} ({cf_val*100:.0f}%)")
    
    print("\n" + "=" * 70)