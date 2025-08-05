import sys
import os
if __name__ == "__main__":
    custom_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wondermail'))
    if custom_module_path not in sys.path:
        sys.path.append(custom_module_path)
    

    from wondermail.wonderMail import WMSParser

    password = input("Enter WonderMail code: ")
    try:
        sanitized_code = WMSParser.sanitize(password)
        unscrambled_code = WMSParser.unscrambleString(sanitized_code)
        encryptedbits = WMSParser.bytesToBits(unscrambled_code)
        decrypted = WMSParser.decryptbitstream(encryptedbits)
        output = WMSParser.bitsToStructure(decrypted)

        print(f"Decrypted WonderMail code: {output}")
    except ValueError as e:
        print(f"Error: {e}")