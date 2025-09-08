import logging
from src.config.settings import settings
from src.indexing.file_scanner import FileScanner

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("++HyperFile Search Tool++")
    print("=" * 50)
    
    try:
        # Test configuration step by step
        print("Loading configuration...")
        
        print("Getting search directories...")
        search_dirs = settings.get_search_directories()
        print(f"Found {len(search_dirs)} valid directories:")
        for directory in search_dirs:
            print(f"   - {directory}")
        
        if not search_dirs:
            print("No valid search directories found! Check your config.yaml paths.")
            return
        
        print(f"File types configured: {len(settings.get_file_extensions())}")
        print(f"Max file size: {settings.get_max_file_size() / 1024 / 1024:.1f} MB")
        
        # Test file scanning with timeout/limit
        print("\nStarting file scan (limited to first 20 files)...")
        file_scanner = FileScanner()
        
        file_count = 0
        for file_path in file_scanner.scan_files():
            if file_count < 5: 
                print(f"    Found: {file_path}")
            elif file_count == 5:
                print("   ... (showing first 5 files)")
            
            file_count += 1
            
            if file_count >= 5000:
                print(f"Stopping at {file_count} files for testing")
                break
        
        print(f"\nSuccessfully scanned {file_count} files")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    main()