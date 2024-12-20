import os
from pathlib import Path

def split_file(input_path: str, num_chunks: int, output_dir: str = None):
    """Split a file into specified number of roughly equal chunks"""
    
    # Get file name without extension
    file_name = Path(input_path).stem
    file_ext = Path(input_path).suffix
    
    # Use same directory as input file if output_dir not specified
    if output_dir is None:
        output_dir = str(Path(input_path).parent)
    
    # Read the entire file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Calculate chunk size
    total_length = len(content)
    chunk_size = total_length // num_chunks
    
    # Split at nearest paragraph break
    chunks = []
    start = 0
    
    for i in range(num_chunks - 1):
        end = start + chunk_size
        
        # Find next paragraph break after the calculated end
        while end < total_length and content[end] != '\n':
            end += 1
        
        # If we're at the end of the file, break
        if end >= total_length:
            break
            
        # Add chunk
        chunks.append(content[start:end])
        start = end + 1
    
    # Add the final chunk
    chunks.append(content[start:])
    
    # Write chunks to files
    for i, chunk in enumerate(chunks, 1):
        output_path = os.path.join(output_dir, f"{file_name}-part{i}{file_ext}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f"Created: {output_path}")

def main():
    # Base directory for reference documents
    base_dir = Path(__file__).parent.parent / "src" / "reference-documents" / "style-guide"
    
    # Split Haldeman file into 3 parts
    haldeman_path = base_dir / "haldeman-the-forever-war.txt"
    split_file(str(haldeman_path), 3)
    
    # Split Asimov file into 8 parts
    asimov_path = base_dir / "asimov-foundation.txt"
    split_file(str(asimov_path), 8)
    
    # Remove original files
    os.remove(haldeman_path)
    os.remove(asimov_path)
    
    print("\nFile splitting complete!")

if __name__ == "__main__":
    main() 