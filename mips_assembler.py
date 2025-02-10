import sys

def register_number(reg):
    return int(reg.replace('$', ''))

def parse_r_type(parts):
    opcode = '000000'
    rs = register_number(parts[2])
    rt = register_number(parts[3])
    rd = register_number(parts[1])
    shamt = '00000'
    funct = {
        'add': '100000',
        'sub': '100010',
        'and': '100100',
        'or': '100101',
        'sll': '000000',
        'srl': '000010',
        'sllv': '000100',
        'srlv': '000110'
    }[parts[0]]
    return f"{opcode}{rs:05b}{rt:05b}{rd:05b}{shamt}{funct}"

def parse_i_type(parts, labels, current_address):
    opcode = {
        'addi': '001000',
        'andi': '001100',
        'lw': '100011',
        'sw': '101011',
        'beq': '000100',
        'bne': '000101',
        'blez': '000110',
        'bgtz': '000111'
    }[parts[0]]
    rs = register_number(parts[2])
    rt = register_number(parts[1])
    if parts[0] in ['beq', 'bne', 'blez', 'bgtz']:
        label = parts[3]
        if label not in labels:
            raise KeyError(f"Label {label} not found in labels: {labels}")
        label_address = labels[label]
        offset = (label_address - current_address - 4) // 4
        imm = offset & 0xFFFF
    else:
        imm = int(parts[3]) & 0xFFFF
    return f"{opcode}{rs:05b}{rt:05b}{imm:016b}"

def parse_j_type(parts, labels):
    opcode = '000010'
    label = parts[1]
    if label not in labels:
        raise KeyError(f"Label {label} not found in labels: {labels}")
    address = (labels[label] >> 2) & 0x3FFFFFF
    return f"{opcode}{address:026b}"

def assemble_line(line, labels, current_address):
    # Clean and split the line
    line = line.replace(',', ' ').replace('(', ' ').replace(')', ' ')
    parts = [part.strip() for part in line.split()]
    
    if not parts:
        return None

    if parts[0] in ['add', 'sub', 'and', 'or', 'sll', 'srl', 'sllv', 'srlv']:
        return parse_r_type(parts)
    elif parts[0] in ['addi', 'andi', 'lw', 'sw', 'beq', 'bne', 'blez', 'bgtz']:
        return parse_i_type(parts, labels, current_address)
    elif parts[0] == 'j':
        return parse_j_type(parts, labels)
    return None

def main(input_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    
    labels = {}
    current_address = 0x00400000
    
    # First pass: find all labels
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue  # Skip empty lines and comments
        if ':' in line:
            label = line.split(':')[0].strip()
            labels[label] = current_address
            print(f"Label found: {label} at address {current_address:08x}")
            # Remove the label from the line for further processing
            line = line.split(':')[1].strip()
        if line:  # Only increment address for non-empty lines
            current_address += 4

    print("Labels collected:", labels)

    # Second pass: assemble instructions
    current_address = 0x00400000
    output_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.endswith(':') or line.startswith('#'):
            continue
        if ':' in line:
            # Remove the label part
            line = line.split(':')[1].strip()
        try:
            machine_code = assemble_line(line, labels, current_address)
            if machine_code:
                output_lines.append(f"{current_address:08x} {int(machine_code, 2):08x}")
                current_address += 4
        except KeyError as e:
            print(f"Error processing line '{line}': {e}")
            continue

    output_filename = input_filename.replace('.asm', '.obj')
    with open(output_filename, 'w') as file:
        for line in output_lines:
            file.write(line + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mips_assembler.py <source_code.asm>")
    else:
        main(sys.argv[1])
