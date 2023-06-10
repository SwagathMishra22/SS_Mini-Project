def strreverse(begin, end):
    while end > begin:
        aux = end
        end -= 1
        begin += 1
        aux, begin, end = begin, aux, end

def itoa(value, str, base):
    num = "0123456789abcdefghijklmnopqrstuvwxyz"
    wstr = str
    sign = 0

    # Validate base
    if base < 2 or base > 35:
        wstr = '\0'
        return

    # Take care of sign
    if value < 0:
        sign = value
        value = -value

    # Conversion. Number is reversed.
    while True:
        res = divmod(value, base)
        wstr += num[res[1]]
        value = res[0]
        if value == 0:
            break

    if sign < 0:
        wstr += '-'

    wstr = wstr[::-1]  # Reverse string
    str = wstr

def main():
    char_a = [""] * 10
    char_ad = [""] * 10
    label = [""] * 10
    opcode = [""] * 10
    operand = [""] * 10
    mnemonic = [""] * 10
    symbol = [""] * 10
    i = locctr = start = length = 0
    address = sa = code = add = actual_len = tcount = 0

    fp1 = open("input.dat", "r")
    fp2 = open("symtab.dat", "w")
    fp3 = open("intermediate.dat", "w")
    fp4 = open("opTab.dat", "r")
    fp5 = open("out.dat", "w")

    # scan the first line (should be start)
    label[0], opcode[0], operand[0] = fp1.readline().split()
    if opcode[0] == "START":
        start = int(operand[0])  # Get starting address
        locctr = start  # set locctr as the starting address

        # print to output and scan next line from input
        fp3.write(f"{label[0]}\t{opcode[0]}\t{operand[0]}\n")
        label[0], opcode[0], operand[0] = fp1.readline().split()
    else: 
        # No start opcode, take locctr as 0
        locctr = 0

    while opcode[0] != "END":
        fp3.write(f"{locctr}\t")

        if label[0] != "~":
            fp2.write(f"{label[0]}\t{locctr}\n")

        fp4.seek(0)  # goto beginning of file
        mnemonic[0], code = fp4.readline().split()  # scan first code
        while mnemonic[0] != "END":  # check for end opcode
            if opcode[0] == mnemonic[0]:  # compare all opcodes
                locctr += 3  # 3 bytes
                break
            mnemonic[0], code = fp4.readline().split()

        if opcode[0] == "WORD":
            locctr += 3  # 1 word = 3 byte
        elif opcode[0] == "RESW":
            locctr += 3 * int(operand[0])  # n words
        elif opcode[0] == "RESB":
            locctr += int(operand[0])  # n bytes
        elif opcode[0] == "BYTE":
            locctr += 1  # 1 byte

        # print to output and scan next line from input
        fp3.write(f"{label[0]}\t{opcode[0]}\t{operand[0]}\n")
        label[0], opcode[0], operand[0] = fp1.readline().split()

    # END opcode
    fp3.write(f"{locctr}\t{label[0]}\t{opcode[0]}\t{operand[0]}\n")
    length = locctr - start
    print(f"The length of the program is {length}")

    # Reset file pointers and variables
    fp1.seek(0)
    fp2.close()
    fp3.close()
    fp4.close()

    fp1 = open("asmlist.dat", "w")
    fp2 = open("symtab.dat", "r")
    fp3 = open("intermediate.dat", "r")
    fp4 = open("opTab.dat", "r")
    fp5 = open("out.dat", "w")
    label[0], opcode[0], operand[0] = fp3.readline().split()

    if opcode[0] == "START":
        fp1.write(f"\t{label[0]}\t{opcode[0]}\t{operand[0]}\n")
        fp5.write(f"H{label[0]:<6s}{operand[0]:<6s}26")
        address, label[0], opcode[0], operand[0] = fp3.readline().split()
        sa = int(address)

    while opcode[0] != "END":
        if opcode[0] == "BYTE":
            fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\t")
            length = len(operand[0])
            actual_len = length - 3
            i = 2
            while i < actual_len + 2:
                itoa(ord(operand[0][i]), char_ad, 16)
                fp1.write(char_ad[0])
                i += 1
            fp1.write("\n")
        elif opcode[0] == "WORD":
            length = len(operand[0])
            itoa(int(operand[0]), char_a, 10)
            fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\t00000{char_a[0]}\n")
        elif opcode[0] == "RESB" or opcode[0] == "RESW":
            fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\n")
        else:
            fp4.seek(0)
            mnemonic[0], code = fp4.readline().split()
            while opcode[0] != mnemonic[0]:
                mnemonic[0], code = fp4.readline().split()
            if operand[0] == "~":
                fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\t{code}0000\n")
                if tcount == 10:
                    fp5.write(f"\nT{address}{00}{code}0000")
                    tcount = 0
                else:
                    fp5.write(f"{code}0000")
                    tcount += 1
            else:
                fp2.seek(0)
                symbol[0], add = fp2.readline().split()
                while operand[0] != symbol[0]:
                    symbol[0], add = fp2.readline().split()
                fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\t{code}{add}\n")
                if tcount == 10:
                    fp5.write(f"\nT{address}{00}{code}{add}")
                    tcount = 0
                else:
                    fp5.write(f"{code}{add}")
                    tcount += 1
        address, label[0], opcode[0], operand[0] = fp3.readline().split()

    fp1.write(f"{address}\t{label[0]}\t{opcode[0]}\t{operand[0]}\n")
    fp5.write(f"\nE{sa:<6d}\n")
    print("Finished")

    fp1.close()
    fp2.close()
    fp3.close()
    fp4.close()
    fp5.close()

if __name__ == "__main__":
    main()