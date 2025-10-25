"""
Knowledge Base Manager
Module untuk mengelola knowledge base (CRUD operations)
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class KnowledgeBaseManager:
    """Manager untuk knowledge base operations"""
    
    def __init__(self, kb_dir: str = "knowledge_base"):
        """
        Initialize KB Manager
        
        Args:
            kb_dir: Directory knowledge base
        """
        self.kb_dir = kb_dir
        self.rules_file = os.path.join(kb_dir, "rules.json")
        self.symptoms_file = os.path.join(kb_dir, "symptoms.json")
        self.diagnoses_file = os.path.join(kb_dir, "diagnoses.json")
        
        self._ensure_kb_dir()
    
    def _ensure_kb_dir(self):
        """Pastikan directory knowledge base ada"""
        if not os.path.exists(self.kb_dir):
            os.makedirs(self.kb_dir)
    
    def _load_json(self, filepath: str) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding {filepath}: {e}")
            return {}
    
    def _save_json(self, filepath: str, data: Dict) -> bool:
        """Save to JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
            return False
    
    # === RULES MANAGEMENT ===
    
    def add_rule(self, rule_id: str, rule_data: Dict) -> bool:
        """
        Tambah rule baru
        
        Args:
            rule_id: ID rule (e.g., "R56")
            rule_data: Data rule dengan keys: IF, THEN, CF, description, source
            
        Returns:
            True jika berhasil
        """
        rules = self._load_json(self.rules_file)
        
        # Validasi
        if not self._validate_rule(rule_data):
            print("Rule validation failed")
            return False
        
        if rule_id in rules.get('rules', {}):
            print(f"Rule {rule_id} already exists")
            return False
        
        # Tambahkan rule
        if 'rules' not in rules:
            rules['rules'] = {}
        
        rules['rules'][rule_id] = {
            'id': rule_id,
            'IF': rule_data.get('IF', []),
            'THEN': rule_data.get('THEN', ''),
            'CF': rule_data.get('CF', 0.8),
            'category': rule_data.get('category', 'general'),
            'description': rule_data.get('description', ''),
            'source': rule_data.get('source', 'User-defined'),
            'created_at': datetime.now().isoformat()
        }
        
        # Update metadata
        if 'metadata' not in rules:
            rules['metadata'] = {}
        rules['metadata']['total_rules'] = len(rules['rules'])
        rules['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.rules_file, rules)
    
    def update_rule(self, rule_id: str, rule_data: Dict) -> bool:
        """
        Update rule existing
        
        Args:
            rule_id: ID rule yang akan diupdate
            rule_data: Data rule baru
            
        Returns:
            True jika berhasil
        """
        rules = self._load_json(self.rules_file)
        
        if rule_id not in rules.get('rules', {}):
            print(f"Rule {rule_id} not found")
            return False
        
        # Validasi
        if not self._validate_rule(rule_data):
            print("Rule validation failed")
            return False
        
        # Update rule (keep original created_at)
        original_created = rules['rules'][rule_id].get('created_at')
        
        rules['rules'][rule_id].update({
            'IF': rule_data.get('IF', []),
            'THEN': rule_data.get('THEN', ''),
            'CF': rule_data.get('CF', 0.8),
            'category': rule_data.get('category', 'general'),
            'description': rule_data.get('description', ''),
            'source': rule_data.get('source', 'User-defined'),
            'updated_at': datetime.now().isoformat()
        })
        
        if original_created:
            rules['rules'][rule_id]['created_at'] = original_created
        
        # Update metadata
        rules['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.rules_file, rules)
    
    def delete_rule(self, rule_id: str) -> bool:
        """
        Hapus rule
        
        Args:
            rule_id: ID rule yang akan dihapus
            
        Returns:
            True jika berhasil
        """
        rules = self._load_json(self.rules_file)
        
        if rule_id not in rules.get('rules', {}):
            print(f"Rule {rule_id} not found")
            return False
        
        del rules['rules'][rule_id]
        
        # Update metadata
        rules['metadata']['total_rules'] = len(rules['rules'])
        rules['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.rules_file, rules)
    
    def get_rule(self, rule_id: str) -> Optional[Dict]:
        """
        Ambil rule berdasarkan ID
        
        Args:
            rule_id: ID rule
            
        Returns:
            Rule data atau None
        """
        rules = self._load_json(self.rules_file)
        return rules.get('rules', {}).get(rule_id)
    
    def get_all_rules(self) -> Dict:
        """Ambil semua rules"""
        rules = self._load_json(self.rules_file)
        return rules.get('rules', {})
    
    def search_rules(self, keyword: str) -> Dict:
        """
        Cari rules berdasarkan keyword
        
        Args:
            keyword: Keyword pencarian
            
        Returns:
            Dictionary rules yang match
        """
        all_rules = self.get_all_rules()
        results = {}
        
        keyword_lower = keyword.lower()
        
        for rule_id, rule_data in all_rules.items():
            # Search in description, THEN, or IF conditions
            if (keyword_lower in rule_data.get('description', '').lower() or
                keyword_lower in rule_data.get('THEN', '').lower() or
                any(keyword_lower in cond.lower() for cond in rule_data.get('IF', []))):
                results[rule_id] = rule_data
        
        return results
    
    def _validate_rule(self, rule_data: Dict) -> bool:
        """
        Validasi rule data
        
        Args:
            rule_data: Data rule
            
        Returns:
            True jika valid
        """
        # Required fields
        if 'IF' not in rule_data or 'THEN' not in rule_data:
            return False
        
        # IF must be list and not empty
        if not isinstance(rule_data['IF'], list) or len(rule_data['IF']) == 0:
            return False
        
        # THEN must be string and not empty
        if not isinstance(rule_data['THEN'], str) or not rule_data['THEN']:
            return False
        
        # CF must be between 0 and 1
        cf = rule_data.get('CF', 0.8)
        if not isinstance(cf, (int, float)) or cf < 0 or cf > 1:
            return False
        
        return True
    
    # === SYMPTOMS MANAGEMENT ===
    
    def add_symptom(self, symptom_id: str, symptom_data: Dict) -> bool:
        """
        Tambah symptom baru
        
        Args:
            symptom_id: ID symptom
            symptom_data: Data symptom
            
        Returns:
            True jika berhasil
        """
        symptoms = self._load_json(self.symptoms_file)
        
        if symptom_id in symptoms.get('symptoms', {}):
            print(f"Symptom {symptom_id} already exists")
            return False
        
        if 'symptoms' not in symptoms:
            symptoms['symptoms'] = {}
        
        symptoms['symptoms'][symptom_id] = {
            'id': symptom_id,
            'name': symptom_data.get('name', ''),
            'category': symptom_data.get('category', 'general'),
            'description': symptom_data.get('description', ''),
            'severity': symptom_data.get('severity', 'medium'),
            'question': symptom_data.get('question', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Update metadata
        if 'metadata' not in symptoms:
            symptoms['metadata'] = {}
        symptoms['metadata']['total_symptoms'] = len(symptoms['symptoms'])
        symptoms['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.symptoms_file, symptoms)
    
    def update_symptom(self, symptom_id: str, symptom_data: Dict) -> bool:
        """Update symptom existing"""
        symptoms = self._load_json(self.symptoms_file)
        
        if symptom_id not in symptoms.get('symptoms', {}):
            print(f"Symptom {symptom_id} not found")
            return False
        
        original_created = symptoms['symptoms'][symptom_id].get('created_at')
        
        symptoms['symptoms'][symptom_id].update({
            'name': symptom_data.get('name', ''),
            'category': symptom_data.get('category', 'general'),
            'description': symptom_data.get('description', ''),
            'severity': symptom_data.get('severity', 'medium'),
            'question': symptom_data.get('question', ''),
            'updated_at': datetime.now().isoformat()
        })
        
        if original_created:
            symptoms['symptoms'][symptom_id]['created_at'] = original_created
        
        symptoms['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.symptoms_file, symptoms)
    
    def delete_symptom(self, symptom_id: str) -> bool:
        """Hapus symptom"""
        symptoms = self._load_json(self.symptoms_file)
        
        if symptom_id not in symptoms.get('symptoms', {}):
            print(f"Symptom {symptom_id} not found")
            return False
        
        del symptoms['symptoms'][symptom_id]
        
        symptoms['metadata']['total_symptoms'] = len(symptoms['symptoms'])
        symptoms['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.symptoms_file, symptoms)
    
    def get_symptom(self, symptom_id: str) -> Optional[Dict]:
        """Ambil symptom berdasarkan ID"""
        symptoms = self._load_json(self.symptoms_file)
        return symptoms.get('symptoms', {}).get(symptom_id)
    
    def get_all_symptoms(self) -> Dict:
        """Ambil semua symptoms"""
        symptoms = self._load_json(self.symptoms_file)
        return symptoms.get('symptoms', {})
    
    def get_symptoms_by_category(self, category: str) -> Dict:
        """Ambil symptoms berdasarkan kategori"""
        all_symptoms = self.get_all_symptoms()
        return {k: v for k, v in all_symptoms.items() if v.get('category') == category}
    
    # === DIAGNOSES MANAGEMENT ===
    
    def add_diagnosis(self, diagnosis_id: str, diagnosis_data: Dict) -> bool:
        """Tambah diagnosis baru"""
        diagnoses = self._load_json(self.diagnoses_file)
        
        if diagnosis_id in diagnoses.get('diagnoses', {}):
            print(f"Diagnosis {diagnosis_id} already exists")
            return False
        
        if 'diagnoses' not in diagnoses:
            diagnoses['diagnoses'] = {}
        
        diagnoses['diagnoses'][diagnosis_id] = {
            'id': diagnosis_id,
            'name': diagnosis_data.get('name', ''),
            'type': diagnosis_data.get('type', 'hardware'),
            'severity': diagnosis_data.get('severity', 'medium'),
            'description': diagnosis_data.get('description', ''),
            'causes': diagnosis_data.get('causes', []),
            'solutions': diagnosis_data.get('solutions', []),
            'prevention': diagnosis_data.get('prevention', []),
            'estimated_cost': diagnosis_data.get('estimated_cost', '0'),
            'repair_difficulty': diagnosis_data.get('repair_difficulty', 'medium'),
            'source': diagnosis_data.get('source', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Update metadata
        if 'metadata' not in diagnoses:
            diagnoses['metadata'] = {}
        diagnoses['metadata']['total_diagnoses'] = len(diagnoses['diagnoses'])
        diagnoses['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.diagnoses_file, diagnoses)
    
    def update_diagnosis(self, diagnosis_id: str, diagnosis_data: Dict) -> bool:
        """Update diagnosis existing"""
        diagnoses = self._load_json(self.diagnoses_file)
        
        if diagnosis_id not in diagnoses.get('diagnoses', {}):
            print(f"Diagnosis {diagnosis_id} not found")
            return False
        
        original_created = diagnoses['diagnoses'][diagnosis_id].get('created_at')
        
        diagnoses['diagnoses'][diagnosis_id].update({
            'name': diagnosis_data.get('name', ''),
            'type': diagnosis_data.get('type', 'hardware'),
            'severity': diagnosis_data.get('severity', 'medium'),
            'description': diagnosis_data.get('description', ''),
            'causes': diagnosis_data.get('causes', []),
            'solutions': diagnosis_data.get('solutions', []),
            'prevention': diagnosis_data.get('prevention', []),
            'estimated_cost': diagnosis_data.get('estimated_cost', '0'),
            'repair_difficulty': diagnosis_data.get('repair_difficulty', 'medium'),
            'source': diagnosis_data.get('source', ''),
            'updated_at': datetime.now().isoformat()
        })
        
        if original_created:
            diagnoses['diagnoses'][diagnosis_id]['created_at'] = original_created
        
        diagnoses['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.diagnoses_file, diagnoses)
    
    def delete_diagnosis(self, diagnosis_id: str) -> bool:
        """Hapus diagnosis"""
        diagnoses = self._load_json(self.diagnoses_file)
        
        if diagnosis_id not in diagnoses.get('diagnoses', {}):
            print(f"Diagnosis {diagnosis_id} not found")
            return False
        
        del diagnoses['diagnoses'][diagnosis_id]
        
        diagnoses['metadata']['total_diagnoses'] = len(diagnoses['diagnoses'])
        diagnoses['metadata']['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.diagnoses_file, diagnoses)
    
    def get_diagnosis(self, diagnosis_id: str) -> Optional[Dict]:
        """Ambil diagnosis berdasarkan ID"""
        diagnoses = self._load_json(self.diagnoses_file)
        return diagnoses.get('diagnoses', {}).get(diagnosis_id)
    
    def get_all_diagnoses(self) -> Dict:
        """Ambil semua diagnoses"""
        diagnoses = self._load_json(self.diagnoses_file)
        return diagnoses.get('diagnoses', {})
    
    def get_diagnoses_by_type(self, diagnosis_type: str) -> Dict:
        """Ambil diagnoses berdasarkan tipe (hardware/software)"""
        all_diagnoses = self.get_all_diagnoses()
        return {k: v for k, v in all_diagnoses.items() if v.get('type') == diagnosis_type}
    
    # === STATISTICS ===
    
    def get_statistics(self) -> Dict:
        """Dapatkan statistik knowledge base"""
        rules = self._load_json(self.rules_file)
        symptoms = self._load_json(self.symptoms_file)
        diagnoses = self._load_json(self.diagnoses_file)
        
        # Count by category
        rule_categories = {}
        symptom_categories = {}
        diagnosis_types = {}
        
        for rule in rules.get('rules', {}).values():
            cat = rule.get('category', 'general')
            rule_categories[cat] = rule_categories.get(cat, 0) + 1
        
        for symptom in symptoms.get('symptoms', {}).values():
            cat = symptom.get('category', 'general')
            symptom_categories[cat] = symptom_categories.get(cat, 0) + 1
        
        for diagnosis in diagnoses.get('diagnoses', {}).values():
            dtype = diagnosis.get('type', 'unknown')
            diagnosis_types[dtype] = diagnosis_types.get(dtype, 0) + 1
        
        return {
            'total_rules': len(rules.get('rules', {})),
            'total_symptoms': len(symptoms.get('symptoms', {})),
            'total_diagnoses': len(diagnoses.get('diagnoses', {})),
            'rule_categories': rule_categories,
            'symptom_categories': symptom_categories,
            'diagnosis_types': diagnosis_types,
            'last_updated': {
                'rules': rules.get('metadata', {}).get('last_updated', 'N/A'),
                'symptoms': symptoms.get('metadata', {}).get('last_updated', 'N/A'),
                'diagnoses': diagnoses.get('metadata', {}).get('last_updated', 'N/A')
            }
        }
    
    # === EXPORT/IMPORT ===
    
    def export_knowledge_base(self, output_file: str) -> bool:
        """
        Export seluruh knowledge base ke satu file
        
        Args:
            output_file: Path file output
            
        Returns:
            True jika berhasil
        """
        try:
            kb = {
                'rules': self._load_json(self.rules_file),
                'symptoms': self._load_json(self.symptoms_file),
                'diagnoses': self._load_json(self.diagnoses_file),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(kb, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting KB: {e}")
            return False
    
    def import_knowledge_base(self, input_file: str) -> bool:
        """
        Import knowledge base dari file
        
        Args:
            input_file: Path file input
            
        Returns:
            True jika berhasil
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            
            # Save each component
            if 'rules' in kb:
                self._save_json(self.rules_file, kb['rules'])
            if 'symptoms' in kb:
                self._save_json(self.symptoms_file, kb['symptoms'])
            if 'diagnoses' in kb:
                self._save_json(self.diagnoses_file, kb['diagnoses'])
            
            return True
        except Exception as e:
            print(f"Error importing KB: {e}")
            return False


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("KNOWLEDGE BASE MANAGER - TEST")
    print("=" * 70)
    
    manager = KnowledgeBaseManager()
    
    # Test: Add new rule
    print("\n1. Testing Add Rule...")
    new_rule = {
        'IF': ['test_symptom_1', 'test_symptom_2'],
        'THEN': 'test_diagnosis',
        'CF': 0.85,
        'category': 'test',
        'description': 'This is a test rule',
        'source': 'Test Case'
    }
    
    success = manager.add_rule('R_TEST', new_rule)
    print(f"Add rule: {'SUCCESS' if success else 'FAILED'}")
    
    # Test: Get rule
    print("\n2. Testing Get Rule...")
    rule = manager.get_rule('R_TEST')
    if rule:
        print(f"Retrieved rule: {rule['id']} - {rule['description']}")
    
    # Test: Update rule
    print("\n3. Testing Update Rule...")
    updated_rule = new_rule.copy()
    updated_rule['description'] = 'Updated test rule'
    success = manager.update_rule('R_TEST', updated_rule)
    print(f"Update rule: {'SUCCESS' if success else 'FAILED'}")
    
    # Test: Statistics
    print("\n4. Testing Statistics...")
    stats = manager.get_statistics()
    print(f"Total Rules: {stats['total_rules']}")
    print(f"Total Symptoms: {stats['total_symptoms']}")
    print(f"Total Diagnoses: {stats['total_diagnoses']}")
    
    # Test: Delete rule
    print("\n5. Testing Delete Rule...")
    success = manager.delete_rule('R_TEST')
    print(f"Delete rule: {'SUCCESS' if success else 'FAILED'}")
    
    print("\n" + "=" * 70)