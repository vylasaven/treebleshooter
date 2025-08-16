#!/usr/bin/env python3
"""
GUI Test Script - Tests walking through guides multiple times
Simulates the issue where answer options disappear after first walkthrough
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication, QRadioButton
from PyQt5.QtCore import QTimer
from src.views.guide_executor_view import GuideExecutorView
from src.controllers.file_controller import FileController
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_multiple_walkthroughs():
    """Test walking through guides multiple times to ensure UI remains functional."""
    app = QApplication(sys.argv)
    
    # Create executor and file controller
    executor = GuideExecutorView()
    executor.show()
    file_controller = FileController()
    
    # Test guides
    test_guides = [
        "data/examples/mirror-too-enthusiastic.tsg",
        "data/examples/duck-offering-solutions.tsg",
        "data/examples/coffee-both-hot-and-cold.tsg"
    ]
    
    results = []
    
    for guide_path in test_guides:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing guide: {guide_path}")
        
        # Load guide
        guide = file_controller.load_guide(guide_path)
        if not guide:
            logger.error(f"Failed to load guide: {guide_path}")
            continue
            
        # Test walking through the guide 3 times
        for walkthrough_num in range(1, 4):
            logger.info(f"\nWalkthrough #{walkthrough_num}")
            
            # Load/reload the guide
            executor.load_guide(guide)
            app.processEvents()
            
            # Check answers are visible
            if not executor.answers_group.isVisible():
                logger.error(f"FAIL: Answers not visible on walkthrough {walkthrough_num}")
                results.append(("FAIL", guide_path, walkthrough_num, "Answers not visible"))
                break
                
            # Check radio buttons exist
            radio_buttons = executor.answers_group.findChildren(QRadioButton)
            if not radio_buttons:
                logger.error(f"FAIL: No radio buttons on walkthrough {walkthrough_num}")
                results.append(("FAIL", guide_path, walkthrough_num, "No radio buttons"))
                break
            
            logger.info(f"  ✓ Answers visible with {len(radio_buttons)} options")
            
            # Navigate through a few steps
            steps_taken = 0
            max_steps = 3
            
            while steps_taken < max_steps and executor.answers_group.isVisible():
                radio_buttons = executor.answers_group.findChildren(QRadioButton)
                if not radio_buttons:
                    break
                    
                # Select first option
                radio_buttons[0].setChecked(True)
                executor.go_next()
                app.processEvents()
                steps_taken += 1
                
                logger.info(f"  Step {steps_taken}: Navigated")
                
            # If we reached a solution, restart
            if executor.solution_group.isVisible():
                logger.info("  Reached solution, restarting...")
                executor.restart_guide()
                app.processEvents()
                
                # Verify restart worked
                if not executor.answers_group.isVisible():
                    logger.error(f"FAIL: Answers not visible after restart on walkthrough {walkthrough_num}")
                    results.append(("FAIL", guide_path, walkthrough_num, "Answers not visible after restart"))
                else:
                    radio_buttons = executor.answers_group.findChildren(QRadioButton)
                    if radio_buttons:
                        logger.info(f"  ✓ Restart successful, {len(radio_buttons)} options available")
                        results.append(("PASS", guide_path, walkthrough_num, "Complete"))
                    else:
                        logger.error(f"FAIL: No radio buttons after restart on walkthrough {walkthrough_num}")
                        results.append(("FAIL", guide_path, walkthrough_num, "No radio buttons after restart"))
            else:
                results.append(("PASS", guide_path, walkthrough_num, "Partial navigation"))
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    passed = sum(1 for r in results if r[0] == "PASS")
    failed = sum(1 for r in results if r[0] == "FAIL")
    
    for result in results:
        status, guide, walkthrough, message = result
        guide_name = os.path.basename(guide).replace('.tsg', '')
        logger.info(f"{status}: {guide_name} walkthrough #{walkthrough} - {message}")
    
    logger.info(f"\nTotal: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed == 0:
        logger.info("\n✅ SUCCESS: All guides can be walked through multiple times!")
        return 0
    else:
        logger.error(f"\n❌ FAILURE: {failed} tests failed")
        return 1


if __name__ == "__main__":
    exit_code = test_multiple_walkthroughs()
    sys.exit(exit_code)