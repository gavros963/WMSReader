import sys
import os
if __name__ == "__main__":
    custom_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wondermail'))
    if custom_module_path not in sys.path:
        sys.path.append(custom_module_path)
    

    from wondermail.wonderMail import WMSParser
    from wondermail import wmutils

    password = input("Enter WonderMail code: ")
    try:
        sanitized_code = WMSParser.sanitize(password)
        unscrambled_code = WMSParser.unscrambleString(sanitized_code)
        encryptedbits = WMSParser.bytesToBits(unscrambled_code)
        decrypted = WMSParser.decryptbitstream(encryptedbits)
        output = WMSParser.bitsToStructure(decrypted)
        annotations = {}
        annotations['client'] = wmutils.getPokeName(output['client'])
        annotations['target'] = wmutils.getPokeName(output['target'])
        annotations['dungeon'] = wmutils.getDungeonName(output['dungeon'])
        annotations['reward'] = wmutils.getItemName(output['reward'])
        annotations['targetItem'] = wmutils.getItemName(output['targetItem'])
        match output['rewardType']:
            case 0:
                annotations['rewardType'] = 'Cash'
            case 1:
                annotations['rewardType'] = 'Cash + ??? (Reward item)'
            case 2:
                annotations['rewardType'] = 'Item'
            case 3:
                annotations['rewardType'] = 'Item + ??? (Random)'
            case 4:
                annotations['rewardType'] = '??? (Reward item)'
            case 5:
                annotations['rewardType'] = '??? (Egg)'
            case 6:
                annotations['rewardType'] = '??? (Client joins)'
            case _:
                annotations['rewardType'] = 'Unknown reward type'
        result = f"sanitized: {sanitized_code}\n"
        result += f"unscrambled: {unscrambled_code}\n"
        result += f"encrypted bits: {encryptedbits}\n"
        result += f"decrypted: {decrypted}\n"
        result += "structured output:\n"
        for key in output:
            value = output[key]
            if key in annotations and annotations[key]:
                value = f"{value} ({annotations[key]})"
            result += f"{key}: {value}\n"

        print(result)
    except ValueError as e:
        print(f"Error: {e}")