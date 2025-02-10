# MIPS Assembler

## Overview

This project implements a MIPS assembler in Python, capable of converting MIPS assembly code into machine code. The assembler processes MIPS instructions, recognizes labels, and generates corresponding binary instructions.

## Features

- Supports **R-type, I-type, and J-type** instructions.
- Recognizes and processes labels for branch and jump instructions.
- Converts assembly code into **32-bit machine code**.
- Outputs the assembled machine code in hexadecimal format.

## Code Structure

The assembler consists of the following key functions:

### **Instruction Parsing**
- `assemble_line(line, labels, current_address)`: Determines the type of instruction and calls the corresponding parsing function.
- `parse_r_type(parts)`: Converts R-type instructions into machine code.
- `parse_i_type(parts, labels, current_address)`: Converts I-type instructions into machine code.
- `parse_j_type(parts, labels)`: Converts J-type instructions into machine code.

### **Label Handling**
- `get_labels(lines)`: Extracts labels and their corresponding addresses.
- The assembler makes a **first pass** to collect label locations before processing instructions.

### **Main Functionality**
- Reads assembly code from a file.
- Converts it into machine code.
- Outputs the assembled code in hexadecimal format.

## Usage

To use the MIPS assembler:

1. Ensure you have **Python** installed.
2. Run the assembler with a MIPS assembly file:
   ```bash
   python mips_assembler.py <source_code.asm>
3. The assembled output will be saved in a `.obj` file.

---

## Example

### **Input (MIPS Assembly Code)**

```assembly
.text
again: add  $11, $12, $23
show: addi $8 , $7, -1234
      andi $3 , $7 , 127
      beq $8, $10, show
      bne $4, $6, x1
x1:   sll $17, $18, 4
      j    again

```
## Output (Machine Code)
```plaintext
00400000 01975820
00400004 20e8fb2e
00400008 30e3007f
0040000c 1148fffe
00400010 14c40001
00400014 02448800
00400018 08100001
```
## Dependencies

- Python 3.x (Recommended)
- No external libraries are required.

## Notes

- Labels are resolved before processing instructions.
- Immediate values are converted to 16-bit signed integers.
- The assembler supports basic MIPS instruction formats but can be extended for more functionality.

