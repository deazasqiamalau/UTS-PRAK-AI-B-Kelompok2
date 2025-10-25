"""
Test Cases untuk Sistem Pakar Smartphone
Comprehensive testing untuk semua komponen
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from inference_engine.forward_chaining import ForwardChaining
from inference_engine.certainty_factor import CFCalculator
from datetime import datetime
import json


class Color:
    """ANSI color codes untuk output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class TestRunner:
    """Test runner untuk sistem pakar"""
    
    def __init__(self):
        """Initialize test runner"""
        self.engine = ForwardChaining()
        self.cf_calculator = CFCalculator()
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, 
                 test_name: str, 
                 symptoms: list, 
                 expected_diagnosis: str,
                 expected_cf_min: float = 0.7):
        """
        Jalankan satu test case
        
        Args:
            test_name: Nama test case
            symptoms: List of symptoms
            expected_diagnosis: Diagnosis yang diharapkan
            expected_cf_min: Minimum CF yang diharapkan
        """
        print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
        print(f"{Color.BOLD}TEST: {test_name}{Color.RESET}")
        print(f"{Color.BOLD}{'='*70}{Color.RESET}")
        
        # Reset engine
        self.engine.reset()
        
        # Add symptoms
        self.engine.add_facts(symptoms)
        print(f"\n{Color.BLUE}Input Gejala ({len(symptoms)}):{Color.RESET}")
        for symptom in symptoms:
            print(f"  - {symptom}")
        
        # Run inference
        start_time = datetime.now()
        results = self.engine.forward_chain()
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        # Get diagnoses
        diagnoses = results['final_diagnoses']
        
        print(f"\n{Color.BLUE}Hasil Inferensi:{Color.RESET}")
        print(f"  Iterasi: {results['iterations']}")
        print(f"  Rules fired: {len(results['fired_rules'])}")
        print(f"  Response time: {response_time:.3f}s")
        
        # Display diagnoses
        print(f"\n{Color.BLUE}Diagnosis:{Color.RESET}")
        if diagnoses:
            for i, diag in enumerate(diagnoses[:3], 1):
                print(f"  {i}. {diag['diagnosis']}")
                print(f"     Confidence: {diag['percentage']:.1f}%")
        else:
            print(f"  {Color.YELLOW}Tidak ada diagnosis ditemukan{Color.RESET}")
        
        # Validation
        passed = False
        reason = ""
        
        if not diagnoses:
            reason = "Tidak ada diagnosis yang ditemukan"
        elif expected_diagnosis not in [d['diagnosis'] for d in diagnoses]:
            reason = f"Expected diagnosis '{expected_diagnosis}' tidak ditemukan"
        else:
            # Check CF
            found_diag = next(d for d in diagnoses if d['diagnosis'] == expected_diagnosis)
            if found_diag['confidence'] < expected_cf_min:
                reason = f"CF terlalu rendah: {found_diag['confidence']:.2f} < {expected_cf_min}"
            else:
                passed = True
                reason = "All checks passed"
        
        # Print result
        if passed:
            print(f"\n{Color.GREEN}✅ TEST PASSED{Color.RESET}")
            self.passed += 1
        else:
            print(f"\n{Color.RED}❌ TEST FAILED{Color.RESET}")
            print(f"{Color.RED}Reason: {reason}{Color.RESET}")
            self.failed += 1
        
        # Store result
        self.test_results.append({
            'name': test_name,
            'passed': passed,
            'reason': reason,
            'symptoms_count': len(symptoms),
            'diagnoses_count': len(diagnoses),
            'response_time': response_time,
            'top_diagnosis': diagnoses[0]['diagnosis'] if diagnoses else None,
            'top_confidence': diagnoses[0]['confidence'] if diagnoses else 0
        })
        
        return passed
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
        print(f"{Color.BOLD}TEST SUMMARY{Color.RESET}")
        print(f"{Color.BOLD}{'='*70}{Color.RESET}")
        
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\nTotal Tests: {total}")
        print(f"{Color.GREEN}Passed: {self.passed}{Color.RESET}")
        print(f"{Color.RED}Failed: {self.failed}{Color.RESET}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Calculate average response time
        avg_response = sum(r['response_time'] for r in self.test_results) / len(self.test_results)
        print(f"Average Response Time: {avg_response:.3f}s")
        
        # Detailed results
        print(f"\n{Color.BOLD}Detailed Results:{Color.RESET}")
        for i, result in enumerate(self.test_results, 1):
            status = f"{Color.GREEN}✅ PASS{Color.RESET}" if result['passed'] else f"{Color.RED}❌ FAIL{Color.RESET}"
            print(f"\n{i}. {result['name']}")
            print(f"   Status: {status}")
            print(f"   Top Diagnosis: {result['top_diagnosis']}")
            print(f"   Confidence: {result['top_confidence']*100:.1f}%")
            print(f"   Response Time: {result['response_time']:.3f}s")
            if not result['passed']:
                print(f"   {Color.RED}Reason: {result['reason']}{Color.RESET}")


def run_all_tests():
    """Jalankan semua test cases"""
    
    runner = TestRunner()
    
    print(f"\n{Color.BOLD}{Color.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║    SISTEM PAKAR SMARTPHONE - COMPREHENSIVE TEST SUITE             ║")
    print("║    Kelompok 2 - INF313 Kecerdasan Artifisial                     ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}")
    
    # TEST CASE 1: Touchscreen Tidak Merespons
    runner.run_test(
        test_name="TC1 - Touchscreen Tidak Merespons",
        symptoms=[
            'touchscreen_tidak_respons',
            'layar_tampil_normal',
            'tombol_fisik_berfungsi'
        ],
        expected_diagnosis='kerusakan_touchscreen_digitizer',
        expected_cf_min=0.80
    )
    
    # TEST CASE 2: Baterai Cepat Habis (Degradasi)
    runner.run_test(
        test_name="TC2 - Baterai Cepat Habis (Degradasi)",
        symptoms=[
            'baterai_cepat_habis',
            'smartphone_terasa_panas',
            'baterai_berumur_lebih_2tahun'
        ],
        expected_diagnosis='degradasi_baterai',
        expected_cf_min=0.85
    )
    
    # TEST CASE 3: Aplikasi Force Close
    runner.run_test(
        test_name="TC3 - Aplikasi Force Close (RAM Penuh)",
        symptoms=[
            'aplikasi_force_close',
            'terjadi_pada_semua_aplikasi',
            'smartphone_lemot'
        ],
        expected_diagnosis='kemungkinan_ram_penuh',
        expected_cf_min=0.70
    )
    
    # TEST CASE 4: Tidak Bisa Charging
    runner.run_test(
        test_name="TC4 - Tidak Bisa Charging (Port USB Rusak)",
        symptoms=[
            'tidak_bisa_charging',
            'kabel_data_berfungsi',
            'charger_berfungsi'
        ],
        expected_diagnosis='kerusakan_port_usb',
        expected_cf_min=0.80
    )
    
    # TEST CASE 5: Smartphone Overheat
    runner.run_test(
        test_name="TC5 - Smartphone Overheat (Idle)",
        symptoms=[
            'smartphone_overheat',
            'saat_idle',
            'baterai_cepat_habis'
        ],
        expected_diagnosis='proses_background_berlebihan',
        expected_cf_min=0.70
    )
    
    # TEST CASE 6: Layar Tidak Menyala (Backlight)
    runner.run_test(
        test_name="TC6 - Layar Tidak Menyala (Backlight Rusak)",
        symptoms=[
            'layar_tidak_menyala',
            'tombol_power_berfungsi',
            'led_notifikasi_menyala'
        ],
        expected_diagnosis='kerusakan_lcd_backlight',
        expected_cf_min=0.85
    )
    
    # TEST CASE 7: Charging Lambat
    runner.run_test(
        test_name="TC7 - Charging Lambat",
        symptoms=[
            'charging_lambat',
            'kabel_terkoneksi_normal',
            'smartphone_panas_saat_charging'
        ],
        expected_diagnosis='kemungkinan_charger_tidak_sesuai',
        expected_cf_min=0.65
    )
    
    # TEST CASE 8: Baterai Kembung (CRITICAL)
    runner.run_test(
        test_name="TC8 - Baterai Kembung (BAHAYA)",
        symptoms=[
            'baterai_kembung',
            'casing_terangkat',
            'baterai_cepat_habis'
        ],
        expected_diagnosis='baterai_rusak_berbahaya',
        expected_cf_min=0.95
    )
    
    # TEST CASE 9: Storage Penuh
    runner.run_test(
        test_name="TC9 - Smartphone Lemot (Storage Penuh)",
        symptoms=[
            'smartphone_lemot',
            'storage_hampir_penuh',
            'aplikasi_force_close'
        ],
        expected_diagnosis='storage_penuh_masalah',
        expected_cf_min=0.80
    )
    
    # TEST CASE 10: Layar Bergaris
    runner.run_test(
        test_name="TC10 - Layar Bergaris (LCD Panel Rusak)",
        symptoms=[
            'layar_bergaris',
            'warna_tidak_normal',
            'layar_retak'
        ],
        expected_diagnosis='kerusakan_lcd_panel',
        expected_cf_min=0.80
    )
    
    # Print final summary
    runner.print_summary()
    
    return runner


def test_certainty_factor():
    """Test certainty factor calculations"""
    
    print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
    print(f"{Color.BOLD}CERTAINTY FACTOR TEST{Color.RESET}")
    print(f"{Color.BOLD}{'='*70}{Color.RESET}")
    
    calculator = CFCalculator()
    
    # Test Case 1: Single evidence
    print(f"\n{Color.BLUE}Test 1: Single Evidence{Color.RESET}")
    evidences1 = [
        {'id': 'E1', 'rule_cf': 0.8, 'user_cf': 1.0}
    ]
    
    result1 = calculator.calculate_and_track('test_diagnosis_1', evidences1)
    print(f"CF Final: {result1['final_cf']:.3f}")
    print(f"Percentage: {result1['percentage']:.1f}%")
    print(f"Category: {result1['category']}")
    
    # Test Case 2: Multiple evidences
    print(f"\n{Color.BLUE}Test 2: Multiple Evidences{Color.RESET}")
    evidences2 = [
        {'id': 'E1', 'rule_cf': 0.7, 'user_cf': 1.0},
        {'id': 'E2', 'rule_cf': 0.8, 'user_cf': 0.9},
        {'id': 'E3', 'rule_cf': 0.9, 'user_cf': 1.0}
    ]
    
    result2 = calculator.calculate_and_track('test_diagnosis_2', evidences2)
    print(f"CF Final: {result2['final_cf']:.3f}")
    print(f"Percentage: {result2['percentage']:.1f}%")
    print(f"Category: {result2['category']}")
    
    print(f"\n{Color.BLUE}Calculation Steps:{Color.RESET}")
    for step in result2['calculation_steps']:
        print(f"  {step}")
    
    # Test Case 3: Low confidence
    print(f"\n{Color.BLUE}Test 3: Low Confidence{Color.RESET}")
    evidences3 = [
        {'id': 'E1', 'rule_cf': 0.4, 'user_cf': 0.5}
    ]
    
    result3 = calculator.calculate_and_track('test_diagnosis_3', evidences3)
    print(f"CF Final: {result3['final_cf']:.3f}")
    print(f"Percentage: {result3['percentage']:.1f}%")
    print(f"Category: {result3['category']}")
    
    print(f"\n{Color.GREEN}✅ Certainty Factor tests completed{Color.RESET}")


def test_knowledge_base_integrity():
    """Test knowledge base integrity"""
    
    print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
    print(f"{Color.BOLD}KNOWLEDGE BASE INTEGRITY TEST{Color.RESET}")
    print(f"{Color.BOLD}{'='*70}{Color.RESET}")
    
    # Load KB files
    kb_files = {
        'rules': 'knowledge_base/rules.json',
        'symptoms': 'knowledge_base/symptoms.json',
        'diagnoses': 'knowledge_base/diagnoses.json'
    }
    
    all_valid = True
    
    for name, filepath in kb_files.items():
        print(f"\n{Color.BLUE}Testing {name}.json{Color.RESET}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure
            if name == 'rules':
                if 'rules' not in data:
                    print(f"{Color.RED}❌ Missing 'rules' key{Color.RESET}")
                    all_valid = False
                else:
                    rules_count = len(data['rules'])
                    print(f"{Color.GREEN}✅ Valid structure{Color.RESET}")
                    print(f"   Total rules: {rules_count}")
                    
                    # Check each rule
                    invalid_rules = []
                    for rule_id, rule in data['rules'].items():
                        if 'IF' not in rule or 'THEN' not in rule:
                            invalid_rules.append(rule_id)
                    
                    if invalid_rules:
                        print(f"{Color.YELLOW}⚠️  Invalid rules: {', '.join(invalid_rules)}{Color.RESET}")
                        all_valid = False
                    else:
                        print(f"{Color.GREEN}✅ All rules valid{Color.RESET}")
            
            elif name == 'symptoms':
                if 'symptoms' not in data:
                    print(f"{Color.RED}❌ Missing 'symptoms' key{Color.RESET}")
                    all_valid = False
                else:
                    symptoms_count = len(data['symptoms'])
                    print(f"{Color.GREEN}✅ Valid structure{Color.RESET}")
                    print(f"   Total symptoms: {symptoms_count}")
            
            elif name == 'diagnoses':
                if 'diagnoses' not in data:
                    print(f"{Color.RED}❌ Missing 'diagnoses' key{Color.RESET}")
                    all_valid = False
                else:
                    diagnoses_count = len(data['diagnoses'])
                    print(f"{Color.GREEN}✅ Valid structure{Color.RESET}")
                    print(f"   Total diagnoses: {diagnoses_count}")
        
        except FileNotFoundError:
            print(f"{Color.RED}❌ File not found: {filepath}{Color.RESET}")
            all_valid = False
        except json.JSONDecodeError as e:
            print(f"{Color.RED}❌ Invalid JSON: {str(e)}{Color.RESET}")
            all_valid = False
        except Exception as e:
            print(f"{Color.RED}❌ Error: {str(e)}{Color.RESET}")
            all_valid = False
    
    if all_valid:
        print(f"\n{Color.GREEN}✅ All knowledge base files are valid{Color.RESET}")
    else:
        print(f"\n{Color.RED}❌ Some knowledge base files have issues{Color.RESET}")
    
    return all_valid


def test_performance():
    """Test performance metrics"""
    
    print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
    print(f"{Color.BOLD}PERFORMANCE TEST{Color.RESET}")
    print(f"{Color.BOLD}{'='*70}{Color.RESET}")
    
    engine = ForwardChaining()
    
    # Test with varying number of symptoms
    test_cases = [
        (3, ['touchscreen_tidak_respons', 'layar_tampil_normal', 'tombol_fisik_berfungsi']),
        (5, ['baterai_cepat_habis', 'smartphone_terasa_panas', 'baterai_berumur_lebih_2tahun', 
             'smartphone_lemot', 'aplikasi_force_close']),
        (8, ['layar_tidak_menyala', 'baterai_cepat_habis', 'charging_lambat',
             'smartphone_overheat', 'aplikasi_force_close', 'storage_hampir_penuh',
             'touchscreen_ghost_touch', 'restart_sendiri'])
    ]
    
    print(f"\n{Color.BLUE}Testing response time with varying symptoms:{Color.RESET}")
    
    for symptom_count, symptoms in test_cases:
        engine.reset()
        engine.add_facts(symptoms)
        
        start_time = datetime.now()
        results = engine.forward_chain()
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        print(f"\n  Symptoms: {symptom_count}")
        print(f"  Response Time: {response_time:.3f}s")
        print(f"  Iterations: {results['iterations']}")
        print(f"  Rules Fired: {len(results['fired_rules'])}")
        print(f"  Diagnoses: {len(results['final_diagnoses'])}")
        
        # Performance criteria
        if response_time < 1.0:
            print(f"  {Color.GREEN}✅ Excellent performance (< 1s){Color.RESET}")
        elif response_time < 2.0:
            print(f"  {Color.GREEN}✅ Good performance (< 2s){Color.RESET}")
        elif response_time < 3.0:
            print(f"  {Color.YELLOW}⚠️  Acceptable performance (< 3s){Color.RESET}")
        else:
            print(f"  {Color.RED}❌ Poor performance (>= 3s){Color.RESET}")


def test_edge_cases():
    """Test edge cases and error handling"""
    
    print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
    print(f"{Color.BOLD}EDGE CASES TEST{Color.RESET}")
    print(f"{Color.BOLD}{'='*70}{Color.RESET}")
    
    engine = ForwardChaining()
    
    # Test 1: Empty symptoms
    print(f"\n{Color.BLUE}Test 1: Empty Symptoms{Color.RESET}")
    engine.reset()
    results = engine.forward_chain()
    
    if len(results['final_diagnoses']) == 0:
        print(f"{Color.GREEN}✅ Correctly handled empty symptoms{Color.RESET}")
    else:
        print(f"{Color.RED}❌ Should not return diagnoses with no symptoms{Color.RESET}")
    
    # Test 2: Single symptom
    print(f"\n{Color.BLUE}Test 2: Single Symptom{Color.RESET}")
    engine.reset()
    engine.add_facts(['layar_tidak_menyala'])
    results = engine.forward_chain()
    
    print(f"  Diagnoses found: {len(results['final_diagnoses'])}")
    if results['final_diagnoses']:
        print(f"  Top diagnosis: {results['final_diagnoses'][0]['diagnosis']}")
    print(f"{Color.GREEN}✅ Handled single symptom{Color.RESET}")
    
    # Test 3: Conflicting symptoms
    print(f"\n{Color.BLUE}Test 3: Potentially Conflicting Symptoms{Color.RESET}")
    engine.reset()
    conflicting_symptoms = [
        'smartphone_berumur_kurang_1tahun',
        'baterai_berumur_lebih_2tahun'  # Contradiction
    ]
    engine.add_facts(conflicting_symptoms)
    results = engine.forward_chain()
    
    print(f"  System handled conflicting symptoms")
    print(f"  Diagnoses: {len(results['final_diagnoses'])}")
    print(f"{Color.GREEN}✅ No crash on conflicting symptoms{Color.RESET}")
    
    # Test 4: Maximum symptoms
    print(f"\n{Color.BLUE}Test 4: Many Symptoms (15+){Color.RESET}")
    engine.reset()
    many_symptoms = [
        'layar_tidak_menyala', 'baterai_cepat_habis', 'charging_lambat',
        'smartphone_overheat', 'aplikasi_force_close', 'touchscreen_ghost_touch',
        'smartphone_lemot', 'restart_sendiri', 'storage_hampir_penuh',
        'speaker_tidak_bunyi', 'layar_bergaris', 'warna_tidak_normal',
        'baterai_kembung', 'port_goyang', 'smartphone_terasa_panas'
    ]
    engine.add_facts(many_symptoms)
    
    start_time = datetime.now()
    results = engine.forward_chain()
    end_time = datetime.now()
    
    response_time = (end_time - start_time).total_seconds()
    
    print(f"  Total symptoms: {len(many_symptoms)}")
    print(f"  Response time: {response_time:.3f}s")
    print(f"  Diagnoses: {len(results['final_diagnoses'])}")
    
    if response_time < 3.0:
        print(f"{Color.GREEN}✅ Good performance with many symptoms{Color.RESET}")
    else:
        print(f"{Color.YELLOW}⚠️  Slow performance with many symptoms{Color.RESET}")


def generate_test_report(runner):
    """Generate comprehensive test report"""
    
    report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("SISTEM PAKAR SMARTPHONE - TEST REPORT\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Tests: {len(runner.test_results)}\n")
        f.write(f"Passed: {runner.passed}\n")
        f.write(f"Failed: {runner.failed}\n")
        
        success_rate = (runner.passed / len(runner.test_results) * 100) if runner.test_results else 0
        f.write(f"Success Rate: {success_rate:.1f}%\n\n")
        
        f.write("="*70 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("="*70 + "\n\n")
        
        for i, result in enumerate(runner.test_results, 1):
            f.write(f"\nTest {i}: {result['name']}\n")
            f.write(f"Status: {'PASS' if result['passed'] else 'FAIL'}\n")
            f.write(f"Symptoms: {result['symptoms_count']}\n")
            f.write(f"Top Diagnosis: {result['top_diagnosis']}\n")
            f.write(f"Confidence: {result['top_confidence']*100:.1f}%\n")
            f.write(f"Response Time: {result['response_time']:.3f}s\n")
            
            if not result['passed']:
                f.write(f"Failure Reason: {result['reason']}\n")
            
            f.write("-"*70 + "\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")
    
    print(f"\n{Color.GREEN}📄 Test report saved to: {report_filename}{Color.RESET}")


# Main execution
if __name__ == "__main__":
    print(f"\n{Color.BOLD}{Color.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║      SISTEM PAKAR IDENTIFIKASI KERUSAKAN SMARTPHONE              ║")
    print("║              COMPREHENSIVE TEST SUITE                            ║")
    print("║                                                                   ║")
    print("║      Kelompok 2 - INF313 Kecerdasan Artifisial                  ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}\n")
    
    try:
        # Run all test suites
        print(f"{Color.BOLD}Starting test execution...{Color.RESET}\n")
        
        # 1. Knowledge Base Integrity
        print(f"\n{Color.BOLD}[1/5] Knowledge Base Integrity Test{Color.RESET}")
        kb_valid = test_knowledge_base_integrity()
        
        if not kb_valid:
            print(f"\n{Color.RED}⚠️  Knowledge base has issues. Please fix before continuing.{Color.RESET}")
            sys.exit(1)
        
        # 2. Main Test Cases
        print(f"\n{Color.BOLD}[2/5] Main Diagnosis Test Cases{Color.RESET}")
        runner = run_all_tests()
        
        # 3. Certainty Factor Tests
        print(f"\n{Color.BOLD}[3/5] Certainty Factor Tests{Color.RESET}")
        test_certainty_factor()
        
        # 4. Performance Tests
        print(f"\n{Color.BOLD}[4/5] Performance Tests{Color.RESET}")
        test_performance()
        
        # 5. Edge Cases
        print(f"\n{Color.BOLD}[5/5] Edge Cases Tests{Color.RESET}")
        test_edge_cases()
        
        # Generate report
        generate_test_report(runner)
        
        # Final summary
        print(f"\n{Color.BOLD}{'='*70}{Color.RESET}")
        print(f"{Color.BOLD}OVERALL TEST RESULTS{Color.RESET}")
        print(f"{Color.BOLD}{'='*70}{Color.RESET}")
        
        if runner.failed == 0:
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 ALL TESTS PASSED! 🎉{Color.RESET}")
            print(f"{Color.GREEN}The system is working correctly.{Color.RESET}")
        else:
            print(f"\n{Color.YELLOW}⚠️  SOME TESTS FAILED{Color.RESET}")
            print(f"{Color.YELLOW}Please review the test report for details.{Color.RESET}")
        
        print(f"\n{Color.BOLD}Test execution completed successfully.{Color.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Test execution interrupted by user.{Color.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Color.RED}Error during test execution: {str(e)}{Color.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)