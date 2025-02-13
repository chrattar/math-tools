import pandas as pd
import xml.etree.ElementTree as ET
import json
import numpy as np

def read_cat_file(filename):
    """Read the .cat file and return its content"""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def register_namespace():
    """Register the BattleScribe namespace"""
    ET.register_namespace('', 'http://www.battlescribe.net/schema/catalogueSchema')
    return {'bs': 'http://www.battlescribe.net/schema/catalogueSchema'}

def create_unit_dataframes(xml_content):
    """Create separate dataframes for different aspects of units"""
    ns = register_namespace()
    root = ET.fromstring(xml_content)
    
    # Main units dataframe
    units_data = []
    weapons_data = []
    profiles_data = []
    abilities_data = []
    
    # Look in sharedSelectionEntries for unit entries
    shared_entries = root.find('.//bs:sharedSelectionEntries', namespaces=ns)
    if shared_entries is not None:
        for entry in shared_entries.findall('.//bs:selectionEntry[@type="unit"]', namespaces=ns):
            unit_id = entry.get('id')
            unit_name = entry.get('name')
            
            # Find points cost
            costs = entry.findall('.//bs:cost[@name="pts"]', namespaces=ns)
            points = costs[0].get('value') if costs else None
            
            unit_base = {
                'unit_id': unit_id,
                'name': unit_name,
                'points': points
            }
            units_data.append(unit_base)
            
            # Parse profiles
            for profile in entry.findall('.//bs:profile', namespaces=ns):
                profile_type = profile.get('typeName')
                profile_name = profile.get('name')
                
                if profile_type == 'Unit':
                    characteristics = {}
                    for char in profile.findall('.//bs:characteristic', namespaces=ns):
                        char_type = char.get('typeId')
                        char_value = char.text
                        characteristics[char_type] = char_value
                    
                    profile_data = {
                        'unit_id': unit_id,
                        'name': profile_name,
                        **characteristics
                    }
                    profiles_data.append(profile_data)
                
                elif profile_type in ['Ranged Weapons', 'Melee Weapons']:
                    characteristics = {}
                    for char in profile.findall('.//bs:characteristic', namespaces=ns):
                        char_type = char.get('typeId')
                        char_value = char.text
                        characteristics[char_type] = char_value
                    
                    weapon_data = {
                        'unit_id': unit_id,
                        'name': profile_name,
                        'type': profile_type,
                        **characteristics
                    }
                    weapons_data.append(weapon_data)
                
                elif profile_type == 'Abilities':
                    description = profile.find('.//bs:characteristic', namespaces=ns).text
                    ability_data = {
                        'unit_id': unit_id,
                        'name': profile_name,
                        'description': description
                    }
                    abilities_data.append(ability_data)
    
    # Create dataframes
    df_units = pd.DataFrame(units_data)
    df_weapons = pd.DataFrame(weapons_data)
    df_profiles = pd.DataFrame(profiles_data)
    df_abilities = pd.DataFrame(abilities_data)
    
    return {
        'units': df_units,
        'weapons': df_weapons,
        'profiles': df_profiles,
        'abilities': df_abilities
    }

if __name__ == "__main__":
    cat_file_path = "C:\\stentor\\wh40\\datafiles\\wh40k-10e-main\\Imperium - Black Templars.cat"  # Replace with your actual file path
    
    # Read the file
    xml_content = read_cat_file(cat_file_path)
    
    # Create dataframes
    dataframes = create_unit_dataframes(xml_content)
    
    # Display each dataframe
    for name, df in dataframes.items():
        print(f"\n{name.upper()} DataFrame:")
        print("\nShape:", df.shape)
        print("\nColumns:", df.columns.tolist() if not df.empty else "No columns")
        print("\nContent:")
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(df)
        print("\n" + "="*80 + "\n")
