"""Example Background Script - Template for creating new scripts

This module demonstrates how to create background scripts in the background package.
Copy this template and customize for your needs.
"""
import asyncio
import sys
from typing import Optional
from background.utils.logger import get_logger, TaskLogger


logger = get_logger(__name__)


class ScriptRunner:
    """Base class for background scripts"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logger
    
    async def run(self, *args, **kwargs):
        """
        Main script execution logic
        
        Override this method in subclasses with actual script logic.
        """
        with TaskLogger(self.logger, self.name):
            self.logger.info(f"Running {self.name}...")
            # Add your script logic here
            pass
    
    async def validate(self) -> bool:
        """
        Validate prerequisites before running
        
        Override this method to check for required dependencies, configs, etc.
        """
        return True


class ExampleScript(ScriptRunner):
    """Example script implementation"""
    
    def __init__(self):
        super().__init__("ExampleScript")
    
    async def validate(self) -> bool:
        """Validate configuration"""
        self.logger.info("Validating configuration...")
        # Add validation logic here
        return True
    
    async def run(self, *args, **kwargs):
        """Execute the script"""
        if not await self.validate():
            self.logger.error("Validation failed")
            return False
        
        with TaskLogger(self.logger, self.name):
            try:
                self.logger.info("Starting example script")
                
                # Example: Process some data
                data = ["item1", "item2", "item3"]
                for item in data:
                    self.logger.info(f"Processing: {item}")
                    await asyncio.sleep(0.1)  # Simulate work
                
                self.logger.info("Example script completed successfully")
                return True
                
            except Exception as e:
                self.logger.error(f"Script failed: {e}")
                return False


async def main():
    """Main entry point"""
    script = ExampleScript()
    success = await script.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
