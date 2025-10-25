"""
Logging System
Advanced logging untuk sistem pakar smartphone
"""

import logging
import os
from datetime import datetime
from pathlib import Path
import json


class SmartphoneExpertLogger:
    """Advanced logger untuk sistem pakar"""
    
    def __init__(self, name: str = 'smartphone_expert', log_dir: str = 'logs'):
        """
        Initialize logger
        
        Args:
            name: Logger name
            log_dir: Directory untuk log files
        """
        self.name = name
        self.log_dir = log_dir
        self._ensure_log_dir()
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
        
        # Session info
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.session_log_file = os.path.join(
            log_dir, 
            f'session_{self.session_id}.json'
        )
        self.session_events = []
    
    def _ensure_log_dir(self):
        """Pastikan directory log ada"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _setup_handlers(self):
        """Setup logging handlers"""
        
        # File Handler - All levels
        all_log_file = os.path.join(self.log_dir, 'system.log')
        file_handler = logging.FileHandler(all_log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # File Handler - Error only
        error_log_file = os.path.join(self.log_dir, 'errors.log')
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
    
    # Basic logging methods
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message)
        self._log_session_event('DEBUG', message, kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message)
        self._log_session_event('INFO', message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message)
        self._log_session_event('WARNING', message, kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message)
        self._log_session_event('ERROR', message, kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message)
        self._log_session_event('CRITICAL', message, kwargs)
    
    # Domain-specific logging methods
    def log_diagnosis_start(self, symptoms: list):
        """Log start of diagnosis"""
        message = f"Diagnosis started with {len(symptoms)} symptoms"
        self.info(message, symptoms=symptoms)
        
        self._log_session_event('DIAGNOSIS_START', message, {
            'symptoms': symptoms,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_diagnosis_result(self, diagnosis: str, confidence: float):
        """Log diagnosis result"""
        message = f"Diagnosis: {diagnosis} (CF: {confidence:.2f})"
        self.info(message)
        
        self._log_session_event('DIAGNOSIS_RESULT', message, {
            'diagnosis': diagnosis,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_rule_fired(self, rule_id: str, conditions: list, conclusion: str):
        """Log when a rule is fired"""
        message = f"Rule fired: {rule_id} -> {conclusion}"
        self.debug(message)
        
        self._log_session_event('RULE_FIRED', message, {
            'rule_id': rule_id,
            'conditions': conditions,
            'conclusion': conclusion,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_inference_iteration(self, iteration: int, facts_count: int):
        """Log inference iteration"""
        message = f"Iteration {iteration}: {facts_count} facts"
        self.debug(message)
        
        self._log_session_event('INFERENCE_ITERATION', message, {
            'iteration': iteration,
            'facts_count': facts_count,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_kb_operation(self, operation: str, target: str, success: bool):
        """Log knowledge base operation"""
        status = "SUCCESS" if success else "FAILED"
        message = f"KB Operation {operation} on {target}: {status}"
        
        if success:
            self.info(message)
        else:
            self.warning(message)
        
        self._log_session_event('KB_OPERATION', message, {
            'operation': operation,
            'target': target,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_user_action(self, action: str, details: dict = None):
        """Log user action"""
        message = f"User action: {action}"
        self.info(message)
        
        self._log_session_event('USER_ACTION', message, {
            'action': action,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        })
    
    def log_error_with_traceback(self, error: Exception, context: str = ""):
        """Log error with full traceback"""
        import traceback
        
        message = f"Error in {context}: {str(error)}"
        self.error(message)
        
        tb = traceback.format_exc()
        self.error(f"Traceback:\n{tb}")
        
        self._log_session_event('ERROR_TRACEBACK', message, {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': tb,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_performance(self, operation: str, duration: float):
        """Log performance metrics"""
        message = f"Performance: {operation} took {duration:.3f}s"
        self.debug(message)
        
        self._log_session_event('PERFORMANCE', message, {
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    # Session management
    def _log_session_event(self, event_type: str, message: str, data: dict):
        """Log event to session"""
        event = {
            'event_type': event_type,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.session_events.append(event)
    
    def save_session(self):
        """Save session log to JSON file"""
        try:
            session_data = {
                'session_id': self.session_id,
                'start_time': self.session_events[0]['timestamp'] if self.session_events else None,
                'end_time': datetime.now().isoformat(),
                'total_events': len(self.session_events),
                'events': self.session_events
            }
            
            with open(self.session_log_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            self.info(f"Session saved to {self.session_log_file}")
            return True
        
        except Exception as e:
            self.error(f"Failed to save session: {str(e)}")
            return False
    
    def get_session_summary(self) -> dict:
        """Get summary of current session"""
        event_types = {}
        for event in self.session_events:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        return {
            'session_id': self.session_id,
            'total_events': len(self.session_events),
            'event_types': event_types,
            'duration': self._calculate_session_duration()
        }
    
    def _calculate_session_duration(self) -> float:
        """Calculate session duration in seconds"""
        if not self.session_events:
            return 0.0
        
        try:
            start = datetime.fromisoformat(self.session_events[0]['timestamp'])
            end = datetime.fromisoformat(self.session_events[-1]['timestamp'])
            return (end - start).total_seconds()
        except:
            return 0.0
    
    # Analysis methods
    def get_diagnosis_statistics(self) -> dict:
        """Get statistics from diagnosis events"""
        diagnoses = []
        
        for event in self.session_events:
            if event['event_type'] == 'DIAGNOSIS_RESULT':
                diagnoses.append({
                    'diagnosis': event['data'].get('diagnosis'),
                    'confidence': event['data'].get('confidence'),
                    'timestamp': event['data'].get('timestamp')
                })
        
        return {
            'total_diagnoses': len(diagnoses),
            'diagnoses': diagnoses,
            'average_confidence': sum(d['confidence'] for d in diagnoses) / len(diagnoses) if diagnoses else 0
        }
    
    def get_rule_firing_statistics(self) -> dict:
        """Get statistics about rule firing"""
        fired_rules = []
        
        for event in self.session_events:
            if event['event_type'] == 'RULE_FIRED':
                fired_rules.append(event['data'].get('rule_id'))
        
        # Count frequency
        rule_frequency = {}
        for rule_id in fired_rules:
            rule_frequency[rule_id] = rule_frequency.get(rule_id, 0) + 1
        
        return {
            'total_rules_fired': len(fired_rules),
            'unique_rules': len(set(fired_rules)),
            'rule_frequency': rule_frequency,
            'most_common_rule': max(rule_frequency.items(), key=lambda x: x[1])[0] if rule_frequency else None
        }
    
    def get_error_log(self) -> list:
        """Get all error events"""
        errors = []
        
        for event in self.session_events:
            if event['event_type'] in ['ERROR', 'ERROR_TRACEBACK', 'CRITICAL']:
                errors.append({
                    'type': event['event_type'],
                    'message': event['message'],
                    'data': event['data'],
                    'timestamp': event['timestamp']
                })
        
        return errors
    
    def export_session_report(self, output_file: str = None):
        """Export session as readable report"""
        if output_file is None:
            output_file = os.path.join(
                self.log_dir, 
                f'session_report_{self.session_id}.txt'
            )
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("SESSION REPORT\n")
                f.write("=" * 70 + "\n\n")
                
                summary = self.get_session_summary()
                f.write(f"Session ID: {summary['session_id']}\n")
                f.write(f"Total Events: {summary['total_events']}\n")
                f.write(f"Duration: {summary['duration']:.2f} seconds\n\n")
                
                f.write("Event Types:\n")
                for event_type, count in summary['event_types'].items():
                    f.write(f"  - {event_type}: {count}\n")
                
                # Diagnosis stats
                f.write("\n" + "=" * 70 + "\n")
                f.write("DIAGNOSIS STATISTICS\n")
                f.write("=" * 70 + "\n\n")
                
                diag_stats = self.get_diagnosis_statistics()
                f.write(f"Total Diagnoses: {diag_stats['total_diagnoses']}\n")
                f.write(f"Average Confidence: {diag_stats['average_confidence']:.2%}\n\n")
                
                for diag in diag_stats['diagnoses']:
                    f.write(f"  - {diag['diagnosis']}: {diag['confidence']:.2%}\n")
                
                # Rule stats
                f.write("\n" + "=" * 70 + "\n")
                f.write("RULE FIRING STATISTICS\n")
                f.write("=" * 70 + "\n\n")
                
                rule_stats = self.get_rule_firing_statistics()
                f.write(f"Total Rules Fired: {rule_stats['total_rules_fired']}\n")
                f.write(f"Unique Rules: {rule_stats['unique_rules']}\n")
                f.write(f"Most Common Rule: {rule_stats['most_common_rule']}\n\n")
                
                f.write("Rule Frequency:\n")
                for rule_id, count in sorted(
                    rule_stats['rule_frequency'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]:
                    f.write(f"  - {rule_id}: {count} times\n")
                
                # Errors
                errors = self.get_error_log()
                if errors:
                    f.write("\n" + "=" * 70 + "\n")
                    f.write("ERRORS\n")
                    f.write("=" * 70 + "\n\n")
                    
                    for error in errors:
                        f.write(f"[{error['timestamp']}] {error['type']}: {error['message']}\n")
                
                f.write("\n" + "=" * 70 + "\n")
            
            self.info(f"Session report exported to {output_file}")
            return output_file
        
        except Exception as e:
            self.error(f"Failed to export session report: {str(e)}")
            return None


# Singleton instance
_logger_instance = None

def get_logger(name: str = 'smartphone_expert') -> SmartphoneExpertLogger:
    """
    Get logger instance (singleton)
    
    Args:
        name: Logger name
        
    Returns:
        SmartphoneExpertLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SmartphoneExpertLogger(name)
    return _logger_instance


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("LOGGING SYSTEM TEST")
    print("=" * 70)
    
    # Get logger
    logger = get_logger()
    
    # Test basic logging
    logger.info("System started")
    logger.debug("Debug information")
    logger.warning("Warning message")
    
    # Test domain-specific logging
    logger.log_diagnosis_start(['layar_tidak_menyala', 'baterai_cepat_habis'])
    logger.log_rule_fired('R1', ['layar_tidak_menyala'], 'kemungkinan_baterai_habis')
    logger.log_rule_fired('R10', ['baterai_cepat_habis'], 'degradasi_baterai')
    logger.log_diagnosis_result('degradasi_baterai', 0.85)
    
    logger.log_user_action('export_pdf', {'diagnosis': 'degradasi_baterai'})
    logger.log_performance('forward_chaining', 1.234)
    
    # Test error logging
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.log_error_with_traceback(e, "Testing error handler")
    
    # Get statistics
    print("\n" + "=" * 70)
    print("SESSION SUMMARY")
    print("=" * 70)
    
    summary = logger.get_session_summary()
    print(f"Session ID: {summary['session_id']}")
    print(f"Total Events: {summary['total_events']}")
    print(f"Duration: {summary['duration']:.2f}s")
    
    print("\nEvent Types:")
    for event_type, count in summary['event_types'].items():
        print(f"  - {event_type}: {count}")
    
    # Diagnosis statistics
    print("\n" + "=" * 70)
    print("DIAGNOSIS STATISTICS")
    print("=" * 70)
    
    diag_stats = logger.get_diagnosis_statistics()
    print(f"Total Diagnoses: {diag_stats['total_diagnoses']}")
    print(f"Average Confidence: {diag_stats['average_confidence']:.2%}")
    
    # Rule statistics
    print("\n" + "=" * 70)
    print("RULE STATISTICS")
    print("=" * 70)
    
    rule_stats = logger.get_rule_firing_statistics()
    print(f"Total Rules Fired: {rule_stats['total_rules_fired']}")
    print(f"Unique Rules: {rule_stats['unique_rules']}")
    
    # Save session
    logger.save_session()
    
    # Export report
    report_file = logger.export_session_report()
    print(f"\nReport exported to: {report_file}")
    
    print("\n" + "=" * 70)