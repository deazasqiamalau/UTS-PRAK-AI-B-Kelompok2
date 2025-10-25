"""
Input Validator Module
Validasi input untuk sistem pakar smartphone
"""

import re
from typing import List, Dict, Any, Tuple
import json


class ValidationError(Exception):
    """Custom exception untuk validation errors"""
    pass


class InputValidator:
    """Validator untuk berbagai input sistem"""
    
    def __init__(self):
        """Initialize validator"""
        self.errors = []
        
    def reset_errors(self):
        """Reset error list"""
        self.errors = []
    
    def add_error(self, field: str, message: str):
        """
        Tambahkan error ke list
        
        Args:
            field: Nama field yang error
            message: Pesan error
        """
        self.errors.append({
            'field': field,
            'message': message
        })
    
    def has_errors(self) -> bool:
        """Check apakah ada errors"""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[Dict]:
        """Get semua errors"""
        return self.errors
    
    def get_error_messages(self) -> List[str]:
        """Get error messages saja"""
        return [f"{err['field']}: {err['message']}" for err in self.errors]
    
    # Symptom Validation
    def validate_symptom_id(self, symptom_id: str) -> bool:
        """
        Validasi symptom ID
        
        Args:
            symptom_id: ID symptom
            
        Returns:
            True jika valid
        """
        if not symptom_id:
            self.add_error('symptom_id', 'Symptom ID tidak boleh kosong')
            return False
        
        if not isinstance(symptom_id, str):
            self.add_error('symptom_id', 'Symptom ID harus berupa string')
            return False
        
        # Check format (huruf kecil, underscore, angka)
        if not re.match(r'^[a-z][a-z0-9_]*$', symptom_id):
            self.add_error('symptom_id', 
                          'Symptom ID harus huruf kecil, angka, dan underscore')
            return False
        
        return True
    
    def validate_symptoms_list(self, 
                              symptoms: List[str], 
                              min_count: int = 1, 
                              max_count: int = 15) -> bool:
        """
        Validasi list symptoms
        
        Args:
            symptoms: List symptom IDs
            min_count: Minimum jumlah symptoms
            max_count: Maximum jumlah symptoms
            
        Returns:
            True jika valid
        """
        if not isinstance(symptoms, list):
            self.add_error('symptoms', 'Symptoms harus berupa list')
            return False
        
        if len(symptoms) < min_count:
            self.add_error('symptoms', 
                          f'Minimal {min_count} symptom harus dipilih')
            return False
        
        if len(symptoms) > max_count:
            self.add_error('symptoms', 
                          f'Maksimal {max_count} symptoms dapat dipilih')
            return False
        
        # Validate each symptom
        for symptom in symptoms:
            if not self.validate_symptom_id(symptom):
                return False
        
        # Check duplicates
        if len(symptoms) != len(set(symptoms)):
            self.add_error('symptoms', 'Terdapat symptom duplikat')
            return False
        
        return True
    
    # Certainty Factor Validation
    def validate_cf(self, cf: float, cf_type: str = 'general') -> bool:
        """
        Validasi Certainty Factor value
        
        Args:
            cf: Nilai CF
            cf_type: Tipe CF (general, user, rule)
            
        Returns:
            True jika valid
        """
        if not isinstance(cf, (int, float)):
            self.add_error('cf', 'CF harus berupa angka')
            return False
        
        if cf < 0.0 or cf > 1.0:
            self.add_error('cf', 'CF harus antara 0.0 dan 1.0')
            return False
        
        return True
    
    def validate_cf_dict(self, cf_dict: Dict[str, float]) -> bool:
        """
        Validasi dictionary CF untuk multiple symptoms
        
        Args:
            cf_dict: Dictionary {symptom_id: cf_value}
            
        Returns:
            True jika valid
        """
        if not isinstance(cf_dict, dict):
            self.add_error('cf_dict', 'CF dict harus berupa dictionary')
            return False
        
        for symptom_id, cf in cf_dict.items():
            if not self.validate_symptom_id(symptom_id):
                return False
            if not self.validate_cf(cf, 'user'):
                return False
        
        return True
    
    # Rule Validation
    def validate_rule_structure(self, rule: Dict) -> bool:
        """
        Validasi struktur rule
        
        Args:
            rule: Rule dictionary
            
        Returns:
            True jika valid
        """
        # Required fields
        required_fields = ['IF', 'THEN']
        
        for field in required_fields:
            if field not in rule:
                self.add_error('rule', f'Field {field} wajib ada')
                return False
        
        # Validate IF (conditions)
        if not isinstance(rule['IF'], list):
            self.add_error('rule', 'IF harus berupa list')
            return False
        
        if len(rule['IF']) == 0:
            self.add_error('rule', 'IF tidak boleh kosong')
            return False
        
        for condition in rule['IF']:
            if not isinstance(condition, str):
                self.add_error('rule', 'Kondisi IF harus berupa string')
                return False
        
        # Validate THEN (conclusion)
        if not isinstance(rule['THEN'], str):
            self.add_error('rule', 'THEN harus berupa string')
            return False
        
        if not rule['THEN']:
            self.add_error('rule', 'THEN tidak boleh kosong')
            return False
        
        # Validate CF (optional)
        if 'CF' in rule:
            if not self.validate_cf(rule['CF'], 'rule'):
                return False
        
        return True
    
    def validate_rule_id(self, rule_id: str) -> bool:
        """
        Validasi rule ID
        
        Args:
            rule_id: ID rule
            
        Returns:
            True jika valid
        """
        if not rule_id:
            self.add_error('rule_id', 'Rule ID tidak boleh kosong')
            return False
        
        # Format: R + angka atau R + angka + underscore + text
        if not re.match(r'^R\d+(_[a-zA-Z0-9_]+)?$', rule_id):
            self.add_error('rule_id', 
                          'Rule ID harus format R<angka> (contoh: R1, R10)')
            return False
        
        return True
    
    # Diagnosis Validation
    def validate_diagnosis_structure(self, diagnosis: Dict) -> bool:
        """
        Validasi struktur diagnosis
        
        Args:
            diagnosis: Diagnosis dictionary
            
        Returns:
            True jika valid
        """
        required_fields = ['id', 'name', 'type', 'description']
        
        for field in required_fields:
            if field not in diagnosis:
                self.add_error('diagnosis', f'Field {field} wajib ada')
                return False
        
        # Validate type
        valid_types = ['hardware', 'software', 'hybrid']
        if diagnosis['type'] not in valid_types:
            self.add_error('diagnosis', 
                          f'Type harus salah satu dari: {", ".join(valid_types)}')
            return False
        
        # Validate lists
        list_fields = ['causes', 'solutions', 'prevention']
        for field in list_fields:
            if field in diagnosis and not isinstance(diagnosis[field], list):
                self.add_error('diagnosis', f'{field} harus berupa list')
                return False
        
        return True
    
    # JSON Validation
    def validate_json_file(self, filepath: str) -> bool:
        """
        Validasi JSON file
        
        Args:
            filepath: Path ke JSON file
            
        Returns:
            True jika valid
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return True
        except FileNotFoundError:
            self.add_error('json_file', f'File tidak ditemukan: {filepath}')
            return False
        except json.JSONDecodeError as e:
            self.add_error('json_file', f'Invalid JSON: {str(e)}')
            return False
        except Exception as e:
            self.add_error('json_file', f'Error: {str(e)}')
            return False
    
    # Knowledge Base Validation
    def validate_knowledge_base_rules(self, rules: Dict) -> bool:
        """
        Validasi keseluruhan rules dalam knowledge base
        
        Args:
            rules: Dictionary berisi rules
            
        Returns:
            True jika valid
        """
        if not isinstance(rules, dict):
            self.add_error('rules', 'Rules harus berupa dictionary')
            return False
        
        if 'rules' not in rules:
            self.add_error('rules', 'Key "rules" tidak ditemukan')
            return False
        
        # Validate each rule
        for rule_id, rule in rules['rules'].items():
            if not self.validate_rule_id(rule_id):
                return False
            if not self.validate_rule_structure(rule):
                return False
        
        return True
    
    # User Input Validation
    def validate_user_certainty(self, certainty: Any) -> bool:
        """
        Validasi input certainty dari user
        
        Args:
            certainty: Input certainty (bisa int 1-5 atau float 0-1)
            
        Returns:
            True jika valid
        """
        if isinstance(certainty, int):
            if certainty < 1 or certainty > 5:
                self.add_error('certainty', 
                              'Certainty (integer) harus antara 1 dan 5')
                return False
            return True
        
        elif isinstance(certainty, float):
            if certainty < 0.0 or certainty > 1.0:
                self.add_error('certainty', 
                              'Certainty (float) harus antara 0.0 dan 1.0')
                return False
            return True
        
        else:
            self.add_error('certainty', 
                          'Certainty harus berupa integer (1-5) atau float (0.0-1.0)')
            return False
    
    # String Validation
    def validate_non_empty_string(self, value: str, field_name: str) -> bool:
        """
        Validasi string tidak kosong
        
        Args:
            value: Nilai string
            field_name: Nama field
            
        Returns:
            True jika valid
        """
        if not isinstance(value, str):
            self.add_error(field_name, f'{field_name} harus berupa string')
            return False
        
        if not value or value.strip() == '':
            self.add_error(field_name, f'{field_name} tidak boleh kosong')
            return False
        
        return True
    
    def validate_string_length(self, 
                              value: str, 
                              field_name: str,
                              min_length: int = 1,
                              max_length: int = 1000) -> bool:
        """
        Validasi panjang string
        
        Args:
            value: Nilai string
            field_name: Nama field
            min_length: Minimum panjang
            max_length: Maximum panjang
            
        Returns:
            True jika valid
        """
        if not self.validate_non_empty_string(value, field_name):
            return False
        
        if len(value) < min_length:
            self.add_error(field_name, 
                          f'{field_name} minimal {min_length} karakter')
            return False
        
        if len(value) > max_length:
            self.add_error(field_name, 
                          f'{field_name} maksimal {max_length} karakter')
            return False
        
        return True
    
    # Session Validation
    def validate_session_id(self, session_id: str) -> bool:
        """
        Validasi session ID
        
        Args:
            session_id: Session ID
            
        Returns:
            True jika valid
        """
        if not session_id:
            self.add_error('session_id', 'Session ID tidak boleh kosong')
            return False
        
        # Format: YYYYMMDD_HHMMSS atau similar
        if not re.match(r'^[A-Za-z0-9_-]+$', session_id):
            self.add_error('session_id', 
                          'Session ID hanya boleh huruf, angka, underscore, dan dash')
            return False
        
        return True


class DataSanitizer:
    """Sanitizer untuk membersihkan input data"""
    
    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        Bersihkan string dari karakter berbahaya
        
        Args:
            value: Input string
            
        Returns:
            Cleaned string
        """
        if not isinstance(value, str):
            return str(value)
        
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # Remove multiple spaces
        value = re.sub(r'\s+', ' ', value)
        
        return value
    
    @staticmethod
    def sanitize_symptom_id(symptom_id: str) -> str:
        """
        Bersihkan symptom ID
        
        Args:
            symptom_id: Symptom ID
            
        Returns:
            Cleaned symptom ID
        """
        # Convert to lowercase
        symptom_id = symptom_id.lower()
        
        # Replace spaces with underscore
        symptom_id = symptom_id.replace(' ', '_')
        
        # Remove non-alphanumeric except underscore
        symptom_id = re.sub(r'[^a-z0-9_]', '', symptom_id)
        
        return symptom_id
    
    @staticmethod
    def sanitize_cf(cf: Any) -> float:
        """
        Normalisasi CF value
        
        Args:
            cf: CF value
            
        Returns:
            Normalized CF (0.0 - 1.0)
        """
        if isinstance(cf, int):
            # Assume 1-5 scale
            if 1 <= cf <= 5:
                return cf / 5.0
        
        if isinstance(cf, float):
            # Clamp to 0-1
            return max(0.0, min(1.0, cf))
        
        return 0.5  # Default


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("INPUT VALIDATOR TEST")
    print("=" * 70)
    
    validator = InputValidator()
    
    # Test 1: Validate symptoms list
    print("\n1. Testing Symptoms Validation")
    print("-" * 70)
    
    valid_symptoms = ['layar_tidak_menyala', 'baterai_cepat_habis']
    validator.reset_errors()
    
    if validator.validate_symptoms_list(valid_symptoms):
        print("✅ Valid symptoms list")
    else:
        print("❌ Validation errors:")
        for error in validator.get_error_messages():
            print(f"   - {error}")
    
    # Test 2: Validate rule structure
    print("\n2. Testing Rule Validation")
    print("-" * 70)
    
    valid_rule = {
        'IF': ['touchscreen_tidak_respons', 'layar_tampil_normal'],
        'THEN': 'kerusakan_digitizer',
        'CF': 0.85
    }
    
    validator.reset_errors()
    if validator.validate_rule_structure(valid_rule):
        print("✅ Valid rule structure")
    else:
        print("❌ Validation errors:")
        for error in validator.get_error_messages():
            print(f"   - {error}")
    
    # Test 3: Validate CF
    print("\n3. Testing CF Validation")
    print("-" * 70)
    
    test_cfs = [0.8, 1.2, -0.5, 0.0, 1.0]
    
    for cf in test_cfs:
        validator.reset_errors()
        if validator.validate_cf(cf):
            print(f"✅ CF {cf} is valid")
        else:
            print(f"❌ CF {cf} is invalid: {validator.get_error_messages()}")
    
    # Test 4: Sanitizer
    print("\n4. Testing Data Sanitizer")
    print("-" * 70)
    
    sanitizer = DataSanitizer()
    
    dirty_string = "  Multiple    Spaces   "
    clean_string = sanitizer.sanitize_string(dirty_string)
    print(f"Original: '{dirty_string}'")
    print(f"Cleaned:  '{clean_string}'")
    
    dirty_symptom = "Layar Tidak Menyala!!!"
    clean_symptom = sanitizer.sanitize_symptom_id(dirty_symptom)
    print(f"\nOriginal: '{dirty_symptom}'")
    print(f"Cleaned:  '{clean_symptom}'")
    
    print("\n" + "=" * 70)